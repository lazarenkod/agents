# Kubernetes Compliance Frameworks

## Table of Contents

- [CIS Kubernetes Benchmark](#cis-kubernetes-benchmark)
- [NIST SP 800-190](#nist-sp-800-190)
- [SOC 2 Type II](#soc-2-type-ii)
- [PCI-DSS](#pci-dss)
- [HIPAA](#hipaa)
- [GDPR](#gdpr)
- [ISO 27001](#iso-27001)
- [Compliance Automation](#compliance-automation)

## CIS Kubernetes Benchmark

### Overview

The CIS Kubernetes Benchmark provides prescriptive guidance for establishing a secure configuration posture for Kubernetes.

**Current Version**: 1.8.0 (for Kubernetes 1.27+)

**Coverage Areas**:
1. Control Plane Components
2. Etcd
3. Control Plane Configuration
4. Worker Nodes
5. Policies

### Control Plane Security

#### 1.1 API Server

**1.1.1 - API Server Pod Specification File Permissions**

```bash
# Audit
stat -c %a /etc/kubernetes/manifests/kube-apiserver.yaml

# Remediation
chmod 644 /etc/kubernetes/manifests/kube-apiserver.yaml
```

**Policy Implementation:**

```yaml
# Falco rule
- rule: CIS 1.1.1 - API Server Config File Permissions
  desc: API server config file should be 644
  condition: >
    open_write and
    fd.name = "/etc/kubernetes/manifests/kube-apiserver.yaml" and
    not proc.name in (kubeadm, kubectl, vim, nano)
  output: >
    Unauthorized modification of API server config
    (user=%user.name process=%proc.name file=%fd.name)
  priority: CRITICAL
  tags: [cis, control_plane]
```

**1.1.2 - API Server Pod Specification File Ownership**

```bash
# Audit
stat -c %U:%G /etc/kubernetes/manifests/kube-apiserver.yaml

# Remediation
chown root:root /etc/kubernetes/manifests/kube-apiserver.yaml
```

**1.1.11 - Ensure that the admission control plugin AlwaysPullImages is set**

```yaml
# kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --enable-admission-plugins=AlwaysPullImages,NodeRestriction,PodSecurityPolicy
```

**Kyverno Policy:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-1-1-11-always-pull-images
  annotations:
    policies.kyverno.io/title: CIS 1.1.11 - Always Pull Images
    policies.kyverno.io/category: CIS Benchmark
spec:
  validationFailureAction: Audit
  rules:
  - name: always-pull-images
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CIS 1.1.11 - Containers must always pull images"
      pattern:
        spec:
          containers:
          - name: "*"
            imagePullPolicy: Always
```

#### 1.2 API Server Configuration

**1.2.1 - Ensure that the --anonymous-auth argument is set to false**

```yaml
# kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --anonymous-auth=false
```

**1.2.5 - Ensure that the --kubelet-certificate-authority argument is set**

```yaml
# kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --kubelet-certificate-authority=/etc/kubernetes/pki/ca.crt
```

**1.2.19 - Ensure that the --audit-log-path argument is set**

```yaml
# kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-log-maxage=30
    - --audit-log-maxbackup=10
    - --audit-log-maxsize=100
```

**1.2.22 - Ensure that the --audit-log-maxage argument is set to 30 or greater**

```yaml
# Audit
ps -ef | grep kube-apiserver | grep audit-log-maxage

# kube-apiserver.yaml
- --audit-log-maxage=30
```

### Etcd Security

#### 2.1 - Ensure that the --cert-file and --key-file arguments are set

```yaml
# etcd.yaml
spec:
  containers:
  - command:
    - etcd
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --key-file=/etc/kubernetes/pki/etcd/server.key
```

#### 2.2 - Ensure that the --client-cert-auth argument is set to true

```yaml
# etcd.yaml
- --client-cert-auth=true
```

#### 2.7 - Ensure that etcd is encrypted at rest

```yaml
# encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: <base64-encoded-secret>
    - identity: {}

# kube-apiserver.yaml
- --encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

### Worker Node Security

#### 4.2.1 - Ensure that the --anonymous-auth argument is set to false

```yaml
# kubelet-config.yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous:
    enabled: false
```

#### 4.2.6 - Ensure that the --protect-kernel-defaults argument is set to true

```yaml
# kubelet-config.yaml
protectKernelDefaults: true
```

**Validation Script:**

```bash
#!/bin/bash
# Check kubelet configuration

echo "Checking CIS Worker Node compliance..."

# 4.2.1 - Anonymous auth
if grep -q "anonymous: enabled: false" /var/lib/kubelet/config.yaml; then
  echo "✓ 4.2.1 - Anonymous auth disabled"
else
  echo "✗ 4.2.1 - Anonymous auth not disabled"
fi

# 4.2.6 - Protect kernel defaults
if grep -q "protectKernelDefaults: true" /var/lib/kubelet/config.yaml; then
  echo "✓ 4.2.6 - Kernel defaults protected"
else
  echo "✗ 4.2.6 - Kernel defaults not protected"
fi
```

### Pod Security Policies

#### 5.2 - Pod Security Standards

**5.2.1 - Minimize the admission of privileged containers**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-2-1-disallow-privileged
  annotations:
    policies.kyverno.io/title: CIS 5.2.1 - Disallow Privileged Containers
    policies.kyverno.io/category: CIS Benchmark
spec:
  validationFailureAction: Enforce
  background: true
  rules:
  - name: privileged-containers
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CIS 5.2.1 - Privileged containers are not allowed"
      pattern:
        spec:
          containers:
          - =(securityContext):
              =(privileged): false
```

**5.2.2 - Minimize the admission of containers with root user**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-2-2-require-run-as-nonroot
spec:
  validationFailureAction: Enforce
  rules:
  - name: run-as-non-root
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CIS 5.2.2 - Containers must run as non-root user"
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
          containers:
          - securityContext:
              runAsNonRoot: true
```

**5.2.3 - Minimize the admission of containers with NET_RAW capability**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-2-3-disallow-net-raw
spec:
  validationFailureAction: Enforce
  rules:
  - name: drop-net-raw
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CIS 5.2.3 - NET_RAW capability must be dropped"
      pattern:
        spec:
          containers:
          - securityContext:
              capabilities:
                drop:
                - NET_RAW
```

**5.2.6 - Minimize the admission of containers with allowPrivilegeEscalation**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-2-6-disallow-privilege-escalation
spec:
  validationFailureAction: Enforce
  rules:
  - name: disallow-privilege-escalation
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CIS 5.2.6 - Privilege escalation is not allowed"
      pattern:
        spec:
          containers:
          - securityContext:
              allowPrivilegeEscalation: false
```

### Network Policies

#### 5.3.2 - Ensure that all Namespaces have Network Policies defined

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-3-2-require-network-policy
spec:
  validationFailureAction: Audit
  background: true
  rules:
  - name: validate-networkpolicy
    match:
      any:
      - resources:
          kinds:
          - Namespace
    validate:
      message: "CIS 5.3.2 - All namespaces must have a NetworkPolicy"
      deny:
        conditions:
          all:
          - key: "{{ request.object.metadata.name }}"
            operator: NotIn
            value:
            - kube-system
            - kube-public
            - default
```

**Auto-generate NetworkPolicy:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cis-5-3-2-generate-network-policy
spec:
  background: true
  rules:
  - name: default-deny
    match:
      any:
      - resources:
          kinds:
          - Namespace
    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
          - kube-public
    generate:
      kind: NetworkPolicy
      name: default-deny
      namespace: "{{request.object.metadata.name}}"
      synchronize: true
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

### CIS Compliance Scanning

**kube-bench:**

```bash
# Install kube-bench
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# View results
kubectl logs -f job/kube-bench

# CronJob for continuous scanning
apiVersion: batch/v1
kind: CronJob
metadata:
  name: kube-bench
  namespace: security
spec:
  schedule: "0 0 * * *"  # Daily at midnight
  jobTemplate:
    spec:
      template:
        spec:
          hostPID: true
          containers:
          - name: kube-bench
            image: aquasec/kube-bench:latest
            command: ["kube-bench"]
            volumeMounts:
            - name: var-lib-etcd
              mountPath: /var/lib/etcd
              readOnly: true
            - name: var-lib-kubelet
              mountPath: /var/lib/kubelet
              readOnly: true
            - name: etc-systemd
              mountPath: /etc/systemd
              readOnly: true
            - name: etc-kubernetes
              mountPath: /etc/kubernetes
              readOnly: true
          restartPolicy: Never
          volumes:
          - name: var-lib-etcd
            hostPath:
              path: /var/lib/etcd
          - name: var-lib-kubelet
            hostPath:
              path: /var/lib/kubelet
          - name: etc-systemd
            hostPath:
              path: /etc/systemd
          - name: etc-kubernetes
            hostPath:
              path: /etc/kubernetes
```

## NIST SP 800-190

### Application Container Security Guide

**Image Security (Section 3)**

**3.1 - Image Vulnerabilities**

```yaml
# Require vulnerability scanning
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-3-1-require-scan
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-image-scanned
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "*"
      attestations:
      - predicateType: https://cosign.sigstore.dev/attestation/vuln/v1
        attestors:
        - entries:
          - keys:
              publicKeys: |-
                -----BEGIN PUBLIC KEY-----
                ...
                -----END PUBLIC KEY-----
        conditions:
        - all:
          - key: "{{ scanner.result.summary.CRITICAL }}"
            operator: Equals
            value: 0
          - key: "{{ scanner.result.summary.HIGH }}"
            operator: LessThan
            value: 5
```

**3.2 - Image Configuration Defects**

```yaml
# Disallow root user
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-3-2-no-root
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-non-root
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "NIST 3.2 - Containers must not run as root"
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
          containers:
          - securityContext:
              runAsNonRoot: true
              readOnlyRootFilesystem: true
              capabilities:
                drop:
                - ALL
```

**3.3 - Embedded Malware**

```yaml
# Require signed images from trusted registries
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-3-3-verify-signatures
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-image-signature
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "gcr.io/mycompany/*"
      - "registry.company.com/*"
      attestors:
      - count: 1
        entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
```

**Registry Security (Section 4)**

**4.1 - Insecure Connections**

```yaml
# Require TLS for registry connections
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-4-1-secure-registries
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-secure-registry
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "NIST 4.1 - Images must be from HTTPS registries"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            any:
            - key: "{{ element.image }}"
              operator: In
              value:
              - "http://*"
              - "*/insecure/*"
```

**Orchestrator Security (Section 5)**

**5.1 - Unbounded Administrative Access**

```yaml
# Limit cluster-admin bindings
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-5-1-limit-cluster-admin
spec:
  validationFailureAction: Audit
  rules:
  - name: restrict-cluster-admin
    match:
      any:
      - resources:
          kinds:
          - ClusterRoleBinding
    validate:
      message: "NIST 5.1 - cluster-admin role should be restricted"
      deny:
        conditions:
          all:
          - key: "{{ request.object.roleRef.name }}"
            operator: Equals
            value: cluster-admin
          - key: "{{ request.object.subjects[].name }}"
            operator: NotIn
            value:
            - approved-admin-1
            - approved-admin-2
```

**5.4 - Poorly Separated Inter-Container Network Traffic**

```yaml
# Require network policies
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-5-4-require-netpol
spec:
  background: true
  rules:
  - name: generate-default-deny
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      kind: NetworkPolicy
      name: default-deny-all
      namespace: "{{request.object.metadata.name}}"
      synchronize: true
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

**Container Runtime Security (Section 6)**

**6.1 - Insecure Container Runtime Configurations**

```yaml
# Enforce seccomp, AppArmor, SELinux
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: nist-6-1-runtime-security
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-seccomp
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "NIST 6.1 - Seccomp profile required"
      pattern:
        spec:
          securityContext:
            seccompProfile:
              type: RuntimeDefault | Localhost
```

## SOC 2 Type II

### Trust Services Criteria

**CC6.1 - Logical and Physical Access Controls**

```yaml
# RBAC enforcement
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: soc2-cc6-1-rbac-required
  annotations:
    compliance: "SOC2 CC6.1"
spec:
  validationFailureAction: Audit
  rules:
  - name: require-rbac-subjects
    match:
      any:
      - resources:
          kinds:
          - RoleBinding
          - ClusterRoleBinding
    validate:
      message: "SOC2 CC6.1 - RBAC bindings must reference approved subjects"
      deny:
        conditions:
          any:
          - key: "{{ request.object.subjects[?kind == 'User'].name }}"
            operator: AnyNotIn
            value:
            - approved-user-1@company.com
            - approved-user-2@company.com
```

**CC6.6 - Logical Access Removal**

```yaml
# Detect stale service accounts
apiVersion: batch/v1
kind: CronJob
metadata:
  name: soc2-cc6-6-cleanup-stale-sa
spec:
  schedule: "0 0 * * 0"  # Weekly
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: sa-cleanup
          containers:
          - name: cleanup
            image: bitnami/kubectl:latest
            command:
            - /bin/bash
            - -c
            - |
              # Find ServiceAccounts unused for 90 days
              kubectl get sa -A -o json | \
              jq -r '.items[] |
                select(.metadata.creationTimestamp < (now - 7776000 | todate)) |
                "\(.metadata.namespace)/\(.metadata.name)"' | \
              while read SA; do
                NS=$(echo $SA | cut -d/ -f1)
                NAME=$(echo $SA | cut -d/ -f2)
                echo "Deleting stale ServiceAccount: $NS/$NAME"
                kubectl delete sa $NAME -n $NS
              done
          restartPolicy: OnFailure
```

**CC7.2 - System Monitoring**

```yaml
# Falco monitoring for SOC2
- rule: SOC2 CC7.2 - Unauthorized File Access
  desc: Detect access to sensitive files (SOC2 CC7.2)
  condition: >
    open_read and
    (fd.name glob "/etc/kubernetes/pki/*" or
     fd.name glob "/var/lib/etcd/*" or
     fd.name glob "/etc/kubernetes/*.conf") and
    not proc.name in (kube-apiserver, etcd, kubelet)
  output: >
    SOC2 CC7.2 - Unauthorized sensitive file access
    (user=%user.name process=%proc.name file=%fd.name)
  priority: WARNING
  tags: [soc2, cc7.2]
```

**CC7.3 - Quality Monitoring**

```yaml
# Monitor policy violations
apiVersion: v1
kind: ConfigMap
metadata:
  name: soc2-cc7-3-monitoring
data:
  prometheus-rules.yaml: |
    groups:
    - name: soc2-compliance
      interval: 60s
      rules:
      - alert: SOC2PolicyViolations
        expr: sum(kyverno_policy_results_total{policy_result="fail"}) > 10
        for: 5m
        labels:
          severity: warning
          compliance: soc2
        annotations:
          summary: "High number of policy violations"
          description: "{{ $value }} policy violations in last 5m"
```

**CC8.1 - Change Management**

```yaml
# Audit all changes
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: soc2-cc8-1-audit-changes
spec:
  validationFailureAction: Audit  # Always audit
  background: true
  rules:
  - name: audit-all-changes
    match:
      any:
      - resources:
          kinds:
          - Deployment
          - StatefulSet
          - DaemonSet
          - ConfigMap
          - Secret
    validate:
      message: "SOC2 CC8.1 - Change audited"
      pattern:
        metadata:
          annotations:
            change-ticket: "?*"
            approved-by: "?*"
```

## PCI-DSS

### Payment Card Industry Data Security Standard

**Requirement 2 - Default Settings**

```yaml
# Prohibit default passwords/secrets
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: pci-dss-req2-no-defaults
  annotations:
    compliance: "PCI-DSS Req 2.1"
spec:
  validationFailureAction: Enforce
  rules:
  - name: no-default-secrets
    match:
      any:
      - resources:
          kinds:
          - Secret
    validate:
      message: "PCI-DSS Req 2.1 - Default/weak secrets not allowed"
      deny:
        conditions:
          any:
          - key: "{{ base64_decode(request.object.data.password || '') }}"
            operator: In
            value:
            - "password"
            - "admin"
            - "default"
            - "12345"
```

**Requirement 6 - Secure Development**

```yaml
# Require vulnerability scanning
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: pci-dss-req6-vuln-scan
  annotations:
    compliance: "PCI-DSS Req 6.2"
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-no-critical-vulns
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "*"
      attestations:
      - predicateType: https://cosign.sigstore.dev/attestation/vuln/v1
        conditions:
        - all:
          - key: "{{ scanner.result.summary.CRITICAL }}"
            operator: Equals
            value: 0
```

**Requirement 10 - Logging and Monitoring**

```yaml
# Ensure audit logging
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: pci-dss-req10-audit-log
  annotations:
    compliance: "PCI-DSS Req 10.1"
spec:
  background: false
  rules:
  - name: log-cardholder-access
    match:
      any:
      - resources:
          kinds:
          - Pod
          namespaces:
          - payments
          - cardholder-data
    validate:
      message: "PCI-DSS Req 10.1 - Audit logging required"
      pattern:
        metadata:
          annotations:
            audit-logging: "enabled"
```

**Falco PCI-DSS Rules:**

```yaml
- rule: PCI-DSS Req 10.2 - Cardholder Data Access
  desc: Log all access to cardholder data
  condition: >
    open_read and
    fd.name glob "/data/cardholder/*" and
    not proc.name in (payment-processor, vault-service)
  output: >
    PCI-DSS 10.2 - Cardholder data accessed
    (user=%user.name
    user_loginuid=%user.loginuid
    process=%proc.name
    file=%fd.name
    container=%container.name)
  priority: WARNING
  tags: [pci_dss, req_10_2]

- rule: PCI-DSS Req 10.2.2 - Privileged User Actions
  desc: All actions by privileged users must be logged
  condition: >
    spawned_process and
    user.name in (root, admin, operator) and
    proc.name in (kubectl, docker, crictl)
  output: >
    PCI-DSS 10.2.2 - Privileged user action
    (user=%user.name
    process=%proc.name
    cmdline=%proc.cmdline
    container=%container.name)
  priority: INFO
  tags: [pci_dss, req_10_2_2]
```

**Requirement 11 - Security Testing**

```yaml
# Continuous vulnerability scanning
apiVersion: batch/v1
kind: CronJob
metadata:
  name: pci-dss-req11-vuln-scan
spec:
  schedule: "0 0 * * *"  # Daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: trivy
            image: aquasec/trivy:latest
            command:
            - trivy
            - image
            - --severity
            - CRITICAL,HIGH
            - --exit-code
            - "1"
            - --format
            - json
            - --output
            - /reports/scan-$(date +%Y%m%d).json
            - $(IMAGES)
          restartPolicy: OnFailure
```

## HIPAA

### Health Insurance Portability and Accountability Act

**164.308(a)(1) - Security Management**

```yaml
# Risk analysis and management
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: hipaa-164-308-security-mgmt
  annotations:
    compliance: "HIPAA 164.308(a)(1)"
spec:
  validationFailureAction: Audit
  rules:
  - name: phi-access-control
    match:
      any:
      - resources:
          kinds:
          - Pod
          namespaces:
          - healthcare
          - phi-data
    validate:
      message: "HIPAA 164.308(a)(1) - PHI access requires approval"
      pattern:
        metadata:
          labels:
            phi-access-approved: "true"
            risk-assessment-date: "?*"
```

**164.312(a)(1) - Access Control**

```yaml
# Technical safeguards
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: hipaa-164-312-access-control
spec:
  validationFailureAction: Enforce
  rules:
  - name: unique-user-id
    match:
      any:
      - resources:
          kinds:
          - ServiceAccount
          namespaces:
          - healthcare
    validate:
      message: "HIPAA 164.312(a)(2)(i) - Unique user IDs required"
      pattern:
        metadata:
          annotations:
            user-id: "?*"
            user-type: "healthcare-worker | admin | system"
```

**164.312(b) - Audit Controls**

```yaml
# Falco HIPAA audit rules
- rule: HIPAA 164.312(b) - PHI Access
  desc: Log all access to PHI
  condition: >
    open_read and
    (fd.name glob "/data/phi/*" or
     fd.name glob "/mnt/ehr/*") and
    not proc.name in (ehr-service, patient-portal)
  output: >
    HIPAA 164.312(b) - PHI data accessed
    (user=%user.name
    user_loginuid=%user.loginuid
    process=%proc.name
    file=%fd.name
    container=%container.name
    image=%container.image.repository)
  priority: WARNING
  tags: [hipaa, audit_controls]

- rule: HIPAA 164.312(c) - Integrity Controls
  desc: Detect unauthorized modification of PHI
  condition: >
    open_write and
    fd.name glob "/data/phi/*" and
    not proc.name in (ehr-service, backup-agent)
  output: >
    HIPAA 164.312(c) - PHI data modified
    (user=%user.name process=%proc.name file=%fd.name)
  priority: CRITICAL
  tags: [hipaa, integrity]
```

**164.312(e) - Transmission Security**

```yaml
# Require encryption in transit
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: hipaa-164-312-transmission
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-tls
    match:
      any:
      - resources:
          kinds:
          - Ingress
          namespaces:
          - healthcare
    validate:
      message: "HIPAA 164.312(e) - TLS required for PHI transmission"
      pattern:
        spec:
          tls:
          - secretName: "?*"
```

## GDPR

### General Data Protection Regulation

**Article 32 - Security of Processing**

```yaml
# Encryption and pseudonymization
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: gdpr-article32-encryption
  annotations:
    compliance: "GDPR Article 32"
spec:
  validationFailureAction: Enforce
  rules:
  - name: require-encryption-at-rest
    match:
      any:
      - resources:
          kinds:
          - PersistentVolumeClaim
          namespaces:
          - customer-data
          - personal-data
    validate:
      message: "GDPR Article 32 - Encryption at rest required for personal data"
      pattern:
        metadata:
          annotations:
            encrypted: "true"
            encryption-type: "AES256 | AES128"
```

**Falco GDPR Rules:**

```yaml
- rule: GDPR Article 32 - Personal Data Access
  desc: Log access to personal data
  condition: >
    open_read and
    (fd.name glob "/data/personal/*" or
     fd.name glob "/data/customer/*") and
    not proc.name in (customer-service, gdpr-compliance-agent)
  output: >
    GDPR Article 32 - Personal data accessed
    (user=%user.name process=%proc.name file=%fd.name
    purpose=%container.labels.data-processing-purpose)
  priority: INFO
  tags: [gdpr, article32]
```

## ISO 27001

### Information Security Management

**A.9.2 - User Access Management**

```yaml
# Access provisioning
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: iso27001-a9-2-access-mgmt
spec:
  validationFailureAction: Audit
  rules:
  - name: require-approval
    match:
      any:
      - resources:
          kinds:
          - RoleBinding
          - ClusterRoleBinding
    validate:
      message: "ISO 27001 A.9.2 - Access requires approval"
      pattern:
        metadata:
          annotations:
            approval-ticket: "?*"
            approver: "?*"
            approval-date: "?*"
```

## Compliance Automation

### Policy-as-Code Repository

```
compliance/
├── cis/
│   ├── control-plane/
│   ├── worker-nodes/
│   └── policies/
├── nist/
│   ├── image-security/
│   ├── runtime-security/
│   └── network-security/
├── soc2/
│   ├── access-control/
│   ├── monitoring/
│   └── change-management/
├── pci-dss/
│   └── cardholder-data/
└── reports/
    ├── daily/
    └── monthly/
```

### Continuous Compliance Scanning

```yaml
# compliance-scan.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: compliance-scan
  namespace: compliance
spec:
  schedule: "0 0 * * *"  # Daily
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: compliance-scanner
          containers:
          - name: scanner
            image: compliance-scanner:latest
            command:
            - /bin/bash
            - -c
            - |
              #!/bin/bash
              set -e

              DATE=$(date +%Y%m%d)
              REPORT_DIR=/reports/$DATE

              mkdir -p $REPORT_DIR

              # CIS Benchmark
              echo "Running CIS Benchmark scan..."
              kube-bench > $REPORT_DIR/cis-benchmark.txt

              # Kyverno policy violations
              echo "Checking Kyverno policies..."
              kubectl get policyreport -A -o json > $REPORT_DIR/kyverno-violations.json

              # Falco alerts
              echo "Collecting Falco alerts..."
              kubectl logs -n falco -l app=falco --since=24h > $REPORT_DIR/falco-alerts.log

              # Generate compliance report
              /usr/local/bin/generate-compliance-report \
                --cis $REPORT_DIR/cis-benchmark.txt \
                --kyverno $REPORT_DIR/kyverno-violations.json \
                --falco $REPORT_DIR/falco-alerts.log \
                --output $REPORT_DIR/compliance-report.pdf

              # Upload to compliance storage
              aws s3 sync $REPORT_DIR s3://compliance-reports/$DATE/

              echo "Compliance scan complete: $DATE"
          restartPolicy: OnFailure
```

### Compliance Dashboard

```yaml
# Grafana dashboard for compliance metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: compliance-dashboard
  namespace: monitoring
data:
  compliance.json: |
    {
      "dashboard": {
        "title": "Compliance Monitoring",
        "panels": [
          {
            "title": "CIS Benchmark Score",
            "targets": [
              {
                "expr": "avg(cis_benchmark_score)"
              }
            ]
          },
          {
            "title": "Policy Violations by Framework",
            "targets": [
              {
                "expr": "sum by (compliance_framework) (policy_violations_total)"
              }
            ]
          },
          {
            "title": "Falco Security Alerts",
            "targets": [
              {
                "expr": "sum by (priority) (rate(falco_events_total[1h]))"
              }
            ]
          }
        ]
      }
    }
```

## References

- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- [SOC 2 Trust Services Criteria](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/trustdataintegritytaskforce.html)
- [PCI-DSS Requirements](https://www.pcisecuritystandards.org/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [GDPR Official Text](https://gdpr-info.eu/)
- [ISO 27001 Standard](https://www.iso.org/isoiec-27001-information-security.html)
