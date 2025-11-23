---
name: service-mesh-patterns
description: Comprehensive service mesh implementation with Istio, Linkerd, and Cilium. Covers traffic management, security, observability, and multi-cluster patterns. Use when implementing service mesh, configuring mTLS, managing traffic routing, or troubleshooting mesh issues.
---

# Service Mesh Patterns

Production-grade service mesh implementation patterns for Kubernetes using Istio, Linkerd, and Cilium. Based on best practices from AWS, Google Cloud, Microsoft Azure, and leading cloud-native organizations.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

## When to Use This Skill

- Implement service mesh for microservices communication
- Configure mutual TLS (mTLS) for zero-trust security
- Manage advanced traffic routing (canary, blue-green, A/B testing)
- Implement circuit breaking and fault injection
- Set up multi-cluster service mesh
- Configure egress traffic control
- Troubleshoot service mesh performance issues
- Migrate between service mesh solutions
- Implement observability for service-to-service communication

## Service Mesh Overview

### What is a Service Mesh?

A service mesh is a dedicated infrastructure layer for managing service-to-service communication in microservices architectures. It provides:

1. **Traffic Management** - Intelligent routing, load balancing, retries, timeouts
2. **Security** - Mutual TLS, authentication, authorization
3. **Observability** - Metrics, logs, distributed tracing
4. **Resilience** - Circuit breaking, fault injection, rate limiting

### Architecture Components

**Data Plane:**
- Sidecar proxies (Envoy, Linkerd2-proxy) injected into application pods
- Intercepts all network traffic
- Enforces policies and collects telemetry

**Control Plane:**
- Manages and configures proxies
- Provides service discovery
- Issues and rotates certificates
- Aggregates telemetry

## Istio Implementation

**Reference:** See `references/istio-patterns.md` for detailed Istio patterns

### 1. Istio Installation

**Production installation with istioctl:**

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.20.0 sh -
cd istio-1.20.0
export PATH=$PWD/bin:$PATH

# Create production configuration
cat <<EOF > istio-production.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-production
  namespace: istio-system
spec:
  profile: production

  # High availability control plane
  components:
    pilot:
      k8s:
        replicaCount: 3
        resources:
          requests:
            cpu: 500m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        hpaSpec:
          minReplicas: 3
          maxReplicas: 10
          metrics:
          - type: Resource
            resource:
              name: cpu
              targetAverageUtilization: 80

    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        replicaCount: 3
        resources:
          requests:
            cpu: 1000m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 2Gi
        service:
          type: LoadBalancer
          ports:
          - port: 80
            targetPort: 8080
            name: http2
          - port: 443
            targetPort: 8443
            name: https
          - port: 15021
            targetPort: 15021
            name: status-port

    egressGateways:
    - name: istio-egressgateway
      enabled: true
      k8s:
        replicaCount: 2
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi

  # Mesh configuration
  meshConfig:
    # Enable access logging
    accessLogFile: /dev/stdout
    accessLogEncoding: JSON

    # Default tracing configuration
    defaultConfig:
      tracing:
        sampling: 10.0
        zipkin:
          address: jaeger-collector.monitoring:9411

    # Enable automatic mTLS
    enableAutoMtls: true

    # Outbound traffic policy
    outboundTrafficPolicy:
      mode: REGISTRY_ONLY

  # Global values
  values:
    global:
      # Production logging level
      logAsJson: true
      logging:
        level: "default:info"

      # Multi-cluster configuration
      multiCluster:
        clusterName: production-us-east-1

      # Proxy configuration
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 2000m
            memory: 1Gi

        # Automatic sidecar injection
        autoInject: enabled

        # Concurrency (defaults to 2)
        concurrency: 2
EOF

# Install Istio
istioctl install -f istio-production.yaml -y

# Verify installation
kubectl get pods -n istio-system
istioctl verify-install
```

### 2. Automatic Sidecar Injection

```bash
# Enable automatic injection for namespace
kubectl label namespace production istio-injection=enabled

# Verify injection is enabled
kubectl get namespace -L istio-injection
```

**Control injection per deployment:**

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
        # Disable injection for this pod
        sidecar.istio.io/inject: "false"

        # Custom proxy resources
        sidecar.istio.io/proxyCPU: "200m"
        sidecar.istio.io/proxyMemory: "256Mi"
```

