---
name: observability-monitoring
description: Comprehensive observability and monitoring for Kubernetes using Prometheus, Grafana, OpenTelemetry, Loki, and Jaeger. Implements production-grade metrics, logging, and tracing with alerting strategies. Use when implementing observability stack, setting up monitoring, configuring alerts, or troubleshooting distributed systems.
---

# Kubernetes Observability & Monitoring

Production-grade observability implementation for Kubernetes clusters using CNCF graduated and incubating projects following best practices from AWS, Google Cloud, Microsoft Azure, and leading cloud-native companies.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

## When to Use This Skill

- Implement comprehensive observability stack for Kubernetes
- Set up Prometheus monitoring with long-term storage (Thanos/VictoriaMetrics)
- Configure Grafana dashboards for cluster and application metrics
- Implement distributed tracing with Jaeger and OpenTelemetry
- Set up centralized logging with Loki or Fluentd
- Design alert rules and notification strategies
- Troubleshoot performance issues in distributed systems
- Implement SLO/SLI-based monitoring
- Set up cost monitoring and optimization

## Core Observability Pillars

### The Three Pillars
1. **Metrics** - Quantitative measurements over time (Prometheus, VictoriaMetrics, Thanos)
2. **Logs** - Discrete events with context (Loki, Fluentd, Fluent Bit)
3. **Traces** - Request flows through distributed systems (Jaeger, Zipkin, OpenTelemetry)

### Modern Additions
4. **Continuous Profiling** - CPU, memory, I/O analysis (Parca, Pyroscope)
5. **Real User Monitoring (RUM)** - Frontend performance tracking
6. **Security Events** - Audit logs, security incidents (Falco)

## Prometheus Stack Implementation

### 1. Prometheus Operator Setup

**Production-grade installation:**

```yaml
# prometheus-stack-values.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-stack-values
  namespace: monitoring
data:
  values.yaml: |
    prometheus:
      prometheusSpec:
        # Resource allocation for production
        resources:
          requests:
            cpu: 2000m
            memory: 8Gi
          limits:
            cpu: 4000m
            memory: 16Gi

        # Data retention
        retention: 15d
        retentionSize: "50GB"

        # Storage class
        storageSpec:
          volumeClaimTemplate:
            spec:
              storageClassName: fast-ssd
              accessModes: ["ReadWriteOnce"]
              resources:
                requests:
                  storage: 100Gi

        # High availability
        replicas: 2

        # Service monitoring
        serviceMonitorSelectorNilUsesHelmValues: false
        podMonitorSelectorNilUsesHelmValues: false

        # External labels for multi-cluster
        externalLabels:
          cluster: production-us-east-1
          environment: production

        # Remote write for long-term storage (Thanos)
        remoteWrite:
        - url: http://thanos-receive:19291/api/v1/receive
          queueConfig:
            capacity: 10000
            maxShards: 50
            minShards: 10
          writeRelabelConfigs:
          - sourceLabels: [__name__]
            regex: 'kubernetes_build_info|up'
            action: keep

    grafana:
      enabled: true
      adminPassword: CHANGE_ME
      persistence:
        enabled: true
        storageClassName: fast-ssd
        size: 10Gi

      # High availability
      replicas: 2

      # Datasources
      datasources:
        datasources.yaml:
          apiVersion: 1
          datasources:
          - name: Prometheus
            type: prometheus
            url: http://prometheus-operated:9090
            access: proxy
            isDefault: true
          - name: Loki
            type: loki
            url: http://loki:3100
            access: proxy
          - name: Jaeger
            type: jaeger
            url: http://jaeger-query:16686
            access: proxy

      # Dashboard providers
      dashboardProviders:
        dashboardproviders.yaml:
          apiVersion: 1
          providers:
          - name: 'default'
            orgId: 1
            folder: ''
            type: file
            disableDeletion: false
            editable: true
            options:
              path: /var/lib/grafana/dashboards/default

      # Pre-configured dashboards
      dashboardsConfigMaps:
        default: grafana-dashboards

    alertmanager:
      enabled: true
      alertmanagerSpec:
        replicas: 3
        storage:
          volumeClaimTemplate:
            spec:
              storageClassName: fast-ssd
              accessModes: ["ReadWriteOnce"]
              resources:
                requests:
                  storage: 10Gi

      config:
        global:
          resolve_timeout: 5m
          slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

        route:
          group_by: ['alertname', 'cluster', 'service']
          group_wait: 30s
          group_interval: 5m
          repeat_interval: 12h
          receiver: 'default'
          routes:
          - match:
              severity: critical
            receiver: 'pagerduty-critical'
            continue: true
          - match:
              severity: warning
            receiver: 'slack-warnings'

        receivers:
        - name: 'default'
          slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ .GroupLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

        - name: 'pagerduty-critical'
          pagerduty_configs:
          - service_key: YOUR_PAGERDUTY_KEY
            description: '{{ .GroupLabels.alertname }}'

        - name: 'slack-warnings'
          slack_configs:
          - channel: '#warnings'
            send_resolved: true
```

