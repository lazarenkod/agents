# Alerting Best Practices for Kubernetes

## Лучшие практики алертинга / Alert Design Principles

### The Philosophy of Good Alerting

> **"Pages should be urgent, important, actionable, and real."** - Google SRE

Every alert should answer:
1. **What is broken?** - Clear problem statement
2. **Why should I care?** - User impact
3. **What should I do?** - Clear action items

### Alert Severity Levels

| Severity | When to Use | Response Time | Examples |
|----------|-------------|---------------|----------|
| **Critical** (Page) | User-facing impact NOW | Immediate (5 min) | Service down, data loss, security breach |
| **Warning** (Ticket) | Will cause Critical soon | Business hours (4 hours) | Disk 85% full, error rate elevated |
| **Info** (Log) | Awareness only | Optional review | Deployment completed, configuration changed |

## Multi-Window, Multi-Burn-Rate Alerting

### SLO-Based Alerting Strategy

For a 99.9% availability SLO (43m 50s downtime per month):

**Error Budget:** 0.1% = 43m 50s per month

**Burn Rate Table:**

| Severity | Time Window | Burn Rate Multiplier | Alert Threshold | Budget Consumed | Time to Exhaustion |
|----------|-------------|---------------------|-----------------|-----------------|-------------------|
| Page | 1h & 5m | 14.4x | >1.44% error rate | 2% | 2 days |
| Page | 6h & 30m | 6x | >0.6% error rate | 5% | 5 days |
| Ticket | 3d & 6h | 1x | >0.1% error rate | 10% | 30 days |

### Implementation

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-alerts
  namespace: monitoring
