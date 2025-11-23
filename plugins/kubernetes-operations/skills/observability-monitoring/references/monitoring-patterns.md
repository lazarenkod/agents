# Monitoring Patterns for Kubernetes

## Мониторинг Kubernetes: Паттерны и Антипаттерны / Monitoring Patterns and Anti-Patterns

### The Four Golden Signals (Google SRE)

1. **Latency** / Латентность
   - Time it takes to service a request
   - Distinguish between successful and failed requests
   - Track percentiles (p50, p95, p99, p99.9)

2. **Traffic** / Трафик
   - Demand on your system
   - HTTP requests per second
   - Transactions per second
   - Network I/O

3. **Errors** / Ошибки
   - Rate of failed requests
   - Explicit failures (HTTP 500s)
   - Implicit failures (HTTP 200 with wrong content)
   - Policy violations

4. **Saturation** / Насыщенность
   - How "full" your service is
   - CPU, memory, disk, network utilization
   - Queue depth
   - Thread pool usage

### The USE Method (Brendan Gregg)

For every resource, monitor:

1. **Utilization** / Использование
   - Percentage of time the resource is busy
   - Average over time interval
   - Example: CPU utilization, memory usage

2. **Saturation** / Насыщение
   - Degree to which resource has extra work it can't service
   - Often queuing or waiting
   - Example: Run queue length, swap usage

3. **Errors** / Ошибки
   - Count of error events
   - Example: NIC errors, disk I/O errors

**Applied to Kubernetes Nodes:**

```promql
# Utilization
node:node_cpu_utilization:ratio = 1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m]))

node:node_memory_utilization:ratio = 1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

# Saturation
node:node_cpu_saturation:ratio = avg by (node) (node_load1) / count by (node) (node_cpu_seconds_total{mode="idle"})

node:node_memory_saturation:ratio = node_memory_SwapFree_bytes / node_memory_SwapTotal_bytes

# Errors
node:node_disk_errors:rate = rate(node_disk_io_time_seconds_total{job="node-exporter"}[5m])
```

### The RED Method (Tom Wilkie)

For every service, monitor:

1. **Rate** / Скорость
   - Requests per second
   - `rate(http_requests_total[5m])`

2. **Errors** / Ошибки
   - Failed requests per second
   - `rate(http_requests_total{code=~"5.."}[5m])`

3. **Duration** / Длительность
   - Latency distribution
   - `histogram_quantile(0.95, http_request_duration_seconds_bucket)`

**Implementation:**

```promql
# Rate - requests per second
sum(rate(http_requests_total[5m])) by (service)

# Errors - error rate
sum(rate(http_requests_total{code=~"5.."}[5m])) by (service)
/
sum(rate(http_requests_total[5m])) by (service)

# Duration - p95 latency
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)
```

## Kubernetes-Specific Patterns

### 1. Cluster Health Monitoring

**Pattern: Component Health Checks**

```promql
# API Server availability
up{job="kubernetes-apiservers"} == 1

# Controller Manager leader election
sum(up{job="kube-controller-manager"}) >= 1

# Scheduler health
sum(up{job="kube-scheduler"}) >= 1

# etcd cluster health
sum(up{job="etcd"}) >= (count(up{job="etcd"}) / 2 + 1)

# CoreDNS availability
sum(up{job="kube-dns"}) >= 2
```

**Pattern: Node Readiness**

```promql
# Count of ready nodes
sum(kube_node_status_condition{condition="Ready",status="true"})

# Percentage of ready nodes
sum(kube_node_status_condition{condition="Ready",status="true"})
/
count(kube_node_info)
* 100

# Nodes with memory pressure
sum(kube_node_status_condition{condition="MemoryPressure",status="true"})

# Nodes with disk pressure
sum(kube_node_status_condition{condition="DiskPressure",status="true"})
```

### 2. Workload Monitoring

**Pattern: Deployment Health**

```promql
# Deployments with replica mismatch
kube_deployment_spec_replicas != kube_deployment_status_replicas_available

# Deployment rollout stuck
kube_deployment_status_condition{condition="Progressing",status="false"}

# Deployment with old replicasets
sum by (namespace, deployment) (
  kube_replicaset_owner{owner_kind="Deployment"}
  * on (replicaset, namespace) group_left(deployment)
  kube_replicaset_created > time() - 86400
) > 1
```