### 3. Traffic Management

**VirtualService for advanced routing:**

**Asset:** See `assets/istio-virtual-service.yaml` for production examples

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
  namespace: production
spec:
  hosts:
  - reviews
  http:
  # Canary deployment (10% to v2, 90% to v1)
  - match:
    - headers:
        end-user:
          exact: "beta-tester"
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10

    # Request timeout
    timeout: 10s

    # Retries configuration
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure,refused-stream
```

**DestinationRule for load balancing and circuit breaking:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
  namespace: production
spec:
  host: reviews
  trafficPolicy:
    # Connection pool settings
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2

    # Load balancer settings
    loadBalancer:
      consistentHash:
        httpHeaderName: x-user-id

    # Outlier detection (circuit breaking)
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40

  # Subsets for different versions
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        simple: LEAST_REQUEST
  - name: v2
    labels:
      version: v2
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
```

**Gateway for ingress traffic:**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: app-gateway
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
      credentialName: app-tls-cert
    hosts:
    - "app.example.com"
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "app.example.com"
    tls:
      httpsRedirect: true
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app
  namespace: production
spec:
  hosts:
  - "app.example.com"
  gateways:
  - app-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: api-service
        port:
          number: 8080
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: frontend-service
        port:
          number: 80
```

### 4. Security Configuration

**Strict mTLS for entire namespace:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Allow specific port in PERMISSIVE mode
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-app
  namespace: production
spec:
  selector:
    matchLabels:
      app: legacy-service
  mtls:
    mode: PERMISSIVE
  portLevelMtls:
    9090:
      mode: DISABLE
```

