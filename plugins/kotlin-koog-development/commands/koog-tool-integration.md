---
name: koog-tool-integration
description: Expert command for designing and implementing custom tool integrations for Koog agents including REST/GraphQL API wrappers, database connectors, message queue integration, MCP servers, and multi-system orchestration with resilience patterns.
---

# Koog Tool Integration Command

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Purpose

Provides a comprehensive workflow for designing and implementing custom tool integrations for Koog AI agents. Handles API client generation, database connectors, message queue integration, resilience patterns (circuit breakers, retries), and multi-system orchestration with proper error handling and monitoring.

## Quick Start

```bash
/koog-tool-integration
```

Follow the interactive prompts to design your tool integration.

## Configuration Options

### Integration Type
```bash
--type rest-api         # REST API client integration
--type graphql          # GraphQL API integration
--type database         # Database connector (SQL/NoSQL)
--type message-queue    # Kafka, RabbitMQ, Redis integration
--type mcp              # Model Context Protocol server
--type websocket        # WebSocket real-time integration
--type grpc             # gRPC service integration
--type composite        # Multi-system orchestration
```

### API Configuration
```bash
--api-url <url>                  # Base URL for API
--auth-type none|apikey|oauth2|jwt  # Authentication method
--client-library okhttp|ktor     # HTTP client library (default: okhttp)
--retry-strategy exponential     # Retry strategy (default: exponential)
--circuit-breaker                # Enable circuit breaker (default: true)
--rate-limit <rps>               # Client-side rate limiting
```

### Database Configuration
```bash
--db-type postgresql|mysql|mongodb|redis  # Database type
--pool-size <num>                # Connection pool size (default: 10)
--timeout <ms>                   # Connection timeout (default: 30000)
--transaction-support            # Enable transaction support (default: true)
--migration-tool flyway|liquibase  # Migration tool (optional)
```

### Message Queue Configuration
```bash
--queue-type kafka|rabbitmq|redis  # Message queue type
--consumer-group <name>          # Consumer group ID
--partition-strategy <strategy>  # Kafka partition strategy
--serialization json|avro|proto  # Message serialization format
```

### Resilience Patterns
```bash
--enable-retries                 # Enable retry logic (default: true)
--max-retries <num>              # Maximum retry attempts (default: 3)
--enable-circuit-breaker         # Enable circuit breaker (default: true)
--circuit-threshold <num>        # Failure threshold (default: 5)
--enable-timeout                 # Enable request timeouts (default: true)
--timeout-ms <ms>                # Request timeout (default: 30000)
--enable-bulkhead                # Enable bulkhead pattern (default: false)
```

### Project Configuration
```bash
--agent-path <path>              # Path to agent project (required)
--tool-name <name>               # Tool name (required)
--output-path <path>             # Output path for tool code (default: src/main/kotlin/tools)
--include-tests                  # Generate test suite (default: true)
--include-mocks                  # Generate mock implementations (default: true)
--async-execution                # Use coroutines for async (default: true)
```

## Execution Workflow

This command orchestrates tool integration design and implementation using the **koog-integration-architect** agent.

### Phase 1: Integration Requirements Analysis

**Goal**: Analyze integration requirements and design tool architecture

**Actions**:
1. Analyze target system API/protocol documentation
2. Identify authentication and authorization requirements
3. Assess data models and serialization needs
4. Determine error scenarios and handling strategies
5. Design tool interface (parameters, return types)
6. Plan resilience patterns (retries, circuit breakers)
7. Identify monitoring and observability needs

**Output**: Integration architecture document

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```yaml
Integration Architecture:
  Tool Name: weather-api-client
  Integration Type: REST API
  Target System: OpenWeatherMap API v2.5

  Authentication:
    Type: API Key
    Location: Query parameter
    Key Name: appid

  Endpoints:
    - GET /weather (current weather)
    - GET /forecast (5-day forecast)

  Data Models:
    - WeatherResponse: temperature, condition, humidity
    - ForecastResponse: list of forecasts

  Error Scenarios:
    - Network failures → Retry with exponential backoff
    - Rate limiting (429) → Backoff and retry
    - Invalid API key (401) → Fail fast, no retry
    - Service unavailable (503) → Circuit breaker

  Resilience Patterns:
    - Retry: Exponential backoff, max 3 attempts
    - Circuit Breaker: Open after 5 failures, reset after 1 min
    - Timeout: 30s connection, 60s read

  Monitoring:
    - Request duration histogram
    - Success/failure counters
    - Circuit breaker state gauge
    - API response status codes
```

