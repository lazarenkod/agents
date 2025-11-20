# OPA Rego Patterns and Examples

## Table of Contents

- [Rego Language Fundamentals](#rego-language-fundamentals)
- [ConstraintTemplate Patterns](#constrainttemplate-patterns)
- [Advanced Rego Techniques](#advanced-rego-techniques)
- [External Data Integration](#external-data-integration)
- [Testing and Debugging](#testing-and-debugging)
- [Performance Optimization](#performance-optimization)

## Rego Language Fundamentals

### Basic Syntax

```rego
# Package declaration (required)
package kubernetes.admission

# Import libraries
import data.lib.core
import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Deny rule - returns violation message
deny[msg] {
  # Condition 1
  input.request.kind.kind == "Pod"

  # Condition 2
  container := input.request.object.spec.containers[_]

  # Condition 3
  container.securityContext.privileged == true

  # Return message
  msg := sprintf("Privileged container '%s' is not allowed", [container.name])
}

# Violation rule (Gatekeeper format)
violation[{"msg": msg}] {
  input.review.kind.kind == "Pod"
  container := input.review.object.spec.containers[_]
  container.securityContext.privileged
  msg := sprintf("Container '%s' is privileged", [container.name])
}
```

### Common Patterns

**1. Iterate Over Arrays:**

```rego
# Bad: Inefficient
violation[{"msg": msg}] {
  containers := input.review.object.spec.containers
  count(containers) > 0
  container := containers[i]  # Iterate with index
  not container.resources.limits.memory
  msg := sprintf("Container %s missing memory limit", [container.name])
}

# Good: Efficient
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]  # Use underscore
  not container.resources.limits.memory
  msg := sprintf("Container %s missing memory limit", [container.name])
}
```

**2. Check for Existence:**

```rego
# Check if field exists
has_field(obj, field) {
  obj[field]
}

has_field(obj, field) = false {
  not obj[field]
}

# Check if nested field exists
has_security_context(container) {
  container.securityContext
}

# Usage
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not has_security_context(container)
  msg := sprintf("Container %s missing securityContext", [container.name])
}
```

**3. Default Values:**

```rego
# Provide default if field missing
get_image(container) = image {
  image := container.image
}

get_image(container) = "unknown" {
  not container.image
}

# Default rule
default allow = false

allow {
  # Conditions for allow
}
```

**4. String Matching:**

```rego
# Exact match
violation[{"msg": msg}] {
  input.review.object.spec.hostNetwork == true
  msg := "hostNetwork is not allowed"
}

# Regex match
violation[{"msg": msg}] {
  image := input.review.object.spec.containers[_].image
  not regex.match(`^(gcr.io|registry.company.com)/`, image)
  msg := sprintf("Image %s from unauthorized registry", [image])
}

# Prefix/suffix match
violation[{"msg": msg}] {
  image := input.review.object.spec.containers[_].image
  endswith(image, ":latest")
  msg := "Image tag 'latest' is not allowed"
}

# Contains match
violation[{"msg": msg}] {
  name := input.review.object.metadata.name
  contains(name, "test")  # Requires: import future.keywords.contains
  msg := "Resource name cannot contain 'test'"
}
```

## ConstraintTemplate Patterns

### Basic Template Structure

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
  annotations:
    description: Requires resources to contain specified labels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        # OpenAPIV3 schema for parameters
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
              description: List of required labels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          # Get required labels from constraint parameters
          required := {label | label := input.parameters.labels[_]}

          # Get labels from resource
          provided := {label | input.review.object.metadata.labels[label]}

          # Calculate missing labels
          missing := required - provided
          count(missing) > 0

          msg := sprintf("Missing required labels: %v", [missing])
        }
```

**Constraint Instance:**

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod", "Service"]
    namespaces:
      - "production"
  parameters:
    labels:
      - "team"
      - "cost-center"
      - "environment"
```

### Advanced Template Patterns

**1. Resource Limits:**

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8scontainerresources
spec:
  crd:
    spec:
      names:
        kind: K8sContainerResources
      validation:
        openAPIV3Schema:
          type: object
          properties:
            exemptImages:
              type: array
              items:
                type: string
            maxCpu:
              type: string
            maxMemory:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8scontainerresources

        import future.keywords.in

        # Convert resource string to numeric value
        mem_to_bytes(mem) = bytes {
          # Handle Ki, Mi, Gi suffixes
          endswith(mem, "Gi")
          count := trim_suffix(mem, "Gi")
          bytes := to_number(count) * 1024 * 1024 * 1024
        }

        mem_to_bytes(mem) = bytes {
          endswith(mem, "Mi")
          count := trim_suffix(mem, "Mi")
          bytes := to_number(count) * 1024 * 1024
        }

        mem_to_bytes(mem) = bytes {
          endswith(mem, "Ki")
          count := trim_suffix(mem, "Ki")
          bytes := to_number(count) * 1024
        }

        cpu_to_millicores(cpu) = millicores {
          # Handle m suffix
          endswith(cpu, "m")
          count := trim_suffix(cpu, "m")
          millicores := to_number(count)
        }

        cpu_to_millicores(cpu) = millicores {
          # Whole number (cores)
          not endswith(cpu, "m")
          millicores := to_number(cpu) * 1000
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]

          # Skip exempt images
          not is_exempt(container.image)

          # Check memory limit
          not container.resources.limits.memory
          msg := sprintf("Container %s missing memory limit", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not is_exempt(container.image)

          max_mem := mem_to_bytes(input.parameters.maxMemory)
          container_mem := mem_to_bytes(container.resources.limits.memory)
          container_mem > max_mem

          msg := sprintf("Container %s memory limit %s exceeds maximum %s",
                         [container.name, container.resources.limits.memory, input.parameters.maxMemory])
        }

        is_exempt(image) {
          exempt := input.parameters.exemptImages[_]
          startswith(image, exempt)
        }
```

**2. Image Registry Validation:**

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedrepos
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRepos
      validation:
        openAPIV3Schema:
          type: object
          properties:
            repos:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedrepos

        violation[{"msg": msg}] {
          container := get_containers[_]
          not is_allowed_repo(container.image)
          msg := sprintf("Image '%s' comes from unauthorized registry. Allowed: %v",
                         [container.image, input.parameters.repos])
        }

        get_containers[container] {
          container := input.review.object.spec.containers[_]
        }

        get_containers[container] {
          container := input.review.object.spec.initContainers[_]
        }

        get_containers[container] {
          container := input.review.object.spec.ephemeralContainers[_]
        }

        is_allowed_repo(image) {
          repo := input.parameters.repos[_]
          startswith(image, repo)
        }
```

**3. Network Policy Enforcement:**

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequirenetworkpolicy
spec:
  crd:
    spec:
      names:
        kind: K8sRequireNetworkPolicy
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequirenetworkpolicy

        violation[{"msg": msg}] {
          input.review.kind.kind == "Namespace"
          namespace := input.review.object.metadata.name

          # Check if NetworkPolicy exists for namespace
          not has_network_policy(namespace)

          msg := sprintf("Namespace '%s' must have a NetworkPolicy", [namespace])
        }

        has_network_policy(namespace) {
          # Query data.inventory for existing NetworkPolicies
          netpol := data.inventory.cluster["networking.k8s.io/v1"]["NetworkPolicy"][namespace][_]
        }
```

## Advanced Rego Techniques

### Library Functions

Create reusable functions in a library:

```rego
# lib/core.rego
package lib.core

# Check if container runs as root
is_root_container(container) {
  not container.securityContext.runAsNonRoot
}

is_root_container(container) {
  container.securityContext.runAsUser == 0
}

# Check if container has privilege escalation
allows_privilege_escalation(container) {
  container.securityContext.allowPrivilegeEscalation
}

allows_privilege_escalation(container) {
  not has_field(container.securityContext, "allowPrivilegeEscalation")
}

# Check if field exists
has_field(obj, field) {
  _ := obj[field]
}

# Get all containers (including init and ephemeral)
all_containers[container] {
  container := input.review.object.spec.containers[_]
}

all_containers[container] {
  container := input.review.object.spec.initContainers[_]
}

all_containers[container] {
  container := input.review.object.spec.ephemeralContainers[_]
}

# Parse image registry
get_registry(image) = registry {
  parts := split(image, "/")
  count(parts) > 1
  registry := parts[0]
}

get_registry(image) = "docker.io" {
  parts := split(image, "/")
  count(parts) == 1
}
```

**Using Library:**

```rego
package k8ssecuritycontext

import data.lib.core

violation[{"msg": msg}] {
  container := core.all_containers[_]
  core.is_root_container(container)
  msg := sprintf("Container %s runs as root", [container.name])
}
```

### Complex Logic Patterns

**1. Conditional Violations:**

```rego
# Different violations based on environment
violation[{"msg": msg}] {
  # Production namespace
  is_production_namespace
  container := input.review.object.spec.containers[_]
  container.image contains ":latest"
  msg := "Production pods cannot use :latest tag"
}

violation[{"msg": msg}] {
  # Development namespace (warning only)
  not is_production_namespace
  container := input.review.object.spec.containers[_]
  container.image contains ":latest"
  msg := "WARNING: Using :latest tag is discouraged"
}

is_production_namespace {
  namespace := input.review.object.metadata.namespace
  namespace == "production"
}

is_production_namespace {
  labels := input.review.object.metadata.labels
  labels.environment == "production"
}
```

**2. Aggregation and Counting:**

```rego
# Limit total CPU across all containers
violation[{"msg": msg}] {
  total_cpu := sum([cpu |
    container := input.review.object.spec.containers[_]
    cpu := cpu_to_millicores(container.resources.requests.cpu)
  ])

  max_cpu := 4000  # 4 cores
  total_cpu > max_cpu

  msg := sprintf("Total CPU requests (%dm) exceeds limit (%dm)", [total_cpu, max_cpu])
}

# Count violations
violation[{"msg": msg}] {
  privileged_count := count([c |
    c := input.review.object.spec.containers[_]
    c.securityContext.privileged
  ])

  privileged_count > 0
  msg := sprintf("%d privileged containers found", [privileged_count])
}
```

**3. Cross-Resource Validation:**

```rego
# Validate Service matches Deployment selector
violation[{"msg": msg}] {
  input.review.kind.kind == "Service"
  service_selector := input.review.object.spec.selector

  # Find matching Deployments
  deployment := data.inventory.cluster["apps/v1"]["Deployment"][_][_]
  deployment_selector := deployment.spec.selector.matchLabels

  # Check if selectors match
  not selectors_match(service_selector, deployment_selector)

  msg := sprintf("Service selector does not match any Deployment", [])
}

selectors_match(s1, s2) {
  s1 == s2
}
```

## External Data Integration

### Provider Configuration

```yaml
apiVersion: externaldata.gatekeeper.sh/v1beta1
kind: Provider
metadata:
  name: image-scanner
spec:
  url: http://image-scanner.security.svc.cluster.local:8080/scan
  timeout: 5
  caBundle: LS0tLS1...  # Base64 CA cert
```

### Using External Data in Rego

```rego
package k8simagescan

violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  image := container.image

  # Call external provider
  response := external_data({
    "provider": "image-scanner",
    "keys": [image]
  })

  # Parse response
  scan_result := response[image]

  # Check vulnerability count
  critical_vulns := scan_result.criticalVulnerabilities
  critical_vulns > 0

  msg := sprintf("Image %s has %d critical vulnerabilities", [image, critical_vulns])
}
```

**External Provider Example (Go):**

```go
package main

import (
  "encoding/json"
  "net/http"
)

type ScanRequest struct {
  Keys []string `json:"keys"`
}

type ScanResponse struct {
  Items []ScanResult `json:"items"`
}

type ScanResult struct {
  Key    string `json:"key"`
  Value  string `json:"value"`
  Error  string `json:"error,omitempty"`
}

func scanHandler(w http.ResponseWriter, r *http.Request) {
  var req ScanRequest
  json.NewDecoder(r.Body).Decode(&req)

  var results []ScanResult
  for _, image := range req.Keys {
    // Scan image (call Trivy, Clair, etc.)
    vulns := scanImage(image)

    resultData, _ := json.Marshal(map[string]int{
      "criticalVulnerabilities": vulns.Critical,
      "highVulnerabilities":     vulns.High,
    })

    results = append(results, ScanResult{
      Key:   image,
      Value: string(resultData),
    })
  }

  json.NewEncoder(w).Encode(ScanResponse{Items: results})
}
```

## Testing and Debugging

### Unit Testing with Conftest

**Install Conftest:**

```bash
brew install conftest
# or
curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz | tar xz
```

**Test Structure:**

```
policies/
├── policy.rego
└── policy_test.rego
```

**policy_test.rego:**

```rego
package k8srequiredlabels

# Test data
test_pod_missing_labels {
  input := {
    "review": {
      "kind": {"kind": "Pod"},
      "object": {
        "metadata": {
          "name": "test-pod",
          "labels": {}
        }
      }
    },
    "parameters": {
      "labels": ["team", "environment"]
    }
  }

  # Expect violation
  count(violation) > 0

  # Check message
  violation[_].msg == "Missing required labels: {\"environment\", \"team\"}"
}

test_pod_with_labels {
  input := {
    "review": {
      "kind": {"kind": "Pod"},
      "object": {
        "metadata": {
          "name": "test-pod",
          "labels": {
            "team": "platform",
            "environment": "prod"
          }
        }
      }
    },
    "parameters": {
      "labels": ["team", "environment"]
    }
  }

  # Expect no violation
  count(violation) == 0
}
```

**Run Tests:**

```bash
conftest verify -p policies/
# PASS: policies/policy_test.rego
```

### Testing with Gator

**Gator Test Suite:**

```yaml
# suite.yaml
kind: Suite
apiVersion: test.gatekeeper.sh/v1alpha1
tests:
  - name: require-labels-deployment
    template: k8srequiredlabels
    constraint: require-team-label.yaml
    cases:
      - name: deployment-missing-labels
        object: testdata/deployment-no-labels.yaml
        assertions:
          - violations: yes
      - name: deployment-with-labels
        object: testdata/deployment-with-labels.yaml
        assertions:
          - violations: no
```

**Run Gator Tests:**

```bash
gator test -f policies/ -f tests/
# ok    k8srequiredlabels    0.020s
```

### Debugging Rego Policies

**1. Print Debugging:**

```rego
violation[{"msg": msg}] {
  # Print intermediate values
  trace(sprintf("Input object: %v", [input.review.object]))

  container := input.review.object.spec.containers[_]
  trace(sprintf("Checking container: %v", [container.name]))

  container.securityContext.privileged
  msg := "Container is privileged"
}
```

**2. OPA REPL:**

```bash
# Start REPL
opa run policies/

# Load input
> data.kubernetes.admission.violation with input as {"review": {...}}

# Evaluate expressions
> container := input.review.object.spec.containers[_]

# Check intermediate results
> container.name
```

**3. Gatekeeper Dry Run:**

```bash
# Apply constraint in dry-run mode
kubectl apply --dry-run=server -f constraint.yaml

# Check what would be violated
gator test -f policies/ -f manifests/
```

### Performance Profiling

```bash
# Profile policy execution
opa test -b policies/ --profile

# Measure time per rule
opa eval --profile --bundle policies/ data.kubernetes.admission.violation
```

## Performance Optimization

### Best Practices

**1. Minimize Iterations:**

```rego
# Bad: Multiple iterations
violation[{"msg": msg}] {
  containers := input.review.object.spec.containers
  count(containers) > 0
  container := containers[i]
  not container.resources.limits
  msg := "Missing limits"
}

# Good: Single iteration
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.resources.limits
  msg := sprintf("Container %s missing limits", [container.name])
}
```

**2. Early Exit:**

```rego
# Bad: Check all conditions
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  expensive_check(container)
  another_expensive_check(container)
  final_check(container)
  msg := "Violation"
}

# Good: Check cheapest first
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]

  # Cheap check first
  container.securityContext.privileged

  # Expensive checks only if needed
  expensive_check(container)
  msg := "Violation"
}
```

**3. Cache Results:**

```rego
# Bad: Recalculate for each container
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  # Expensive calculation
  max := calculate_max_cpu(input.parameters)
  container_cpu := get_cpu(container)
  container_cpu > max
  msg := "Exceeds max CPU"
}