**Pattern: Pod Health**

```promql
# Pods in crash loop
rate(kube_pod_container_status_restarts_total[15m]) > 0

# Pods waiting
kube_pod_container_status_waiting_reason > 0

# Pods terminated
kube_pod_container_status_terminated_reason > 0

# Pod resource requests vs limits
sum by (namespace, pod) (kube_pod_container_resource_requests{resource="cpu"})
/
sum by (namespace, pod) (kube_pod_container_resource_limits{resource="cpu"})
```

### 3. Resource Utilization Patterns

**Pattern: Namespace Resource Quotas**

```promql
# Namespace CPU usage vs quota
sum by (namespace) (
  rate(container_cpu_usage_seconds_total{container!=""}[5m])
)
/
kube_resourcequota{resource="cpu", type="hard"}

# Namespace memory usage vs quota
sum by (namespace) (
  container_memory_working_set_bytes{container!=""}
)
/
kube_resourcequota{resource="memory", type="hard"}
```

**Pattern: Container Right-Sizing**

```promql
# Containers using >90% of CPU limit
(
  rate(container_cpu_usage_seconds_total{container!=""}[5m])
  /
  on (namespace, pod, container) group_left()
  kube_pod_container_resource_limits{resource="cpu"}
) > 0.9

# Containers using <20% of CPU request (over-provisioned)
(
  rate(container_cpu_usage_seconds_total{container!=""}[5m])
  /
  on (namespace, pod, container) group_left()
  kube_pod_container_resource_requests{resource="cpu"}
) < 0.2

# Memory usage vs request ratio
container_memory_working_set_bytes{container!=""}
/
on (namespace, pod, container) group_left()
kube_pod_container_resource_requests{resource="memory"}
```

## Advanced Patterns

### 1. Multi-Cluster Aggregation

**Pattern: Global Service Availability**

```promql
# Aggregate availability across clusters
avg by (service) (
  (
    sum by (cluster, service) (rate(http_requests_total{code!~"5.."}[5m]))
    /
    sum by (cluster, service) (rate(http_requests_total[5m]))
  )
)
```

### 2. Capacity Planning

**Pattern: Resource Growth Prediction**

```promql
# Predict when disk will be full (linear regression)
predict_linear(
  node_filesystem_avail_bytes{mountpoint="/"}[1h],
  86400 * 7  # 7 days
) < 0

# Memory growth rate
deriv(
  node_memory_MemAvailable_bytes[1h]
)
```

### 3. SLO-Based Monitoring

**Pattern: Error Budget Tracking**

```promql
# Error budget remaining (99.9% SLO over 30 days)
1 - (
  (1 - 0.999) -  # SLO budget
  (
    sum(rate(http_requests_total{code=~"5.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))
  )
) / (1 - 0.999)

# Days until error budget exhausted
(
  1 - (
    sum(rate(http_requests_total{code=~"5.."}[1h]))
    /
    sum(rate(http_requests_total[1h]))
  )
) / (1 - 0.999) * 30
```

**Pattern: Multi-Window, Multi-Burn-Rate**

For 99.9% SLO (43m 50s downtime per month):

| Time Window | Burn Rate | Alert After | Budget Consumed |
|-------------|-----------|-------------|-----------------|
| 1h & 5m     | 14.4      | 2m          | 2%              |
| 6h & 30m    | 6         | 15m         | 5%              |
| 3d & 6h     | 1         | 1h          | 10%             |