### Phase 2: Tool Interface Design

**Goal**: Design type-safe tool interface with clear contracts

**Actions**:
1. Define tool annotation and metadata
2. Design parameter schema with validation
3. Define return type structures
4. Create domain model classes
5. Design error hierarchy
6. Document tool behavior for LLMs
7. Add parameter examples and constraints

**Output**: Tool interface definitions and data models

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```kotlin
// src/main/kotlin/tools/WeatherTool.kt
package ai.koog.tools.weather

import ai.koog.annotations.Tool
import ai.koog.annotations.Parameter
import com.fasterxml.jackson.annotation.JsonProperty

/**
 * Weather API integration tool for fetching current weather and forecasts.
 * Uses OpenWeatherMap API v2.5 with API key authentication.
 */
class WeatherTool(
    private val apiKey: String,
    private val baseUrl: String = "https://api.openweathermap.org/data/2.5"
) {

    @Tool(
        name = "get_current_weather",
        description = """
            Get the current weather conditions for a specific city.
            Returns temperature, weather condition, and humidity.
            Use when the agent needs real-time weather data.
        """
    )
    fun getCurrentWeather(
        @Parameter(
            name = "city",
            description = "City name (e.g., 'London', 'New York')",
            required = true,
            example = "London"
        )
        city: String,

        @Parameter(
            name = "units",
            description = "Temperature units: 'metric' (Celsius) or 'imperial' (Fahrenheit)",
            required = false,
            defaultValue = "metric",
            validValues = ["metric", "imperial"]
        )
        units: String = "metric"
    ): WeatherResponse {
        require(city.isNotBlank()) { "City name cannot be blank" }
        require(units in setOf("metric", "imperial")) {
            "Units must be 'metric' or 'imperial'"
        }

        // Implementation in Phase 3
        TODO("Implementation in Phase 3")
    }

    @Tool(
        name = "get_forecast",
        description = """
            Get 5-day weather forecast for a city with 3-hour intervals.
            Returns list of forecast entries with timestamps.
        """
    )
    fun getForecast(
        @Parameter(
            name = "city",
            description = "City name",
            required = true
        )
        city: String,

        @Parameter(
            name = "days",
            description = "Number of forecast days (1-5)",
            required = false,
            defaultValue = "5"
        )
        days: Int = 5
    ): ForecastResponse {
        require(days in 1..5) { "Days must be between 1 and 5" }

        TODO("Implementation in Phase 3")
    }
}

// Domain models
data class WeatherResponse(
    val city: String,
    val temperature: Double,
    val feelsLike: Double,
    val condition: String,
    val description: String,
    val humidity: Int,
    val pressure: Int,
    val windSpeed: Double,
    val timestamp: Long
)

data class ForecastResponse(
    val city: String,
    val forecasts: List<ForecastEntry>
)

data class ForecastEntry(
    val timestamp: Long,
    val temperature: Double,
    val condition: String,
    val description: String,
    val precipitationProbability: Double
)

// Error hierarchy
sealed class WeatherAPIException(message: String, cause: Throwable? = null) :
    Exception(message, cause) {

    class NetworkError(message: String, cause: Throwable? = null) :
        WeatherAPIException(message, cause)

    class AuthenticationError(message: String) :
        WeatherAPIException(message)

    class RateLimitError(message: String, val retryAfter: Int?) :
        WeatherAPIException(message)

    class InvalidRequest(message: String) :
        WeatherAPIException(message)

    class ServiceUnavailable(message: String) :
        WeatherAPIException(message)
}
```

### Phase 3: Resilient Client Implementation

**Goal**: Implement robust client with resilience patterns

**Actions**:
1. Implement HTTP client with connection pooling
2. Add authentication mechanism
3. Implement retry logic with exponential backoff
4. Add circuit breaker pattern
5. Implement request/response serialization
6. Add timeout configuration
7. Implement error classification and handling
8. Add request logging and metrics

