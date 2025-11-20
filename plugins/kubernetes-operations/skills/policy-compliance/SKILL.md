---
name: policy-compliance
description: Kubernetes policy enforcement and compliance frameworks. Use when implementing admission control, runtime security, CIS benchmarks, or regulatory compliance (NIST, SOC2, PCI-DSS) using OPA Gatekeeper, Kyverno, or Falco.
---

# Kubernetes Policy Compliance / Соблюдение Политик Kubernetes

## When to Use This Skill / Когда Использовать

**English:**
- Implementing admission control policies (OPA Gatekeeper, Kyverno)
- Enforcing security policies and compliance standards
- Runtime security monitoring with Falco
- Meeting regulatory requirements (CIS, NIST, SOC2, PCI-DSS)
- Policy-as-Code implementation and testing
- Compliance auditing and reporting
- Validating, mutating, or generating Kubernetes resources
- Preventing misconfigurations and security violations

**Русский:**
- Внедрение политик контроля допуска (OPA Gatekeeper, Kyverno)
- Обеспечение соблюдения политик безопасности и стандартов
- Мониторинг безопасности времени выполнения с Falco
- Соответствие нормативным требованиям (CIS, NIST, SOC2, PCI-DSS)
- Внедрение и тестирование Policy-as-Code
- Аудит и отчетность по соблюдению требований
- Валидация, мутация или генерация ресурсов Kubernetes
- Предотвращение неправильных конфигураций и нарушений безопасности

## Policy Enforcement Frameworks / Фреймворки Обеспечения Политик

### OPA Gatekeeper

**Core Concepts:**

OPA (Open Policy Agent) Gatekeeper is a Kubernetes-native admission controller using the Rego policy language. It validates, mutates, and audits resources declaratively.

**Architecture Components:**

```yaml
# ConstraintTemplate - Reusable policy definition
# Constraint - Policy instance with parameters
# Config - Gatekeeper configuration
# Audit - Periodic compliance scanning
```

**Key Features:**
- **Declarative Policy**: Rego-based policy language
- **Template Reusability**: ConstraintTemplates for policy libraries
- **Audit Mode**: Detect violations without blocking
- **External Data**: Query external systems in policies
- **Mutation**: Modify resources before admission
- **Metrics**: Prometheus integration for policy violations

**When to Use:**
- Complex policy logic requiring Rego's expressiveness
- Multi-cluster policy consistency
- External data integration (e.g., CMDB, registries)
- Advanced mutation scenarios
- Organizations already using OPA ecosystem

### Kyverno

**Core Concepts:**

Kyverno is a Kubernetes-native policy engine using YAML for policy definitions. No new language required.

**Architecture Components:**

```yaml
# ClusterPolicy - Cluster-wide policies
# Policy - Namespace-scoped policies
# PolicyException - Temporary exemptions
# PolicyReport - Compliance status
```

**Key Features:**
- **YAML-Native**: No new language, use familiar Kubernetes syntax
- **Validate**: Block non-compliant resources
- **Mutate**: Modify resources (defaults, labels, annotations)
- **Generate**: Create additional resources (NetworkPolicies, ConfigMaps)
- **Verify Images**: Cosign signature verification
- **Policy Reports**: Standard wgpolicyk8s.io/v1alpha2 reports

**When to Use:**
- Teams prefer YAML over Rego
- Image verification with Cosign/Notary
- Resource generation patterns (e.g., auto-create NetworkPolicies)
- Simpler policy requirements
- Kubernetes-first environments

### Falco Runtime Security

**Core Concepts:**

Falco monitors kernel syscalls and Kubernetes audit logs to detect runtime security threats and compliance violations.

**Architecture Components:**

```yaml
# Falco Rules - Threat detection patterns
# Falco Sidekick - Alert routing and response
# Falco Exporter - Prometheus metrics
# Audit Log Source - K8s API audit events
```

**Key Features:**
- **Kernel-Level Monitoring**: eBPF or kernel module
- **Kubernetes Audit**: API server audit log analysis
- **Real-Time Alerts**: Detect suspicious behavior immediately
- **Rule Customization**: Extend or override default rules
- **Response Actions**: Integrate with SIEM, PagerDuty, Slack
- **CIS Compliance**: Built-in CIS benchmark detection

