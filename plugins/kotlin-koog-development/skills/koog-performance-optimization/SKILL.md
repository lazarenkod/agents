---
name: koog-performance-optimization
description: Performance tuning and optimization strategies for Koog AI agents including token optimization, latency reduction, caching, parallel execution, and resource management. Use when optimizing agent performance, reducing costs, improving response times, scaling throughput, or troubleshooting performance issues.
---

# Koog Performance Optimization

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Reducing agent response latency
- Optimizing token usage and costs
- Improving agent throughput and scalability
- Implementing caching strategies
- Optimizing parallel execution
- Reducing memory consumption
- Minimizing API calls to LLM providers
- Troubleshooting performance bottlenecks
- Implementing history compression
- Optimizing tool execution performance

## Core Concepts

### Token Optimization Strategies

#### Strategy 1: Instruction Optimization

```kotlin
// ✗ Bad: Verbose, repetitive instructions (500+ tokens)
agent("verbose") {
    instruction("""
        You are a helpful AI assistant. You should always be polite and courteous.
        When responding to users, make sure to be comprehensive in your answers.
        Always think carefully about what the user is asking before responding.
        Provide detailed explanations when appropriate.
        Make sure your responses are well-structured and easy to understand.
        Consider the context of the conversation when formulating your response.
        Be respectful and professional at all times.
        If you're not sure about something, it's okay to say so.
        ...
    """)
}

// ✓ Good: Concise, focused instructions (50 tokens)
agent("concise") {
    instruction("""
        Classify sentiment as: positive, negative, or neutral.
        Return only the classification label.
    """)
}
```

#### Strategy 2: History Compression

```kotlin
agent("compressed_history") {
    instruction("Maintain conversation context efficiently")

    strategy {
        node("process_request") {
            nodeLLMRequest(instruction = "Respond to user query")
        }

        // Compress history when it gets too long
        decision("should_compress") {
            condition { context.messages.size > 20 } to node("compress")
            default() to node("process_request")
        }

        node("compress") {
            nodeLLMCompressHistory(
                strategy = when {
                    // Full compression for very long histories
                    context.messages.size > 100 -> HistoryCompressionStrategy.WholeHistory()

                    // Keep recent messages, summarize old ones
                    context.messages.size > 50 -> HistoryCompressionStrategy.FromLastNMessages(n = 10)

                    // Chunk-based compression
                    else -> HistoryCompressionStrategy.Chunked(chunkSize = 10)
                }
            )
        }
    }
}
```

#### Strategy 3: Selective Tool Exposure

```kotlin
// ✗ Bad: Exposing all tools increases token usage
agent("bloated") {
    tool("weather")
    tool("database")
    tool("email")
    tool("calendar")
    tool("file_system")
    tool("web_search")
    // ... 20 more tools
    // LLM must consider all tools in every request
}

// ✓ Good: Expose only relevant tools
agent("focused") {
    instruction("Classify email sentiment")

    // Only include tools actually needed
    tool("get_email_content")
    tool("analyze_sentiment")
    // Just 2 tools - much lower token overhead
}
```

#### Strategy 4: Smart Context Management

```kotlin
class TokenOptimizedAgent(
    private val maxContextTokens: Int = 2000
) {
    private val tokenCounter = TokenCounter()

    suspend fun execute(input: String, history: List<Message>): String {
        // Estimate token usage
        val currentTokens = tokenCounter.count(history + UserMessage(input))

        val optimizedHistory = if (currentTokens > maxContextTokens) {
            compressHistory(history)
        } else {
            history
        }

        return agent.execute(
            prompt = Prompt(optimizedHistory + UserMessage(input))
        )
    }

    private fun compressHistory(history: List<Message>): List<Message> {
        // Keep system message
        val systemMessage = history.firstOrNull { it is SystemMessage }

        // Keep only recent exchanges
        val recentMessages = history.takeLast(10)

        // Create summary of older messages
        val olderMessages = history.dropLast(10)
        val summary = if (olderMessages.isNotEmpty()) {
            listOf(SystemMessage("Previous conversation summary: ${summarize(olderMessages)}"))
        } else {
            emptyList()
        }

        return listOfNotNull(systemMessage) + summary + recentMessages
    }
}
```

### Latency Optimization

#### Parallel Tool Execution

