---
name: koog-production-deployment
description: Production deployment patterns, monitoring, scaling, and operations for Koog AI agents. Covers containerization, orchestration, observability, security, and reliability engineering. Use when deploying agents to production, implementing monitoring and alerting, scaling agent systems, ensuring high availability, or managing agent operations.
---

# Koog Production Deployment

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Deploying Koog agents to production environments
- Implementing monitoring and observability for agents
- Scaling agent systems for high throughput
- Ensuring high availability and fault tolerance
- Securing agent deployments and API keys
- Managing agent configuration across environments
- Implementing cost optimization strategies
- Debugging production agent issues
- Setting up CI/CD pipelines for agents
- Managing multi-region agent deployments

## Core Concepts

### Deployment Architecture Patterns

#### Pattern 1: Spring Boot Microservice

```kotlin
@SpringBootApplication
@EnableScheduling
class AgentServiceApplication

@Configuration
class AgentConfiguration {

    @Bean
    fun llmProvider(
        @Value("\${openai.api.key}") apiKey: String,
        @Value("\${openai.model}") model: String
    ): LLMProvider {
        return OpenAiLLMClient(
            apiKey = apiKey,
            modelId = model,
            timeout = 30.seconds
        )
    }

    @Bean
    fun customerSupportAgent(llmProvider: LLMProvider): Agent {
        return agent("customer_support") {
            this.llmProvider = llmProvider

            instruction("""
                You are a customer support agent. Be helpful, concise, and professional.
                Use tools to access customer data and resolve issues.
            """)

            tool("get_customer_info") {
                implementation = CustomerInfoTool()
            }

            tool("check_order_status") {
                implementation = OrderStatusTool()
            }

            tool("create_ticket") {
                implementation = TicketCreationTool()
            }

            features.add(OpenTelemetryTracing())
            features.add(PrometheusMetrics())
        }
    }

    @Bean
    fun agentMetrics(): MeterRegistry {
        return SimpleMeterRegistry()
    }
}

@RestController
@RequestMapping("/api/v1/agent")
class AgentController(
    private val agent: Agent,
    private val meterRegistry: MeterRegistry
) {

    private val requestCounter = meterRegistry.counter("agent.requests.total")
    private val errorCounter = meterRegistry.counter("agent.errors.total")
    private val latencyTimer = meterRegistry.timer("agent.request.duration")

    @PostMapping("/chat")
    fun chat(@RequestBody request: ChatRequest): ResponseEntity<ChatResponse> {
        requestCounter.increment()

        return latencyTimer.recordCallable {
            try {
                val result = agent.execute(request.message)
                ResponseEntity.ok(ChatResponse(result))
            } catch (e: Exception) {
                errorCounter.increment()
                ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(ChatResponse(error = e.message))
            }
        }!!
    }

    @GetMapping("/health")
    fun health(): ResponseEntity<Map<String, Any>> {
        return ResponseEntity.ok(mapOf(
            "status" to "UP",
            "agent" to "operational",
            "timestamp" to System.currentTimeMillis()
        ))
    }
}
```

#### Pattern 2: Ktor Async Service

```kotlin
fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
        })
    }

    install(CallLogging) {
        level = Level.INFO
        format { call ->
            val status = call.response.status()
            val method = call.request.httpMethod.value
            val path = call.request.path()
            val duration = call.processingTimeMillis()
            "$method $path - $status (${duration}ms)"
        }
    }

    install(StatusPages) {
        exception<Throwable> { call, cause ->
            call.application.log.error("Unhandled exception", cause)
            call.respond(
                HttpStatusCode.InternalServerError,
                mapOf("error" to (cause.message ?: "Unknown error"))
            )
        }
    }

    val agent = createAgent()

    routing {
        post("/api/v1/agent/chat") {
            val request = call.receive<ChatRequest>()

            val result = withContext(Dispatchers.IO) {
                agent.execute(request.message)
            }

            call.respond(ChatResponse(result))
        }

        get("/health") {
            call.respond(mapOf(
                "status" to "UP",
                "version" to "1.0.0"
            ))
        }

        get("/metrics") {
            val metrics = collectMetrics()
            call.respond(metrics)
        }
    }
}

fun createAgent(): Agent {
    val config = loadConfiguration()

    return agent("async_agent") {
        llmProvider = OpenAiLLMClient(
            apiKey = config.openAiKey,
            modelId = config.model
        )

        instruction("Process requests efficiently")

        // Async tool execution
        tool("async_database_query") {
            implementation = AsyncDatabaseTool()
            timeout = 5.seconds
        }

        features.add(RequestTracing())
        features.add(CircuitBreaker(
            failureThreshold = 5,
            resetTimeout = 60.seconds
        ))
    }
}
```

