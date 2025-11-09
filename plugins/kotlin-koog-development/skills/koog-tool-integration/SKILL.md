---
name: koog-tool-integration
description: Custom tool development and integration patterns for Koog agents including tool design, parameter validation, error handling, async operations, and Model Context Protocol (MCP) integration. Use when creating custom tools, integrating external APIs, implementing MCP servers, designing tool interfaces, or troubleshooting tool interactions.
---

# Koog Tool Integration

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Creating custom tools for Koog agents
- Integrating external APIs and services
- Implementing Model Context Protocol (MCP) servers
- Designing tool parameter schemas
- Handling tool errors and retries
- Building asynchronous tools
- Creating tool chains and compositions
- Implementing tool caching strategies
- Validating tool inputs and outputs
- Debugging tool integration issues

## Core Concepts

### Tool Design Fundamentals

#### Basic Tool Structure

```kotlin
import ai.koog.tool.*

class WeatherTool : Tool {
    override val name = "get_weather"
    override val description = "Get current weather for a location"

    override val parameters = listOf(
        ToolParameter(
            name = "location",
            type = ParameterType.STRING,
            description = "City name or coordinates",
            required = true
        ),
        ToolParameter(
            name = "units",
            type = ParameterType.STRING,
            description = "Temperature units: celsius or fahrenheit",
            required = false,
            default = "celsius",
            enum = listOf("celsius", "fahrenheit")
        )
    )

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val location = arguments["location"] as? String
            ?: return ToolResult.error("Missing location parameter")

        val units = arguments["units"] as? String ?: "celsius"

        return try {
            val weather = fetchWeather(location, units)
            ToolResult.success(weather)
        } catch (e: Exception) {
            ToolResult.error("Failed to fetch weather: ${e.message}")
        }
    }

    private suspend fun fetchWeather(location: String, units: String): Map<String, Any> {
        // API call implementation
        return mapOf(
            "location" to location,
            "temperature" to 22.5,
            "units" to units,
            "conditions" to "Partly cloudy"
        )
    }
}
```

#### DSL-Based Tool Definition

```kotlin
fun weatherTool() = tool("get_weather") {
    description("Get current weather for a location")

    parameter("location", String::class) {
        description("City name or coordinates")
        required()
    }

    parameter("units", String::class) {
        description("Temperature units")
        optional()
        default("celsius")
        enum("celsius", "fahrenheit")
    }

    implementation { args ->
        val location = args["location"] as String
        val units = args["units"] as? String ?: "celsius"

        val weather = fetchWeather(location, units)
        ToolResult.success(weather)
    }
}
```

### Advanced Parameter Validation

#### Type-Safe Parameter Schema

```kotlin
import kotlinx.serialization.*

@Serializable
data class SearchParameters(
    @LLMDescription("Search query string")
    val query: String,

    @LLMDescription("Maximum number of results (1-100)")
    val maxResults: Int = 10,

    @LLMDescription("Filter by category")
    val category: String? = null,

    @LLMDescription("Sort order: relevance, date, popularity")
    val sortBy: SortOrder = SortOrder.RELEVANCE
)

enum class SortOrder {
    RELEVANCE, DATE, POPULARITY
}

class SearchTool : TypedTool<SearchParameters, SearchResults> {
    override val name = "search"
    override val description = "Search for content"

    override suspend fun execute(params: SearchParameters): ToolResult<SearchResults> {
        // Automatic validation from data class
        validateParameters(params)

        val results = performSearch(params)
        return ToolResult.success(results)
    }

    private fun validateParameters(params: SearchParameters) {
        require(params.query.isNotBlank()) { "Query cannot be blank" }
        require(params.maxResults in 1..100) { "Max results must be between 1 and 100" }
    }
}
```

#### Custom Validators