**Installation:**

```bash
# Add Prometheus community Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values prometheus-stack-values.yaml \
  --version 55.0.0
```

### 2. Custom Metrics with ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
  namespace: production
  labels:
    app: my-app
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    relabelings:
    # Add custom labels
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    - sourceLabels: [__meta_kubernetes_pod_node_name]
      targetLabel: node
```

### 3. Alert Rules

**Reference:** See `references/alerting-best-practices.md`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kubernetes-alerts
  namespace: monitoring
spec:
  groups:
  - name: kubernetes.nodes
    interval: 30s
    rules:
    # Node CPU pressure
    - alert: NodeCPUPressure
      expr: |
        (1 - avg by (node) (rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100 > 80
      for: 15m
      labels:
        severity: warning
        component: node
      annotations:
        summary: "Node {{ $labels.node }} CPU pressure"
        description: "CPU usage on node {{ $labels.node }} is {{ $value | humanize }}% for more than 15 minutes."
        runbook_url: "https://runbooks.example.com/node-cpu-pressure"

    # Node memory pressure
    - alert: NodeMemoryPressure
      expr: |
        (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
      for: 10m
      labels:
        severity: critical
        component: node
      annotations:
        summary: "Node {{ $labels.node }} memory pressure"
        description: "Memory usage on node {{ $labels.node }} is {{ $value | humanize }}%."

    # Node disk pressure
    - alert: NodeDiskPressure
      expr: |
        (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100 > 85
      for: 5m
      labels:
        severity: warning
        component: node
      annotations:
        summary: "Node {{ $labels.node }} disk pressure"
        description: "Disk usage on node {{ $labels.node }} is {{ $value | humanize }}%."

  - name: kubernetes.pods
    interval: 30s
    rules:
    # Pod restart rate
    - alert: PodRestartingFrequently
      expr: |
        rate(kube_pod_container_status_restarts_total[1h]) * 3600 > 5
      for: 15m
      labels:
        severity: warning
        component: pod
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} restarting frequently"
        description: "Pod has restarted {{ $value }} times in the last hour."

    # Pod OOMKilled
    - alert: PodOOMKilled
      expr: |
        kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1
      for: 1m
      labels:
        severity: critical
        component: pod
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} OOMKilled"
        description: "Pod was killed due to out of memory."

    # Pod pending
    - alert: PodPending
      expr: |
        kube_pod_status_phase{phase="Pending"} == 1
      for: 15m
      labels:
        severity: warning
        component: pod
      annotations:
        summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} pending"
        description: "Pod has been in Pending state for more than 15 minutes."

  - name: kubernetes.deployments
    interval: 30s
    rules:
    # Deployment replicas mismatch
    - alert: DeploymentReplicasMismatch
      expr: |
        kube_deployment_spec_replicas != kube_deployment_status_replicas_available
      for: 15m
      labels:
        severity: warning
        component: deployment
      annotations:
        summary: "Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replicas mismatch"
        description: "Deployment has {{ $value }} available replicas, expected {{ $labels.spec_replicas }}."

  - name: application.slo
    interval: 30s
    rules:
    # SLO: Availability (99.9%)
    - alert: SLOAvailabilityBreach
      expr: |
        (
          sum(rate(http_requests_total{code!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
        ) < 0.999
      for: 5m
      labels:
        severity: critical
        component: slo
      annotations:
        summary: "SLO availability breach"
        description: "Service availability is {{ $value | humanizePercentage }}, below SLO of 99.9%."

    # SLO: Latency (p95 < 500ms)
    - alert: SLOLatencyBreach
      expr: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
        ) > 0.5
      for: 10m
      labels:
        severity: warning
        component: slo
      annotations:
        summary: "SLO latency breach"
        description: "P95 latency is {{ $value }}s, above SLO of 500ms."
```