**Output**: Production-ready client implementation

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```kotlin
// src/main/kotlin/tools/weather/WeatherAPIClient.kt
package ai.koog.tools.weather

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.HttpUrl.Companion.toHttpUrl
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import kotlinx.coroutines.delay
import java.time.Duration
import java.time.Instant
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger
import java.util.concurrent.atomic.AtomicReference

class WeatherAPIClient(
    private val apiKey: String,
    private val baseUrl: String,
    private val retryConfig: RetryConfig = RetryConfig(),
    private val circuitBreakerConfig: CircuitBreakerConfig = CircuitBreakerConfig()
) {
    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .connectionPool(okhttp3.ConnectionPool(
            maxIdleConnections = 10,
            keepAliveDuration = 5,
            TimeUnit.MINUTES
        ))
        .build()

    private val mapper = jacksonObjectMapper()
    private val circuitBreaker = CircuitBreaker(circuitBreakerConfig)

    suspend fun getCurrentWeather(city: String, units: String): WeatherResponse {
        return executeWithResilience {
            val url = "$baseUrl/weather"
                .toHttpUrl()
                .newBuilder()
                .addQueryParameter("q", city)
                .addQueryParameter("units", units)
                .addQueryParameter("appid", apiKey)
                .build()

            val request = Request.Builder()
                .url(url)
                .get()
                .header("User-Agent", "KoogAgent/1.0")
                .build()

            httpClient.newCall(request).execute().use { response ->
                when (response.code) {
                    200 -> {
                        val body = response.body?.string()
                            ?: throw WeatherAPIException.InvalidRequest("Empty response")
                        parseWeatherResponse(body)
                    }
                    401 -> throw WeatherAPIException.AuthenticationError("Invalid API key")
                    404 -> throw WeatherAPIException.InvalidRequest("City not found: $city")
                    429 -> {
                        val retryAfter = response.header("Retry-After")?.toIntOrNull()
                        throw WeatherAPIException.RateLimitError(
                            "Rate limit exceeded",
                            retryAfter
                        )
                    }
                    in 500..599 -> throw WeatherAPIException.ServiceUnavailable(
                        "Service error: ${response.code}"
                    )
                    else -> throw WeatherAPIException.InvalidRequest(
                        "Unexpected status: ${response.code}"
                    )
                }
            }
        }
    }

    private suspend fun <T> executeWithResilience(block: suspend () -> T): T {
        // Check circuit breaker
        if (circuitBreaker.isOpen()) {
            throw WeatherAPIException.ServiceUnavailable("Circuit breaker is open")
        }

        var lastException: Exception? = null
        var attempt = 0

        while (attempt <= retryConfig.maxAttempts) {
            try {
                val result = block()
                circuitBreaker.recordSuccess()
                return result

            } catch (e: Exception) {
                lastException = e
                circuitBreaker.recordFailure()

                // Don't retry on non-transient errors
                if (!isTransientError(e)) {
                    throw e
                }

                attempt++
                if (attempt <= retryConfig.maxAttempts) {
                    val backoffMs = calculateBackoff(attempt, retryConfig)
                    delay(backoffMs)
                }
            }
        }

        throw lastException ?: WeatherAPIException.NetworkError("Unknown error")
    }

    private fun isTransientError(e: Exception): Boolean = when (e) {
        is WeatherAPIException.NetworkError -> true
        is WeatherAPIException.ServiceUnavailable -> true
        is WeatherAPIException.RateLimitError -> true
        is WeatherAPIException.AuthenticationError -> false
        is WeatherAPIException.InvalidRequest -> false
        else -> false
    }

    private fun calculateBackoff(attempt: Int, config: RetryConfig): Long {
        val exponentialDelay = config.initialDelayMs * (1 shl (attempt - 1))
        val jitter = (0..config.jitterMs).random()
        return (exponentialDelay + jitter).coerceAtMost(config.maxDelayMs)
    }

    private fun parseWeatherResponse(json: String): WeatherResponse {
        val root = mapper.readTree(json)

        return WeatherResponse(
            city = root.get("name").asText(),
            temperature = root.get("main").get("temp").asDouble(),
            feelsLike = root.get("main").get("feels_like").asDouble(),
            condition = root.get("weather").get(0).get("main").asText(),
            description = root.get("weather").get(0).get("description").asText(),
            humidity = root.get("main").get("humidity").asInt(),
            pressure = root.get("main").get("pressure").asInt(),
            windSpeed = root.get("wind").get("speed").asDouble(),
            timestamp = root.get("dt").asLong()
        )
    }
}

// Circuit Breaker implementation
class CircuitBreaker(private val config: CircuitBreakerConfig) {
    private val failureCount = AtomicInteger(0)
    private val state = AtomicReference(State.CLOSED)
    private val lastFailureTime = AtomicReference<Instant?>(null)

    enum class State { CLOSED, OPEN, HALF_OPEN }

    fun isOpen(): Boolean {
        if (state.get() == State.OPEN) {
            val lastFailure = lastFailureTime.get()
            if (lastFailure != null &&
                Duration.between(lastFailure, Instant.now()) > config.resetTimeout) {
                state.set(State.HALF_OPEN)
                return false
            }
            return true
        }
        return false
    }

    fun recordSuccess() {
        failureCount.set(0)
        state.set(State.CLOSED)
    }

    fun recordFailure() {
        val failures = failureCount.incrementAndGet()
        lastFailureTime.set(Instant.now())

        if (failures >= config.failureThreshold) {
            state.set(State.OPEN)
        }
    }
}

// Configuration classes
data class RetryConfig(
    val maxAttempts: Int = 3,
    val initialDelayMs: Long = 100,
    val maxDelayMs: Long = 5000,
    val jitterMs: Long = 100
)

data class CircuitBreakerConfig(
    val failureThreshold: Int = 5,
    val resetTimeout: Duration = Duration.ofMinutes(1)
)
```