**When to Use:**
- Runtime threat detection (container escapes, privilege escalation)
- Compliance monitoring (file access, network connections)
- Audit log analysis for suspicious API activity
- Integration with security incident response
- Detecting cryptomining, reverse shells, or unauthorized processes

## Policy-as-Code Best Practices / Лучшие Практики Policy-as-Code

### Design Principles

**1. Shift-Left Security:**
- Test policies in CI/CD before deployment
- Validate against sample manifests
- Fail fast in development, not production

**2. Gradual Rollout:**
```yaml
# Start with audit mode
enforcementAction: audit
# Monitor violations
# Fix issues
# Switch to enforcement
enforcementAction: deny
```

**3. Clear Messaging:**
```yaml
# Provide actionable error messages
message: |
  Container must not run as root.
  Set securityContext.runAsNonRoot: true
  and securityContext.runAsUser to UID > 0.
```

**4. Policy Testing:**
```bash
# OPA Gatekeeper testing
gator test -f policies/ -f test/

# Kyverno CLI testing
kyverno test policies/ --values-file test/values.yaml
```

**5. Version Control:**
- Store policies in Git
- Use semantic versioning
- Implement GitOps deployment
- Maintain policy changelog

### Policy Organization / Организация Политик

**Recommended Structure:**

```
policies/
├── baseline/              # CIS Kubernetes Benchmark baseline
│   ├── pod-security/
│   ├── network-security/
│   └── rbac-security/
├── organizational/        # Company-specific policies
│   ├── naming-conventions/
│   ├── resource-quotas/
│   └── label-requirements/
├── compliance/            # Regulatory compliance
│   ├── pci-dss/
│   ├── soc2/
│   └── nist/
└── testing/              # Policy test cases
    ├── test-cases/
    └── test-values/
```

**Policy Lifecycle:**

1. **Development**: Write policy + tests
2. **Validation**: Test against known good/bad manifests
3. **Audit**: Deploy in audit mode, collect violations
4. **Remediation**: Fix existing violations
5. **Enforcement**: Switch to deny/enforce mode
6. **Monitoring**: Track violations, refine policies

## Compliance Frameworks / Фреймворки Соответствия

### CIS Kubernetes Benchmark

**Coverage Areas:**

**Control Plane:**
- API Server configuration
- Controller Manager settings
- Scheduler security
- etcd encryption and access

**Worker Nodes:**
- Kubelet configuration
- Node-level security
- Container runtime settings

**Policies:**
- Pod Security Standards
- RBAC restrictions
- Network policies
- Audit logging

**Implementation:**

```yaml
# Example: CIS 5.2.1 - Minimize admission of privileged containers
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
  annotations:
    policies.kyverno.io/title: Disallow Privileged Containers
    policies.kyverno.io/category: Pod Security Standards (Baseline)
    policies.kyverno.io/severity: high
    policies.kyverno.io/subject: Pod
    policies.kyverno.io/description: >-
      CIS 5.2.1 - Privileged containers have access to all Linux Kernel
      capabilities and devices. Containers should not be allowed to run
      as privileged.
spec:
  validationFailureAction: Audit  # Start with audit
  background: true
  rules:
  - name: check-privileged
    match:
      any:
      - resources:
          kinds:
          - Pod
    validate:
      message: >-
        Privileged mode is not allowed. Set privileged to false.
        CIS Benchmark 5.2.1
      pattern:
        spec:
          containers:
          - =(securityContext):
              =(privileged): false
```

### NIST SP 800-190 (Application Container Security)

**Key Controls:**

1. **Image Security**: Vulnerability scanning, trusted registries
2. **Registry Security**: Access control, image signing
3. **Orchestrator Security**: RBAC, network segmentation
4. **Container Runtime**: Read-only filesystems, capability dropping
5. **Host OS**: Hardened nodes, kernel updates

### SOC2 Type II

**Relevant Trust Services Criteria:**

**CC6.1 - Logical Access:**
- RBAC policies
- Service account restrictions
- API audit logging

**CC6.6 - Logical Access Removal:**
- Automated RBAC cleanup
- Service account lifecycle management

**CC7.2 - System Monitoring:**
- Falco runtime monitoring
- Policy violation alerts
- Audit log retention

