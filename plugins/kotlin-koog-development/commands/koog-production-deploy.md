---
name: koog-production-deploy
description: Comprehensive production deployment command for Koog agents covering containerization, Kubernetes orchestration, monitoring setup, secrets management, auto-scaling, and production validation. Use to deploy agents to production with zero-downtime and full observability.
---

# Koog Production Deployment Command

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Purpose

Provides an end-to-end workflow for deploying Koog AI agents to production environments. Handles containerization, Kubernetes manifest generation, monitoring setup, secrets management, auto-scaling configuration, and production validation with zero-downtime deployment strategies.

## Quick Start

```bash
/koog-production-deploy
```

Follow the interactive prompts to configure your production deployment.

## Configuration Options

### Deployment Target
```bash
--target kubernetes     # Kubernetes deployment (default)
--target docker         # Docker Compose deployment
--target cloud-run      # Google Cloud Run
--target ecs            # AWS ECS/Fargate
--target azure          # Azure Container Instances
```

### Container Configuration
```bash
--base-image jre17             # Eclipse Temurin JRE 17 (default)
--base-image jre21             # Eclipse Temurin JRE 21
--base-image graalvm           # GraalVM native image
--registry dockerhub           # Docker Hub (default)
--registry gcr                 # Google Container Registry
--registry ecr                 # AWS Elastic Container Registry
--registry acr                 # Azure Container Registry
```

### Kubernetes Strategy
```bash
--strategy rolling      # Rolling update (default, zero-downtime)
--strategy blue-green   # Blue-green deployment
--strategy canary       # Canary deployment with gradual rollout
--replicas 3            # Initial replica count (default: 3)
--enable-hpa            # Enable Horizontal Pod Autoscaler (default: true)
--enable-vpa            # Enable Vertical Pod Autoscaler (default: false)
```

### Monitoring & Observability
```bash
--monitoring prometheus        # Prometheus metrics (default)
--monitoring datadog           # Datadog integration
--monitoring newrelic          # New Relic APM
--tracing opentelemetry        # OpenTelemetry tracing (default)
--tracing jaeger               # Jaeger tracing
--logging structured           # Structured JSON logging (default)
--logging plaintext            # Plain text logging
```

### Secrets Management
```bash
--secrets kubernetes           # Kubernetes Secrets (default)
--secrets vault                # HashiCorp Vault
--secrets aws-secrets          # AWS Secrets Manager
--secrets gcp-secrets          # GCP Secret Manager
--secrets azure-keyvault       # Azure Key Vault
--secrets sealed               # Sealed Secrets (GitOps-friendly)
```

### Project Configuration
```bash
--agent-path <path>              # Path to agent project (required)
--namespace <name>               # Kubernetes namespace (default: koog-agents)
--domain <domain>                # Public domain for ingress (optional)
--tls-enabled                    # Enable TLS/SSL (default: false)
--cert-manager                   # Use cert-manager for TLS (default: false)
--resource-limits <preset>       # Resource limits: small, medium, large, custom
```

## Execution Workflow

This command orchestrates production deployment through multiple phases using the **koog-production-engineer** agent.

### Phase 1: Pre-Deployment Analysis

**Goal**: Analyze agent and assess production readiness

**Actions**:
1. Analyze agent source code and dependencies
2. Check for production configuration files
3. Verify build configuration (Gradle/Maven)
4. Assess resource requirements (CPU, memory)
5. Identify external dependencies (databases, APIs)
6. Validate health check endpoints exist

**Output**: Production readiness report with recommendations

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```yaml
Production Readiness Assessment:
  Agent Type: workflow_agent
  Dependencies:
    - PostgreSQL database (connection pooling: ✓)
    - External weather API (retry logic: ✓)
    - Kafka message queue (consumer group: ✓)
  Health Checks:
    - Liveness endpoint: ✓ /health/liveness
    - Readiness endpoint: ✓ /health/readiness
  Resource Requirements:
    - CPU: 500m-1000m (estimated)
    - Memory: 512Mi-1Gi (JVM heap + overhead)
  Recommendations:
    - Add Prometheus metrics endpoint
    - Implement structured logging
    - Configure connection pool limits
    - Add graceful shutdown handler
```

### Phase 2: Containerization

**Goal**: Create optimized production-ready Docker image

**Actions**:
1. Generate multi-stage Dockerfile
2. Configure JVM settings for containers
3. Add non-root user for security
4. Set up health check in container
5. Optimize layer caching
6. Configure build arguments for flexibility
7. Generate .dockerignore file