### Phase 4: Database Connector Implementation

**Goal**: Create database tool with connection pooling and transactions

**Actions**:
1. Set up HikariCP connection pool
2. Implement parameterized query execution
3. Add transaction support
4. Create type-safe result mapping
5. Implement connection health checks
6. Add query timeout configuration
7. Generate migration scripts (if selected)

**Output**: Database connector with connection pooling

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```kotlin
// src/main/kotlin/tools/database/DatabaseTool.kt
package ai.koog.tools.database

import ai.koog.annotations.Tool
import ai.koog.annotations.Parameter
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import java.sql.ResultSet
import javax.sql.DataSource

class DatabaseTool(
    jdbcUrl: String,
    username: String,
    password: String,
    poolConfig: PoolConfig = PoolConfig()
) {
    private val dataSource: HikariDataSource

    init {
        val config = HikariConfig().apply {
            this.jdbcUrl = jdbcUrl
            this.username = username
            this.password = password
            maximumPoolSize = poolConfig.maxPoolSize
            minimumIdle = poolConfig.minIdle
            connectionTimeout = poolConfig.connectionTimeoutMs
            idleTimeout = poolConfig.idleTimeoutMs
            maxLifetime = poolConfig.maxLifetimeMs
            leakDetectionThreshold = poolConfig.leakDetectionMs
            poolName = "KoogAgentPool"
        }
        dataSource = HikariDataSource(config)
    }

    @Tool(
        name = "query_database",
        description = """
            Execute a safe parameterized SQL SELECT query.
            Returns results as a list of row maps.
            Only SELECT queries are allowed for safety.
        """
    )
    fun query(
        @Parameter(
            name = "sql",
            description = "SQL SELECT query with ? placeholders",
            required = true,
            example = "SELECT * FROM users WHERE age > ?"
        )
        sql: String,

        @Parameter(
            name = "parameters",
            description = "Parameter values for placeholders",
            required = false
        )
        parameters: List<Any> = emptyList()
    ): QueryResult {
        // Validate read-only
        require(sql.trim().uppercase().startsWith("SELECT")) {
            "Only SELECT queries allowed. Use execute_transaction for modifications."
        }

        return dataSource.connection.use { conn ->
            conn.prepareStatement(sql).use { stmt ->
                // Bind parameters
                parameters.forEachIndexed { index, value ->
                    stmt.setObject(index + 1, value)
                }

                stmt.executeQuery().use { rs ->
                    QueryResult(
                        columns = getColumnNames(rs),
                        rows = extractRows(rs),
                        rowCount = extractRows(rs).size
                    )
                }
            }
        }
    }

    @Tool(
        name = "execute_transaction",
        description = """
            Execute multiple SQL statements in a single transaction.
            Automatically rolls back on any failure.
        """
    )
    fun executeTransaction(
        @Parameter(
            name = "statements",
            description = "List of SQL statements with parameters",
            required = true
        )
        statements: List<SqlStatement>
    ): TransactionResult {
        dataSource.connection.use { conn ->
            conn.autoCommit = false

            try {
                val results = statements.map { stmt ->
                    conn.prepareStatement(stmt.sql).use { ps ->
                        stmt.parameters.forEachIndexed { index, value ->
                            ps.setObject(index + 1, value)
                        }
                        ps.executeUpdate()
                    }
                }

                conn.commit()
                return TransactionResult(
                    success = true,
                    affectedRows = results,
                    error = null
                )

            } catch (e: Exception) {
                conn.rollback()
                return TransactionResult(
                    success = false,
                    affectedRows = emptyList(),
                    error = e.message
                )
            }
        }
    }

    private fun getColumnNames(rs: ResultSet): List<String> {
        val metadata = rs.metaData
        return (1..metadata.columnCount).map { metadata.getColumnName(it) }
    }

    private fun extractRows(rs: ResultSet): List<Map<String, Any?>> {
        val rows = mutableListOf<Map<String, Any?>>()
        val columns = getColumnNames(rs)

        while (rs.next()) {
            val row = columns.associateWith { rs.getObject(it) }
            rows.add(row)
        }

        return rows
    }

    fun close() {
        dataSource.close()
    }
}

data class PoolConfig(
    val maxPoolSize: Int = 10,
    val minIdle: Int = 2,
    val connectionTimeoutMs: Long = 30000,
    val idleTimeoutMs: Long = 600000,
    val maxLifetimeMs: Long = 1800000,
    val leakDetectionMs: Long = 60000
)

data class QueryResult(
    val columns: List<String>,
    val rows: List<Map<String, Any?>>,
    val rowCount: Int
)

data class SqlStatement(
    val sql: String,
    val parameters: List<Any> = emptyList()
)

data class TransactionResult(
    val success: Boolean,
    val affectedRows: List<Int>,
    val error: String?
)
```