### PCI-DSS 3.2.1

**Key Requirements:**

**Req 2 - Default Credentials:**
- Prohibit default secrets
- Enforce secret rotation

**Req 6 - Secure Development:**
- Image vulnerability scanning
- Approved base images only

**Req 10 - Logging:**
- Audit all API access
- Immutable audit logs
- 90-day retention

**Req 11 - Security Testing:**
- Runtime security scanning
- Network segmentation testing

## Policy Patterns / Паттерны Политик

### Validation Patterns

**1. Required Labels:**

```yaml
# Enforce organizational labels
- name: require-labels
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
# Enforce CPU/memory limits
- name: require-resource-limits
  validate:
    message: "CPU and memory limits required"
    pattern:
      spec:
        containers:
        - resources:
            limits:
              memory: "?*"
              cpu: "?*"
            requests:
              memory: "?*"
              cpu: "?*"
```

**3. Image Registry Restriction:**

```yaml
# Only allow approved registries
- name: restrict-image-registries
  validate:
    message: "Images must come from approved registries: gcr.io/mycompany, registry.company.com"
    pattern:
      spec:
        containers:
        - image: "gcr.io/mycompany/* | registry.company.com/*"
```

### Mutation Patterns

**1. Add Default Labels:**

```yaml
# Auto-add labels
- name: add-default-labels
  mutate:
    patchStrategicMerge:
      metadata:
        labels:
          managed-by: kyverno
          +(environment): "{{request.namespace}}"
```

**2. Enforce Security Defaults:**

```yaml
# Set secure defaults
- name: add-security-context
  mutate:
    patchStrategicMerge:
      spec:
        securityContext:
          runAsNonRoot: true
          seccompProfile:
            type: RuntimeDefault
        containers:
        - (name): "*"
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
              - ALL
```

**3. Add Resource Defaults:**

```yaml
# Set default resource limits
- name: add-default-resources
  mutate:
    patchStrategicMerge:
      spec:
        containers:
        - (name): "*"
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
            requests:
              memory: "256Mi"
              cpu: "100m"
```

### Generation Patterns

**1. Auto-Generate NetworkPolicy:**

```yaml
# Generate deny-all NetworkPolicy for new namespaces
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-network-policy
spec:
  rules:
  - name: generate-deny-all
    match:
      any:
      - resources:
          kinds:
          - Namespace
    generate:
      apiVersion: networking.k8s.io/v1
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

**2. Auto-Generate ResourceQuota:**

```yaml
# Generate ResourceQuota for new namespaces
- name: generate-resource-quota
  generate:
    apiVersion: v1
    kind: ResourceQuota
    name: default-quota
    namespace: "{{request.object.metadata.name}}"
    data:
      spec:
        hard:
          requests.cpu: "10"
          requests.memory: "20Gi"
          limits.cpu: "20"
          limits.memory: "40Gi"
```

## Audit and Reporting / Аудит и Отчетность

### Policy Reports (wgpolicyk8s.io)

**PolicyReport Resource:**

```yaml
apiVersion: wgpolicyk8s.io/v1alpha2
kind: PolicyReport
metadata:
  name: polr-ns-default
  namespace: default
summary:
  pass: 45
  fail: 3
  warn: 2
  error: 0
  skip: 0
results:
- policy: require-labels
  rule: check-team-label
  resource:
    apiVersion: v1
    kind: Pod
    name: nginx
    namespace: default
  result: fail
  scored: true
  message: "Required label 'team' is missing"
  timestamp:
    seconds: 1634567890
```

### Compliance Dashboards

**Prometheus Metrics:**

```promql
# Policy violation rate
rate(gatekeeper_violations_total[5m])

# Policy enforcement by action
sum by (enforcement_action) (gatekeeper_constraint_template_count)

# Kyverno policy results
kyverno_policy_results_total{policy_result="fail"}
```

**Grafana Dashboard Panels:**

1. **Violation Trends**: Time series of violations
2. **Top Violators**: Resources with most violations
3. **Compliance Score**: Percentage of compliant resources
4. **Policy Coverage**: Policies per namespace/cluster
5. **Remediation Time**: Time to fix violations

### Continuous Compliance Scanning

**Scheduled Audits:**

```yaml
# Gatekeeper audit runs every hour
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
spec:
  audit:
    auditInterval: 3600
    constraintViolationsLimit: 1000
    auditFromCache: Enabled
