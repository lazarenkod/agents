# Kyverno Policies Library and Best Practices

## Table of Contents

- [Policy Structure](#policy-structure)
- [Validation Policies](#validation-policies)
- [Mutation Policies](#mutation-policies)
- [Generation Policies](#generation-policies)
- [Image Verification](#image-verification)
- [Advanced Patterns](#advanced-patterns)
- [Policy Exceptions](#policy-exceptions)
- [Testing and Validation](#testing-and-validation)

## Policy Structure

### ClusterPolicy vs Policy

**ClusterPolicy** - Cluster-wide scope:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-pod-security-standards
  annotations:
    policies.kyverno.io/title: Require Pod Security Standards
    policies.kyverno.io/category: Pod Security Standards (Baseline)
    policies.kyverno.io/severity: high
    policies.kyverno.io/subject: Pod
    policies.kyverno.io/description: >-
      Enforces Pod Security Standards baseline profile across all namespaces.
spec:
  # Applies to all namespaces
  validationFailureAction: Audit  # or Enforce
  background: true  # Scan existing resources
  rules:
  - name: baseline-pss
    # Rule definition
```

**Policy** - Namespace-scoped:

```yaml
apiVersion: kyverno.io/v1
kind: Policy
metadata:
  name: require-team-label
  namespace: production
spec:
  # Only applies to production namespace
  validationFailureAction: Enforce
  rules:
  - name: check-team-label
    # Rule definition
```

### Policy Fields

```yaml
spec:
  # Validation failure action
  validationFailureAction: Audit | Enforce

  # Apply to existing resources (audit)
  background: true | false

  # Failure policy if webhook fails
  failurePolicy: Fail | Ignore

  # Webhook timeout
  webhookTimeoutSeconds: 10

  # Resource matching
  rules:
  - name: rule-name
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          namespaces:
          - production
          - staging
          selector:
            matchLabels:
              app: critical

    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
          - kube-public

    # Condition (CEL or JMESPath)
    preconditions:
      all:
      - key: "{{ request.operation }}"
        operator: NotEquals
        value: DELETE

    # Validation, mutation, or generation
    validate: {...}
    mutate: {...}
    generate: {...}
```

## Validation Policies

### Basic Validation

**1. Require Labels:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  background: true
  rules:
  - name: check-required-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
          - Deployment
          - Service
    validate:
      message: "Required labels missing: team, environment, cost-center"
      pattern:
        metadata:
          labels:
            team: "?*"
            environment: "dev | staging | prod"
            cost-center: "?*"
```

**2. Resource Limits:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
  - name: validate-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "CPU and memory limits are required"
      pattern:
        spec:
          containers:
          - name: "*"
            resources:
              limits:
                memory: "?*"
                cpu: "?*"
              requests:
                memory: "?*"
                cpu: "?*"
```

**3. Security Context:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-security-context
spec:
  validationFailureAction: Enforce
  rules:
  - name: non-root-user
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Containers must run as non-root user"
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
          containers:
          - name: "*"
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                drop:
                - ALL
              seccompProfile:
                type: RuntimeDefault
```

### Advanced Validation with CEL

**CEL (Common Expression Language):**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cel-validation-example
spec:
  validationFailureAction: Enforce
  rules:
  - name: validate-replica-count
    match:
      any:
      - resources:
          kinds:
          - Deployment
    validate:
      cel:
        expressions:
        - expression: "object.spec.replicas >= 2"
          message: "Deployments must have at least 2 replicas for HA"

        - expression: "object.spec.replicas <= 100"
          message: "Deployments cannot exceed 100 replicas"

        - expression: |
            object.metadata.namespace == 'production' ?
              object.spec.replicas >= 3 : true
          message: "Production deployments require minimum 3 replicas"
```

### Validation with foreach

**Validate Each Container:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-container-images
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-image-registry
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Container images must be from approved registries"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            all:
            - key: "{{ element.image }}"
              operator: NotIn
              value:
              - "gcr.io/*"
              - "registry.company.com/*"
              - "quay.io/company/*"
```

**Validate Resource Ratios:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-resource-ratios
spec:
  validationFailureAction: Audit
  rules:
  - name: memory-limit-request-ratio
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: "Memory limit cannot exceed 2x request"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            all:
            - key: "{{ divide(to_number(element.resources.limits.memory || '0'), to_number(element.resources.requests.memory || '1')) }}"
              operator: GreaterThan
              value: 2
```

## Mutation Policies

### Strategic Merge Patch

**Add Default Labels:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  background: false
  rules:
  - name: add-labels
    match:
      any:
      - resources:
          kinds:
          - Pod
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            +(managed-by): "kyverno"
            +(compliance-scanned): "true"
            # + prefix: add if not exists
            # no prefix: replace if exists
```

**Add Security Context:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-security-context
spec:
  background: false
  rules:
  - name: set-security-context
    match:
      any:
      - resources:
          kinds:
          - Pod
    exclude:
      any:
      - resources:
          namespaces:
          - kube-system
    mutate:
      patchStrategicMerge:
        spec:
          securityContext:
            +(runAsNonRoot): true
            +(seccompProfile):
              type: RuntimeDefault
          containers:
          - (name): "*"
            securityContext:
              +(allowPrivilegeEscalation): false
              +(capabilities):
                drop:
                - ALL
              +(readOnlyRootFilesystem): true
```

**Add Resource Limits:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-resources
spec:
  background: false
  rules:
  - name: add-resources
    match:
      any:
      - resources:
          kinds:
          - Pod
    preconditions:
      all:
      - key: "{{ request.object.metadata.namespace }}"
        operator: NotEquals
        value: "kube-system"
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - (name): "*"
            resources:
              +(limits):
                +(memory): "512Mi"
                +(cpu): "500m"
              +(requests):
                +(memory): "256Mi"
                +(cpu): "100m"
```

### JSON Patch

**Add Annotation:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-timestamp-annotation
spec:
  background: false
  rules:
  - name: add-timestamp
    match:
      any:
      - resources:
          kinds:
          - Deployment
    mutate:
      patchesJson6902: |-
        - op: add
          path: /metadata/annotations/created-by-kyverno
          value: "{{ request.userInfo.username }}"
        - op: add
          path: /metadata/annotations/created-at
          value: "{{ time_now_utc() }}"
```

**Conditional Mutation:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-node-selector-prod
spec:
  background: false
  rules:
  - name: add-node-selector
    match:
      any:
      - resources:
          kinds:
          - Pod
          namespaces:
          - production
    mutate:
      patchesJson6902: |-
        - op: add
          path: /spec/nodeSelector
          value:
            workload-type: production
            node.kubernetes.io/instance-type: n2-standard-8
```

### foreach Mutation

**Inject Sidecar:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: inject-sidecar
spec:
  background: false
  rules:
  - name: inject-logging-sidecar
    match:
      any:
      - resources:
          kinds:
          - Pod
          selector:
            matchLabels:
              inject-logging: "true"
    mutate:
      patchStrategicMerge:
        spec:
          containers:
          - name: logging-sidecar
            image: fluent/fluent-bit:2.0
            volumeMounts:
            - name: varlog
              mountPath: /var/log
          volumes:
          - (name): varlog
            emptyDir: {}
```

## Generation Policies

### Generate NetworkPolicy

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-network-policy
spec:
  background: true
  rules:
  - name: deny-all-traffic
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
      apiVersion: networking.k8s.io/v1
      kind: NetworkPolicy
      name: default-deny-all
      namespace: "{{ request.object.metadata.name }}"
      synchronize: true
      data:
        spec:
          podSelector: {}
          policyTypes:
          - Ingress
          - Egress
```

### Generate ResourceQuota

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-quota
spec:
  rules:
  - name: generate-resourcequota
    match:
      any:
      - resources:
          kinds:
          - Namespace
    exclude:
      any:
      - resources:
          namespaces:
          - kube-*
    generate:
      apiVersion: v1
      kind: ResourceQuota
      name: default-quota
      namespace: "{{ request.object.metadata.name }}"
      synchronize: true
      data:
        spec:
          hard:
            requests.cpu: "10"
            requests.memory: "20Gi"
            limits.cpu: "20"
            limits.memory: "40Gi"
            persistentvolumeclaims: "10"
            services.loadbalancers: "2"
```

### Generate LimitRange

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-limitrange
spec:
  rules:
  - name: generate-default-limits
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: v1
      kind: LimitRange
      name: default-limits
      namespace: "{{ request.object.metadata.name }}"
      synchronize: true
      data:
        spec:
          limits:
          - default:
              cpu: "500m"
              memory: "512Mi"
            defaultRequest:
              cpu: "100m"
              memory: "256Mi"
            max:
              cpu: "2"
              memory: "2Gi"
            min:
              cpu: "50m"
              memory: "128Mi"
            type: Container
```

### Generate from ConfigMap

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: clone-configmap
spec:
  rules:
  - name: clone-company-ca
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: v1
      kind: ConfigMap
      name: company-ca-bundle
      namespace: "{{ request.object.metadata.name }}"
      synchronize: true
      clone:
        namespace: kube-system
        name: company-ca-bundle
```

## Image Verification

### Cosign Signature Verification

**Basic Signature Verification:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: Enforce
  background: false
  webhookTimeoutSeconds: 30
  rules:
  - name: verify-signature
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
              MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
              -----END PUBLIC KEY-----
```

**Keyless Verification (OIDC):**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-keyless
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-keyless
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "ghcr.io/myorg/*"
      attestors:
      - entries:
        - keyless:
            subject: "https://github.com/myorg/*"
            issuer: "https://token.actions.githubusercontent.com"
            rekor:
              url: https://rekor.sigstore.dev
```

**Attestation Verification:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-attestations
spec:
  validationFailureAction: Enforce
  rules:
  - name: verify-sbom
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "gcr.io/mycompany/*"
      attestations:
      - predicateType: https://spdx.dev/Document
        attestors:
        - entries:
          - keys:
              publicKeys: |-
                -----BEGIN PUBLIC KEY-----
                MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
                -----END PUBLIC KEY-----
        conditions:
        - all:
          - key: "{{ packages[].name }}"
            operator: NotIn
            value:
            - log4j  # Banned package
```

**Vulnerability Scan Results:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-scan-results
spec:
  validationFailureAction: Enforce
  rules:
  - name: check-vulnerabilities
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
            operator: LessThan
            value: 1
          - key: "{{ scanner.result.summary.HIGH }}"
            operator: LessThan
            value: 5
```

## Advanced Patterns

### Context Variables

**API Call Context:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-ingress-host
spec:
  rules:
  - name: check-host-unique
    match:
      any:
      - resources:
          kinds:
          - Ingress
    context:
    - name: allIngresses
      apiCall:
        urlPath: "/apis/networking.k8s.io/v1/ingresses"
        jmesPath: "items[].spec.rules[].host"
    validate:
      message: "Ingress host must be unique"
      deny:
        conditions:
          any:
          - key: "{{ request.object.spec.rules[].host }}"
            operator: AnyIn
            value: "{{ allIngresses }}"
```

**ConfigMap Context:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: validate-allowed-repos
spec:
  rules:
  - name: check-allowed-registries
    match:
      any:
      - resources:
          kinds:
          - Pod
    context:
    - name: allowedRegistries
      configMap:
        name: allowed-registries
        namespace: kyverno
    validate:
      message: "Image must be from allowed registry: {{ allowedRegistries.data.registries }}"
      foreach:
      - list: "request.object.spec.containers"
        deny:
          conditions:
            all:
            - key: "{{ element.image }}"
              operator: NotIn
              value: "{{ allowedRegistries.data.registries }}"
```

**Variable Context:**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-quota-based-on-env
spec:
  rules:
  - name: set-quota
    match:
      any:
      - resources:
          kinds:
          - Namespace
    context:
    - name: quotaLimits
      variable:
        value:
          dev:
            cpu: "10"
            memory: "20Gi"
          staging:
            cpu: "50"
            memory: "100Gi"
          prod:
            cpu: "100"
            memory: "200Gi"
        jmesPath: "{{ request.object.metadata.labels.environment || 'dev' }}"
    generate:
      apiVersion: v1
      kind: ResourceQuota
      name: env-quota
      namespace: "{{ request.object.metadata.name }}"
      data:
        spec:
          hard:
            requests.cpu: "{{ quotaLimits.cpu }}"
            requests.memory: "{{ quotaLimits.memory }}"
```

### JMESPath Expressions

**Common Patterns:**

```yaml
# Check if all containers have resource limits
validate:
  message: "All containers must have resource limits"
  deny:
    conditions:
      any:
      - key: "{{ request.object.spec.containers[?!resources.limits.memory] | length(@) }}"
        operator: GreaterThan
        value: 0

# Get unique image registries
context:
- name: imageRegistries
  variable:
    value: "{{ request.object.spec.containers[].image | [].split(@, '/')[0] | unique(@) }}"

# Check if any container is privileged
validate:
  deny:
    conditions:
      any:
      - key: "{{ request.object.spec.containers[?securityContext.privileged] | length(@) }}"
        operator: GreaterThan
        value: 0

# Calculate total CPU requests
context:
- name: totalCPU
  variable:
    value: "{{ request.object.spec.containers[].resources.requests.cpu | sum(@) }}"
```

### Preconditions

**Operation-Based:**

```yaml
rules:
- name: validate-update-only
  match:
    any:
    - resources:
        kinds:
        - ConfigMap
  preconditions:
    all:
    - key: "{{ request.operation }}"
      operator: Equals
      value: UPDATE
  validate:
    message: "Cannot modify immutable ConfigMap"
    deny:
      conditions:
        all:
        - key: "{{ request.object.metadata.labels.immutable }}"
          operator: Equals
          value: "true"
```

**Label-Based:**

```yaml
rules:
- name: require-approval
  match:
    any:
    - resources:
        kinds:
        - Deployment
  preconditions:
    all:
    - key: "{{ request.object.metadata.namespace }}"
      operator: Equals
      value: production
    - key: "{{ request.operation }}"
      operator: In
      value:
      - CREATE
      - UPDATE
  validate:
    message: "Production deployments require approval label"
    pattern:
      metadata:
        labels:
          approved-by: "?*"
          approved-date: "?*"
```

## Policy Exceptions

### PolicyException Resource

```yaml
apiVersion: kyverno.io/v2alpha1
kind: PolicyException
metadata:
  name: legacy-app-exception
  namespace: legacy-system
spec:
  # Which policies to exempt
  exceptions:
  - policyName: disallow-privileged-containers
    ruleNames:
    - check-privileged
  - policyName: require-resource-limits
    ruleNames:
    - validate-resources

  # What resources are exempted
  match:
    any:
    - resources:
        kinds:
        - Pod
        namespaces:
        - legacy-system
        names:
        - legacy-app-*
        - old-system-*

  # Optional: Conditions for exception
  conditions:
    all:
    - key: "{{ request.object.metadata.labels.legacy }}"
      operator: Equals
      value: "true"
```

**Time-Limited Exception:**

```yaml
apiVersion: kyverno.io/v2alpha1
kind: PolicyException
metadata:
  name: temporary-exception
  annotations:
    expires-on: "2024-12-31"
    jira-ticket: "SEC-12345"
    approved-by: "security-team@company.com"
spec:
  exceptions:
  - policyName: require-security-context
    ruleNames:
    - non-root-user
  match:
    any:
    - resources:
        kinds:
        - Deployment
        namespaces:
        - migration
        names:
        - database-migration
```

## Testing and Validation

### Kyverno CLI Testing

**Test Structure:**

```yaml
# kyverno-test.yaml
name: policy-tests
policies:
  - policies/require-labels.yaml
  - policies/require-resources.yaml
resources:
  - resources/good-pod.yaml
  - resources/bad-pod.yaml
results:
  # Test 1: Good pod should pass
  - policy: require-labels
    rule: check-required-labels
    resource: good-pod
    namespace: default
    kind: Pod
    result: pass

  # Test 2: Bad pod should fail
  - policy: require-labels
    rule: check-required-labels
    resource: bad-pod
    namespace: default
    kind: Pod
    result: fail

  # Test 3: Pod without resources should fail
  - policy: require-resources
    rule: validate-resources
    resource: bad-pod
    kind: Pod
    result: fail
```

**Run Tests:**

```bash
# Test policies
kyverno test kyverno-test.yaml

# Test with values file
kyverno test kyverno-test.yaml --values-file values.yaml

# Test specific policy
kyverno test . --policy require-labels.yaml
```

### Apply Command (Dry Run)

```bash
# Test policy against resources
kyverno apply policies/ --resource resources/ --audit

# Test with specific values
kyverno apply policy.yaml --resource deployment.yaml \
  --set request.namespace=production

# Test mutation
kyverno apply mutate-policy.yaml --resource pod.yaml \
  --output yaml

# Test generation
kyverno apply generate-policy.yaml --resource namespace.yaml \
  --output yaml
```

### Policy Validation

```bash
# Validate policy syntax
kubectl apply --dry-run=server -f policy.yaml

# Kyverno validation
kyverno validate policy.yaml

# Check policy references
kyverno validate policy.yaml --audit
```

### CI/CD Integration

**GitHub Actions:**

```yaml
name: Kyverno Policy Tests
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Kyverno CLI
        uses: kyverno/action-install-cli@v0.2.0

      - name: Validate Policies
        run: kyverno validate policies/*.yaml

      - name: Run Policy Tests
        run: kyverno test tests/kyverno-test.yaml

      - name: Test Against Sample Resources
        run: kyverno apply policies/ --resource examples/ --audit

      - name: Generate Policy Report
        run: |
          kyverno apply policies/ --resource examples/ \
            --policy-report > policy-report.yaml

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: policy-report
          path: policy-report.yaml
```

## Best Practices

### Policy Organization

```yaml
# Use consistent naming
metadata:
  name: {action}-{resource}-{condition}
  # Examples:
  # - require-pod-resources
  # - disallow-privileged-containers
  # - add-default-labels

# Use annotations
annotations:
  policies.kyverno.io/title: Human-Readable Title
  policies.kyverno.io/category: Pod Security Standards (Baseline)
  policies.kyverno.io/severity: high | medium | low
  policies.kyverno.io/subject: Pod | Deployment | Service
  policies.kyverno.io/description: >-
    Detailed description of policy purpose and requirements
  policies.kyverno.io/minversion: "1.9.0"
```

### Error Messages

```yaml
# Good: Actionable messages
validate:
  message: |
    Container {{ element.name }} must not run as root.
    Set securityContext.runAsNonRoot: true
    and securityContext.runAsUser to UID > 0.

# Bad: Vague messages
validate:
  message: "Security violation"
```

### Performance

```yaml
# 1. Disable background scanning for mutations
mutate:
  ...
spec:
  background: false

# 2. Use specific resource matching
match:
  any:
  - resources:
      kinds:  # Specific kinds
      - Pod
      - Deployment
      namespaces:  # Specific namespaces
      - production
      - staging

# 3. Use preconditions to skip unnecessary checks
preconditions:
  all:
  - key: "{{ request.operation }}"
    operator: NotEquals
    value: DELETE

# 4. Limit webhook scope
webhookTimeoutSeconds: 10
failurePolicy: Ignore  # For non-critical policies
```

### Gradual Rollout

```yaml
# Phase 1: Audit mode
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: new-policy
spec:
  validationFailureAction: Audit  # Monitor violations
  background: true

# Phase 2: Enforce in non-production
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: new-policy
spec:
  validationFailureAction: Enforce
  background: true
  match:
    any:
    - resources:
        namespaces:
        - dev-*
        - test-*

# Phase 3: Enforce everywhere
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: new-policy
spec:
  validationFailureAction: Enforce
  background: true
```

## Common Patterns

### Pod Security Standards

```yaml
# Baseline Profile
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: pss-baseline
spec:
  validationFailureAction: Enforce
  background: true
  rules:
  - name: disallow-privileged
    match:
      any:
      - resources:
          kinds: [Pod]
    validate:
      podSecurity:
        level: baseline
        version: latest
```

### Multi-Tenancy

```yaml
# Enforce namespace isolation
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: namespace-isolation
spec:
  validationFailureAction: Enforce
  rules:
  - name: deny-cross-namespace
    match:
      any:
      - resources:
          kinds:
          - RoleBinding
          - ClusterRoleBinding
    validate:
      message: "Cannot reference ServiceAccounts from other namespaces"
      deny:
        conditions:
          any:
          - key: "{{ request.object.subjects[?namespace != '{{ request.namespace }}'] | length(@) }}"
            operator: GreaterThan
            value: 0
```

## References

- [Kyverno Documentation](https://kyverno.io/docs/)
- [Kyverno Policy Library](https://kyverno.io/policies/)
- [Kyverno CLI](https://kyverno.io/docs/kyverno-cli/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [JMESPath Specification](https://jmespath.org/)
- [CEL Language](https://github.com/google/cel-spec)