## Thanos for Long-Term Storage

### 1. Thanos Sidecar Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thanos-sidecar
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: thanos-sidecar
  template:
    metadata:
      labels:
        app: thanos-sidecar
    spec:
      containers:
      - name: prometheus
        image: quay.io/prometheus/prometheus:v2.45.0
        args:
        - --config.file=/etc/prometheus/prometheus.yml
        - --storage.tsdb.path=/prometheus
        - --storage.tsdb.retention.time=2d
        - --storage.tsdb.min-block-duration=2h
        - --storage.tsdb.max-block-duration=2h
        - --web.enable-lifecycle
        volumeMounts:
        - name: prometheus-storage
          mountPath: /prometheus
        - name: prometheus-config
          mountPath: /etc/prometheus

      - name: thanos-sidecar
        image: quay.io/thanos/thanos:v0.32.0
        args:
        - sidecar
        - --tsdb.path=/prometheus
        - --prometheus.url=http://localhost:9090
        - --objstore.config-file=/etc/thanos/objstore.yml
        - --grpc-address=0.0.0.0:10901
        - --http-address=0.0.0.0:10902
        volumeMounts:
        - name: prometheus-storage
          mountPath: /prometheus
        - name: thanos-objstore-config
          mountPath: /etc/thanos

      volumes:
      - name: prometheus-storage
        persistentVolumeClaim:
          claimName: prometheus-storage
      - name: prometheus-config
        configMap:
          name: prometheus-config
      - name: thanos-objstore-config
        secret:
          secretName: thanos-objstore-config
```

**Object storage configuration (S3):**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: thanos-objstore-config
  namespace: monitoring
type: Opaque
stringData:
  objstore.yml: |
    type: S3
    config:
      bucket: thanos-metrics
      endpoint: s3.us-east-1.amazonaws.com
      access_key: YOUR_ACCESS_KEY
      secret_key: YOUR_SECRET_KEY
      insecure: false
```

### 2. Thanos Query

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thanos-query
  namespace: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: thanos-query
  template:
    metadata:
      labels:
        app: thanos-query
    spec:
      containers:
      - name: thanos-query
        image: quay.io/thanos/thanos:v0.32.0
        args:
        - query
        - --http-address=0.0.0.0:10902
        - --grpc-address=0.0.0.0:10901
        - --store=dnssrv+_grpc._tcp.thanos-sidecar.monitoring.svc.cluster.local
        - --store=dnssrv+_grpc._tcp.thanos-store.monitoring.svc.cluster.local
        - --query.replica-label=replica
        ports:
        - name: http
          containerPort: 10902
        - name: grpc
          containerPort: 10901
---
apiVersion: v1
kind: Service
metadata:
  name: thanos-query
  namespace: monitoring
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 9090
    targetPort: http
  - name: grpc
    port: 10901
    targetPort: grpc
  selector:
    app: thanos-query
```

## Grafana Dashboards

**Reference:** See `references/dashboard-examples.md` for complete dashboard JSON

### Essential Dashboards

1. **Cluster Overview Dashboard**
   - Node resource utilization (CPU, Memory, Disk, Network)
   - Pod count by namespace
   - Container resource requests vs usage
   - Top pods by CPU/Memory
   - Cluster events timeline

2. **Node Dashboard**
   - CPU usage (user, system, iowait)
   - Memory usage breakdown
   - Disk I/O and latency
   - Network traffic
   - Load average

3. **Pod Dashboard**
   - Container CPU/Memory usage
   - Network traffic
   - Restart count
   - Log error rates
   - Request/Error rates (if instrumented)

4. **Application Dashboard**
   - Request rate, error rate, duration (RED method)
   - Latency percentiles (p50, p95, p99)
   - Database query performance
   - Cache hit rates
   - Queue depths

**Dashboard best practices:**
- Use template variables for dynamic filtering
- Include links to runbooks
- Add annotations for deployments
- Use consistent color schemes
- Include time-to-detect (TTD) and time-to-resolve (TTR) metrics

**Asset:** See `assets/grafana-dashboards/` for production-ready dashboards

## Loki for Log Aggregation

### 1. Loki Stack Installation

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  --set promtail.enabled=true \
  --set grafana.enabled=false \
  --set loki.persistence.enabled=true \
  --set loki.persistence.size=100Gi
```