**Authorization policies:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-access
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
  # Allow from frontend
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]

  # Allow from specific namespace
  - from:
    - source:
        namespaces: ["production"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/health"]
---
# Deny all by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}
---
# Custom authorization with JWT
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    audiences:
    - "api.example.com"
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-service
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["*"]
    when:
    - key: request.auth.claims[role]
      values: ["admin", "user"]
```

### 5. Observability

**Telemetry configuration:**

```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  # Metrics
  metrics:
  - providers:
    - name: prometheus
    overrides:
    - match:
        metric: ALL_METRICS
      tagOverrides:
        source_cluster:
          value: "production-us-east-1"

  # Access logging
  accessLogging:
  - providers:
    - name: envoy
    filter:
      expression: response.code >= 400

  # Tracing
  tracing:
  - providers:
    - name: zipkin
    randomSamplingPercentage: 10.0
    customTags:
      environment:
        literal:
          value: production
```

## Linkerd Implementation

**Reference:** See `references/linkerd-guide.md` for detailed Linkerd guide

### 1. Linkerd Installation

```bash
# Install Linkerd CLI
curl -sL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

# Validate cluster
linkerd check --pre

# Install CRDs
linkerd install --crds | kubectl apply -f -

# Install control plane
linkerd install \
  --ha \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | kubectl apply -f -

# Verify installation
linkerd check

# Install observability extensions
linkerd viz install | kubectl apply -f -
```

### 2. Mesh Applications

```bash
# Inject Linkerd proxy
kubectl get deploy -n production -o yaml \
  | linkerd inject - \
  | kubectl apply -f -

# Verify mesh status
linkerd -n production check --proxy

# View metrics
linkerd viz dashboard &
```

### 3. Traffic Split (Canary Deployments)

```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: api-canary
  namespace: production
spec:
  service: api-service
  backends:
  - service: api-service-stable
    weight: 90
  - service: api-service-canary
    weight: 10
```

### 4. Service Profiles for Advanced Routing

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: api-service.production.svc.cluster.local
  namespace: production
spec:
  routes:
  - name: GET /api/users
    condition:
      method: GET
      pathRegex: /api/users
    timeout: 5s
    retries:
      limit: 3
      timeout: 1s
  - name: POST /api/users
    condition:
      method: POST
      pathRegex: /api/users
    timeout: 10s
    isRetryable: false
```

## Cilium Service Mesh

### 1. Cilium Installation with Service Mesh

```bash
# Add Cilium Helm repo
helm repo add cilium https://helm.cilium.io/
helm repo update

# Install Cilium with service mesh enabled
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set kubeProxyReplacement=strict \
  --set k8sServiceHost=API_SERVER_IP \
  --set k8sServicePort=API_SERVER_PORT \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set envoy.enabled=true \
  --set ingressController.enabled=true

# Verify installation
cilium status
```

### 2. Network Policies with L7 Awareness

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-l7-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: api-service
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/api/users"
        - method: "POST"
          path: "/api/users"
          headers:
          - "Content-Type: application/json"
```

### 3. Service Mesh with Hubble Observability

```bash
# Enable Hubble observability
cilium hubble enable

# View service map
hubble observe --namespace production

# Monitor specific service
hubble observe --from-pod production/api-service --to-pod production/database
```

## Service Mesh Comparison

**Asset:** See `assets/mesh-comparison.md` for detailed comparison

### Quick Comparison

| Feature | Istio | Linkerd | Cilium |
|---------|-------|---------|--------|
| **Proxy** | Envoy | Linkerd2-proxy | Envoy |
| **Control Plane Language** | Go | Go/Rust | Go |
| **Resource Overhead** | High | Low | Medium |
| **Complexity** | High | Low | Medium |
| **Features** | Comprehensive | Focused | Network-centric |
| **mTLS** | Yes | Automatic | Yes |
| **Multi-cluster** | Yes | Yes | Yes |
| **Protocol Support** | HTTP/1.1, HTTP/2, gRPC, TCP | HTTP/1.1, HTTP/2, gRPC, TCP | HTTP, gRPC, Kafka, DNS |
| **Service Discovery** | Kubernetes | Kubernetes | Kubernetes + DNS |

### Selection Criteria

**Choose Istio when:**
- Need comprehensive traffic management features
- Require advanced security policies
- Multi-cloud/multi-cluster deployment
- Large organization with dedicated platform team
- Willing to accept higher resource overhead

**Choose Linkerd when:**
- Simplicity and ease of use are priorities
- Want minimal resource overhead
- Need fast, automatic mTLS
- Smaller teams or getting started with service mesh
- Focus on core service mesh features

**Choose Cilium when:**
- Need eBPF-based networking
- Want L7 network policies
- Kubernetes network plugin replacement
- High-performance requirements
- Need deep visibility at kernel level

## Multi-Cluster Patterns

### Istio Multi-Cluster Setup

**Primary-remote cluster topology:**

```bash
# On primary cluster
istioctl install -f istio-primary.yaml

# Create remote secret
istioctl x create-remote-secret \
  --context=remote-cluster \
  --name=remote-cluster | \
  kubectl apply -f - --context=primary-cluster

# On remote cluster
istioctl install -f istio-remote.yaml
```

**Multi-primary topology:**

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-multi-primary
spec:
  profile: default
  values:
    global:
      meshID: mesh1
      multiCluster:
        clusterName: cluster1
      network: network1
```

### Linkerd Multi-Cluster

```bash
# Install on both clusters
linkerd multicluster install | kubectl apply -f -

# Link clusters
linkerd --context=cluster1 multicluster link --cluster-name cluster1 | \
  kubectl --context=cluster2 apply -f -

# Export service
kubectl --context=cluster1 label svc/api-service \
  mirror.linkerd.io/exported=true

# Verify
linkerd --context=cluster2 multicluster gateways
```

## Best Practices

### 1. Security

- **Enable mTLS everywhere** - Use STRICT mode in production
- **Implement zero-trust** - Deny-all policies with explicit allows
- **Rotate certificates** - Automate certificate rotation
- **Audit authorization** - Log all authorization decisions
- **Limit egress** - Control external service access

### 2. Traffic Management

- **Start conservative** - Begin with simple routing, add complexity gradually
- **Use timeouts** - Set reasonable timeouts on all services
- **Implement retries** - Use exponential backoff
- **Circuit breaking** - Protect downstream services
- **Rate limiting** - Prevent resource exhaustion

### 3. Observability

- **Golden signals** - Monitor latency, traffic, errors, saturation
- **Distributed tracing** - Enable tracing with appropriate sampling
- **Service-level metrics** - Collect RED (Rate, Errors, Duration) metrics
- **Dashboard creation** - Build service-specific dashboards
- **Alert on SLOs** - Alert on business-impacting issues

### 4. Performance

- **Resource limits** - Set appropriate proxy resource limits
- **Connection pooling** - Configure connection pools
- **Concurrency** - Tune proxy worker threads
- **Sampling rates** - Balance observability vs performance
- **Protocol selection** - Use HTTP/2 or gRPC when possible

### 5. Operations

- **Gradual rollout** - Enable mesh namespace by namespace
- **Version compatibility** - Test control plane upgrades in non-prod
- **Monitoring overhead** - Track proxy resource consumption
- **Canary control plane** - Upgrade control plane with canary revisions
- **Disaster recovery** - Document rollback procedures

## Troubleshooting

### Common Istio Issues

**1. Sidecar injection not working:**
```bash
# Check namespace label
kubectl get namespace production -o yaml | grep istio-injection

# Check webhook
kubectl get mutatingwebhookconfigurations istio-sidecar-injector -o yaml

# Manual injection
istioctl kube-inject -f deployment.yaml | kubectl apply -f -
```

**2. mTLS issues:**
```bash
# Check mTLS status
istioctl authn tls-check pod-name.production

# Verify certificates
istioctl proxy-config secret pod-name.production -o json

# Check peer authentication
kubectl get peerauthentication -A
```

**3. Traffic routing not working:**
```bash
# Verify configuration
istioctl analyze

# Check route configuration
istioctl proxy-config route pod-name.production -o json

# Debug with Envoy logs
kubectl logs pod-name -c istio-proxy --tail=100
```

### Common Linkerd Issues

**1. Proxy not injected:**
```bash
# Check annotation
kubectl get deploy api-service -o yaml | grep linkerd.io/inject

# Force injection
kubectl annotate deploy api-service linkerd.io/inject=enabled

# Restart deployment
kubectl rollout restart deploy/api-service
```

**2. Certificate issues:**
```bash
# Check certificate expiration
linkerd check --proxy

# View certificate details
kubectl get secret -n linkerd linkerd-identity-issuer -o yaml
```

**3. Traffic split not working:**
```bash
# Verify TrafficSplit
kubectl describe trafficsplit api-canary

# Check endpoints
kubectl get endpoints api-service-stable api-service-canary

# View metrics
linkerd viz stat trafficsplit/api-canary
```

### Performance Debugging

**High latency investigation:**

```bash
# Istio: Check proxy overhead
kubectl exec -it pod-name -c istio-proxy -- \
  curl localhost:15000/stats/prometheus | grep duration

# Linkerd: Check proxy metrics
linkerd viz stat deploy/api-service --from deploy/frontend

# Cilium: Check Hubble flows
hubble observe --namespace production --protocol http \
  --http-status 200 --http-method GET
```

**High memory usage:**

```bash
# Check proxy resource usage
kubectl top pod -n production

# Increase proxy resources
kubectl patch deployment api-service \
  -p '{"spec":{"template":{"metadata":{"annotations":{"sidecar.istio.io/proxyMemoryLimit":"512Mi"}}}}}'

# Analyze heap dump (Envoy)
kubectl exec -it pod-name -c istio-proxy -- \
  curl -X POST localhost:15000/heap_dump
```

## Migration Strategies

### Migrating Between Service Meshes

**Istio to Linkerd:**

1. Install Linkerd alongside Istio
2. Gradually inject Linkerd proxies per namespace
3. Update traffic management configs
4. Validate functionality
5. Remove Istio sidecars
6. Uninstall Istio

**No Service Mesh to Service Mesh:**

1. **Phase 1: Observability** - Install mesh in monitoring-only mode
2. **Phase 2: Security** - Enable mTLS in PERMISSIVE mode
3. **Phase 3: Strict mTLS** - Switch to STRICT mode
4. **Phase 4: Traffic Management** - Implement routing rules
5. **Phase 5: Advanced Features** - Add circuit breaking, retries, etc.

## References

- `references/istio-patterns.md` - Comprehensive Istio configuration patterns
- `references/linkerd-guide.md` - Linkerd deployment and operations guide

## Assets

- `assets/istio-virtual-service.yaml` - Production VirtualService examples
- `assets/mesh-comparison.md` - Detailed feature comparison and benchmarks

## Related Skills

- `observability-monitoring` - Service mesh observability integration
- `k8s-security-policies` - Network policies and security
- `gitops-workflow` - Service mesh configuration management