### Containerization with Docker

#### Production Dockerfile

```dockerfile
# Multi-stage build for minimal image size
FROM gradle:8-jdk17 AS build

WORKDIR /app

# Copy dependency definitions
COPY build.gradle.kts settings.gradle.kts ./
COPY gradle ./gradle

# Download dependencies (cached layer)
RUN gradle dependencies --no-daemon

# Copy source code
COPY src ./src

# Build application
RUN gradle clean build -x test --no-daemon

# Production image
FROM eclipse-temurin:17-jre-alpine

# Security: Run as non-root user
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

WORKDIR /app

# Copy JAR from build stage
COPY --from=build /app/build/libs/*.jar app.jar

# Security: Set ownership
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# JVM optimization for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"

# Run application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

#### Docker Compose for Local Development

```yaml
version: '3.8'

services:
  agent-service:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=development
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/agents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=agents
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Kubernetes Deployment

#### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: koog-agent-service
  labels:
    app: koog-agent
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: koog-agent
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: koog-agent
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      containers:
      - name: agent
        image: myregistry/koog-agent:1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-credentials
              key: openai-api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: agent-config

---
apiVersion: v1
kind: Service
metadata:
  name: koog-agent-service
  labels:
    app: koog-agent
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: koog-agent

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: koog-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: koog-agent-service
  minReplicas: 3
  maxReplicas: 10
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
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

### Observability and Monitoring

#### Structured Logging

```kotlin
import mu.KotlinLogging
import net.logstash.logback.argument.StructuredArguments.*

private val logger = KotlinLogging.logger {}

class ObservableAgent(
    private val agent: Agent,
    private val requestId: String
) {

    suspend fun execute(input: String): String {
        val startTime = System.currentTimeMillis()

        logger.info(
            "Agent request started",
            kv("request_id", requestId),
            kv("agent", agent.name),
            kv("input_length", input.length)
        )

        return try {
            val result = agent.execute(input)

            val duration = System.currentTimeMillis() - startTime

            logger.info(
                "Agent request completed",
                kv("request_id", requestId),
                kv("agent", agent.name),
                kv("duration_ms", duration),
                kv("output_length", result.length),
                kv("status", "success")
            )

            result
        } catch (e: Exception) {
            val duration = System.currentTimeMillis() - startTime

            logger.error(
                "Agent request failed",
                kv("request_id", requestId),
                kv("agent", agent.name),
                kv("duration_ms", duration),
                kv("error_type", e::class.simpleName),
                kv("error_message", e.message),
                kv("status", "error"),
                e
            )

            throw e
        }
    }
}
```

#### OpenTelemetry Tracing

```kotlin
import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.StatusCode
import io.opentelemetry.context.Context

class TracedAgentExecutor(private val agent: Agent) {

    private val tracer = GlobalOpenTelemetry.getTracer("koog-agent")

    suspend fun execute(input: String): String {
        val span = tracer.spanBuilder("agent.execute")
            .setAttribute("agent.name", agent.name)
            .setAttribute("input.length", input.length.toLong())
            .startSpan()

        return try {
            Context.current().with(span).makeCurrent().use {
                val result = executeWithTracing(input, span)

                span.setAttribute("output.length", result.length.toLong())
                span.setStatus(StatusCode.OK)

                result
            }
        } catch (e: Exception) {
            span.recordException(e)
            span.setStatus(StatusCode.ERROR, e.message ?: "Unknown error")
            throw e
        } finally {
            span.end()
        }
    }

    private suspend fun executeWithTracing(input: String, parentSpan: Span): String {
        // Tool call tracing
        val toolSpan = tracer.spanBuilder("agent.tool_execution")
            .setParent(Context.current().with(parentSpan))
            .startSpan()

        return try {
            agent.execute(input)
        } finally {
            toolSpan.end()
        }
    }
}
```

#### Prometheus Metrics