```kotlin
agent("parallel_tools") {
    strategy {
        // Execute multiple independent tools in parallel
        node("gather_data") {
            parallel(
                listOf(
                    node("fetch_user") {
                        tool("get_user_data")
                    },
                    node("fetch_account") {
                        tool("get_account_info")
                    },
                    node("fetch_preferences") {
                        tool("get_user_preferences")
                    },
                    node("fetch_history") {
                        tool("get_purchase_history")
                    }
                ),
                mergeStrategy = MergeStrategy.Combine { results ->
                    // Combine all results into single context
                    results.flatten()
                }
            )
        }

        node("analyze") {
            nodeLLMRequest(instruction = "Analyze combined user data")
        }
    }
}

// Sequential: 4 tools × 100ms each = 400ms
// Parallel: max(4 tools) = 100ms
// 4x improvement!
```

#### Async Tool Implementation

```kotlin
class AsyncDatabaseTool : Tool {
    override val name = "query_database"

    private val connectionPool = HikariDataSource(HikariConfig().apply {
        jdbcUrl = "jdbc:postgresql://localhost:5432/db"
        maximumPoolSize = 20
        minimumIdle = 5
    })

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        return withContext(Dispatchers.IO) {
            // Non-blocking database query
            connectionPool.connection.use { conn ->
                val query = arguments["query"] as String
                val stmt = conn.prepareStatement(query)
                val rs = stmt.executeQuery()

                val results = buildList {
                    while (rs.next()) {
                        add(extractRow(rs))
                    }
                }

                ToolResult.success(mapOf("rows" to results))
            }
        }
    }
}
```

#### Request Batching

```kotlin
class BatchingAgent(
    private val batchSize: Int = 10,
    private val batchWindow: Duration = 100.milliseconds
) {
    private val pendingRequests = mutableListOf<PendingRequest>()
    private val mutex = Mutex()

    suspend fun execute(input: String): String {
        val deferred = CompletableDeferred<String>()

        mutex.withLock {
            pendingRequests.add(PendingRequest(input, deferred))

            if (pendingRequests.size >= batchSize) {
                processBatch()
            } else {
                scheduleBatchProcessing()
            }
        }

        return deferred.await()
    }

    private suspend fun processBatch() {
        val batch = pendingRequests.toList()
        pendingRequests.clear()

        // Process all requests in single LLM call
        val combinedPrompt = batch.joinToString("\n---\n") { it.input }
        val responses = agent.executeBatch(combinedPrompt)

        // Distribute responses
        batch.zip(responses).forEach { (request, response) ->
            request.deferred.complete(response)
        }
    }
}
```

### Caching Strategies

#### Response Caching

```kotlin
import com.github.benmanes.caffeine.cache.*
import java.util.concurrent.TimeUnit

class CachedAgent(
    private val agent: Agent,
    private val cacheDuration: Duration = 5.minutes
) {
    private val cache: Cache<String, CachedResponse> = Caffeine.newBuilder()
        .expireAfterWrite(cacheDuration.toJavaDuration())
        .maximumSize(10_000)
        .recordStats()
        .build()

    suspend fun execute(input: String): String {
        // Generate cache key
        val cacheKey = generateCacheKey(input)

        // Try cache first
        cache.getIfPresent(cacheKey)?.let { cached ->
            metrics.cacheHits.increment()
            logger.debug("Cache hit for input hash: ${input.hashCode()}")
            return cached.response
        }

        // Cache miss - execute agent
        metrics.cacheMisses.increment()
        val response = agent.execute(input)

        // Store in cache
        cache.put(cacheKey, CachedResponse(response, System.currentTimeMillis()))

        return response
    }

    private fun generateCacheKey(input: String): String {
        return input.lowercase().trim().hashCode().toString()
    }

    fun getCacheStats(): CacheStats {
        return cache.stats()
    }
}

data class CachedResponse(
    val response: String,
    val timestamp: Long
)
```

#### Semantic Caching

```kotlin
class SemanticCachedAgent(
    private val agent: Agent,
    private val embeddings: EmbeddingsProvider,
    private val similarityThreshold: Double = 0.95
) {
    private val cache = mutableListOf<SemanticCacheEntry>()

    suspend fun execute(input: String): String {
        val inputEmbedding = embeddings.embed(input)

        // Find semantically similar cached response
        val similar = cache.firstOrNull { entry ->
            cosineSimilarity(inputEmbedding, entry.inputEmbedding) >= similarityThreshold
        }

        if (similar != null) {
            metrics.semanticCacheHits.increment()
            logger.info("Semantic cache hit: '${input}' similar to '${similar.input}'")
            return similar.response
        }

        // No similar cached response - execute
        val response = agent.execute(input)

        // Add to semantic cache
        cache.add(SemanticCacheEntry(
            input = input,
            inputEmbedding = inputEmbedding,
            response = response
        ))

        // Limit cache size
        if (cache.size > 1000) {
            cache.removeAt(0) // FIFO eviction
        }

        return response
    }
}

data class SemanticCacheEntry(
    val input: String,
    val inputEmbedding: FloatArray,
    val response: String
)
```