**Output**: Production Dockerfile with best practices

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```dockerfile
# Dockerfile
# Stage 1: Build
FROM gradle:8.5-jdk17 AS builder

WORKDIR /app

# Cache dependencies layer
COPY build.gradle.kts settings.gradle.kts ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon

# Build application
COPY src ./src
RUN gradle shadowJar --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Security: non-root user
RUN addgroup -g 1001 koog && \
    adduser -D -u 1001 -G koog koog

WORKDIR /app

# Copy artifact from builder
COPY --from=builder /app/build/libs/*-all.jar app.jar

# Set ownership
RUN chown -R koog:koog /app

# Switch to non-root user
USER koog

# JVM configuration for containers
ENV JAVA_OPTS="-XX:+UseG1GC \
    -XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:InitialRAMPercentage=50.0 \
    -XX:+ExitOnOutOfMemoryError \
    -Djava.security.egd=file:/dev/./urandom"

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health/liveness || exit 1

EXPOSE 8080

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### Phase 3: Kubernetes Manifest Generation

**Goal**: Generate production-ready Kubernetes manifests

**Actions**:
1. Create Deployment manifest with best practices
2. Generate Service configuration
3. Add ConfigMap for application settings
4. Configure resource requests and limits
5. Set up liveness and readiness probes
6. Add pod anti-affinity for HA
7. Generate Horizontal Pod Autoscaler
8. Create Ingress (if domain provided)

**Output**: Complete Kubernetes manifest set

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-agent
  namespace: koog-agents
  labels:
    app: sentiment-agent
    version: v1.0.0
    component: ai-agent
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deployments

  selector:
    matchLabels:
      app: sentiment-agent

  template:
    metadata:
      labels:
        app: sentiment-agent
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"

    spec:
      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

      # High availability: spread across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - sentiment-agent
              topologyKey: kubernetes.io/hostname

      # Graceful termination
      terminationGracePeriodSeconds: 60

      containers:
      - name: sentiment-agent
        image: myregistry/sentiment-agent:v1.0.0
        imagePullPolicy: IfNotPresent

        ports:
        - name: http
          containerPort: 8080
          protocol: TCP

        # Resource management
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: http
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /health/readiness
            port: http
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

        # Environment from ConfigMap
        envFrom:
        - configMapRef:
            name: sentiment-agent-config

        # Secrets
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: sentiment-agent-secrets
              key: openai-api-key

        # Volume mounts
        volumeMounts:
        - name: agent-data
          mountPath: /app/data

      volumes:
      - name: agent-data
        persistentVolumeClaim:
          claimName: sentiment-agent-pvc

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: sentiment-agent
  namespace: koog-agents
  labels:
    app: sentiment-agent
spec:
  type: ClusterIP
  selector:
    app: sentiment-agent
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  sessionAffinity: None

---
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sentiment-agent-hpa
  namespace: koog-agents
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sentiment-agent

  minReplicas: 3
  maxReplicas: 20

  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sentiment-agent-config
  namespace: koog-agents
data:
  LOG_LEVEL: "info"
  AGENT_TIMEOUT_MS: "30000"
  MAX_CONCURRENT_REQUESTS: "50"
  ENABLE_TRACING: "true"
  METRICS_ENABLED: "true"
  MODEL_NAME: "gpt-4"
  MODEL_TEMPERATURE: "0.7"
```

### Phase 4: Monitoring & Observability Setup

**Goal**: Configure comprehensive monitoring and observability

**Actions**:
1. Generate Prometheus metrics configuration
2. Create Grafana dashboard JSON
3. Add structured logging configuration
4. Set up OpenTelemetry tracing
5. Configure alert rules
6. Generate health check endpoints
7. Add correlation ID middleware