```kotlin
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer
import java.util.concurrent.atomic.AtomicLong

class MetricsCollector(private val registry: MeterRegistry) {

    private val requestCounter = registry.counter("agent.requests.total")
    private val successCounter = registry.counter("agent.requests.success")
    private val errorCounter = registry.counter("agent.requests.error")
    private val tokenCounter = registry.counter("agent.tokens.total")
    private val requestTimer = registry.timer("agent.request.duration")

    private val activeRequests = AtomicLong(0)

    init {
        registry.gauge("agent.requests.active", activeRequests)
    }

    suspend fun <T> measureRequest(
        agentName: String,
        block: suspend () -> T
    ): T {
        requestCounter.increment()
        activeRequests.incrementAndGet()

        val sample = Timer.start(registry)

        return try {
            val result = block()
            successCounter.increment()
            result
        } catch (e: Exception) {
            errorCounter.increment()
            throw e
        } finally {
            sample.stop(requestTimer)
            activeRequests.decrementAndGet()
        }
    }

    fun recordTokenUsage(tokens: Int) {
        tokenCounter.increment(tokens.toDouble())
    }
}
```

### Configuration Management

#### Environment-Based Configuration

```kotlin
@ConfigurationProperties(prefix = "agent")
data class AgentConfiguration(
    val llm: LLMConfig,
    val tools: ToolsConfig,
    val features: FeaturesConfig,
    val limits: LimitsConfig
)

data class LLMConfig(
    val provider: String,
    val model: String,
    val apiKey: String,
    val timeout: Duration,
    val maxRetries: Int
)

data class ToolsConfig(
    val database: DatabaseConfig,
    val cache: CacheConfig,
    val externalApis: Map<String, ApiConfig>
)

data class FeaturesConfig(
    val tracing: Boolean,
    val metrics: Boolean,
    val historyCompression: Boolean,
    val contentModeration: Boolean
)

data class LimitsConfig(
    val maxConcurrentRequests: Int,
    val maxTokensPerRequest: Int,
    val requestTimeout: Duration,
    val rateLimitPerMinute: Int
)

// application.yml
```

```yaml
agent:
  llm:
    provider: openai
    model: gpt-4-turbo
    api-key: ${OPENAI_API_KEY}
    timeout: 30s
    max-retries: 3

  tools:
    database:
      url: ${DATABASE_URL}
      max-connections: 20
      timeout: 5s
    cache:
      url: ${REDIS_URL}
      ttl: 5m

  features:
    tracing: true
    metrics: true
    history-compression: true
    content-moderation: true

  limits:
    max-concurrent-requests: 100
    max-tokens-per-request: 4000
    request-timeout: 60s
    rate-limit-per-minute: 60
```

### Security Patterns

#### API Key Management

```kotlin
import com.amazonaws.services.secretsmanager.AWSSecretsManager
import com.amazonaws.services.secretsmanager.model.GetSecretValueRequest

class SecretManager(private val secretsManager: AWSSecretsManager) {

    fun getOpenAiApiKey(): String {
        return getSecret("production/openai/api-key")
    }

    fun getDatabaseCredentials(): DatabaseCredentials {
        val secret = getSecret("production/database/credentials")
        return Json.decodeFromString(secret)
    }

    private fun getSecret(secretName: String): String {
        val request = GetSecretValueRequest()
            .withSecretId(secretName)

        val result = secretsManager.getSecretValue(request)
        return result.secretString
    }
}

// Usage in application
@Configuration
class SecureAgentConfiguration(
    private val secretManager: SecretManager
) {

    @Bean
    fun llmProvider(): LLMProvider {
        val apiKey = secretManager.getOpenAiApiKey()

        return OpenAiLLMClient(
            apiKey = apiKey,
            modelId = "gpt-4-turbo"
        )
    }
}
```

#### Content Security

```kotlin
class SecureAgent(
    private val agent: Agent,
    private val moderator: ContentModerator
) {

    suspend fun execute(input: String): String {
        // Input validation
        validateInput(input)

        // Content moderation
        val inputModeration = moderator.moderate(input)
        if (inputModeration.isHarmful) {
            throw SecurityException("Input contains harmful content: ${inputModeration.categories}")
        }

        // Execute agent
        val output = agent.execute(input)

        // Output moderation
        val outputModeration = moderator.moderate(output)
        if (outputModeration.isHarmful) {
            logger.warn("Agent generated harmful content, filtering")
            return "I apologize, but I cannot provide that information."
        }

        return output
    }

    private fun validateInput(input: String) {
        require(input.length <= 10000) { "Input exceeds maximum length" }
        require(input.isNotBlank()) { "Input cannot be blank" }
    }
}
```

### Reliability Patterns

#### Circuit Breaker