#### Tool Result Caching

```kotlin
class CachedTool(
    private val tool: Tool,
    private val ttl: Duration = 1.minutes
) : Tool by tool {

    private val cache = ConcurrentHashMap<String, CachedResult>()

    override suspend fun execute(arguments: Map<String, Any>): ToolResult {
        val key = cacheKey(arguments)

        // Check cache
        cache[key]?.let { cached ->
            if (!cached.isExpired()) {
                return cached.result
            } else {
                cache.remove(key)
            }
        }

        // Execute and cache
        val result = tool.execute(arguments)
        cache[key] = CachedResult(result, System.currentTimeMillis() + ttl.inWholeMilliseconds)

        return result
    }

    private fun cacheKey(arguments: Map<String, Any>): String {
        return arguments.entries
            .sortedBy { it.key }
            .joinToString("|") { "${it.key}:${it.value}" }
    }

    data class CachedResult(
        val result: ToolResult,
        val expiresAt: Long
    ) {
        fun isExpired() = System.currentTimeMillis() > expiresAt
    }
}
```

### Memory Optimization

#### Streaming Responses

```kotlin
class StreamingAgent(private val agent: Agent) {

    fun executeStream(input: String): Flow<String> = flow {
        // Stream response chunks as they arrive
        agent.executeStream(input).collect { chunk ->
            emit(chunk)
        }
    }
}

// Usage
suspend fun handleRequest(input: String, outputStream: OutputStream) {
    streamingAgent.executeStream(input).collect { chunk ->
        outputStream.write(chunk.toByteArray())
        outputStream.flush()
    }
}
```

#### Lazy Tool Loading

```kotlin
class LazyToolRegistry {
    private val toolFactories = mutableMapOf<String, () -> Tool>()
    private val loadedTools = mutableMapOf<String, Tool>()

    fun register(name: String, factory: () -> Tool) {
        toolFactories[name] = factory
    }

    fun get(name: String): Tool {
        // Load tool only when first accessed
        return loadedTools.getOrPut(name) {
            toolFactories[name]?.invoke()
                ?: throw IllegalArgumentException("Tool not found: $name")
        }
    }
}

// Usage
val registry = LazyToolRegistry().apply {
    // Tool not created until first use
    register("heavy_tool") { HeavyDatabaseTool(createConnection()) }
    register("expensive_tool") { ExpensiveApiTool(initializeClient()) }
}
```

#### History Pruning

```kotlin
class HistoryPruningAgent(
    private val maxMessages: Int = 50,
    private val pruneStrategy: PruneStrategy = PruneStrategy.KEEP_RECENT
) {
    private val messages = mutableListOf<Message>()

    suspend fun execute(input: String): String {
        messages.add(UserMessage(input))

        // Prune if necessary
        if (messages.size > maxMessages) {
            pruneHistory()
        }

        val response = agent.execute(Prompt(messages))
        messages.add(AssistantMessage(response))

        return response
    }

    private fun pruneHistory() {
        when (pruneStrategy) {
            PruneStrategy.KEEP_RECENT -> {
                // Keep system message and recent exchanges
                val systemMsg = messages.firstOrNull { it is SystemMessage }
                val recentMsgs = messages.takeLast(maxMessages - 1)
                messages.clear()
                systemMsg?.let { messages.add(it) }
                messages.addAll(recentMsgs)
            }

            PruneStrategy.KEEP_IMPORTANT -> {
                // Keep system message, user messages, and high-scoring responses
                messages.retainAll { msg ->
                    msg is SystemMessage ||
                    msg is UserMessage ||
                    (msg is AssistantMessage && isImportant(msg))
                }
            }
        }
    }

    private fun isImportant(message: AssistantMessage): Boolean {
        // Score message importance
        return message.content.length > 100 || // Detailed response
               message.content.contains(Regex("```")) || // Code snippet
               message.metadata["important"] == true
    }
}