# Good: Calculate once
max_cpu := calculate_max_cpu(input.parameters)

violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  container_cpu := get_cpu(container)
  container_cpu > max_cpu
  msg := "Exceeds max CPU"
}
```

**4. Use Built-in Functions:**

```rego
# Bad: Manual string matching
violation[{"msg": msg}] {
  image := input.review.object.spec.containers[_].image
  parts := split(image, "/")
  registry := parts[0]
  registry != "gcr.io"
  registry != "registry.company.com"
  msg := "Unauthorized registry"
}

# Good: Use regex
violation[{"msg": msg}] {
  image := input.review.object.spec.containers[_].image
  not regex.match(`^(gcr.io|registry.company.com)/`, image)
  msg := "Unauthorized registry"
}
```

### Gatekeeper Optimization

**1. Namespace Exclusions:**

```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
spec:
  match:
  - excludedNamespaces:
    - kube-system
    - kube-public
    - kube-node-lease
    - gatekeeper-system
  - processes:
    - "*"
```

**2. Audit Interval:**

```yaml
spec:
  audit:
    auditInterval: 3600  # Audit every hour instead of 60s
```

**3. Resource Caching:**

```yaml
spec:
  sync:
    syncOnly:
    - group: ""
      version: "v1"
      kind: "Namespace"
    - group: "apps"
      version: "v1"
      kind: "Deployment"