**Output**: Complete monitoring infrastructure

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```kotlin
// src/main/kotlin/monitoring/AgentMetrics.kt
package ai.koog.monitoring

import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer
import io.micrometer.core.instrument.Counter
import io.micrometer.prometheus.PrometheusConfig
import io.micrometer.prometheus.PrometheusMeterRegistry

class AgentMetrics(private val registry: MeterRegistry) {

    private val requestCounter = Counter.builder("agent_requests_total")
        .description("Total agent requests")
        .tag("agent", "sentiment_classifier")
        .register(registry)

    private val requestTimer = Timer.builder("agent_request_duration_seconds")
        .description("Request processing time")
        .tag("agent", "sentiment_classifier")
        .publishPercentiles(0.5, 0.95, 0.99)
        .register(registry)

    private val errorCounter = Counter.builder("agent_errors_total")
        .description("Total errors")
        .tag("agent", "sentiment_classifier")
        .register(registry)

    private val tokenCounter = Counter.builder("agent_tokens_consumed_total")
        .description("Total LLM tokens consumed")
        .tag("agent", "sentiment_classifier")
        .register(registry)

    fun recordRequest(durationMs: Long, success: Boolean, tokens: Int) {
        requestCounter.increment()
        requestTimer.record(durationMs, java.util.concurrent.TimeUnit.MILLISECONDS)
        tokenCounter.increment(tokens.toDouble())

        if (!success) {
            errorCounter.increment()
        }
    }
}

// Health check implementation
class HealthCheck(
    private val dataSource: DataSource,
    private val externalAPI: ExternalAPIClient
) {

    fun livenessProbe(): HealthStatus {
        return HealthStatus(
            status = "UP",
            checks = mapOf("application" to "running")
        )
    }

    fun readinessProbe(): HealthStatus {
        val dbHealthy = checkDatabase()
        val apiHealthy = checkExternalAPI()

        return if (dbHealthy && apiHealthy) {
            HealthStatus("UP", mapOf(
                "database" to "connected",
                "external_api" to "reachable"
            ))
        } else {
            HealthStatus("DOWN", mapOf(
                "database" to if (dbHealthy) "connected" else "disconnected",
                "external_api" to if (apiHealthy) "reachable" else "unreachable"
            ))
        }
    }

    private fun checkDatabase(): Boolean =
        try {
            dataSource.connection.use { it.isValid(3) }
        } catch (e: Exception) {
            false
        }

    private fun checkExternalAPI(): Boolean =
        try {
            externalAPI.ping()
            true
        } catch (e: Exception) {
            false
        }
}

data class HealthStatus(val status: String, val checks: Map<String, String>)
```

### Phase 5: Secrets Management Configuration

**Goal**: Set up secure secrets management

**Actions**:
1. Identify all sensitive configuration (API keys, passwords)
2. Generate Kubernetes Secret manifests (gitignored)
3. Configure External Secrets Operator (if selected)
4. Set up secret rotation policies
5. Add environment variable injection patterns
6. Generate secret creation scripts
7. Document secret management procedures

**Output**: Secrets infrastructure and documentation

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```bash
#!/bin/bash
# scripts/create-secrets.sh
# DO NOT commit this file with actual secrets

kubectl create secret generic sentiment-agent-secrets \
  --namespace koog-agents \
  --from-literal=openai-api-key="${OPENAI_API_KEY}" \
  --from-literal=db-password="${DATABASE_PASSWORD}" \
  --from-literal=api-token="${API_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secrets created successfully in koog-agents namespace"
```

```yaml
# k8s/external-secrets.yaml (if using External Secrets Operator)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: sentiment-agent-secrets
  namespace: koog-agents
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore

  target:
    name: sentiment-agent-secrets
    creationPolicy: Owner

  data:
  - secretKey: openai-api-key
    remoteRef:
      key: koog-agents/sentiment-agent
      property: openai_api_key

  - secretKey: db-password
    remoteRef:
      key: koog-agents/sentiment-agent
      property: database_password
```

### Phase 6: Deployment Execution

**Goal**: Execute production deployment with validation

**Actions**:
1. Build Docker image
2. Tag and push to container registry
3. Apply Kubernetes manifests
4. Monitor rollout status
5. Verify pod health and readiness
6. Run smoke tests
7. Monitor metrics and logs
8. Validate zero-downtime deployment

**Output**: Deployed application with validation report

**Agent**: koog-production-engineer (Haiku)

**Example Commands**:
```bash
# Build and push image
docker build -t myregistry/sentiment-agent:v1.0.0 .
docker push myregistry/sentiment-agent:v1.0.0

# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl create -f k8s/secrets.yaml  # Only if not using external secrets
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Monitor rollout
kubectl rollout status deployment/sentiment-agent -n koog-agents

# Verify deployment
kubectl get pods -n koog-agents -l app=sentiment-agent
kubectl logs -n koog-agents -l app=sentiment-agent --tail=50

# Run smoke tests
curl http://sentiment-agent.koog-agents.svc.cluster.local/health/readiness
```

### Phase 7: Post-Deployment Validation

**Goal**: Validate production deployment success

**Actions**:
1. Verify all pods are running and ready
2. Check health endpoints return healthy
3. Validate metrics are being collected
4. Test agent functionality with sample requests
5. Verify logs are properly structured
6. Check resource utilization
7. Validate auto-scaling triggers
8. Generate deployment report

**Output**: Deployment validation report

**Agent**: koog-production-engineer (Haiku)