```kotlin
class ValidationRule<T>(
    val name: String,
    val validate: (T) -> Boolean,
    val errorMessage: String
)

class ValidatedTool : Tool {
    override val name = "create_user"

    private val emailValidator = ValidationRule<String>(
        name = "email_format",
        validate = { it.matches(Regex("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$")) },
        errorMessage = "Invalid email format"
    )

    private val passwordValidator = ValidationRule<String>(
        name = "password_strength",
        validate = { it.length >= 8 && it.any { c -> c.isDigit() } },
        errorMessage = "Password must be at least 8 characters with a number"
    )

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val email = arguments["email"] as? String ?: return ToolResult.error("Missing email")
        val password = arguments["password"] as? String ?: return ToolResult.error("Missing password")

        // Validate email
        if (!emailValidator.validate(email)) {
            return ToolResult.error(emailValidator.errorMessage)
        }

        // Validate password
        if (!passwordValidator.validate(password)) {
            return ToolResult.error(passwordValidator.errorMessage)
        }

        // Create user
        val user = createUser(email, password)
        return ToolResult.success(user)
    }
}
```

### Async Tool Operations

#### Non-Blocking API Calls

```kotlin
import kotlinx.coroutines.*
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*

class AsyncHttpTool(private val httpClient: HttpClient) : Tool {
    override val name = "fetch_url"
    override val description = "Fetch content from URL asynchronously"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val url = arguments["url"] as? String
            ?: return ToolResult.error("Missing URL")

        return withContext(Dispatchers.IO) {
            try {
                val response = httpClient.get(url)
                val content = response.bodyAsText()

                ToolResult.success(mapOf(
                    "url" to url,
                    "status" to response.status.value,
                    "content" to content,
                    "contentLength" to content.length
                ))
            } catch (e: Exception) {
                ToolResult.error("Failed to fetch URL: ${e.message}")
            }
        }
    }
}
```

#### Parallel Tool Execution

```kotlin
class ParallelDataFetcher : Tool {
    override val name = "fetch_multiple_sources"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val sources = arguments["sources"] as? List<String>
            ?: return ToolResult.error("Missing sources")

        // Execute all fetches in parallel
        val results = coroutineScope {
            sources.map { source ->
                async(Dispatchers.IO) {
                    fetchSource(source)
                }
            }.awaitAll()
        }

        return ToolResult.success(mapOf(
            "sources" to sources.size,
            "results" to results
        ))
    }

    private suspend fun fetchSource(source: String): Map<String, Any> {
        // Fetch implementation
        delay(100) // Simulated API call
        return mapOf(
            "source" to source,
            "data" to "content from $source"
        )
    }
}
```

### Tool Error Handling

#### Retry Logic

```kotlin
class ResilientTool(
    private val maxRetries: Int = 3,
    private val retryDelay: Duration = 1.seconds
) : Tool {
    override val name = "resilient_api_call"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        var lastException: Exception? = null

        repeat(maxRetries) { attempt ->
            try {
                return performApiCall(arguments)
            } catch (e: Exception) {
                lastException = e
                logger.warn("Attempt ${attempt + 1} failed: ${e.message}")

                if (attempt < maxRetries - 1) {
                    delay(retryDelay.toMillis() * (attempt + 1)) // Exponential backoff
                }
            }
        }

        return ToolResult.error(
            "Failed after $maxRetries attempts: ${lastException?.message}"
        )
    }

    private suspend fun performApiCall(arguments: Map<String, Any>): ToolResult {
        // API call implementation
        throw Exception("API temporarily unavailable")
    }
}
```

#### Graceful Degradation

```kotlin
class FallbackTool(
    private val primaryService: ExternalService,
    private val fallbackService: ExternalService
) : Tool {
    override val name = "resilient_search"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val query = arguments["query"] as String

        // Try primary service
        try {
            val result = primaryService.search(query)
            return ToolResult.success(result)
        } catch (e: Exception) {
            logger.warn("Primary service failed, using fallback", e)
        }

        // Fallback to secondary service
        try {
            val result = fallbackService.search(query)
            return ToolResult.success(result, metadata = mapOf("source" to "fallback"))
        } catch (e: Exception) {
            return ToolResult.error("Both services unavailable: ${e.message}")
        }
    }
}
```

### Tool Caching