### Phase 5: Multi-System Orchestration

**Goal**: Create orchestration tool coordinating multiple systems

**Actions**:
1. Design saga pattern for distributed transactions
2. Implement compensation logic for rollbacks
3. Create parallel tool execution utilities
4. Add timeout and cancellation support
5. Implement event-driven coordination
6. Add state persistence for long-running workflows
7. Create monitoring for orchestration steps

**Output**: Orchestration tool with saga pattern

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```kotlin
// src/main/kotlin/tools/orchestration/OrderOrchestrationTool.kt
package ai.koog.tools.orchestration

import ai.koog.annotations.Tool
import ai.koog.annotations.Parameter
import kotlinx.coroutines.*

class OrderOrchestrationTool(
    private val paymentService: PaymentService,
    private val inventoryService: InventoryService,
    private val shippingService: ShippingService,
    private val notificationService: NotificationService
) {

    @Tool(
        name = "process_order_saga",
        description = """
            Process complete order using saga pattern with compensation.
            Coordinates payment, inventory, shipping, and notifications.
            Automatically rolls back on any step failure.
        """
    )
    suspend fun processOrder(
        @Parameter(name = "order", description = "Order object", required = true)
        order: Order
    ): OrderResult = coroutineScope {

        val saga = OrderSaga()

        try {
            // Step 1: Process payment
            val paymentResult = saga.executeStep(
                name = "payment",
                execute = { paymentService.charge(order.total, order.paymentMethod) },
                compensate = { result -> paymentService.refund(result.transactionId) }
            )

            // Step 2: Reserve inventory
            val inventoryResult = saga.executeStep(
                name = "inventory",
                execute = { inventoryService.reserve(order.items) },
                compensate = { inventoryService.release(order.items) }
            )

            // Step 3: Create shipment
            val shipmentResult = saga.executeStep(
                name = "shipment",
                execute = { shippingService.createShipment(order) },
                compensate = { result -> shippingService.cancelShipment(result.shipmentId) }
            )

            // Step 4: Send notifications (no compensation needed)
            notificationService.sendOrderConfirmation(
                orderId = order.id,
                trackingNumber = shipmentResult.trackingNumber
            )

            OrderResult.Success(
                orderId = order.id,
                transactionId = paymentResult.transactionId,
                trackingNumber = shipmentResult.trackingNumber
            )

        } catch (e: Exception) {
            // Saga failed, compensate all completed steps
            saga.compensate()

            OrderResult.Failed(
                orderId = order.id,
                error = e.message ?: "Unknown error",
                compensatedSteps = saga.completedSteps
            )
        }
    }
}

class OrderSaga {
    private val steps = mutableListOf<SagaStep<*>>()
    val completedSteps: List<String> get() = steps.map { it.name }

    suspend fun <T> executeStep(
        name: String,
        execute: suspend () -> T,
        compensate: suspend (T) -> Unit
    ): T {
        val result = execute()
        steps.add(SagaStep(name, result, compensate))
        return result
    }

    suspend fun compensate() {
        steps.reversed().forEach { step ->
            try {
                @Suppress("UNCHECKED_CAST")
                (step as SagaStep<Any>).compensate(step.result)
            } catch (e: Exception) {
                // Log compensation failure but continue
                println("Failed to compensate step ${step.name}: ${e.message}")
            }
        }
    }

    private data class SagaStep<T>(
        val name: String,
        val result: T,
        val compensate: suspend (T) -> Unit
    )
}

// Domain models
data class Order(
    val id: String,
    val items: List<OrderItem>,
    val total: Double,
    val paymentMethod: String,
    val shippingAddress: Address
)

data class OrderItem(
    val productId: String,
    val quantity: Int,
    val price: Double
)

data class Address(
    val street: String,
    val city: String,
    val state: String,
    val zipCode: String,
    val country: String
)

sealed class OrderResult {
    data class Success(
        val orderId: String,
        val transactionId: String,
        val trackingNumber: String
    ) : OrderResult()

    data class Failed(
        val orderId: String,
        val error: String,
        val compensatedSteps: List<String>
    ) : OrderResult()
}
```