```

**Automated Reporting:**

```bash
#!/bin/bash
# Daily compliance report

# Collect Gatekeeper violations
kubectl get constraint -A -o json > gatekeeper-violations.json

# Collect Kyverno PolicyReports
kubectl get policyreport -A -o json > kyverno-reports.json

# Collect Falco alerts (last 24h)
kubectl logs -n falco -l app=falco --since=24h > falco-alerts.log

# Generate compliance report
./generate-compliance-report.sh \
  --gatekeeper gatekeeper-violations.json \
  --kyverno kyverno-reports.json \
  --falco falco-alerts.log \
  --output compliance-report-$(date +%Y%m%d).pdf

# Send to compliance team
aws s3 cp compliance-report-$(date +%Y%m%d).pdf s3://compliance-reports/
```

## Testing and Validation / Тестирование и Валидация

### Policy Testing Strategy

**1. Unit Tests:**

Test individual policies against sample manifests.

```yaml
# test/pod-security/test.yaml (Kyverno)
name: disallow-privileged-test
policies:
  - ../policies/pod-security/disallow-privileged.yaml
resources:
  - resources.yaml
results:
  - policy: disallow-privileged-containers
    rule: check-privileged
    resource: privileged-pod
    kind: Pod
    result: fail
  - policy: disallow-privileged-containers
    rule: check-privileged
    resource: non-privileged-pod
    kind: Pod
    result: pass
```

**2. Integration Tests:**

Test policy enforcement in test cluster.

```bash
# Test enforcement
kubectl apply -f test/bad-manifest.yaml
# Should be denied

kubectl apply -f test/good-manifest.yaml
# Should be allowed
```

**3. Regression Tests:**

Ensure policy changes don't break existing workloads.

```bash
# Export current cluster resources
kubectl get all,cm,secret -A -o yaml > current-state.yaml

# Apply new policies in audit mode
kubectl apply -f policies/

# Check for new violations
kubectl get constraint -A
# Review violations before enforcement
```

### CI/CD Integration

**GitHub Actions Example:**

```yaml
name: Policy Validation
on: [pull_request]
jobs:
  validate-policies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Kyverno CLI
        run: |
          curl -LO https://github.com/kyverno/kyverno/releases/download/v1.10.0/kyverno-cli_v1.10.0_linux_x86_64.tar.gz
          tar -xzf kyverno-cli_v1.10.0_linux_x86_64.tar.gz
          sudo mv kyverno /usr/local/bin/

      - name: Install Gator (Gatekeeper)
        run: |
          curl -LO https://github.com/open-policy-agent/gatekeeper/releases/download/v3.13.0/gator-v3.13.0-linux-amd64.tar.gz
          tar -xzf gator-v3.13.0-linux-amd64.tar.gz
          sudo mv gator /usr/local/bin/

      - name: Test Kyverno Policies
        run: kyverno test policies/kyverno/ --values-file test/values.yaml

      - name: Test Gatekeeper Policies
        run: gator test -f policies/gatekeeper/ -f test/gatekeeper/

      - name: Validate Policy Syntax
        run: |
          kubectl apply --dry-run=server -f policies/
```

## Security Best Practices / Лучшие Практики Безопасности

### Defense in Depth

**Layer 1 - Image Security:**
- Scan images for vulnerabilities
- Verify image signatures
- Use minimal base images
- Prohibit latest tags

**Layer 2 - Admission Control:**
- Validate security contexts
- Enforce resource limits
- Restrict capabilities
- Block privileged containers

**Layer 3 - Runtime Security:**
- Monitor syscalls with Falco
- Detect anomalous behavior
- Alert on policy violations
- Automated incident response

**Layer 4 - Network Security:**
- Default-deny NetworkPolicies
- Egress filtering
- Service mesh mTLS
- API server authentication

### Least Privilege

**Pod Security:**
```yaml
# Minimal security context
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  fsGroup: 10001
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

**RBAC:**
```yaml
# Minimal permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

### Policy Exemptions

**Use Sparingly:**

```yaml
# Kyverno PolicyException
apiVersion: kyverno.io/v2alpha1
kind: PolicyException
metadata:
  name: legacy-app-exception