```

## Common Pitfalls

**1. Forgetting to Handle Missing Fields:**

```rego
# Bad: Crashes if securityContext missing
violation[{"msg": msg}] {
  container.securityContext.runAsUser == 0
  msg := "Running as root"
}

# Good: Check existence first
violation[{"msg": msg}] {
  container.securityContext
  container.securityContext.runAsUser == 0
  msg := "Running as root"
}
```

**2. Incorrect Set Operations:**

```rego
# Bad: Comparing arrays
required := input.parameters.labels  # Array
provided := input.review.object.metadata.labels  # Object
missing := required - provided  # Type mismatch!

# Good: Convert to sets
required := {label | label := input.parameters.labels[_]}
provided := {label | input.review.object.metadata.labels[label]}
missing := required - provided
```

**3. Not Handling All Container Types:**

```rego
# Bad: Only checks regular containers
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  # Check container
}

# Good: Check all container types
violation[{"msg": msg}] {
  container := all_containers[_]
  # Check container
}

all_containers[c] { c := input.review.object.spec.containers[_] }
all_containers[c] { c := input.review.object.spec.initContainers[_] }
all_containers[c] { c := input.review.object.spec.ephemeralContainers[_] }
```

## References

- [Rego Language Reference](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [Gatekeeper Policy Library](https://github.com/open-policy-agent/gatekeeper-library)
- [OPA Built-in Functions](https://www.openpolicyagent.org/docs/latest/policy-reference/)
- [Conftest Testing](https://www.conftest.dev/)
- [Gator Testing](https://open-policy-agent.github.io/gatekeeper/website/docs/gator/)
