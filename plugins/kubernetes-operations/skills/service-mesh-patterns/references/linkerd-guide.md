# Linkerd Production Guide

Comprehensive guide to deploying and operating Linkerd service mesh in production environments, based on best practices from cloud-native organizations.

## Table of Contents

1. [Installation and Setup](#installation-and-setup)
2. [Certificate Management](#certificate-management)
3. [Traffic Management](#traffic-management)
4. [Observability](#observability)
5. [Multi-Cluster Setup](#multi-cluster-setup)
6. [Performance Optimization](#performance-optimization)

## Installation and Setup

### Prerequisites

```bash
# Check Kubernetes version (1.21+)
kubectl version --short

# Install Linkerd CLI
curl -fsL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

# Verify CLI
linkerd version

# Validate cluster
linkerd check --pre
```

### Production Installation

#### Step 1: Generate Certificates

**For production, use a proper PKI (cert-manager, Vault, etc.):**

```bash
# Generate root CA (store securely!)
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca \
  --no-password \
  --insecure \
  --not-after 87600h

# Generate intermediate certificate (identity issuer)
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
  --profile intermediate-ca \
  --not-after 8760h \
  --no-password \
  --insecure \
  --ca ca.crt \
  --ca-key ca.key

# Verify certificates
step certificate inspect ca.crt
step certificate inspect issuer.crt
```

#### Step 2: Install Control Plane

```bash
# Install CRDs first
linkerd install --crds | kubectl apply -f -

# Install control plane with HA
linkerd install \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  --ha \
  --set proxyInit.runAsRoot=false \
  --set-file linkerd-sip.tls.crt=issuer.crt \
  --set-file linkerd-sip.tls.key=issuer.key \
  | kubectl apply -f -

# Verify installation
linkerd check

# Wait for control plane to be ready
kubectl wait --for=condition=available --timeout=300s \
  deployment -n linkerd -l linkerd.io/control-plane-component
```

#### Step 3: Install Extensions

```bash
# Install Viz extension (observability)
linkerd viz install | kubectl apply -f -

# Verify viz
linkerd viz check

# Install Jaeger extension (optional, for tracing)
linkerd jaeger install | kubectl apply -f -

# Install Multicluster extension (if needed)
linkerd multicluster install | kubectl apply -f -
```

### Configuration Options

**High-availability deployment:**

```yaml
# linkerd-ha-values.yaml
controllerReplicas: 3

# Resource requests
controllerResources:
  cpu:
    request: 200m
    limit: 1000m
  memory:
    request: 512Mi
    limit: 2Gi

# Proxy defaults
proxy:
  resources:
    cpu:
      request: 100m
      limit: 1000m
    memory:
      request: 20Mi
      limit: 250Mi

# Proxy Init
proxyInit:
  runAsRoot: false
  resources:
    cpu:
      request: 10m
      limit: 100m
    memory:
      request: 10Mi
      limit: 50Mi

# Identity
identity:
  issuer:
    scheme: kubernetes.io/tls

# Enable dashboard
dashboard:
  replicas: 2

# Prometheus (if not using external)
prometheus:
  enabled: true
  replicas: 2
  resources:
    cpu:
      request: 300m
      limit: 1000m
    memory:
      request: 1Gi
      limit: 4Gi
```

## Certificate Management

### Automated Certificate Rotation with cert-manager

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create trust anchor (self-signed root CA)
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: linkerd-trust-anchor
  namespace: linkerd
spec:
  isCA: true
  commonName: root.linkerd.cluster.local
  secretName: linkerd-trust-anchor
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: linkerd-trust-anchor
    kind: Issuer
    group: cert-manager.io
  duration: 87600h # 10 years
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: linkerd-trust-anchor
  namespace: linkerd
spec:
  selfSigned: {}
EOF

# Create identity issuer certificate
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: linkerd-identity-issuer
  namespace: linkerd
spec:
  secretName: linkerd-identity-issuer
  duration: 2160h # 90 days
  renewBefore: 360h # 15 days
  issuerRef:
    name: linkerd-trust-anchor
    kind: Certificate
  commonName: identity.linkerd.cluster.local
  dnsNames:
  - identity.linkerd.cluster.local
  isCA: true
  privateKey:
    algorithm: ECDSA
  usages:
  - cert sign
  - crl sign
  - server auth
  - client auth
EOF

# Linkerd will automatically pick up certificate rotations
```

### Manual Certificate Rotation

```bash
# Generate new issuer certificate
step certificate create identity.linkerd.cluster.local new-issuer.crt new-issuer.key \
  --profile intermediate-ca \
  --not-after 8760h \
  --no-password \
  --insecure \
  --ca ca.crt \
  --ca-key ca.key

# Update secret
kubectl create secret tls linkerd-identity-issuer \
  --cert=new-issuer.crt \
  --key=new-issuer.key \
  --namespace=linkerd \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart identity controller
kubectl rollout restart deployment/linkerd-identity -n linkerd

# Verify
linkerd check --proxy
```

## Traffic Management

### Basic Mesh Injection

```bash
# Annotate namespace for automatic injection
kubectl annotate namespace production linkerd.io/inject=enabled

# Check annotation
kubectl get ns production -o yaml | grep linkerd.io/inject

# Deploy or update applications
kubectl rollout restart deployment -n production

# Verify proxy injection
kubectl get pods -n production -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# Check mesh status
linkerd -n production check --proxy
linkerd -n production stat deploy
```

### Selective Injection

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
spec:
  template:
    metadata:
      annotations:
        # Enable injection (overrides namespace setting)
        linkerd.io/inject: enabled

        # Skip specific ports
        config.linkerd.io/skip-inbound-ports: "8080,8443"
        config.linkerd.io/skip-outbound-ports: "3306"

        # Opaque ports (non-HTTP protocols)
        config.linkerd.io/opaque-ports: "3306,6379"

        # Custom proxy resources
        config.linkerd.io/proxy-cpu-limit: "1"
        config.linkerd.io/proxy-cpu-request: "100m"
        config.linkerd.io/proxy-memory-limit: "250Mi"
        config.linkerd.io/proxy-memory-request: "20Mi"

        # Proxy log level
        config.linkerd.io/proxy-log-level: "warn,linkerd=info"
```

### Traffic Splits (Canary Deployments)

**Using Flagger for automated canary:**

```bash
# Install Flagger
helm repo add flagger https://flagger.app
helm upgrade -i flagger flagger/flagger \
  --namespace linkerd \
  --set meshProvider=linkerd \
  --set metricsServer=http://linkerd-prometheus:9090
```

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api-service
  namespace: production
spec:
  # Deployment reference
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service

  # HPA reference
  autoscalerRef:
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    name: api-service

  # Service spec
  service:
    port: 8080
    targetPort: 8080
    trafficPolicy:
      tls:
        mode: ISTIO_MUTUAL

  # Canary analysis
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10

    # Success rate threshold
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m

    # Load testing
    webhooks:
    - name: load-test
      url: http://flagger-loadtester/
      timeout: 5s
      metadata:
        type: cmd
        cmd: "hey -z 1m -q 10 -c 2 http://api-service-canary.production:8080/"
```

**Manual traffic split:**

```yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: api-rollout
  namespace: production
spec:
  # Root service (what clients call)
  service: api-service

  # Backend services with weights
  backends:
  - service: api-service-stable
    weight: 90
  - service: api-service-canary
    weight: 10
---
# Stable version service
apiVersion: v1
kind: Service
metadata:
  name: api-service-stable
  namespace: production
spec:
  selector:
    app: api-service
    version: stable
  ports:
  - port: 8080
    targetPort: 8080
---
# Canary version service
apiVersion: v1
kind: Service
metadata:
  name: api-service-canary
  namespace: production
spec:
  selector:
    app: api-service
    version: canary
  ports:
  - port: 8080
    targetPort: 8080
```

### Service Profiles

Service Profiles enable per-route metrics and retries:

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: api-service.production.svc.cluster.local
  namespace: production
spec:
  routes:
  # GET /api/users
  - name: GET /api/users
    condition:
      method: GET
      pathRegex: /api/users
    timeout: 5s
    retries:
      limit: 3
      timeout: 1s
    responseClasses:
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true

  # POST /api/users
  - name: POST /api/users
    condition:
      method: POST
      pathRegex: /api/users
    timeout: 10s
    isRetryable: false
    responseClasses:
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true

  # GET /api/users/:id
  - name: GET /api/users/:id
    condition:
      method: GET
      pathRegex: '/api/users/\d+'
    timeout: 3s
    retries:
      limit: 3
      timeout: 1s
```

**Auto-generate service profile from live traffic:**

```bash
# Generate from OpenAPI spec
linkerd profile --open-api swagger.json api-service -n production | kubectl apply -f -

# Generate from live traffic (observe for 1 minute)
linkerd profile -n production api-service --tap deploy/api-service --tap-duration 60s | kubectl apply -f -
```

### Ingress Configuration

**NGINX Ingress with Linkerd:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      proxy_set_header l5d-dst-override api-service.production.svc.cluster.local:8080;
      proxy_hide_header l5d-remote-ip;
      proxy_hide_header l5d-server-id;
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls
```

**Traefik Ingress with Linkerd:**

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: api-ingress
  namespace: production
spec:
  entryPoints:
  - websecure
  routes:
  - match: Host(`api.example.com`)
    kind: Rule
    services:
    - name: api-service
      port: 8080
  tls:
    secretName: api-tls
```

## Observability

### Metrics Collection

```bash
# View real-time metrics
linkerd viz stat deploy -n production

# View per-route metrics (requires ServiceProfile)
linkerd viz routes deploy/api-service -n production

# Top commands (like 'top' for services)
linkerd viz top deploy/api-service -n production

# Tap live traffic
linkerd viz tap deploy/api-service -n production

# Tap specific routes
linkerd viz tap deploy/api-service -n production --path /api/users
```

### Prometheus Metrics

Key Linkerd metrics:

```promql
# Request rate
rate(request_total[5m])

# Success rate
sum(rate(response_total{classification="success"}[5m]))
/
sum(rate(response_total[5m]))

# Latency (p95)
histogram_quantile(0.95,
  sum(rate(response_latency_ms_bucket[5m])) by (le)
)

# TCP connection count
tcp_open_connections

# Proxy CPU usage
process_cpu_seconds_total

# Proxy memory usage
process_resident_memory_bytes
```

### Grafana Dashboards

```bash
# Access Viz dashboard
linkerd viz dashboard &

# Install community Grafana dashboards
kubectl apply -f https://raw.githubusercontent.com/linkerd/linkerd2/main/grafana/dashboards/
```

**Key dashboards:**
- **Top Line** - Overall cluster health (success rate, RPS, latency)
- **Deployment** - Per-deployment metrics
- **Namespace** - Per-namespace metrics
- **Pod** - Per-pod metrics
- **Route** - Per-route metrics (requires ServiceProfile)
- **TCP** - TCP connection metrics
- **Multicluster** - Cross-cluster traffic

### Distributed Tracing

```bash
# Install Jaeger extension
linkerd jaeger install | kubectl apply -f -

# Verify installation
linkerd jaeger check

# Access Jaeger UI
linkerd jaeger dashboard &
```

**Instrumentation:**

```yaml
# Add tracing headers to your application
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    metadata:
      annotations:
        # Enable debug logging for tracing
        config.linkerd.io/trace-collector: linkerd-collector.linkerd-jaeger:55678
        config.linkerd.io/trace-collector-svc-account: linkerd-collector
    spec:
      containers:
      - name: app
        # Your application should propagate these headers:
        # - b3
        # - x-b3-traceid
        # - x-b3-spanid
        # - x-b3-parentspanid
        # - x-b3-sampled
        # - x-b3-flags
```

### Alerting

**PrometheusRule for Linkerd:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: linkerd-alerts
  namespace: linkerd
spec:
  groups:
  - name: linkerd.rules
    interval: 30s
    rules:
    # Success rate below 99%
    - alert: LinkerdServiceLowSuccessRate
      expr: |
        (
          sum(rate(response_total{classification="success",namespace="production"}[5m])) by (deployment)
          /
          sum(rate(response_total{namespace="production"}[5m])) by (deployment)
        ) < 0.99
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Low success rate for {{ $labels.deployment }}"
        description: "Success rate is {{ $value | humanizePercentage }}"

    # High latency (p99 > 1s)
    - alert: LinkerdServiceHighLatency
      expr: |
        histogram_quantile(0.99,
          sum(rate(response_latency_ms_bucket{namespace="production"}[5m])) by (le, deployment)
        ) > 1000
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High latency for {{ $labels.deployment }}"
        description: "P99 latency is {{ $value }}ms"

    # Control plane down
    - alert: LinkerdControlPlaneDown
      expr: up{namespace="linkerd",job="linkerd-controller"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Linkerd control plane is down"

    # Certificate expiration (< 7 days)
    - alert: LinkerdCertificateExpiringSoon
      expr: |
        (linkerd_identity_cert_expiration_timestamp_seconds - time()) / 86400 < 7
      for: 1h
      labels:
        severity: warning
      annotations:
        summary: "Linkerd certificate expiring soon"
        description: "Certificate expires in {{ $value }} days"
```

## Multi-Cluster Setup

### Link Two Clusters

```bash
# Install multicluster extension on both clusters
linkerd --context=cluster1 multicluster install | kubectl --context=cluster1 apply -f -
linkerd --context=cluster2 multicluster install | kubectl --context=cluster2 apply -f -

# Verify installation
linkerd --context=cluster1 multicluster check
linkerd --context=cluster2 multicluster check

# Link cluster2 to cluster1
linkerd --context=cluster1 multicluster link --cluster-name cluster1 | \
  kubectl --context=cluster2 apply -f -

# Link cluster1 to cluster2
linkerd --context=cluster2 multicluster link --cluster-name cluster2 | \
  kubectl --context=cluster1 apply -f -

# Verify gateways
linkerd --context=cluster1 multicluster gateways
linkerd --context=cluster2 multicluster gateways
```

### Export Services

```bash
# Export service from cluster1
kubectl --context=cluster1 label svc/api-service -n production \
  mirror.linkerd.io/exported=true

# Verify mirror service in cluster2
kubectl --context=cluster2 get svc -n production

# You should see: api-service-cluster1
```

### Service Discovery

```yaml
# Application in cluster2 can call:
# - api-service (local)
# - api-service-cluster1 (remote)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: production
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        # Call local first, fallback to remote
        - name: API_SERVICE_URL
          value: "http://api-service:8080"
        - name: API_SERVICE_REMOTE_URL
          value: "http://api-service-cluster1:8080"
```

### Traffic Split Across Clusters

```yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: api-multicluster
  namespace: production
spec:
  service: api-service
  backends:
  # 80% to local cluster
  - service: api-service
    weight: 80
  # 20% to remote cluster
  - service: api-service-cluster1
    weight: 20
```

## Performance Optimization

### Resource Tuning

```yaml
# Proxy resources by workload size
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-traffic-service
spec:
  template:
    metadata:
      annotations:
        # High-traffic service
        config.linkerd.io/proxy-cpu-limit: "2"
        config.linkerd.io/proxy-cpu-request: "500m"
        config.linkerd.io/proxy-memory-limit: "512Mi"
        config.linkerd.io/proxy-memory-request: "256Mi"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: low-traffic-service
spec:
  template:
    metadata:
      annotations:
        # Low-traffic service
        config.linkerd.io/proxy-cpu-limit: "500m"
        config.linkerd.io/proxy-cpu-request: "50m"
        config.linkerd.io/proxy-memory-limit: "128Mi"
        config.linkerd.io/proxy-memory-request: "20Mi"
```

### Connection Pooling

Linkerd2-proxy automatically manages connection pools, but you can tune behavior:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    metadata:
      annotations:
        # Increase idle timeout for persistent connections
        config.linkerd.io/proxy-outbound-connect-timeout: "5000ms"

        # Skip proxy for localhost traffic
        config.linkerd.io/skip-outbound-ports: "127.0.0.1"
```

### Protocol Detection

```yaml
# Mark non-HTTP ports as opaque
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
spec:
  template:
    metadata:
      annotations:
        # Don't protocol-detect these ports
        config.linkerd.io/opaque-ports: "3306,6379,5432"
```

### Benchmark Results

Typical Linkerd overhead (compared to no mesh):

- **Latency**: +1-2ms p50, +2-5ms p99
- **CPU**: 50-200m per proxy (depends on traffic)
- **Memory**: 20-50Mi per proxy (stable)
- **Throughput**: >10,000 RPS per proxy

**Comparison with Istio:**
- 5-10x lower latency overhead
- 3-5x lower memory usage
- 2-3x lower CPU usage
- Simpler operation

## Troubleshooting

### Check Mesh Status

```bash
# Overall check
linkerd check

# Proxy check
linkerd check --proxy

# Check specific namespace
linkerd -n production check --proxy

# Check data plane
linkerd viz stat deploy -n production

# Check control plane
linkerd viz stat -n linkerd deploy
```

### Debug Proxy Issues

```bash
# View proxy logs
kubectl logs pod-name -c linkerd-proxy -n production

# Increase proxy log level
kubectl annotate pod pod-name config.linkerd.io/proxy-log-level=debug -n production

# Restart with new config
kubectl delete pod pod-name -n production

# Check proxy config
linkerd viz diagnostics proxy-metrics pod-name -n production
```

### Certificate Issues

```bash
# Check certificate validity
linkerd check --proxy

# View certificate expiration
kubectl get secret linkerd-identity-issuer -n linkerd -o yaml | \
  yq '.data."tls.crt"' | base64 -d | openssl x509 -noout -text

# Force certificate rotation
kubectl delete secret linkerd-identity-issuer -n linkerd
kubectl rollout restart deployment/linkerd-identity -n linkerd
```

### Traffic Issues

```bash
# Tap live traffic
linkerd viz tap deploy/api-service -n production

# Filter by path
linkerd viz tap deploy/api-service -n production --path /api/users

# Filter by response code
linkerd viz tap deploy/api-service -n production --status 500

# Check routes
linkerd viz routes deploy/api-service -n production

# Profile validation
kubectl describe serviceprofile -n production
```

### Performance Debugging

```bash
# Check resource usage
kubectl top pod -n production

# View proxy metrics
linkerd viz diagnostics proxy-metrics pod-name -n production | grep -E "(cpu|memory|request)"

# Analyze connection stats
linkerd viz tap deploy/api-service -n production -o json | \
  jq '.requestInit // .responseInit | .http'

# Check for retries
linkerd viz stat deploy/api-service -n production --from deploy/frontend -o json | \
  jq '.statTables[].podGroup.rows[].stats.actualRetries'
```

## Upgrade Process

```bash
# Check upgrade constraints
linkerd check --pre

# Download new version
curl -fsL https://run.linkerd.io/install | sh

# Check new version compatibility
linkerd check --pre

# Upgrade CRDs
linkerd upgrade --crds | kubectl apply -f -

# Upgrade control plane
linkerd upgrade \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | kubectl apply -f -

# Verify upgrade
linkerd check

# Upgrade data plane (restart pods to inject new proxy)
kubectl rollout restart deployment -n production

# Upgrade extensions
linkerd viz upgrade | kubectl apply -f -
linkerd multicluster upgrade | kubectl apply -f -
```

## Best Practices

1. **Use ServiceProfiles** - Enable per-route metrics and retries
2. **Monitor certificates** - Alert on expiration < 7 days
3. **Set resource limits** - Tune proxy resources per workload
4. **Enable mTLS everywhere** - Automatic by default
5. **Use opaque ports** - For non-HTTP protocols
6. **Implement gradual rollouts** - Use TrafficSplit or Flagger
7. **Monitor golden signals** - Success rate, latency, throughput
8. **Regular upgrades** - Stay within 2 versions of latest
9. **Test in staging** - Always test upgrades in non-prod first
10. **Document runbooks** - Capture tribal knowledge

## References

- [Linkerd Official Documentation](https://linkerd.io/2.14/overview/)
- [Linkerd Architecture](https://linkerd.io/2.14/reference/architecture/)
- [Linkerd Best Practices](https://linkerd.io/2.14/tasks/)
- [Linkerd2-proxy GitHub](https://github.com/linkerd/linkerd2-proxy)