```kotlin
import com.github.benmanes.caffeine.cache.*
import kotlin.time.Duration.Companion.minutes

class CachedTool(
    private val ttl: Duration = 5.minutes
) : Tool {
    override val name = "cached_api_call"

    private val cache: Cache<String, ToolResult> = Caffeine.newBuilder()
        .expireAfterWrite(ttl.toJavaDuration())
        .maximumSize(1000)
        .build()

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val cacheKey = generateCacheKey(arguments)

        // Try cache first
        cache.getIfPresent(cacheKey)?.let { cached ->
            logger.debug("Cache hit for key: $cacheKey")
            return cached
        }

        // Cache miss - execute and cache
        val result = performExpensiveOperation(arguments)
        cache.put(cacheKey, result)

        return result
    }

    private fun generateCacheKey(arguments: Map<String, Any>): String {
        return arguments.entries
            .sortedBy { it.key }
            .joinToString("|") { "${it.key}=${it.value}" }
    }

    private suspend fun performExpensiveOperation(arguments: Map<String, Any>): ToolResult {
        // Expensive operation
        delay(1000)
        return ToolResult.success("result")
    }
}
```

### Model Context Protocol (MCP) Integration

#### Implementing an MCP Server

```kotlin
import ai.koog.mcp.*

class CustomMCPServer : MCPServer {
    override val name = "custom-tools"
    override val version = "1.0.0"

    override fun getTools(): List<MCPTool> {
        return listOf(
            createFileSystemTool(),
            createDatabaseTool(),
            createApiTool()
        )
    }

    private fun createFileSystemTool() = MCPTool(
        name = "read_file",
        description = "Read file contents",
        inputSchema = JsonSchema {
            property("path", JsonSchemaType.STRING) {
                description = "File path to read"
            }
        },
        handler = { params ->
            val path = params["path"] as String
            val content = readFile(path)
            MCPResult.success(mapOf("content" to content))
        }
    )

    private fun createDatabaseTool() = MCPTool(
        name = "query_database",
        description = "Execute database query",
        inputSchema = JsonSchema {
            property("sql", JsonSchemaType.STRING) {
                description = "SQL query to execute"
            }
            property("params", JsonSchemaType.ARRAY) {
                description = "Query parameters"
                optional()
            }
        },
        handler = { params ->
            val sql = params["sql"] as String
            val queryParams = params["params"] as? List<Any> ?: emptyList()
            val results = executeQuery(sql, queryParams)
            MCPResult.success(mapOf("rows" to results))
        }
    )

    private fun createApiTool() = MCPTool(
        name = "call_api",
        description = "Make HTTP API call",
        inputSchema = JsonSchema {
            property("url", JsonSchemaType.STRING)
            property("method", JsonSchemaType.STRING) {
                enum("GET", "POST", "PUT", "DELETE")
            }
            property("body", JsonSchemaType.OBJECT) {
                optional()
            }
        },
        handler = { params ->
            val url = params["url"] as String
            val method = params["method"] as String
            val body = params["body"] as? Map<String, Any>

            val response = callApi(url, method, body)
            MCPResult.success(response)
        }
    )
}

// Start MCP server
fun main() {
    val server = CustomMCPServer()
    val transport = StdioMCPTransport()

    MCPServerRunner(server, transport).start()
}
```

#### Using MCP Tools in Agents

```kotlin
val mcpProvider = McpToolRegistryProvider(
    transport = StdioTransport("path/to/mcp-server"),
    parser = McpToolDescriptorParser()
)

val agent = agent("mcp_enabled") {
    instruction("Use available MCP tools to complete tasks")

    // All MCP tools automatically available
    tools = mcpProvider.createRegistry()

    // Or selectively include MCP tools
    tool("read_file", mcpProvider.getTool("read_file"))
    tool("query_database", mcpProvider.getTool("query_database"))
}
```

#### Building Domain-Specific MCP Servers

```kotlin
// Google Maps MCP Server Example
class GoogleMapsMCPServer(private val apiKey: String) : MCPServer {
    override val name = "google-maps"
    override val version = "1.0.0"

    override fun getTools(): List<MCPTool> = listOf(
        geocodeTool(),
        placesSearchTool(),
        directionsToolTool(),
        distanceMatrixTool()
    )

    private fun geocodeTool() = MCPTool(
        name = "geocode",
        description = "Convert address to coordinates",
        inputSchema = JsonSchema {
            property("address", JsonSchemaType.STRING) {
                description = "Address to geocode"
            }
        },
        handler = { params ->
            val address = params["address"] as String
            val result = googleMapsClient.geocode(address, apiKey)
            MCPResult.success(result)
        }
    )

    private fun placesSearchTool() = MCPTool(
        name = "search_places",
        description = "Search for places nearby",
        inputSchema = JsonSchema {
            property("query", JsonSchemaType.STRING)
            property("location", JsonSchemaType.STRING)
            property("radius", JsonSchemaType.NUMBER) {
                description = "Search radius in meters"
                default = 5000
            }
        },
        handler = { params ->
            val query = params["query"] as String
            val location = params["location"] as String
            val radius = params["radius"] as? Int ?: 5000

            val results = googleMapsClient.searchPlaces(query, location, radius, apiKey)
            MCPResult.success(mapOf("places" to results))
        }
    )
}
```