### Phase 6: Testing & Mocking Infrastructure

**Goal**: Generate comprehensive tests and mocks

**Actions**:
1. Create unit tests for tool logic
2. Generate mock implementations
3. Add integration tests with real backends
4. Create test fixtures and sample data
5. Add error scenario tests
6. Generate performance tests
7. Create test documentation

**Output**: Complete test suite with mocks

**Agent**: koog-integration-architect (Sonnet)

**Example Output**:
```kotlin
// test/kotlin/tools/WeatherToolTest.kt
package ai.koog.tools.weather

import io.mockk.*
import kotlinx.coroutines.runBlocking
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeEach
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class WeatherToolTest {

    private lateinit var mockClient: WeatherAPIClient
    private lateinit var tool: WeatherTool

    @BeforeEach
    fun setup() {
        mockClient = mockk()
        tool = WeatherTool(mockClient)
    }

    @Test
    fun `should fetch current weather successfully`() = runBlocking {
        // Given
        val expected = WeatherResponse(
            city = "London",
            temperature = 15.5,
            feelsLike = 14.0,
            condition = "Clouds",
            description = "scattered clouds",
            humidity = 72,
            pressure = 1013,
            windSpeed = 3.5,
            timestamp = 1234567890
        )

        coEvery { mockClient.getCurrentWeather("London", "metric") } returns expected

        // When
        val result = tool.getCurrentWeather("London", "metric")

        // Then
        assertEquals(expected, result)
        coVerify(exactly = 1) { mockClient.getCurrentWeather("London", "metric") }
    }

    @Test
    fun `should handle rate limit error with retry`() = runBlocking {
        // Given
        coEvery { mockClient.getCurrentWeather(any(), any()) } throws
            WeatherAPIException.RateLimitError("Rate limit", retryAfter = 60)

        // When/Then
        assertFailsWith<WeatherAPIException.RateLimitError> {
            tool.getCurrentWeather("London", "metric")
        }
    }

    @Test
    fun `should validate city parameter`() = runBlocking {
        // When/Then
        assertFailsWith<IllegalArgumentException> {
            tool.getCurrentWeather("", "metric")
        }
    }
}

// Mock implementations for testing
class MockWeatherService : WeatherAPIClient {
    override suspend fun getCurrentWeather(city: String, units: String): WeatherResponse {
        return WeatherResponse(
            city = city,
            temperature = 20.0,
            feelsLike = 19.0,
            condition = "Clear",
            description = "clear sky",
            humidity = 50,
            pressure = 1015,
            windSpeed = 2.5,
            timestamp = System.currentTimeMillis() / 1000
        )
    }
}
```

