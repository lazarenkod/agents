# Istio Production Patterns

Comprehensive Istio implementation patterns based on production deployments at AWS, Google Cloud, Microsoft Azure, and cloud-native organizations.

## Table of Contents

1. [Installation Patterns](#installation-patterns)
2. [Traffic Management](#traffic-management)
3. [Security Configuration](#security-configuration)
4. [Observability Integration](#observability-integration)
5. [Multi-Cluster Patterns](#multi-cluster-patterns)
6. [Advanced Patterns](#advanced-patterns)

## Installation Patterns

### Pattern 1: Canary Control Plane Upgrades

Istio supports installing multiple control planes (revisions) for safe upgrades:

```bash
# Install new revision
istioctl install --set revision=1-20-0 -f istio-production.yaml

# Verify new revision
kubectl get pods -n istio-system -l app=istiod

# Migrate namespace to new revision
kubectl label namespace production istio.io/rev=1-20-0 --overwrite
kubectl label namespace production istio-injection-

# Rollout workloads
kubectl rollout restart deployment -n production

# Verify migration
istioctl proxy-status

# Remove old revision (after validation)
istioctl uninstall --revision=1-19-0
```

### Pattern 2: External Control Plane

Deploy control plane separately from data plane for isolation:

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: external-istiod
  namespace: external-istiod
spec:
  profile: external
  values:
    global:
      externalIstiod: true
      istioNamespace: external-istiod
  meshConfig:
    trustDomain: external-cluster.local
  components:
    pilot:
      k8s:
        env:
        - name: CLUSTER_ID
          value: external-cluster
        - name: EXTERNAL_ISTIOD
          value: "true"
```

### Pattern 3: Resource Optimization

Production-tuned resource allocation:

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      proxy:
        # Optimize resources per workload profile
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 2000m
            memory: 1Gi

    # Pilot tuning
    pilot:
      cpu:
        targetAverageUtilization: 80
      memory:
        targetAverageUtilization: 80

    # Environment variables for tuning
    global:
      proxy:
        # Number of worker threads
        concurrency: 2

        # Increase connection pool
        envoyStatsd:
          enabled: false

  components:
    pilot:
      k8s:
        env:
        # Push optimization
        - name: PILOT_PUSH_THROTTLE
          value: "100"
        - name: PILOT_DEBOUNCE_AFTER
          value: "100ms"
        - name: PILOT_DEBOUNCE_MAX
          value: "10s"

        # Memory limits
        - name: PILOT_MAX_REQUESTS_PER_SECOND
          value: "100"

        # XDS caching
        - name: PILOT_ENABLE_XDS_CACHE
          value: "true"
```

## Traffic Management

### Pattern 1: Progressive Canary Deployment

Automated canary with Flagger:

```yaml
# Install Flagger
helm repo add flagger https://flagger.app
helm upgrade -i flagger flagger/flagger \
  --namespace istio-system \
  --set meshProvider=istio \
  --set metricsServer=http://prometheus.monitoring:9090

# Canary resource
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api-service
  namespace: production
spec:
  # Target deployment
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service

  # Deployment strategy
  progressDeadlineSeconds: 600

  # HPA reference (optional)
  autoscalerRef:
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    name: api-service

  service:
    port: 8080
    targetPort: 8080
    gateways:
    - api-gateway
    hosts:
    - api.example.com
    trafficPolicy:
      tls:
        mode: ISTIO_MUTUAL

  # Canary analysis
  analysis:
    # Schedule interval
    interval: 1m
    # Max number of failed metric checks
    threshold: 5
    # Max traffic percentage routed to canary
    maxWeight: 50
    # Canary increment step
    stepWeight: 10

    # Metrics
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m

    # Webhooks for custom checks
    webhooks:
    - name: load-test
      url: http://flagger-loadtester/
      timeout: 5s
      metadata:
        type: cmd
        cmd: "hey -z 1m -q 10 -c 2 http://api-service-canary.production:8080/health"
```

### Pattern 2: Multi-Version Traffic Split

A/B testing with header-based routing:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-ab-test
  namespace: production
spec:
  hosts:
  - api-service
  http:
  # Beta testers always go to v2
  - match:
    - headers:
        x-user-group:
          exact: "beta"
    route:
    - destination:
        host: api-service
        subset: v2

  # 10% of production traffic to v2
  - match:
    - headers:
        x-user-group:
          exact: "production"
    route:
    - destination:
        host: api-service
        subset: v1
      weight: 90
    - destination:
        host: api-service
        subset: v2
      weight: 10

  # Default: v1
  - route:
    - destination:
        host: api-service
        subset: v1

    # Mirror 1% to v2 for testing
    mirror:
      host: api-service
      subset: v2
    mirrorPercentage:
      value: 1.0
```

### Pattern 3: Advanced Retry Logic

Sophisticated retry policies:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-retries
  namespace: production
spec:
  hosts:
  - api-service
  http:
  - route:
    - destination:
        host: api-service
    retries:
      attempts: 3
      perTryTimeout: 2s

      # Retry conditions
      retryOn: 5xx,reset,connect-failure,refused-stream,retriable-4xx

      # Retry remote locality on failure
      retryRemoteLocalities: true

    # Per-request timeout
    timeout: 10s

    # Fault injection for testing
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
      abort:
        percentage:
          value: 0.01
        httpStatus: 500
```

### Pattern 4: Egress Gateway

Control external service access:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-api
  namespace: production
spec:
  hosts:
  - api.external.com
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
---
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: egress-gateway
  namespace: istio-system
spec:
  selector:
    istio: egressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - api.external.com
    tls:
      mode: PASSTHROUGH
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: direct-external-through-egress
  namespace: production
spec:
  hosts:
  - api.external.com
  gateways:
  - mesh
  - istio-system/egress-gateway
  http:
  - match:
    - gateways:
      - mesh
      port: 443
    route:
    - destination:
        host: istio-egressgateway.istio-system.svc.cluster.local
        port:
          number: 443
      weight: 100
  - match:
    - gateways:
      - istio-system/egress-gateway
      port: 443
    route:
    - destination:
        host: api.external.com
        port:
          number: 443
      weight: 100
---
# DestinationRule for egress traffic
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: egress-api-external
  namespace: production
spec:
  host: api.external.com
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 10
      http:
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    tls:
      mode: SIMPLE
```

### Pattern 5: Locality-Based Load Balancing

Prioritize local traffic:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: locality-lb
  namespace: production
spec:
  host: api-service
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        # Distribute traffic within locality
        distribute:
        - from: us-east-1a/*
          to:
            "us-east-1a/*": 80
            "us-east-1b/*": 20
        - from: us-east-1b/*
          to:
            "us-east-1b/*": 80
            "us-east-1a/*": 20

        # Failover configuration
        failover:
        - from: us-east-1
          to: us-west-2

    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

## Security Configuration

### Pattern 1: Zero-Trust Security Model

Implement deny-by-default with explicit allows:

```yaml
# Deny all traffic by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}
---
# Allow health checks
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-health-checks
  namespace: production
spec:
  action: ALLOW
  rules:
  - to:
    - operation:
        paths: ["/health", "/ready"]
        methods: ["GET"]
---
# Allow service-to-service communication
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - "cluster.local/ns/production/sa/frontend"
    to:
    - operation:
        methods: ["GET", "POST", "PUT", "DELETE"]
        paths: ["/api/*"]
---
# Allow ingress gateway
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-ingress
  namespace: production
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
  - from:
    - source:
        namespaces: ["istio-system"]
        principals: ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]
```

### Pattern 2: External Authorization

Integrate with OPA (Open Policy Agent):

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: ext-authz-opa
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: CUSTOM
  provider:
    name: opa-ext-authz
  rules:
  - to:
    - operation:
        paths: ["/api/*"]
---
# Configure external authorizer in mesh config
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    extensionProviders:
    - name: opa-ext-authz
      envoyExtAuthzGrpc:
        service: opa.authorization.svc.cluster.local
        port: 9191
        timeout: 1s
        includeRequestHeaders:
        - authorization
        - x-user-id
        includeRequestBody:
          maxRequestBytes: 8192
          allowPartialMessage: true
```

### Pattern 3: Certificate Management

Integrate with cert-manager:

```yaml
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create Issuer
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod
  namespace: istio-system
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: istio
---
# Create Certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls-cert
  namespace: istio-system
spec:
  secretName: api-tls-cert
  issuerRef:
    name: letsencrypt-prod
    kind: Issuer
  dnsNames:
  - api.example.com
  - "*.api.example.com"
---
# Use certificate in Gateway
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: api-tls-cert
    hosts:
    - "api.example.com"
```

### Pattern 4: Workload-Specific mTLS

Fine-grained mTLS control:

```yaml
# Strict mTLS for sensitive services
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: database-strict-mtls
  namespace: production
spec:
  selector:
    matchLabels:
      app: database
  mtls:
    mode: STRICT
---
# Permissive for migration
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-permissive
  namespace: production
spec:
  selector:
    matchLabels:
      app: legacy-service
  mtls:
    mode: PERMISSIVE
  portLevelMtls:
    # Disable mTLS for specific port
    9090:
      mode: DISABLE
---
# Monitor mTLS metrics
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mtls-metrics
  namespace: production
spec:
  metrics:
  - providers:
    - name: prometheus
    overrides:
    - match:
        metric: REQUEST_COUNT
      tagOverrides:
        connection_security_policy:
          value: "connection.mtls | 'unknown'"
```

## Observability Integration

### Pattern 1: Distributed Tracing with OpenTelemetry

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    enableTracing: true
    defaultConfig:
      tracing:
        sampling: 10.0
        max_path_tag_length: 256
        custom_tags:
          environment:
            literal:
              value: production
          version:
            environment:
              name: APP_VERSION
    extensionProviders:
    - name: otel
      opentelemetry:
        service: opentelemetry-collector.monitoring.svc.cluster.local
        port: 4317
---
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: otel-tracing
  namespace: production
spec:
  tracing:
  - providers:
    - name: otel
    randomSamplingPercentage: 10.0
    customTags:
      user_id:
        header:
          name: x-user-id
          defaultValue: anonymous
      request_id:
        header:
          name: x-request-id
```

### Pattern 2: Custom Metrics with Wasm

```yaml
apiVersion: extensions.istio.io/v1alpha1
kind: WasmPlugin
metadata:
  name: custom-metrics
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: api-service
  url: oci://registry.example.com/wasm-plugins/metrics:1.0.0
  phase: STATS
  pluginConfig:
    metrics:
    - name: business_transactions_total
      type: counter
      description: "Total number of business transactions"
      tags:
      - transaction_type
      - status
```

### Pattern 3: Access Log Customization

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: access-logs
  namespace: production
spec:
  accessLogging:
  - providers:
    - name: envoy
    filter:
      expression: |
        response.code >= 400 ||
        connection.mtls == false ||
        request.useragent.contains('bot')
  - providers:
    - name: otel
    match:
      mode: SERVER_AND_CLIENT
```

### Pattern 4: Service-Level Dashboards

Key metrics to monitor:

```promql
# Request rate
rate(istio_requests_total{destination_workload="api-service"}[5m])

# Error rate
rate(istio_requests_total{destination_workload="api-service",response_code=~"5.."}[5m])
/
rate(istio_requests_total{destination_workload="api-service"}[5m])

# Latency (p95)
histogram_quantile(0.95,
  sum(rate(istio_request_duration_milliseconds_bucket{destination_workload="api-service"}[5m])) by (le)
)

# TCP connection count
istio_tcp_connections_opened_total{destination_workload="api-service"}

# mTLS usage
sum(istio_requests_total{destination_workload="api-service",connection_security_policy="mutual_tls"})
/
sum(istio_requests_total{destination_workload="api-service"})
```

## Multi-Cluster Patterns

### Pattern 1: Primary-Remote Topology

Primary cluster hosts control plane:

```bash
# Set up primary cluster
export CTX_CLUSTER1=primary-cluster
kubectl create namespace istio-system --context="${CTX_CLUSTER1}"

# Install on primary
istioctl install --context="${CTX_CLUSTER1}" -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  profile: default
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
EOF

# Enable endpoint discovery for remote cluster
kubectl apply --context="${CTX_CLUSTER1}" -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: istio-remote-secret-cluster2
  namespace: istio-system
  labels:
    istio/multiCluster: "true"
  annotations:
    networking.istio.io/cluster: cluster2
stringData:
  cluster2: |
    $(kubectl get secret -n kube-system \
      $(kubectl get sa -n kube-system default -o jsonpath='{.secrets[0].name}') \
      -o jsonpath='{.data.ca\.crt}' --context="${CTX_CLUSTER2}")
EOF

# Install on remote cluster
export CTX_CLUSTER2=remote-cluster
istioctl install --context="${CTX_CLUSTER2}" -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  profile: remote
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network1
      remotePilotAddress: ${PILOT_ADDRESS}
EOF
```

### Pattern 2: Multi-Primary Topology

All clusters have control planes:

```yaml
# Cluster 1 configuration
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-cluster1
spec:
  profile: default
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
---
# Cluster 2 configuration
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-cluster2
spec:
  profile: default
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster2
      network: network2
```

### Pattern 3: Multi-Network Configuration

Clusters in different networks:

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1

  components:
    ingressGateways:
    # East-west gateway for cross-network traffic
    - name: istio-eastwestgateway
      label:
        istio: eastwestgateway
        app: istio-eastwestgateway
      enabled: true
      k8s:
        env:
        - name: ISTIO_META_REQUESTED_NETWORK_VIEW
          value: network1
        service:
          ports:
          - name: status-port
            port: 15021
            targetPort: 15021
          - name: tls
            port: 15443
            targetPort: 15443
          - name: tls-istiod
            port: 15012
            targetPort: 15012
          - name: tls-webhook
            port: 15017
            targetPort: 15017
```

## Advanced Patterns

### Pattern 1: Sidecar Resource Optimization

Limit sidecar scope for performance:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: api-service-sidecar
  namespace: production
spec:
  workloadSelector:
    labels:
      app: api-service

  # Limit egress traffic
  egress:
  - hosts:
    - "production/*"
    - "istio-system/*"

  # Outbound traffic settings
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY

  # Ingress configuration
  ingress:
  - port:
      number: 8080
      protocol: HTTP
      name: http
    defaultEndpoint: 127.0.0.1:8080
```

### Pattern 2: Istio CNI for Init Container Removal

```bash
# Install Istio CNI
helm install istio-cni istio/cni -n kube-system \
  --set cni.cniBinDir=/opt/cni/bin \
  --set cni.cniConfDir=/etc/cni/net.d \
  --set cni.excludeNamespaces[0]=kube-system \
  --set cni.excludeNamespaces[1]=istio-system

# Install Istio with CNI enabled
istioctl install --set components.cni.enabled=true
```

### Pattern 3: VM Workload Integration

Extend mesh to VMs:

```bash
# Create VM namespace and serviceaccount
kubectl create namespace vm
kubectl create serviceaccount vm-sa -n vm

# Generate files for VM
istioctl x workload group create \
  --name vm-workload \
  --namespace vm \
  --labels app=vm-service \
  --serviceAccount vm-sa > workloadgroup.yaml

kubectl apply -f workloadgroup.yaml

# Generate bootstrap config
istioctl x workload entry configure \
  -f workloadgroup.yaml \
  -o vm-files \
  --clusterID cluster1 \
  --autoregister

# On VM, install and configure
curl -LO https://storage.googleapis.com/istio-release/releases/1.20.0/deb/istio-sidecar.deb
sudo dpkg -i istio-sidecar.deb

# Copy bootstrap files
sudo cp cluster.env /var/lib/istio/envoy/
sudo cp mesh.yaml /etc/istio/config/mesh
sudo cp root-cert.pem /etc/certs/
sudo cp token /var/run/secrets/tokens/

# Start Istio
sudo systemctl start istio
```

### Pattern 4: Rate Limiting with Envoy

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit-filter
  namespace: production
spec:
  workloadSelector:
    labels:
      app: api-service
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_INBOUND
      listener:
        filterChain:
          filter:
            name: envoy.filters.network.http_connection_manager
            subFilter:
              name: envoy.filters.http.router
    patch:
      operation: INSERT_BEFORE
      value:
        name: envoy.filters.http.ratelimit
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.http.ratelimit.v3.RateLimit
          domain: production-ratelimit
          failure_mode_deny: true
          rate_limit_service:
            grpc_service:
              envoy_grpc:
                cluster_name: rate_limit_cluster
            transport_api_version: V3
---
# Rate limit service configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: ratelimit-config
  namespace: production
data:
  config.yaml: |
    domain: production-ratelimit
    descriptors:
      - key: header_match
        value: "api-key"
        rate_limit:
          unit: minute
          requests_per_unit: 100
```

## Performance Tuning

### Control Plane Optimization

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    pilot:
      k8s:
        env:
        # Reduce push debounce time
        - name: PILOT_DEBOUNCE_AFTER
          value: "100ms"
        - name: PILOT_DEBOUNCE_MAX
          value: "10s"

        # Enable XDS caching
        - name: PILOT_ENABLE_XDS_CACHE
          value: "true"

        # Limit config pushes
        - name: PILOT_PUSH_THROTTLE
          value: "100"

        # Optimize memory
        - name: PILOT_FILTER_GATEWAY_CLUSTER_CONFIG
          value: "true"

        # Status QPS limits
        - name: PILOT_STATUS_QPS
          value: "100"
        - name: PILOT_STATUS_BURST
          value: "500"
```

### Data Plane Optimization

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-sidecar-injector
  namespace: istio-system
data:
  values: |
    global:
      proxy:
        # Resource allocation
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 2000m
            memory: 1Gi

        # Concurrency
        concurrency: 2

        # Logging level
        logLevel: warning

        # Component logging
        componentLogLevel: "misc:error"

        # Lifecycle
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

        # Hold application until proxy ready
        holdApplicationUntilProxyStarts: true
```

## Troubleshooting Commands

```bash
# Validate configuration
istioctl analyze --all-namespaces

# Check proxy configuration
istioctl proxy-config cluster pod-name.production
istioctl proxy-config listener pod-name.production
istioctl proxy-config route pod-name.production
istioctl proxy-config endpoint pod-name.production

# Debug proxy
istioctl proxy-status
istioctl dashboard envoy pod-name.production

# Check mTLS
istioctl authn tls-check pod-name.production

# View metrics
kubectl exec -it pod-name -c istio-proxy -- \
  curl localhost:15000/stats/prometheus

# Debug control plane
kubectl logs -n istio-system deploy/istiod -f

# Experimental commands
istioctl experimental describe pod pod-name -n production
istioctl experimental wait --for=distribution Deployment/api-service.production

# Inject configuration
kubectl get deployment api-service -o yaml | \
  istioctl kube-inject -f - | \
  kubectl apply -f -
```

## References

- [Istio Official Documentation](https://istio.io/latest/docs/)
- [Istio Performance and Scalability](https://istio.io/latest/docs/ops/deployment/performance-and-scalability/)
- [Istio Security Best Practices](https://istio.io/latest/docs/ops/best-practices/security/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/envoy/latest/)