### Tool Composition Patterns

#### Sequential Tool Chain

```kotlin
class ToolChain(private val tools: List<Tool>) : Tool {
    override val name = "tool_chain"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        var currentInput = arguments
        var currentResult: ToolResult? = null

        for (tool in tools) {
            currentResult = tool.execute(currentInput)

            if (!currentResult.isSuccess) {
                return currentResult // Return first error
            }

            // Pass output as input to next tool
            currentInput = currentResult.data as? Map<String, Any> ?: currentInput
        }

        return currentResult ?: ToolResult.error("No tools executed")
    }
}

// Usage
val pipeline = ToolChain(
    listOf(
        FetchDataTool(),
        TransformDataTool(),
        ValidateDataTool(),
        SaveDataTool()
    )
)
```

#### Conditional Tool Selection

```kotlin
class ConditionalTool(
    private val condition: (Map<String, Any>) -> Boolean,
    private val trueTool: Tool,
    private val falseTool: Tool
) : Tool {
    override val name = "conditional_tool"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val selectedTool = if (condition(arguments)) trueTool else falseTool
        return selectedTool.execute(arguments)
    }
}

// Usage
val tool = ConditionalTool(
    condition = { args -> (args["priority"] as? String) == "high" },
    trueTool = UrgentProcessorTool(),
    falseTool = StandardProcessorTool()
)
```

#### Tool Result Aggregation

```kotlin
class AggregatorTool(private val tools: List<Tool>) : Tool {
    override val name = "aggregator"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val results = coroutineScope {
            tools.map { tool ->
                async {
                    tool.name to tool.execute(arguments)
                }
            }.awaitAll().toMap()
        }

        val allSuccessful = results.values.all { it.isSuccess }

        return if (allSuccessful) {
            ToolResult.success(mapOf(
                "results" to results.mapValues { it.value.data }
            ))
        } else {
            val errors = results.filter { !it.value.isSuccess }
            ToolResult.error("Some tools failed: $errors")
        }
    }
}
```

### Database Integration Tools

```kotlin
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.dao.*
import org.jetbrains.exposed.dao.id.*

class DatabaseQueryTool(private val database: Database) : Tool {
    override val name = "query_database"
    override val description = "Execute SQL query"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val query = arguments["query"] as? String
            ?: return ToolResult.error("Missing query")

        val params = arguments["params"] as? List<Any> ?: emptyList()

        return newSuspendedTransaction(db = database) {
            try {
                val results = exec(query) { rs ->
                    val metadata = rs.metaData
                    val columnCount = metadata.columnCount

                    buildList {
                        while (rs.next()) {
                            val row = mutableMapOf<String, Any?>()
                            for (i in 1..columnCount) {
                                val columnName = metadata.getColumnName(i)
                                row[columnName] = rs.getObject(i)
                            }
                            add(row)
                        }
                    }
                }

                ToolResult.success(mapOf(
                    "rows" to results,
                    "count" to results.size
                ))
            } catch (e: Exception) {
                ToolResult.error("Query failed: ${e.message}")
            }
        }
    }
}
```

### REST API Integration Tools

```kotlin
class RestApiTool(
    private val httpClient: HttpClient,
    private val baseUrl: String,
    private val apiKey: String
) : Tool {
    override val name = "call_api"

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val endpoint = arguments["endpoint"] as? String
            ?: return ToolResult.error("Missing endpoint")

        val method = arguments["method"] as? String ?: "GET"
        val body = arguments["body"] as? Map<String, Any>

        return withContext(Dispatchers.IO) {
            try {
                val response = when (method.uppercase()) {
                    "GET" -> httpClient.get("$baseUrl$endpoint") {
                        headers {
                            append("Authorization", "Bearer $apiKey")
                        }
                    }
                    "POST" -> httpClient.post("$baseUrl$endpoint") {
                        headers {
                            append("Authorization", "Bearer $apiKey")
                            append("Content-Type", "application/json")
                        }
                        setBody(body)
                    }
                    else -> return@withContext ToolResult.error("Unsupported method: $method")
                }

                val responseBody = response.bodyAsText()
                ToolResult.success(mapOf(
                    "status" to response.status.value,
                    "body" to responseBody
                ))
            } catch (e: Exception) {
                ToolResult.error("API call failed: ${e.message}")
            }
        }
    }
}
```