### Phase 7: Documentation & Integration Guide

**Goal**: Generate comprehensive documentation

**Actions**:
1. Create tool usage guide
2. Document API/database schema requirements
3. Add configuration examples
4. Create troubleshooting guide
5. Document error scenarios and handling
6. Add performance tuning guide
7. Create integration examples with agents

**Output**: Complete integration documentation

**Agent**: koog-integration-architect (Sonnet)

## Execution Parameters

### Required Parameters
- `tool-name`: Name of the tool to create
- `integration-type`: Type of integration (rest-api, database, message-queue, etc.)
- `agent-path`: Path to agent project

### Optional Parameters
- `api-url`: Base URL for API integrations
- `auth-type`: Authentication method (default: none)
- `db-type`: Database type for database integrations
- `retry-strategy`: Retry strategy (default: exponential)
- `enable-circuit-breaker`: Enable circuit breaker (default: true)
- `include-tests`: Generate test suite (default: true)
- `async-execution`: Use coroutines (default: true)

## Success Criteria

### Integration Quality
- ✓ Type-safe tool interface
- ✓ Comprehensive error handling
- ✓ Retry logic with exponential backoff
- ✓ Circuit breaker implemented
- ✓ Connection pooling configured
- ✓ Proper resource cleanup

### Testing Coverage
- ✓ Unit tests for all tool methods
- ✓ Mock implementations provided
- ✓ Integration tests with real backends
- ✓ Error scenario tests
- ✓ Performance tests included

### Documentation
- ✓ Usage examples provided
- ✓ Configuration documented
- ✓ Error scenarios explained
- ✓ Troubleshooting guide included

## Example Use Cases

### Use Case 1: REST API Integration
```bash
/koog-tool-integration \
  --type rest-api \
  --tool-name weather-api \
  --api-url https://api.openweathermap.org \
  --auth-type apikey \
  --enable-circuit-breaker
```

### Use Case 2: Database Connector
```bash
/koog-tool-integration \
  --type database \
  --tool-name postgres-connector \
  --db-type postgresql \
  --pool-size 20 \
  --transaction-support
```

### Use Case 3: Kafka Integration
```bash
/koog-tool-integration \
  --type message-queue \
  --tool-name kafka-events \
  --queue-type kafka \
  --consumer-group order-processors \
  --serialization json
```

### Use Case 4: Multi-System Orchestration
```bash
/koog-tool-integration \
  --type composite \
  --tool-name order-orchestration \
  --include-saga-pattern \
  --enable-compensation
```

## Integration with Other Plugins

### kotlin-koog-development
- Complements `koog-agent-scaffold` with tool implementations
- Works with `koog-test-scaffold` for testing integrations

### backend-development
- Shares API client patterns
- Compatible with microservices architecture

### data-engineering
- Database connector patterns align with data pipelines
- Message queue integration supports event streaming

## Troubleshooting

**Q: Circuit breaker opens too frequently**
A: Increase failure threshold or adjust reset timeout. Review error classification to avoid counting non-transient errors.

**Q: Connection pool exhaustion**
A: Increase pool size. Check for connection leaks. Ensure proper resource cleanup in finally blocks.

**Q: Retries not working as expected**
A: Verify error classification. Check retry configuration. Ensure exceptions are properly caught and classified.

**Q: High latency on API calls**
A: Enable connection pooling. Check timeout settings. Consider caching frequent requests.

**Q: Transaction rollback failures**
A: Verify transaction isolation level. Check for long-running transactions. Ensure proper exception handling.