```promql
# Fast burn (page immediately)
(
  sum(rate(http_requests_total{code=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
) > (1 - 0.999) * 14.4

# Medium burn (page during business hours)
(
  sum(rate(http_requests_total{code=~"5.."}[6h]))
  /
  sum(rate(http_requests_total[6h]))
) > (1 - 0.999) * 6
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Monitoring Everything

**Problem:**
- High cardinality metrics
- Expensive storage
- Alert fatigue
- Slow queries

**Solution:**
- Monitor symptoms, not causes
- Use metric relabeling to drop unnecessary labels
- Implement cardinality limits
- Sample high-frequency metrics

### ❌ Anti-Pattern 2: Alerting on Cause Instead of Symptom

**Problem:**
```promql
# BAD: Alert on CPU usage
node_cpu_utilization > 0.8
```

Why? High CPU might not impact users.

**Solution:**
```promql
# GOOD: Alert on user-visible impact
http_request_duration_seconds{quantile="0.95"} > 0.5
```

### ❌ Anti-Pattern 3: No Alert Runbooks

**Problem:**
- On-call engineer doesn't know what to do
- Wasted time investigating
- Inconsistent responses

**Solution:**
```yaml
annotations:
  summary: "Pod {{ $labels.pod }} OOMKilled"
  description: "Pod was killed due to out of memory."
  runbook_url: "https://runbooks.example.com/pod-oomkilled"
  action: |
    1. Check pod memory limits: kubectl describe pod {{ $labels.pod }}
    2. Review memory usage trends in Grafana
    3. Consider increasing memory limits or optimizing application
```

### ❌ Anti-Pattern 4: Copying Production Alerts to Non-Production

**Problem:**
- Alert fatigue from dev/staging environments
- Desensitization to real issues
- Wasted on-call time

**Solution:**
- Use different severity levels for different environments
- Route non-production alerts to different channels
- Disable paging for non-production

```yaml
route:
  routes:
  - match:
      environment: production
    receiver: pagerduty
  - match:
      environment: staging
    receiver: slack-non-urgent
```

### ❌ Anti-Pattern 5: High-Cardinality Labels

**Problem:**
```yaml
# BAD: User ID as label
http_requests_total{user_id="12345"}

# Result: Millions of time series
```

**Solution:**
```yaml
# GOOD: Use aggregatable labels
http_requests_total{user_tier="premium"}

# Or use logs for high-cardinality data
{"user_id": "12345", "request_path": "/api/users"}
```

## Best Practices Summary

### ✅ Do:
1. **Start with the Four Golden Signals**
2. **Use consistent labeling** across metrics
3. **Implement SLOs** for critical user journeys
4. **Include runbooks** in alert annotations
5. **Test alerts** before deploying
6. **Use recording rules** for expensive queries
7. **Implement alert routing** by severity and team
8. **Monitor your monitoring** (meta-monitoring)
9. **Use dashboards** for troubleshooting, not alerting
10. **Document monitoring decisions**

### ❌ Don't:
1. **Alert on everything**
2. **Use high-cardinality labels**
3. **Monitor causes instead of symptoms**
4. **Copy-paste alerts without understanding**
5. **Ignore alert fatigue**
6. **Skip runbooks**
7. **Over-complicate queries**
8. **Forget to test**
9. **Mix logs and metrics** inappropriately
10. **Neglect retention policies**

## Recording Rules for Performance

```yaml
groups:
- name: kubernetes.aggregation
  interval: 30s
  rules:
  # Pre-aggregate expensive queries
  - record: namespace:container_cpu_usage:sum
    expr: |
      sum by (namespace) (
        rate(container_cpu_usage_seconds_total{container!=""}[5m])
      )

  - record: namespace:container_memory_usage:sum
    expr: |
      sum by (namespace) (
        container_memory_working_set_bytes{container!=""}
      )

  # Node-level aggregations
  - record: node:node_cpu_utilization:ratio
    expr: |
      1 - avg by (node) (
        rate(node_cpu_seconds_total{mode="idle"}[5m])
      )

  - record: node:node_memory_utilization:ratio
    expr: |
      1 - (
        node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
      )

  # Service-level aggregations (RED method)
  - record: service:http_requests:rate5m
    expr: |
      sum by (service) (
        rate(http_requests_total[5m])
      )

  - record: service:http_errors:rate5m
    expr: |
      sum by (service) (
        rate(http_requests_total{code=~"5.."}[5m])
      )

  - record: service:http_request_duration:p95
    expr: |
      histogram_quantile(0.95,
        sum by (le, service) (
          rate(http_request_duration_seconds_bucket[5m])
        )
      )
```

## References

- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [USE Method - Brendan Gregg](http://www.brendangregg.com/usemethod.html)
- [RED Method - Weave Works](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/)
- [SLO Implementation - Google SRE](https://sre.google/workbook/implementing-slos/)