## Patterns and Best Practices

### Pattern 1: Tool Factory

```kotlin
interface ToolFactory {
    fun createTool(config: ToolConfig): Tool
}

class HttpToolFactory : ToolFactory {
    override fun createTool(config: ToolConfig): Tool {
        return RestApiTool(
            httpClient = createHttpClient(config),
            baseUrl = config.baseUrl,
            apiKey = config.apiKey
        )
    }

    private fun createHttpClient(config: ToolConfig): HttpClient {
        return HttpClient {
            install(HttpTimeout) {
                requestTimeoutMillis = config.timeout.toMillis()
            }
            install(Logging) {
                level = LogLevel.INFO
            }
        }
    }
}
```

### Pattern 2: Tool Registry

```kotlin
class ToolRegistry {
    private val tools = mutableMapOf<String, Tool>()

    fun register(tool: Tool) {
        tools[tool.name] = tool
    }

    fun get(name: String): Tool? {
        return tools[name]
    }

    fun all(): List<Tool> {
        return tools.values.toList()
    }

    fun findByCategory(category: String): List<Tool> {
        return tools.values.filter { it.category == category }
    }
}

// Usage
val registry = ToolRegistry().apply {
    register(WeatherTool())
    register(DatabaseTool())
    register(ApiTool())
}
```

### Pattern 3: Tool Middleware

```kotlin
class LoggingToolMiddleware(private val tool: Tool) : Tool by tool {
    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        logger.info("Executing tool: ${tool.name} with args: $arguments")
        val start = System.currentTimeMillis()

        val result = tool.execute(arguments)

        val duration = System.currentTimeMillis() - start
        logger.info("Tool ${tool.name} completed in ${duration}ms: ${result.isSuccess}")

        return result
    }
}

class MetricsToolMiddleware(
    private val tool: Tool,
    private val metrics: MeterRegistry
) : Tool by tool {
    private val counter = metrics.counter("tool.executions", "tool", tool.name)
    private val timer = metrics.timer("tool.duration", "tool", tool.name)

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        counter.increment()
        return timer.recordSuspendCallable {
            tool.execute(arguments)
        }!!
    }
}
```

## Common Pitfalls

### Pitfall 1: Missing Parameter Validation

```kotlin
// ✗ Bad: No validation
override suspend fun execute(arguments: Map<String, Any>): ToolResult {
    val email = arguments["email"] as String // Can crash!
    // ...
}

// ✓ Good: Proper validation
override suspend fun execute(arguments: Map<String, Any>): ToolResult {
    val email = arguments["email"] as? String
        ?: return ToolResult.error("Missing email parameter")

    if (!email.matches(emailRegex)) {
        return ToolResult.error("Invalid email format")
    }
    // ...
}
```

### Pitfall 2: Blocking Operations

```kotlin
// ✗ Bad: Blocking call
override suspend fun execute(arguments: Map<String, Any>): ToolResult {
    val result = blockingApiCall() // Blocks coroutine!
    return ToolResult.success(result)
}

// ✓ Good: Non-blocking
override suspend fun execute(arguments: Map<String, Any>): ToolResult {
    val result = withContext(Dispatchers.IO) {
        blockingApiCall()
    }
    return ToolResult.success(result)
}
```

### Pitfall 3: Poor Error Messages

```kotlin
// ✗ Bad: Unhelpful error
return ToolResult.error("Failed")

// ✓ Good: Descriptive error
return ToolResult.error(
    "Failed to fetch weather data for location '$location': " +
    "API returned 404 - City not found. Please check the city name."
)
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-testing-patterns](/home/user/agents/plugins/kotlin-koog-development/skills/koog-testing-patterns/SKILL.md)
- [Koog Tool Development](https://docs.koog.ai/tools/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Koog MCP Integration](https://docs.koog.ai/model-context-protocol/)
- [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-overview.html)