### 2. Promtail Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: promtail-config
  namespace: monitoring
data:
  promtail.yaml: |
    server:
      http_listen_port: 9080
      grpc_listen_port: 0

    positions:
      filename: /tmp/positions.yaml

    clients:
    - url: http://loki:3100/loki/api/v1/push

    scrape_configs:
    # Kubernetes pod logs
    - job_name: kubernetes-pods
      kubernetes_sd_configs:
      - role: pod

      pipeline_stages:
      # Extract level from JSON logs
      - json:
          expressions:
            level: level
            message: message
            timestamp: timestamp

      # Parse timestamp
      - timestamp:
          source: timestamp
          format: RFC3339Nano

      # Extract log level
      - labels:
          level:

      relabel_configs:
      # Add namespace
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace

      # Add pod name
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

      # Add container name
      - source_labels: [__meta_kubernetes_pod_container_name]
        target_label: container

      # Add app label
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
```

### 3. LogQL Queries

**Essential queries:**

```logql
# All logs from a namespace
{namespace="production"}

# Error logs across all namespaces
{level="error"}

# Logs from specific app with error filtering
{app="my-app"} |= "error"

# Count of errors per minute
sum by (app) (rate({level="error"}[1m]))

# Extract and count HTTP status codes
{app="api"} | json | __error__="" | line_format "{{.status}}" | pattern `<status>` | status >= 500

# Slow query detection
{app="database"} | json | duration > 1s
```

## OpenTelemetry for Tracing

### 1. OpenTelemetry Collector

**Reference:** See `references/otel-patterns.md`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: monitoring
data:
  otel-collector-config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

      # Prometheus metrics receiver
      prometheus:
        config:
          scrape_configs:
          - job_name: 'otel-collector'
            scrape_interval: 10s
            static_configs:
            - targets: ['localhost:8888']

    processors:
      # Batch spans for efficiency
      batch:
        timeout: 10s
        send_batch_size: 1024

      # Add resource attributes
      resource:
        attributes:
        - key: cluster.name
          value: production-us-east-1
          action: insert

      # Sampling (keep 10% of traces)
      probabilistic_sampler:
        sampling_percentage: 10

      # Tail sampling (keep interesting traces)
      tail_sampling:
        policies:
        - name: error-traces
          type: status_code
          status_code:
            status_codes: [ERROR]
        - name: slow-traces
          type: latency
          latency:
            threshold_ms: 1000
        - name: random-sample
          type: probabilistic
          probabilistic:
            sampling_percentage: 1

    exporters:
      # Export to Jaeger
      jaeger:
        endpoint: jaeger-collector:14250
        tls:
          insecure: true

      # Export metrics to Prometheus
      prometheus:
        endpoint: "0.0.0.0:8889"
        namespace: otel

      # Export logs to Loki
      loki:
        endpoint: http://loki:3100/loki/api/v1/push
        labels:
          resource:
            service.name: "service_name"

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch, resource, tail_sampling]
          exporters: [jaeger]

        metrics:
          receivers: [otlp, prometheus]
          processors: [batch, resource]
          exporters: [prometheus]

        logs:
          receivers: [otlp]
          processors: [batch, resource]
          exporters: [loki]

      telemetry:
        logs:
          level: info
        metrics:
          address: 0.0.0.0:8888
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
  namespace: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector-contrib:0.90.0
        args:
        - --config=/conf/otel-collector-config.yaml
        volumeMounts:
        - name: config
          mountPath: /conf
        ports:
        - name: otlp-grpc
          containerPort: 4317
        - name: otlp-http
          containerPort: 4318
        - name: prometheus
          containerPort: 8889
        - name: metrics
          containerPort: 8888
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
      volumes:
      - name: config
        configMap:
          name: otel-collector-config
```

### 2. Jaeger Deployment