enum class PruneStrategy {
    KEEP_RECENT,
    KEEP_IMPORTANT
}
```

### Model Selection Optimization

#### Tiered Model Strategy

```kotlin
class TieredModelAgent(
    private val fastModel: LLMProvider, // Haiku, GPT-3.5
    private val powerfulModel: LLMProvider, // Sonnet, GPT-4
    private val complexityClassifier: ComplexityClassifier
) {

    suspend fun execute(input: String): String {
        val complexity = complexityClassifier.classify(input)

        return when (complexity) {
            Complexity.LOW -> {
                // Use fast, cheap model for simple requests
                metrics.fastModelUsage.increment()
                fastModel.execute(input)
            }

            Complexity.HIGH -> {
                // Use powerful model for complex requests
                metrics.powerfulModelUsage.increment()
                powerfulModel.execute(input)
            }
        }
    }
}

class ComplexityClassifier {
    fun classify(input: String): Complexity {
        val score = calculateComplexityScore(input)

        return when {
            score < 3 -> Complexity.LOW
            else -> Complexity.HIGH
        }
    }

    private fun calculateComplexityScore(input: String): Int {
        var score = 0

        // Check for code
        if (input.contains(Regex("```|class|function|def "))) score += 2

        // Check for multiple questions
        if (input.count { it == '?' } > 1) score += 1

        // Check length
        if (input.length > 500) score += 1

        // Check for technical terms
        val technicalTerms = listOf("algorithm", "architecture", "optimize", "debug")
        if (technicalTerms.any { input.contains(it, ignoreCase = true) }) score += 1

        return score
    }
}
```

#### Fallback Model Strategy

```kotlin
class FallbackModelAgent(
    private val primaryModel: LLMProvider,
    private val fallbackModel: LLMProvider
) {

    suspend fun execute(input: String): String {
        // Try primary model first
        return try {
            withTimeout(10.seconds) {
                primaryModel.execute(input)
            }
        } catch (e: Exception) {
            logger.warn("Primary model failed, using fallback", e)
            metrics.fallbackUsage.increment()

            // Use fallback model
            fallbackModel.execute(input)
        }
    }
}
```

### Connection Pooling and Resource Management

```kotlin
class PooledAgentService(
    private val poolSize: Int = 10
) {
    private val agentPool = Channel<Agent>(poolSize)

    init {
        // Pre-create agents
        repeat(poolSize) {
            agentPool.trySend(createAgent())
        }
    }

    suspend fun execute(input: String): String {
        // Get agent from pool
        val agent = agentPool.receive()

        return try {
            agent.execute(input)
        } finally {
            // Return to pool
            agentPool.send(agent)
        }
    }

    private fun createAgent(): Agent {
        return agent("pooled") {
            instruction("Process requests efficiently")
            // Configure agent
        }
    }
}
```

### Benchmarking and Profiling

```kotlin
class PerformanceBenchmark {

    suspend fun benchmarkAgent(agent: Agent, testInputs: List<String>): BenchmarkResults {
        val results = mutableListOf<RequestMetrics>()

        testInputs.forEach { input ->
            val metrics = measureRequest {
                agent.execute(input)
            }
            results.add(metrics)
        }

        return BenchmarkResults(
            totalRequests = results.size,
            avgLatency = results.map { it.latency }.average(),
            p50Latency = results.map { it.latency }.sorted()[results.size / 2],
            p95Latency = results.map { it.latency }.sorted()[(results.size * 0.95).toInt()],
            p99Latency = results.map { it.latency }.sorted()[(results.size * 0.99).toInt()],
            avgTokens = results.map { it.tokens }.average(),
            totalCost = results.sumOf { it.cost }
        )
    }

    private suspend fun measureRequest(block: suspend () -> String): RequestMetrics {
        val startTime = System.nanoTime()
        val startMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()

        val tokensBefore = metrics.totalTokens.get()
        val result = block()
        val tokensAfter = metrics.totalTokens.get()

        val endTime = System.nanoTime()
        val endMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()

        return RequestMetrics(
            latency = (endTime - startTime) / 1_000_000, // Convert to ms
            tokens = (tokensAfter - tokensBefore).toInt(),
            memoryUsed = endMemory - startMemory,
            cost = calculateCost(tokensAfter - tokensBefore)
        )
    }
}

data class BenchmarkResults(
    val totalRequests: Int,
    val avgLatency: Double,
    val p50Latency: Long,
    val p95Latency: Long,
    val p99Latency: Long,
    val avgTokens: Double,
    val totalCost: Double
)