spec:
  exceptions:
  - policyName: disallow-privileged-containers
    ruleNames:
    - check-privileged
  match:
    any:
    - resources:
        kinds:
        - Pod
        namespaces:
        - legacy-system
        names:
        - legacy-app-*
```

**Exception Guidelines:**
- Document justification
- Set expiration dates
- Require approval workflow
- Periodic review
- Plan remediation

## Troubleshooting / Устранение Неполадок

### Common Issues

**1. Policy Not Enforcing:**

```bash
# Check policy status
kubectl get clusterpolicy -A
kubectl describe clusterpolicy <policy-name>

# Check webhook configuration
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations

# Check controller logs
kubectl logs -n kyverno -l app.kubernetes.io/name=kyverno
kubectl logs -n gatekeeper-system -l control-plane=controller-manager
```

**2. False Positives:**

```bash
# Review policy logic
kubectl get constraint <constraint-name> -o yaml

# Test with sample manifest
kyverno apply policy.yaml --resource manifest.yaml

# Check audit results
kubectl get constraint <constraint-name> -o jsonpath='{.status.violations}'
```

**3. Performance Impact:**

```bash
# Monitor webhook latency
kubectl get --raw /metrics | grep apiserver_admission_webhook_admission_duration_seconds

# Check policy complexity
# Simplify Rego logic
# Use policy caching
# Exclude namespaces

# Gatekeeper audit optimization
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
spec:
  match:
  - excludedNamespaces: ["kube-system", "kube-public"]
```

**4. Falco High CPU:**

```bash
# Reduce rule verbosity
# Use rule priorities
# Filter out noisy rules
# Adjust buffering

# falco.yaml
syscall_event_drops:
  actions:
    - ignore
  rate: 0.1
  max_burst: 1000
```

## Migration Strategies / Стратегии Миграции

### From PodSecurityPolicy to Policy Engine

**Step 1: Inventory PSPs:**

```bash
kubectl get psp -o yaml > psp-backup.yaml
kubectl get pod -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext}{"\n"}{end}'
```

**Step 2: Convert to Kyverno/Gatekeeper:**

```bash
# Use conversion tools
kyverno convert psp psp-backup.yaml

# Manual conversion for complex PSPs
# Map PSP fields to policy patterns
```

**Step 3: Parallel Run:**

```yaml
# Run both PSP and new policies
# Set new policies to audit mode
validationFailureAction: Audit
```

**Step 4: Cutover:**

```bash
# Delete PSPs after validation
kubectl delete psp --all
```

### From Audit to Enforcement

**Gradual Rollout:**

```yaml
# Week 1: Deploy in audit mode
validationFailureAction: Audit

# Week 2: Enforce in dev/test
validationFailureAction: Enforce
# Only in dev namespaces

# Week 3: Enforce in staging
# Expand to staging namespaces

# Week 4: Enforce in production
# Full enforcement
```

## References / Ссылки

For detailed implementation patterns, examples, and advanced configurations, see:

- **[OPA Rego Patterns](./references/opa-rego-patterns.md)** - Rego policy examples, testing, debugging
- **[Kyverno Policies](./references/kyverno-policies.md)** - Kyverno policy library and best practices
- **[Falco Rules](./references/falco-rules.md)** - Falco rule examples, custom rules, alert routing
- **[Compliance Frameworks](./references/compliance-frameworks.md)** - CIS, NIST, SOC2, PCI-DSS compliance mapping

**Policy Libraries (Assets):**
- **[Gatekeeper Library](./assets/gatekeeper-library.yaml)** - OPA Gatekeeper policy library
- **[Kyverno Library](./assets/kyverno-library.yaml)** - Kyverno policy library
- **[Falco Rules](./assets/falco-rules.yaml)** - Falco security rules

**External Resources:**
- [OPA Gatekeeper Documentation](https://open-policy-agent.github.io/gatekeeper/)
- [Kyverno Documentation](https://kyverno.io/)
- [Falco Documentation](https://falco.org/docs/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- [Kubernetes Policy WG](https://github.com/kubernetes-sigs/wg-policy-prototypes)