```bash
# Install Jaeger Operator
kubectl create namespace observability
kubectl apply -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.50.0/jaeger-operator.yaml -n observability
```

```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger-production
  namespace: monitoring
spec:
  strategy: production

  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
        index-prefix: jaeger

    esIndexCleaner:
      enabled: true
      numberOfDays: 7
      schedule: "55 23 * * *"

  query:
    replicas: 2
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 1000m
        memory: 2Gi

  collector:
    replicas: 3
    resources:
      requests:
        cpu: 1000m
        memory: 2Gi
      limits:
        cpu: 2000m
        memory: 4Gi
```

## Cost Monitoring with OpenCost

```bash
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm upgrade --install opencost opencost/opencost \
  --namespace opencost \
  --create-namespace \
  --set prometheus.external.url=http://prometheus-operated.monitoring:9090
```

## Best Practices

### 1. Metrics Collection
- Use standardized metric names (Prometheus naming conventions)
- Implement cardinality controls (avoid high-cardinality labels)
- Use metric relabeling to optimize storage
- Implement metric federation for multi-cluster
- Set appropriate retention policies

### 2. Alert Design
- Follow the "Alerting on Symptoms, Not Causes" principle
- Use multi-window, multi-burn-rate alerting for SLOs
- Include runbook links in alert annotations
- Implement alert grouping and routing
- Test alerts with alert dry-runs

### 3. Dashboard Design
- Follow the USE method (Utilization, Saturation, Errors) for resources
- Follow the RED method (Rate, Errors, Duration) for services
- Use consistent color schemes and layouts
- Include deployment annotations
- Add links to related dashboards and runbooks

### 4. Log Management
- Implement structured logging (JSON format)
- Use consistent log levels
- Include correlation IDs for distributed tracing
- Implement log sampling for high-volume apps
- Set retention policies based on compliance requirements

### 5. Trace Collection
- Implement head-based sampling for high-traffic services
- Use tail-based sampling to keep interesting traces
- Include business context in span attributes
- Correlate traces with metrics and logs
- Monitor trace sampling rates

## SLO/SLI Implementation

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-monitoring
  namespace: monitoring
spec:
  groups:
  - name: slo.availability
    interval: 30s
    rules:
    # Error budget calculation (99.9% SLO)
    - record: slo:availability:error_budget_remaining
      expr: |
        1 - (
          (1 - 0.999) -
          (
            sum(rate(http_requests_total{code=~"5.."}[30d]))
            /
            sum(rate(http_requests_total[30d]))
          )
        ) / (1 - 0.999)

    # Multi-window, multi-burn-rate alerts
    - alert: SLOAvailabilityFastBurn
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
      annotations:
        summary: "Fast burn rate on error budget"
        description: "Error budget is burning at 14.4x rate. At this rate, budget will be exhausted in 2 days."
```

## Troubleshooting

**High cardinality metrics:**
```bash
# Find high cardinality metrics
curl -s http://prometheus:9090/api/v1/label/__name__/values | jq -r '.data[]' | wc -l

# Check series count per metric
curl -s http://prometheus:9090/api/v1/query?query=count%20by%20%28__name__%29%20%28%7B__name__%3D~%22.%2B%22%7D%29 | jq
```

**Query performance:**
```bash
# Enable query logging
--query.log-file=/var/log/prometheus-queries.log

# Analyze slow queries
cat /var/log/prometheus-queries.log | jq 'select(.duration > 1)'
```

## References

- `references/monitoring-patterns.md` - Monitoring patterns and anti-patterns
- `references/alerting-best-practices.md` - Alert design and management
- `references/dashboard-examples.md` - Production dashboard examples
- `references/otel-patterns.md` - OpenTelemetry instrumentation patterns
- `references/slo-implementation.md` - SLO/SLI implementation guide

## Assets

- `assets/prometheus-config.yaml` - Production Prometheus configuration
- `assets/alert-rules/` - Alert rule library
- `assets/grafana-dashboards/` - Dashboard JSON files
- `assets/otel-collector-config.yaml` - OpenTelemetry collector config

## Related Skills

- `k8s-security-policies` - Security monitoring and audit logging
- `gitops-workflow` - Deployment annotations and change tracking
- `k8s-manifest-generator` - Adding monitoring annotations to workloads
