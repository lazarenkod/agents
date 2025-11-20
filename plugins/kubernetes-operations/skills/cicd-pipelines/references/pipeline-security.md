# Pipeline Security Best Practices

Comprehensive guide to securing CI/CD pipelines with supply chain security, SLSA compliance, and vulnerability management.

## Table of Contents

- [Supply Chain Security Overview](#supply-chain-security-overview)
- [SLSA Framework](#slsa-framework)
- [Sigstore Integration](#sigstore-integration)
- [Vulnerability Scanning](#vulnerability-scanning)
- [Secret Management](#secret-management)
- [Access Control](#access-control)
- [Audit and Compliance](#audit-and-compliance)
- [Container Security](#container-security)
- [Runtime Protection](#runtime-protection)

## Supply Chain Security Overview

### The Software Supply Chain

```
┌─────────────────────────────────────────────────────────────────┐
│                    Software Supply Chain                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Source Code → Dependencies → Build → Test → Sign → Deploy     │
│       │             │           │       │       │        │       │
│    Verify        Scan        Scan    Scan    Verify   Verify    │
│                                                                  │
│  Threats at each stage:                                         │
│  - Compromised source                                           │
│  - Malicious dependencies                                       │
│  - Build injection                                              │
│  - Unsigned artifacts                                           │
│  - Unauthorized deployment                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Security Principles

1. **Zero Trust** - Verify every step, trust nothing implicitly
2. **Defense in Depth** - Multiple layers of security controls
3. **Least Privilege** - Minimal permissions for each component
4. **Immutability** - Artifacts cannot be modified after creation
5. **Auditability** - Complete trail of all actions
6. **Automation** - Security checks in every pipeline run

## SLSA Framework

### SLSA Levels

**Supply-chain Levels for Software Artifacts (SLSA)**

| Level | Requirements | Protection Against |
|-------|--------------|-------------------|
| **SLSA 0** | No guarantees | N/A |
| **SLSA 1** | Build process documented | Unauthorized modifications |
| **SLSA 2** | Signed provenance | Tampering after build |
| **SLSA 3** | Hardened build platform | Insider threats |
| **SLSA 4** | Two-party review | Sophisticated attacks |

### SLSA Level 3 Implementation

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: slsa-compliant-pipeline
  annotations:
    chains.tekton.dev/transparency: "true"
spec:
  params:
    - name: git-url
      type: string
    - name: git-revision
      type: string
    - name: image
      type: string

  workspaces:
    - name: source

  tasks:
    # 1. Source provenance
    - name: git-clone
      taskRef:
        name: git-clone-verified
      workspaces:
        - name: output
          workspace: source
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)
        - name: verify-commits
          value: "true"  # Verify GPG signatures

    # 2. Dependency verification
    - name: verify-dependencies
      runAfter: [git-clone]
      taskRef:
        name: dependency-check
      workspaces:
        - name: source
          workspace: source

    # 3. Hermetic build
    - name: build
      runAfter: [verify-dependencies]
      taskRef:
        name: hermetic-build
      workspaces:
        - name: source
          workspace: source
      params:
        - name: image
          value: $(params.image)

    # 4. Generate provenance
    - name: generate-provenance
      runAfter: [build]
      taskRef:
        name: slsa-provenance
      params:
        - name: image
          value: $(params.image)
        - name: source-uri
          value: $(params.git-url)
        - name: source-digest
          value: $(tasks.git-clone.results.commit)

    # 5. Sign image and provenance
    - name: sign-artifacts
      runAfter: [generate-provenance]
      taskRef:
        name: cosign-sign-all
      params:
        - name: image
          value: $(params.image)
        - name: provenance
          value: $(tasks.generate-provenance.results.provenance-path)

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: slsa-provenance
spec:
  params:
    - name: image
    - name: source-uri
    - name: source-digest

  results:
    - name: provenance-path

  steps:
    - name: generate
      image: ghcr.io/in-toto/in-toto-golang:latest
      script: |
        #!/usr/bin/env bash
        set -e

        cat > /tmp/provenance.json <<EOF
        {
          "_type": "https://in-toto.io/Statement/v0.1",
          "subject": [{
            "name": "$(params.image)",
            "digest": {
              "sha256": "$(cat /tekton/results/IMAGE_DIGEST)"
            }
          }],
          "predicateType": "https://slsa.dev/provenance/v0.2",
          "predicate": {
            "builder": {
              "id": "https://tekton.dev/chains/v2"
            },
            "buildType": "https://tekton.dev/attestations/chains@v2",
            "invocation": {
              "configSource": {
                "uri": "$(params.source-uri)",
                "digest": {
                  "sha1": "$(params.source-digest)"
                }
              }
            },
            "metadata": {
              "buildInvocationId": "$(context.taskRun.uid)",
              "buildStartedOn": "$(context.taskRun.startTime)",
              "buildFinishedOn": "$(context.taskRun.finishTime)",
              "completeness": {
                "parameters": true,
                "environment": true,
                "materials": true
              },
              "reproducible": false
            },
            "materials": [{
              "uri": "$(params.source-uri)",
              "digest": {
                "sha1": "$(params.source-digest)"
              }
            }]
          }
        }
        EOF

        echo -n "/tmp/provenance.json" | tee $(results.provenance-path.path)

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: hermetic-build
spec:
  description: Build in isolated, reproducible environment
  params:
    - name: image

  workspaces:
    - name: source

  steps:
    - name: build
      image: gcr.io/kaniko-project/executor:latest
      args:
        - --context=$(workspaces.source.path)
        - --destination=$(params.image)
        - --reproducible
        - --snapshot-mode=redo
        - --use-new-run
        - --ignore-path=/product_uuid
        - --ignore-path=/etc/hostname
      securityContext:
        runAsUser: 0
        capabilities:
          drop:
            - ALL
          add:
            - CHOWN
            - DAC_OVERRIDE
            - FOWNER
            - SETGID
            - SETUID
      env:
        - name: DOCKER_CONFIG
          value: /kaniko/.docker
        # Network isolation
        - name: HTTP_PROXY
          value: ""
        - name: HTTPS_PROXY
          value: ""
```

### SLSA Verification

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: verify-slsa-provenance
spec:
  params:
    - name: image
    - name: policy-file
      default: /policies/slsa-policy.json

  steps:
    - name: verify
      image: ghcr.io/slsa-framework/slsa-verifier:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Download provenance
        cosign download attestation $(params.image) > provenance.json

        # Verify provenance
        slsa-verifier verify-image $(params.image) \
          --provenance-path provenance.json \
          --source-uri github.com/org/repo \
          --builder-id https://tekton.dev/chains/v2

        echo "✓ SLSA provenance verified"

    - name: check-policy
      image: openpolicyagent/opa:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Evaluate policy
        opa eval -d $(params.policy-file) \
          -i provenance.json \
          -f pretty \
          'data.slsa.allow'

        echo "✓ Policy compliance verified"
```

## Sigstore Integration

### Cosign - Image Signing

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: cosign-sign
spec:
  params:
    - name: image
    - name: key-secret
      default: cosign-keys

  steps:
    - name: sign-image
      image: gcr.io/projectsigstore/cosign:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Sign the image
        cosign sign --key /secrets/cosign.key $(params.image)

        # Attach SBOM
        cosign attach sbom --sbom /tmp/sbom.spdx $(params.image)

        # Sign SBOM
        cosign sign --key /secrets/cosign.key --attachment sbom $(params.image)

      env:
        - name: COSIGN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: $(params.key-secret)
              key: password
      volumeMounts:
        - name: cosign-keys
          mountPath: /secrets
          readOnly: true

  volumes:
    - name: cosign-keys
      secret:
        secretName: cosign-keys

---
# Keyless signing with OIDC
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: cosign-sign-keyless
spec:
  params:
    - name: image

  steps:
    - name: sign-keyless
      image: gcr.io/projectsigstore/cosign:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Keyless signing with Fulcio
        cosign sign --yes $(params.image)

      env:
        - name: COSIGN_EXPERIMENTAL
          value: "1"
        - name: OIDC_TOKEN
          valueFrom:
            secretKeyRef:
              name: oidc-token
              key: token
```

### Rekor - Transparency Log

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: verify-rekor-entry
spec:
  params:
    - name: image

  steps:
    - name: verify
      image: gcr.io/projectsigstore/cosign:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Verify signature and check Rekor
        cosign verify $(params.image) \
          --certificate-identity-regexp=".*@example.com" \
          --certificate-oidc-issuer=https://token.actions.githubusercontent.com

        # Get Rekor entry
        cosign verify $(params.image) --output=json | \
          jq -r '.[].optional.Bundle.Payload.body' | \
          base64 -d | \
          jq .

        echo "✓ Rekor transparency log verified"
```

### Policy Controller (Admission Webhook)

```yaml
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: require-signed-images
spec:
  images:
    - glob: "registry.example.com/**"

  authorities:
    - key:
        data: |
          -----BEGIN PUBLIC KEY-----
          MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
          -----END PUBLIC KEY-----

    - keyless:
        url: https://fulcio.sigstore.dev
        identities:
          - issuer: https://token.actions.githubusercontent.com
            subject: "https://github.com/org/repo/*"

  policy:
    type: cue
    data: |
      predicateType: "https://slsa.dev/provenance/v0.2"
      predicate: {
        buildType: "https://tekton.dev/attestations/chains@v2"
        builder: id: =~"^https://tekton.dev/chains/v2"
      }
```

## Vulnerability Scanning

### Multi-Layer Scanning Strategy

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: comprehensive-security-scan
spec:
  workspaces:
    - name: source

  tasks:
    # 1. Secret detection
    - name: detect-secrets
      taskRef:
        name: trufflehog-scan

    # 2. SAST (Static Application Security Testing)
    - name: sast-scan
      taskRef:
        name: semgrep-scan
      runAfter: [detect-secrets]

    # 3. Dependency scanning
    - name: dependency-scan
      taskRef:
        name: trivy-filesystem-scan
      runAfter: [detect-secrets]

    # 4. License compliance
    - name: license-check
      taskRef:
        name: fossa-scan
      runAfter: [detect-secrets]

    # Build only if all scans pass
    - name: build-image
      runAfter: [sast-scan, dependency-scan, license-check]
      taskRef:
        name: kaniko-build

    # 5. Container image scanning
    - name: image-scan
      runAfter: [build-image]
      taskRef:
        name: trivy-image-scan

    # 6. Malware scanning
    - name: malware-scan
      runAfter: [build-image]
      taskRef:
        name: clamav-scan

    # 7. Configuration audit
    - name: config-audit
      runAfter: [build-image]
      taskRef:
        name: dockle-scan

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: trufflehog-scan
spec:
  description: Detect secrets in source code
  workspaces:
    - name: source

  steps:
    - name: scan
      image: trufflesecurity/trufflehog:latest
      script: |
        #!/usr/bin/env sh
        set -e

        trufflehog filesystem $(workspaces.source.path) \
          --json \
          --fail \
          --no-update

        echo "✓ No secrets detected"

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: semgrep-scan
spec:
  description: SAST with Semgrep
  workspaces:
    - name: source

  steps:
    - name: scan
      image: returntocorp/semgrep:latest
      script: |
        #!/usr/bin/env bash
        set -e

        cd $(workspaces.source.path)

        semgrep scan \
          --config=auto \
          --error \
          --severity ERROR \
          --severity WARNING \
          --json \
          --output=/tmp/semgrep-results.json

        # Check for critical issues
        CRITICAL=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' /tmp/semgrep-results.json)

        if [ "$CRITICAL" -gt 0 ]; then
          echo "✗ Found $CRITICAL critical security issues"
          jq '.results[] | select(.extra.severity == "ERROR")' /tmp/semgrep-results.json
          exit 1
        fi

        echo "✓ SAST scan passed"

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: trivy-image-scan
spec:
  params:
    - name: image
    - name: severity
      default: CRITICAL,HIGH

  steps:
    - name: scan
      image: aquasec/trivy:latest
      script: |
        #!/usr/bin/env sh
        set -e

        trivy image \
          --severity $(params.severity) \
          --exit-code 1 \
          --no-progress \
          --format json \
          --output /tmp/trivy-results.json \
          $(params.image)

        # Display summary
        trivy image \
          --severity $(params.severity) \
          --format table \
          $(params.image)

    - name: upload-results
      image: curlimages/curl:latest
      script: |
        #!/bin/sh
        # Upload to DefectDojo or similar
        curl -X POST https://defectdojo.example.com/api/v2/import-scan/ \
          -H "Authorization: Token ${DEFECTDOJO_TOKEN}" \
          -F "scan_type=Trivy Scan" \
          -F "file=@/tmp/trivy-results.json" \
          -F "engagement=1"
      env:
        - name: DEFECTDOJO_TOKEN
          valueFrom:
            secretKeyRef:
              name: defectdojo
              key: token

---
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: dockle-scan
spec:
  description: Lint Dockerfile for security best practices
  params:
    - name: image

  steps:
    - name: scan
      image: goodwithtech/dockle:latest
      script: |
        #!/usr/bin/env sh
        set -e

        dockle \
          --exit-code 1 \
          --exit-level fatal \
          --format json \
          --output /tmp/dockle-results.json \
          $(params.image)

        # Check specific issues
        jq '.details[] | select(.level == "FATAL" or .level == "WARN")' /tmp/dockle-results.json

        echo "✓ Container security best practices verified"
```

### Continuous Vulnerability Monitoring

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: continuous-image-scan
  namespace: security
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: image-scanner
          containers:
            - name: scan
              image: aquasec/trivy:latest
              command:
                - sh
                - -c
                - |
                  #!/bin/sh
                  set -e

                  # Get all images in cluster
                  kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | \
                    sort -u > /tmp/images.txt

                  # Scan each image
                  while read image; do
                    echo "Scanning $image"
                    trivy image \
                      --severity CRITICAL,HIGH \
                      --format json \
                      --output /tmp/scan-results.json \
                      "$image" || true

                    # Upload results
                    curl -X POST https://vulnerability-db.example.com/api/scans \
                      -H "Content-Type: application/json" \
                      -d @/tmp/scan-results.json
                  done < /tmp/images.txt
          restartPolicy: OnFailure
```

## Secret Management

### External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: ci-cd
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "ci-cd"
          serviceAccountRef:
            name: external-secrets

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: pipeline-secrets
  namespace: ci-cd
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore

  target:
    name: pipeline-credentials
    creationPolicy: Owner

  data:
    - secretKey: github-token
      remoteRef:
        key: ci-cd/github
        property: token

    - secretKey: registry-password
      remoteRef:
        key: ci-cd/registry
        property: password

    - secretKey: cosign-password
      remoteRef:
        key: ci-cd/cosign
        property: password

    - secretKey: slack-webhook
      remoteRef:
        key: ci-cd/slack
        property: webhook-url
```

### Sealed Secrets

```yaml
# Generate sealed secret
# kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: pipeline-secrets
  namespace: ci-cd
spec:
  encryptedData:
    github-token: AgBX8v2... # Encrypted value
    registry-password: AgCY9k... # Encrypted value
  template:
    metadata:
      name: pipeline-secrets
      namespace: ci-cd
    type: Opaque
```

### Short-Lived Credentials with Vault

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: vault-dynamic-secrets
spec:
  steps:
    - name: get-credentials
      image: vault:latest
      script: |
        #!/usr/bin/env sh
        set -e

        # Login with Kubernetes auth
        VAULT_TOKEN=$(vault write -field=token auth/kubernetes/login \
          role=ci-cd \
          jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token)

        export VAULT_TOKEN

        # Get dynamic AWS credentials (valid for 1 hour)
        vault read -format=json aws/creds/deploy | \
          jq -r '.data | "AWS_ACCESS_KEY_ID=\(.access_key)\nAWS_SECRET_ACCESS_KEY=\(.secret_key)"' > /tmp/aws-creds

        # Get dynamic DB credentials
        vault read -format=json database/creds/app | \
          jq -r '.data | "DB_USER=\(.username)\nDB_PASSWORD=\(.password)"' > /tmp/db-creds

    - name: use-credentials
      image: amazon/aws-cli:latest
      script: |
        #!/usr/bin/env sh
        set -e

        # Source credentials
        . /tmp/aws-creds

        # Use credentials (they auto-expire)
        aws s3 ls

  volumes:
    - name: credentials
      emptyDir: {}
```

## Access Control

### RBAC for Pipelines

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pipeline-runner
  namespace: ci-cd

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pipeline-runner
  namespace: ci-cd
rules:
  # Allow pipeline execution
  - apiGroups: ["tekton.dev"]
    resources: ["pipelineruns", "taskruns"]
    verbs: ["get", "list", "watch", "create"]

  # Allow reading secrets
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["pipeline-credentials", "registry-credentials"]

  # Allow creating pods
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch", "create", "delete"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pipeline-runner
  namespace: ci-cd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pipeline-runner
subjects:
  - kind: ServiceAccount
    name: pipeline-runner
    namespace: ci-cd

---
# Deployment permissions (separate SA)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: deployer
  namespace: ci-cd

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: deployer
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "statefulsets", "daemonsets"]
    verbs: ["get", "list", "create", "update", "patch"]

  - apiGroups: [""]
    resources: ["services", "configmaps"]
    verbs: ["get", "list", "create", "update", "patch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: deployer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: deployer
subjects:
  - kind: ServiceAccount
    name: deployer
    namespace: ci-cd
```

### OPA Gatekeeper Policies

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string

  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Pipeline must have labels: %v", [missing])
        }

---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: pipeline-must-have-labels
spec:
  match:
    kinds:
      - apiGroups: ["tekton.dev"]
        kinds: ["Pipeline", "Task"]
  parameters:
    labels:
      - "app.kubernetes.io/name"
      - "app.kubernetes.io/version"
      - "security-scan"
```

## Audit and Compliance

### Tekton Chains for Attestation

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: chains-config
  namespace: tekton-chains
data:
  artifacts.taskrun.format: "in-toto"
  artifacts.taskrun.storage: "oci"
  artifacts.oci.storage: "oci"
  artifacts.pipelinerun.format: "in-toto"
  artifacts.pipelinerun.storage: "oci"
  transparency.enabled: "true"
  transparency.url: "https://rekor.sigstore.dev"

---
apiVersion: v1
kind: Secret
metadata:
  name: signing-secrets
  namespace: tekton-chains
type: Opaque
stringData:
  cosign.key: |
    -----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----
  cosign.password: "password"
  cosign.pub: |
    -----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----
```

### Audit Logging

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-policy
  namespace: kube-system
data:
  policy.yaml: |
    apiVersion: audit.k8s.io/v1
    kind: Policy
    rules:
      # Log all pipeline executions
      - level: RequestResponse
        resources:
          - group: "tekton.dev"
            resources: ["pipelineruns", "taskruns"]

      # Log all secret access
      - level: Metadata
        resources:
          - group: ""
            resources: ["secrets"]
        namespaces: ["ci-cd"]

      # Log all deployments
      - level: RequestResponse
        resources:
          - group: "apps"
            resources: ["deployments"]
        verbs: ["create", "update", "patch", "delete"]
```

### Compliance Reporting

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: compliance-report
  namespace: ci-cd
spec:
  schedule: "0 0 * * 0"  # Weekly
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: compliance-reporter
          containers:
            - name: report
              image: python:3.11-alpine
              command:
                - python
                - /scripts/compliance-report.py
              volumeMounts:
                - name: scripts
                  mountPath: /scripts
          volumes:
            - name: scripts
              configMap:
                name: compliance-scripts
          restartPolicy: OnFailure

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: compliance-scripts
  namespace: ci-cd
data:
  compliance-report.py: |
    #!/usr/bin/env python3
    import json
    import subprocess
    from datetime import datetime, timedelta

    def check_compliance():
        report = {
            "date": datetime.now().isoformat(),
            "checks": []
        }

        # 1. Check all images are signed
        result = subprocess.run([
            "kubectl", "get", "pods", "--all-namespaces",
            "-o", "json"
        ], capture_output=True)

        pods = json.loads(result.stdout)
        unsigned_images = []

        for pod in pods['items']:
            for container in pod['spec']['containers']:
                image = container['image']
                verify_result = subprocess.run([
                    "cosign", "verify", image
                ], capture_output=True)

                if verify_result.returncode != 0:
                    unsigned_images.append(image)

        report['checks'].append({
            "name": "Image Signing",
            "passed": len(unsigned_images) == 0,
            "details": {
                "unsigned_images": unsigned_images
            }
        })

        # 2. Check vulnerability scan age
        # 3. Check SLSA provenance
        # 4. Check secret rotation

        # Generate report
        print(json.dumps(report, indent=2))

        # Upload to compliance system
        subprocess.run([
            "curl", "-X", "POST",
            "https://compliance.example.com/api/reports",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(report)
        ])

    if __name__ == "__main__":
        check_compliance()
```

## Container Security

### Distroless Images

```dockerfile
# Build stage
FROM golang:1.21 as builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Final stage - distroless
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/main /
USER nonroot:nonroot
ENTRYPOINT ["/main"]
```

### Security Context

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10000
        fsGroup: 10000
        seccompProfile:
          type: RuntimeDefault

      containers:
        - name: app
          image: registry.example.com/app:latest
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /cache

      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
```

## Runtime Protection

### Falco Rules

```yaml
- rule: Suspicious Container Activity
  desc: Detect suspicious activity in CI/CD containers
  condition: >
    container and
    container.name startswith "tekton-" and
    (proc.name in (nc, ncat, netcat, wget, curl) or
     spawned_process and not proc.name in (sh, bash, git, go, npm))
  output: >
    Suspicious activity in CI/CD container
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING
  tags: [ci-cd, container, suspicious]

- rule: Unauthorized Network Connection from Build
  desc: Detect unexpected network connections during build
  condition: >
    container and
    container.name startswith "build-" and
    fd.sip exists and
    not fd.sip in (allowed_registries) and
    fd.l4proto = tcp
  output: >
    Unexpected network connection from build container
    (connection=%fd.name container=%container.name)
  priority: WARNING
```

## Best Practices Summary

### Security Checklist

- [ ] **Source verification**: Verify commit signatures
- [ ] **Dependency scanning**: Check all dependencies for vulnerabilities
- [ ] **SAST**: Run static analysis on code
- [ ] **Secret detection**: Scan for leaked secrets
- [ ] **Hermetic builds**: Isolated, reproducible builds
- [ ] **Image signing**: Sign all container images
- [ ] **SBOM generation**: Create software bill of materials
- [ ] **Vulnerability scanning**: Scan images for CVEs
- [ ] **Policy enforcement**: Automated policy checks
- [ ] **Least privilege**: Minimal RBAC permissions
- [ ] **Audit logging**: Complete audit trail
- [ ] **Runtime protection**: Monitor running containers
- [ ] **Secrets management**: External secrets with rotation
- [ ] **Network policies**: Restrict network access
- [ ] **Compliance reporting**: Regular compliance checks

### Defense in Depth Layers

```
┌─────────────────────────────────────────────────────────┐
│  Layer 7: Compliance & Audit                            │
│  - Audit logs, compliance reports, attestations         │
├─────────────────────────────────────────────────────────┤
│  Layer 6: Runtime Protection                            │
│  - Falco, admission controllers, network policies       │
├─────────────────────────────────────────────────────────┤
│  Layer 5: Deployment Verification                       │
│  - Image signature verification, SLSA checks            │
├─────────────────────────────────────────────────────────┤
│  Layer 4: Artifact Security                             │
│  - Image signing, SBOM, provenance                      │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Build Security                                │
│  - Container scanning, config audit, malware scan       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Code Security                                 │
│  - SAST, dependency scan, secret detection              │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Source Security                               │
│  - Commit signing, branch protection, 2FA               │
└─────────────────────────────────────────────────────────┘
```

## Additional Resources

- [SLSA Framework](https://slsa.dev/)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [CNCF Security Best Practices](https://www.cncf.io/blog/2021/10/05/kubernetes-security-best-practices/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final)