data class RequestMetrics(
    val latency: Long,
    val tokens: Int,
    val memoryUsed: Long,
    val cost: Double
)
```

## Patterns and Best Practices

### Pattern 1: Progressive Enhancement

Start simple and optimize based on metrics:

```kotlin
// Stage 1: Basic implementation
val agent = agent("simple") {
    instruction("Process requests")
}

// Stage 2: Add caching
val cachedAgent = CachedAgent(agent)

// Stage 3: Add parallel execution
val optimizedAgent = agent("optimized") {
    strategy {
        node("parallel_tools") {
            parallel(tools)
        }
    }
}

// Stage 4: Add tiered models
val tieredAgent = TieredModelAgent(cachedAgent, fastModel, powerfulModel)
```

### Pattern 2: Metrics-Driven Optimization

```kotlin
class MetricsCollector {
    val requestLatency = histogram("agent.request.latency")
    val tokenUsage = counter("agent.tokens.total")
    val cacheHitRate = gauge("agent.cache.hit_rate")

    fun recordRequest(latency: Long, tokens: Int, cacheHit: Boolean) {
        requestLatency.record(latency)
        tokenUsage.increment(tokens.toDouble())
        if (cacheHit) cacheHitRate.increment()
    }
}

// Monitor and optimize based on metrics
fun analyzeMetrics(metrics: MetricsCollector) {
    when {
        metrics.requestLatency.mean() > 1000 -> {
            logger.warn("High latency detected - consider parallel execution")
        }
        metrics.tokenUsage.count() > 1_000_000 -> {
            logger.warn("High token usage - review instruction verbosity")
        }
        metrics.cacheHitRate.value() < 0.3 -> {
            logger.info("Low cache hit rate - consider semantic caching")
        }
    }
}
```

### Pattern 3: Load Testing

```kotlin
class LoadTester(private val agent: Agent) {

    suspend fun runLoadTest(
        concurrentUsers: Int = 10,
        requestsPerUser: Int = 100,
        testInputs: List<String>
    ): LoadTestResults {
        val results = ConcurrentHashMap<Int, MutableList<Long>>()

        coroutineScope {
            repeat(concurrentUsers) { userId ->
                launch {
                    results[userId] = mutableListOf()

                    repeat(requestsPerUser) {
                        val input = testInputs.random()
                        val latency = measureTimeMillis {
                            agent.execute(input)
                        }
                        results[userId]!!.add(latency)
                    }
                }
            }
        }

        return LoadTestResults(
            totalRequests = concurrentUsers * requestsPerUser,
            successRate = 1.0, // Track failures in real implementation
            avgLatency = results.values.flatten().average(),
            throughput = calculateThroughput(results)
        )
    }
}
```

## Common Pitfalls

### Pitfall 1: Premature Optimization

Don't optimize before measuring:

```kotlin
// ✗ Bad: Optimizing without metrics
val agent = HyperOptimizedAgent(
    caching = true,
    parallelism = 100,
    tieredModels = true,
    // ... complex optimizations without knowing bottlenecks
)

// ✓ Good: Measure first, optimize bottlenecks
val metrics = benchmarkAgent(simpleAgent)
if (metrics.avgLatency > 1000) {
    // Optimize latency
}
if (metrics.avgTokens > 1000) {
    // Optimize token usage
}
```

### Pitfall 2: Over-Caching

```kotlin
// ✗ Bad: Caching everything forever
val cache = Caffeine.newBuilder()
    .maximumSize(1_000_000) // Too large!
    .expireAfterWrite(Duration.ofDays(365)) // Too long!
    .build()

// ✓ Good: Reasonable cache limits
val cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(5.minutes)
    .build()
```

### Pitfall 3: Ignoring Memory Pressure

```kotlin
// ✗ Bad: Unbounded history growth
val messages = mutableListOf<Message>()
// Never cleared - memory leak!

// ✓ Good: Bounded history
val messages = object : ArrayList<Message>() {
    override fun add(element: Message): Boolean {
        val result = super.add(element)
        if (size > 100) {
            removeAt(0)
        }
        return result
    }
}
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-production-deployment](/home/user/agents/plugins/kotlin-koog-development/skills/koog-production-deployment/SKILL.md)
- [Koog Performance Guide](https://docs.koog.ai/performance/)
- [Koog History Compression](https://docs.koog.ai/history-compression/)
- [Kotlin Coroutines Performance](https://kotlinlang.org/docs/coroutines-guide.html)
- [Caffeine Caching Library](https://github.com/ben-manes/caffeine)