```kotlin
class CircuitBreakerAgent(
    private val agent: Agent,
    private val failureThreshold: Int = 5,
    private val resetTimeout: Duration = 60.seconds
) {
    private enum class State { CLOSED, OPEN, HALF_OPEN }

    private var state: State = State.CLOSED
    private var failureCount = 0
    private var lastFailureTime: Instant? = null

    suspend fun execute(input: String): String {
        when (state) {
            State.OPEN -> {
                if (shouldAttemptReset()) {
                    state = State.HALF_OPEN
                } else {
                    throw CircuitBreakerOpenException("Circuit breaker is OPEN")
                }
            }
            State.HALF_OPEN, State.CLOSED -> {}
        }

        return try {
            val result = agent.execute(input)
            onSuccess()
            result
        } catch (e: Exception) {
            onFailure()
            throw e
        }
    }

    private fun onSuccess() {
        failureCount = 0
        state = State.CLOSED
    }

    private fun onFailure() {
        failureCount++
        lastFailureTime = Instant.now()

        if (failureCount >= failureThreshold) {
            state = State.OPEN
            logger.warn("Circuit breaker opened after $failureCount failures")
        }
    }

    private fun shouldAttemptReset(): Boolean {
        val lastFailure = lastFailureTime ?: return false
        return Duration.between(lastFailure, Instant.now()) >= resetTimeout
    }
}
```

#### Retry with Exponential Backoff

```kotlin
class RetryableAgent(
    private val agent: Agent,
    private val maxRetries: Int = 3,
    private val initialDelay: Duration = 1.seconds
) {

    suspend fun execute(input: String): String {
        var lastException: Exception? = null
        var delay = initialDelay

        repeat(maxRetries) { attempt ->
            try {
                return agent.execute(input)
            } catch (e: Exception) {
                lastException = e
                logger.warn("Agent execution failed (attempt ${attempt + 1}/$maxRetries)", e)

                if (attempt < maxRetries - 1) {
                    delay(delay.toMillis())
                    delay *= 2 // Exponential backoff
                }
            }
        }

        throw RetryExhaustedException("Failed after $maxRetries attempts", lastException)
    }
}
```

## Patterns and Best Practices

### Pattern 1: Blue-Green Deployment

```bash
# Deploy new version (green)
kubectl apply -f deployment-v2.yaml

# Wait for new version to be ready
kubectl rollout status deployment/koog-agent-v2

# Switch traffic to new version
kubectl patch service koog-agent-service -p '{"spec":{"selector":{"version":"v2"}}}'

# Monitor for issues
# If problems detected, rollback:
kubectl patch service koog-agent-service -p '{"spec":{"selector":{"version":"v1"}}}'
```

### Pattern 2: Canary Deployment

```yaml
# Istio VirtualService for canary
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: koog-agent
spec:
  hosts:
  - koog-agent
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: koog-agent
        subset: v2
  - route:
    - destination:
        host: koog-agent
        subset: v1
      weight: 90
    - destination:
        host: koog-agent
        subset: v2
      weight: 10
```

### Pattern 3: Cost Optimization

```kotlin
class CostOptimizedAgent(
    private val expensiveModel: LLMProvider,
    private val cheapModel: LLMProvider,
    private val classifier: ComplexityClassifier
) {

    suspend fun execute(input: String): String {
        val complexity = classifier.classify(input)

        val provider = when (complexity) {
            Complexity.LOW -> cheapModel // Use cheaper model
            Complexity.HIGH -> expensiveModel // Use expensive model only when needed
        }

        return provider.execute(input)
    }
}
```

## Common Pitfalls

### Pitfall 1: Missing Health Checks
Always implement proper health checks:

```kotlin
@GetMapping("/health")
fun health(): ResponseEntity<HealthStatus> {
    val checks = mapOf(
        "database" to checkDatabase(),
        "llm_provider" to checkLLMProvider(),
        "cache" to checkCache()
    )

    val isHealthy = checks.all { it.value }

    return if (isHealthy) {
        ResponseEntity.ok(HealthStatus("UP", checks))
    } else {
        ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
            .body(HealthStatus("DOWN", checks))
    }
}
```

### Pitfall 2: Insufficient Resource Limits
Always set resource limits:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "2000m"
    memory: "4Gi"
```

### Pitfall 3: No Request Timeouts
Implement timeouts everywhere:

```kotlin
val result = withTimeout(30.seconds) {
    agent.execute(input)
}
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-performance-optimization](/home/user/agents/plugins/kotlin-koog-development/skills/koog-performance-optimization/SKILL.md)
- [Koog Production Guide](https://docs.koog.ai/production/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [OpenTelemetry Documentation](https://opentelemetry.io/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