**Example Output**:
```yaml
Deployment Validation Report:
  Deployment: sentiment-agent
  Namespace: koog-agents
  Status: SUCCESS

  Pods:
    - Ready: 3/3
    - Restarts: 0
    - Age: 5m
    - Resource Utilization:
        CPU: 300m / 500m (60%)
        Memory: 400Mi / 512Mi (78%)

  Health Checks:
    - Liveness: ✓ All pods passing
    - Readiness: ✓ All pods ready

  Metrics:
    - Prometheus scraping: ✓ Active
    - Request rate: 15 req/min
    - Error rate: 0%
    - P95 latency: 245ms

  Auto-Scaling:
    - HPA: ✓ Configured
    - Current replicas: 3
    - Target CPU: 70%
    - Target Memory: 80%

  Smoke Tests:
    - Health endpoint: ✓ 200 OK
    - Sample request: ✓ Success
    - Response time: 234ms

  Next Steps:
    - Monitor metrics for 24 hours
    - Set up alerting rules
    - Configure log aggregation
    - Plan capacity testing
```

## Execution Parameters

### Required Parameters
- `agent-path`: Path to agent project directory
- `registry`: Container registry URL (e.g., docker.io/username)
- `image-name`: Docker image name

### Optional Parameters
- `namespace`: Kubernetes namespace (default: koog-agents)
- `replicas`: Initial replica count (default: 3)
- `target`: Deployment platform (default: kubernetes)
- `strategy`: Deployment strategy (default: rolling)
- `monitoring`: Monitoring solution (default: prometheus)
- `secrets`: Secrets management (default: kubernetes)
- `enable-hpa`: Enable auto-scaling (default: true)
- `domain`: Public domain for ingress
- `tls-enabled`: Enable TLS (default: false)

## Success Criteria

### Deployment Success
- ✓ Zero-downtime deployment completed
- ✓ All pods healthy and ready
- ✓ Health checks passing
- ✓ Metrics being collected
- ✓ Logs properly formatted and flowing
- ✓ No errors in pod logs

### Production Readiness
- ✓ Resource limits configured
- ✓ Auto-scaling enabled and working
- ✓ Secrets properly managed
- ✓ Monitoring and alerting active
- ✓ High availability configured (3+ replicas)
- ✓ Graceful shutdown implemented

### Operational Excellence
- ✓ Rollback procedure documented
- ✓ Runbooks for common issues
- ✓ Alert thresholds configured
- ✓ SLOs defined and tracked
- ✓ Incident response plan ready

## Example Use Cases

### Use Case 1: Simple Agent to Kubernetes
```bash
/koog-production-deploy \
  --agent-path ./sentiment-agent \
  --target kubernetes \
  --registry docker.io/mycompany \
  --image-name sentiment-agent \
  --replicas 3
```

### Use Case 2: High-Availability Production Deployment
```bash
/koog-production-deploy \
  --agent-path ./order-processor \
  --target kubernetes \
  --strategy rolling \
  --replicas 5 \
  --enable-hpa \
  --monitoring prometheus \
  --secrets vault \
  --domain api.example.com \
  --tls-enabled
```

### Use Case 3: GCP Cloud Run Deployment
```bash
/koog-production-deploy \
  --agent-path ./chat-agent \
  --target cloud-run \
  --registry gcr.io/my-project \
  --monitoring datadog \
  --secrets gcp-secrets
```

## Integration with Other Plugins

### kotlin-koog-development
- Complements `koog-agent-scaffold` for complete lifecycle
- Works with `koog-test-scaffold` for pre-deployment testing

### devops-automation
- Integrates with CI/CD pipelines
- Shares infrastructure-as-code patterns

### monitoring-observability
- Uses standard monitoring patterns
- Integrates with centralized logging

## Troubleshooting

**Q: Pods stuck in CrashLoopBackOff**
A: Check pod logs with `kubectl logs`. Verify configuration, secrets, and dependencies. Ensure health check endpoints are accessible.

**Q: Deployment timeout during rollout**
A: Check resource availability. Verify image pull permissions. Review pod events with `kubectl describe pod`.

**Q: Health checks failing**
A: Verify health endpoints are implemented. Check readiness dependencies (database, APIs). Adjust probe timing if needed.

**Q: High memory usage**
A: Review JVM settings. Adjust `-XX:MaxRAMPercentage`. Consider increasing memory limits. Check for memory leaks.

**Q: Auto-scaling not triggering**
A: Verify metrics-server is installed. Check HPA status. Ensure resource requests are set. Review scaling thresholds.