spec:
  groups:
  - name: slo.fast-burn
    interval: 30s
    rules:
    # Fast burn: 14.4x burn rate (2% budget in 1h)
    - alert: ErrorBudgetFastBurn
      expr: |
        (
          sum(rate(http_requests_total{code=~"5.."}[1h]))
          /
          sum(rate(http_requests_total[1h]))
        ) > (1 - 0.999) * 14.4
        and
        (
          sum(rate(http_requests_total{code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
        ) > (1 - 0.999) * 14.4
      for: 2m
      labels:
        severity: critical
        burn_rate: fast
        page: "true"
      annotations:
        summary: "Fast error budget burn detected"
        description: "Error budget burning at 14.4x. At this rate, monthly budget exhausted in 2 days."
        impact: "High error rate impacting users NOW"
        action: |
          1. Check recent deployments: kubectl rollout history deployment/{{ $labels.deployment }}
          2. Review error logs: kubectl logs -l app={{ $labels.app }} --tail=100
          3. Consider rollback if deployment-related
          4. Escalate to on-call lead if cause unclear
        runbook_url: "https://runbooks.example.com/error-budget-fast-burn"
        dashboard_url: "https://grafana.example.com/d/service-overview"

  - name: slo.slow-burn
    interval: 30s
    rules:
    # Slow burn: 1x burn rate (10% budget in 3d)
    - alert: ErrorBudgetSlowBurn
      expr: |
        (
          sum(rate(http_requests_total{code=~"5.."}[3d]))
          /
          sum(rate(http_requests_total[3d]))
        ) > (1 - 0.999)
        and
        (
          sum(rate(http_requests_total{code=~"5.."}[6h]))
          /
          sum(rate(http_requests_total[6h]))
        ) > (1 - 0.999)
      for: 1h
      labels:
        severity: warning
        burn_rate: slow
        page: "false"
      annotations:
        summary: "Slow error budget burn detected"
        description: "Error budget burning at baseline rate for extended period."
        impact: "Sustained elevated error rate, may impact SLO"
        action: |
          1. Review error trends over 3 days
          2. Identify patterns (time-based, traffic-based)
          3. Schedule investigation during business hours
          4. Consider if SLO target needs adjustment
        runbook_url: "https://runbooks.example.com/error-budget-slow-burn"
```

## Kubernetes Infrastructure Alerts

### Node-Level Alerts

```yaml
groups:
- name: kubernetes.nodes
  interval: 30s
  rules:
  # Node not ready
  - alert: NodeNotReady
    expr: |
      kube_node_status_condition{condition="Ready",status="true"} == 0
    for: 15m
    labels:
      severity: critical
      component: node
      page: "true"
    annotations:
      summary: "Node {{ $labels.node }} not ready"
      description: "Node has been NotReady for more than 15 minutes."
      impact: "Reduced cluster capacity, pods may be evicted"
      action: |
        1. Check node status: kubectl describe node {{ $labels.node }}
        2. Check node logs: journalctl -u kubelet -n 100
        3. SSH to node and check resource utilization
        4. Restart kubelet if necessary: systemctl restart kubelet
        5. Cordon and drain if persistent: kubectl drain {{ $labels.node }}
      runbook_url: "https://runbooks.example.com/node-not-ready"

  # Node memory pressure
  - alert: NodeMemoryPressure
    expr: |
      (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
    for: 10m
    labels:
      severity: critical
      component: node
      page: "true"
    annotations:
      summary: "Node {{ $labels.node }} memory pressure"
      description: "Node memory usage is {{ $value | humanizePercentage }}."
      impact: "Risk of OOMKiller, pod evictions"
      action: |
        1. Identify top memory consumers: kubectl top pods --all-namespaces --sort-by=memory
        2. Check for memory leaks in applications
        3. Consider evicting non-critical pods
        4. Scale up node pool if persistent
      runbook_url: "https://runbooks.example.com/node-memory-pressure"

  # Node disk pressure
  - alert: NodeDiskPressure
    expr: |
      (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100 > 85
    for: 5m
    labels:
      severity: warning
      component: node
      page: "false"
    annotations:
      summary: "Node {{ $labels.node }} disk pressure"
      description: "Node disk usage is {{ $value | humanizePercentage }}."
      impact: "Risk of disk full, pod evictions, image pulls failing"
      action: |
        1. Clean up unused images: kubectl exec -n kube-system {{ $labels.node }} -- crictl rmi --prune
        2. Check for large log files: kubectl exec -n kube-system {{ $labels.node }} -- du -sh /var/log/*
        3. Identify large volumes: kubectl exec -n kube-system {{ $labels.node }} -- du -sh /var/lib/kubelet/pods/*
        4. Consider increasing disk size
      runbook_url: "https://runbooks.example.com/node-disk-pressure"

  # Node CPU saturation
  - alert: NodeCPUSaturation
    expr: |
      avg by (node) (node_load1) / count by (node) (node_cpu_seconds_total{mode="idle"}) > 2
    for: 15m
    labels:
      severity: warning
      component: node
      page: "false"
    annotations:
      summary: "Node {{ $labels.node }} CPU saturation"
      description: "Load average is {{ $value }} (>2x CPU cores)."
      impact: "Increased latency, potential pod throttling"
      action: |
        1. Check pod CPU usage: kubectl top pods --all-namespaces --sort-by=cpu
        2. Look for CPU-intensive workloads
        3. Consider horizontal pod autoscaling
        4. Scale up node pool if sustained
```

### Pod-Level Alerts

```yaml
groups:
- name: kubernetes.pods
  interval: 30s
  rules:
  # Pod crash looping
  - alert: PodCrashLooping
    expr: |
      rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 15m
    labels:
      severity: warning
      component: pod
      page: "false"
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} crash looping"
      description: "Pod restarted {{ $value }} times in last 15 minutes."
      impact: "Service degradation, potential data loss"
      action: |
        1. Check pod logs: kubectl logs -n {{ $labels.namespace }} {{ $labels.pod }} --previous
        2. Check pod events: kubectl describe pod -n {{ $labels.namespace }} {{ $labels.pod }}
        3. Review recent config changes
        4. Check resource limits: kubectl get pod -n {{ $labels.namespace }} {{ $labels.pod }} -o yaml
        5. Consider rollback if deployment-related
      runbook_url: "https://runbooks.example.com/pod-crash-looping"

  # Pod OOMKilled
  - alert: PodOOMKilled
    expr: |
      kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1
    for: 1m
    labels:
      severity: warning
      component: pod
      page: "false"
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} OOMKilled"
      description: "Container {{ $labels.container }} was killed due to out of memory."
      impact: "Service interruption, potential data loss"
      action: |
        1. Check memory limits: kubectl get pod -n {{ $labels.namespace }} {{ $labels.pod }} -o jsonpath='{.spec.containers[*].resources.limits.memory}'
        2. Review memory usage trends in Grafana
        3. Check for memory leaks in application
        4. Increase memory limits if legitimate usage: kubectl set resources deployment/{{ $labels.deployment }} -c {{ $labels.container }} --limits=memory=2Gi
        5. Consider VPA for automatic right-sizing
      runbook_url: "https://runbooks.example.com/pod-oomkilled"

  # Pod pending too long
  - alert: PodPendingTooLong
    expr: |
      kube_pod_status_phase{phase="Pending"} == 1
    for: 15m
    labels:
      severity: warning
      component: pod
      page: "false"
    annotations:
      summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} pending"
      description: "Pod has been in Pending state for more than 15 minutes."
      impact: "Service not available, capacity issue"
      action: |
        1. Check pod events: kubectl describe pod -n {{ $labels.namespace }} {{ $labels.pod }}
        2. Common causes:
           - Insufficient resources: Scale up cluster
           - Image pull errors: Check image name and credentials
           - PVC binding issues: Check PV availability
           - Node selector/affinity: Relax constraints or add nodes
        3. Check node capacity: kubectl describe nodes
      runbook_url: "https://runbooks.example.com/pod-pending"
```

### Deployment Alerts

```yaml
groups:
- name: kubernetes.deployments
  interval: 30s
  rules:
  # Deployment replicas unavailable
  - alert: DeploymentReplicasUnavailable
    expr: |
      (
        kube_deployment_spec_replicas
        -
        kube_deployment_status_replicas_available
      ) > 0
    for: 15m
    labels:
      severity: warning
      component: deployment
      page: "false"
    annotations:
      summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replicas unavailable"
      description: "{{ $value }} replicas are unavailable (desired: {{ $labels.spec_replicas }})."
      impact: "Reduced capacity, potential service degradation"
      action: |
        1. Check deployment status: kubectl get deployment -n {{ $labels.namespace }} {{ $labels.deployment }}
        2. Check replicaset status: kubectl get rs -n {{ $labels.namespace }} -l app={{ $labels.deployment }}
        3. Check pod status: kubectl get pods -n {{ $labels.namespace }} -l app={{ $labels.deployment }}
        4. Review recent deployment: kubectl rollout history deployment/{{ $labels.deployment }} -n {{ $labels.namespace }}
        5. Consider rollback: kubectl rollout undo deployment/{{ $labels.deployment }} -n {{ $labels.namespace }}
      runbook_url: "https://runbooks.example.com/deployment-replicas-unavailable"

  # Deployment rollout stuck
  - alert: DeploymentRolloutStuck
    expr: |
      kube_deployment_status_condition{condition="Progressing",status="false"} == 1
    for: 15m
    labels:
      severity: critical
      component: deployment
      page: "true"
    annotations:
      summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} rollout stuck"
      description: "Deployment rollout has not progressed for 15 minutes."
      impact: "Deployment failed, service may be degraded"
      action: |
        1. Check rollout status: kubectl rollout status deployment/{{ $labels.deployment }} -n {{ $labels.namespace }}
        2. Check for image pull errors, resource constraints, health check failures
        3. Review deployment events: kubectl describe deployment -n {{ $labels.namespace }} {{ $labels.deployment }}
        4. Rollback if necessary: kubectl rollout undo deployment/{{ $labels.deployment }} -n {{ $labels.namespace }}
      runbook_url: "https://runbooks.example.com/deployment-rollout-stuck"
```

## Application-Level Alerts

### HTTP Service Alerts

```yaml
groups:
- name: application.availability
  interval: 30s
  rules:
  # High error rate
  - alert: HighErrorRate
    expr: |
      (
        sum by (service) (rate(http_requests_total{code=~"5.."}[5m]))
        /
        sum by (service) (rate(http_requests_total[5m]))
      ) > 0.05
    for: 5m
    labels:
      severity: critical
      component: application
      page: "true"
    annotations:
      summary: "High error rate for {{ $labels.service }}"
      description: "Error rate is {{ $value | humanizePercentage }} (>5%)."
      impact: "Users experiencing errors"
      action: |
        1. Check recent deployments: kubectl rollout history deployment/{{ $labels.service }}
        2. Review error logs: kubectl logs -l app={{ $labels.service }} | grep ERROR
        3. Check dependencies (database, cache, external APIs)
        4. Review error types in APM/tracing
        5. Rollback if deployment-related
      runbook_url: "https://runbooks.example.com/high-error-rate"

  # High latency
  - alert: HighLatency
    expr: |
      histogram_quantile(0.95,
        sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
      ) > 1
    for: 10m
    labels:
      severity: warning
      component: application
      page: "false"
    annotations:
      summary: "High latency for {{ $labels.service }}"
      description: "P95 latency is {{ $value }}s (>1s)."
      impact: "Slow user experience"
      action: |
        1. Check CPU/memory usage: kubectl top pods -l app={{ $labels.service }}
        2. Review slow queries in APM
        3. Check database connection pool
        4. Look for N+1 query patterns
        5. Consider horizontal pod autoscaling
      runbook_url: "https://runbooks.example.com/high-latency"

  # Low request rate (potential outage)
  - alert: LowRequestRate
    expr: |
      sum by (service) (rate(http_requests_total[5m])) < 1
    for: 15m
    labels:
      severity: warning
      component: application
      page: "true"
    annotations:
      summary: "Low request rate for {{ $labels.service }}"
      description: "Request rate is {{ $value }} req/s (<1 req/s)."
      impact: "Potential complete service outage"
      action: |
        1. Check if service is receiving traffic
        2. Verify ingress/load balancer configuration
        3. Check pod status: kubectl get pods -l app={{ $labels.service }}
        4. Review DNS resolution
        5. Check network policies
      runbook_url: "https://runbooks.example.com/low-request-rate"
```

## Alert Configuration Best Practices

### 1. Alert Routing

```yaml
# alertmanager-config.yaml
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s        # Wait for additional alerts before sending
  group_interval: 5m     # Minimum time between notifications for a group
  repeat_interval: 12h   # Repeat notifications every 12h

  routes:
  # Critical alerts to PagerDuty
  - match:
      severity: critical
      page: "true"
    receiver: 'pagerduty-critical'
    continue: true  # Also send to Slack

  # Critical alerts to Slack
  - match:
      severity: critical
    receiver: 'slack-critical'

  # Warnings to Slack only
  - match:
      severity: warning
    receiver: 'slack-warnings'

  # Info alerts to logs
  - match:
      severity: info
    receiver: 'null'

receivers:
- name: 'pagerduty-critical'
  pagerduty_configs:
  - service_key: '<PAGERDUTY_SERVICE_KEY>'
    description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
    details:
      impact: '{{ .Annotations.impact }}'
      action: '{{ .Annotations.action }}'
      runbook: '{{ .Annotations.runbook_url }}'

- name: 'slack-critical'
  slack_configs:
  - api_url: '<SLACK_WEBHOOK_URL>'
    channel: '#alerts-critical'
    title: '🚨 {{ .GroupLabels.alertname }}'
    text: |
      *Summary:* {{ .Annotations.summary }}
      *Description:* {{ .Annotations.description }}
      *Impact:* {{ .Annotations.impact }}
      *Runbook:* {{ .Annotations.runbook_url }}
    send_resolved: true

- name: 'slack-warnings'
  slack_configs:
  - api_url: '<SLACK_WEBHOOK_URL>'
    channel: '#alerts-warnings'
    title: '⚠️  {{ .GroupLabels.alertname }}'
    text: '{{ .Annotations.summary }}'
    send_resolved: true

- name: 'null'
```

### 2. Alert Inhibition

**Prevent alert spam:**

```yaml
inhibit_rules:
# Inhibit pod alerts if node is down
- source_match:
    alertname: 'NodeNotReady'
  target_match:
    alertname: 'PodNotReady'
  equal: ['node']

# Inhibit deployment alerts if cluster API is down
- source_match:
    alertname: 'KubeAPIDown'
  target_match_re:
    alertname: 'Deployment.*'

# Inhibit warning if critical is firing
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'
  equal: ['alertname', 'namespace', 'service']
```

### 3. Alert Silencing

**Silence alerts during maintenance:**

```bash
# Silence all alerts for a deployment during maintenance window
amtool silence add \
  deployment="my-app" \
  --start="2025-11-20T22:00:00Z" \
  --end="2025-11-21T02:00:00Z" \
  --author="ops-team" \
  --comment="Scheduled maintenance"

# Silence specific alert
amtool silence add \
  alertname="HighLatency" \
  service="my-app" \
  --duration=2h \
  --author="dev-team" \
  --comment="Performance testing in progress"
```

## Alert Testing

### 1. Validate Alert Syntax

```bash
# Validate Prometheus rules
promtool check rules /etc/prometheus/rules/*.yaml

# Validate Alertmanager config
amtool check-config /etc/alertmanager/config.yml
```

### 2. Test Alert Firing

```bash
# Trigger test alert
curl -X POST http://alertmanager:9093/api/v1/alerts -d '[
  {
    "labels": {
      "alertname": "TestAlert",
      "severity": "critical"
    },
    "annotations": {
      "summary": "This is a test alert"
    },
    "startsAt": "2025-11-20T12:00:00Z",
    "endsAt": "2025-11-20T13:00:00Z"
  }
]'
```

### 3. Alert Dry-Run

```yaml
# Add dry-run label to test alerts without paging
- alert: HighErrorRate
  expr: |
    (
      sum by (service) (rate(http_requests_total{code=~"5.."}[5m]))
      /
      sum by (service) (rate(http_requests_total[5m]))
    ) > 0.05
  labels:
    severity: critical
    dry_run: "true"  # Won't page, only logs
```

## Alert Quality Metrics

### Measuring Alert Effectiveness

```promql
# Alert precision (% of alerts that required action)
alerts_requiring_action / total_alerts_fired

# Alert recall (% of incidents that triggered alerts)
incidents_with_alerts / total_incidents

# Time to detect (TTD)
alert_fire_time - incident_start_time

# Time to resolve (TTR)
incident_resolve_time - alert_fire_time

# Alert fatigue (alerts per on-call shift)
count_by(alertname) over last 7 days
```

## References

- [Google SRE - Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Prometheus Alerting Best Practices](https://prometheus.io/docs/practices/alerting/)
- [Multi-Window, Multi-Burn-Rate Alerts](https://sre.google/workbook/alerting-on-slos/#6-multiwindow-multi-burn-rate-alerts)
- [Alert Runbook Template](https://github.com/kubernetes-monitoring/kubernetes-mixin/blob/master/runbook.md)
