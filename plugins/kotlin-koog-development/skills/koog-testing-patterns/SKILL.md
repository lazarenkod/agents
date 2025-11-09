---
name: koog-testing-patterns
description: Comprehensive testing strategies for Koog AI agents including unit testing, integration testing, property-based testing, and contract testing. Use when designing test suites for agents, implementing test automation, debugging agent behavior, validating tool integration, or ensuring production reliability.
---

# Koog Testing Patterns

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Designing comprehensive test suites for Koog agents
- Implementing automated testing for agent workflows
- Debugging agent behavior and tool interactions
- Validating tool integration and contracts
- Testing multimodal agents with vision and documents
- Performance testing and benchmarking agents
- Ensuring production reliability and safety
- Testing complex strategy graphs and workflows
- Validating structured output and JSON schemas
- Testing agent sessions and state management

## Core Concepts

### Testing Pyramid for AI Agents

The traditional testing pyramid applies to AI agents with some unique considerations:

```
        /\
       /  \        E2E Tests (10%)
      /____\       - Full agent workflows
     /      \      - Real LLM calls
    /________\     - Integration scenarios
   /          \
  /____________\   Integration Tests (30%)
 /              \  - Tool integration
/________________\ - Session management
                   - Strategy graph execution

        Unit Tests (60%)
        - Tool logic
        - Node execution
        - Data transformations
        - Validation logic
```

### Test Categories

#### 1. Unit Tests
**Focus:** Individual components in isolation

```kotlin
import ai.koog.agent
import io.mockk.*
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class AgentToolTests {
    @Test
    fun `tool should process valid input correctly`() {
        // Arrange
        val tool = DatabaseQueryTool()
        val input = mapOf("query" to "SELECT * FROM users")

        // Act
        val result = tool.execute(input)

        // Assert
        assertEquals("success", result.status)
        assertTrue(result.data.isNotEmpty())
    }

    @Test
    fun `tool should handle invalid input gracefully`() {
        val tool = DatabaseQueryTool()
        val input = mapOf("query" to "INVALID SQL")

        val result = tool.execute(input)

        assertEquals("error", result.status)
        assertTrue(result.error.contains("SQL syntax"))
    }
}
```

#### 2. Tool Mocking Tests
**Focus:** Agent behavior with mocked tools

```kotlin
class AgentWithMockedToolsTest {
    @Test
    fun `agent should call tools in correct sequence`() {
        // Mock tools
        val fetchTool = mockk<Tool>()
        val processTool = mockk<Tool>()
        val saveTool = mockk<Tool>()

        every { fetchTool.execute(any()) } returns ToolResult.success("data")
        every { processTool.execute(any()) } returns ToolResult.success("processed")
        every { saveTool.execute(any()) } returns ToolResult.success("saved")

        // Create agent with mocked tools
        val agent = agent("test_workflow") {
            instruction("Process data through pipeline")

            strategy {
                node("fetch") {
                    tool("fetch_data", fetchTool)
                }

                node("process") {
                    tool("process_data", processTool)
                }

                node("save") {
                    tool("save_data", saveTool)
                }

                edge(node("fetch") onToolResult to node("process"))
                edge(node("process") onToolResult to node("save"))
            }
        }

        // Execute
        val result = agent.execute("test input")

        // Verify call sequence
        verifySequence {
            fetchTool.execute(any())
            processTool.execute(any())
            saveTool.execute(any())
        }

        assertEquals("saved", result)
    }
}
```

#### 3. LLM Response Mocking
**Focus:** Testing agent logic without real LLM calls

```kotlin
class MockLLMProvider : LLMProvider {
    private val responses = mutableMapOf<String, String>()

    fun mockResponse(prompt: String, response: String) {
        responses[prompt] = response
    }

    override suspend fun execute(request: LLMRequest): LLMResponse {
        val mockResponse = responses[request.prompt]
            ?: "Default mock response"

        return LLMResponse(
            text = mockResponse,
            tokenUsage = TokenUsage(input = 10, output = 20)
        )
    }
}

@Test
fun `agent should handle LLM response correctly`() {
    val mockProvider = MockLLMProvider()
    mockProvider.mockResponse(
        "Classify the sentiment",
        "positive"
    )

    val agent = agent("sentiment_classifier") {
        llmProvider = mockProvider
        instruction("Classify the sentiment")
    }

    val result = agent.execute("I love this product!")

    assertEquals("positive", result)
}
```

#### 4. Contract Testing
**Focus:** Ensuring tools and agents conform to expected interfaces

```kotlin
import kotlinx.serialization.*
import kotlinx.serialization.json.*

@Serializable
data class UserProfileOutput(
    val userId: String,
    val name: String,
    val email: String,
    val createdAt: String
)

class ContractTest {
    @Test
    fun `agent output should conform to expected schema`() {
        val agent = agent("user_profiler") {
            instruction("Extract user profile information")
        }

        val result = agent.execute("User: John Doe, email: john@example.com")

        // Parse and validate against contract
        val profile = Json.decodeFromString<UserProfileOutput>(result)

        // Validate contract
        assertTrue(profile.userId.isNotEmpty())
        assertTrue(profile.email.contains("@"))
        assertTrue(profile.createdAt.matches(Regex("\\d{4}-\\d{2}-\\d{2}")))
    }

    @Test
    fun `tool should match expected parameter contract`() {
        val tool = DatabaseQueryTool()

        // Tool contract validation
        val requiredParams = setOf("query", "timeout")
        val optionalParams = setOf("maxRows", "cache")

        assertEquals(requiredParams, tool.requiredParameters)
        assertEquals(optionalParams, tool.optionalParameters)
    }
}
```

#### 5. Property-Based Testing
**Focus:** Testing with randomized inputs to find edge cases

```kotlin
import io.kotest.property.Arb
import io.kotest.property.arbitrary.*
import io.kotest.property.checkAll

class PropertyBasedTest {
    @Test
    fun `agent should handle any valid email input`() = runTest {
        checkAll<String>(1000, Arb.email()) { email ->
            val agent = agent("email_validator") {
                instruction("Validate email format")
            }

            val result = agent.execute(email)

            // Should always return valid/invalid, never crash
            assertTrue(result in setOf("valid", "invalid"))
        }
    }

    @Test
    fun `number processing tool should handle any integer`() = runTest {
        checkAll<Int>(1000) { number ->
            val tool = NumberProcessorTool()

            val result = tool.execute(mapOf("value" to number))

            // Should never throw, always return result
            assertNotNull(result)
            assertTrue(result.status in setOf("success", "error"))
        }
    }
}
```

#### 6. Integration Testing
**Focus:** Testing complete workflows with real dependencies

```kotlin
class IntegrationTest {
    private lateinit var testDatabase: TestDatabase
    private lateinit var testCache: TestCache

    @BeforeEach
    fun setup() {
        testDatabase = TestDatabase.create()
        testCache = TestCache.create()
    }

    @AfterEach
    fun teardown() {
        testDatabase.cleanup()
        testCache.cleanup()
    }

    @Test
    fun `agent should execute complete workflow with real services`() {
        val agent = agent("user_registration") {
            instruction("Register new user")

            tool("validate_email") {
                implementation = RealEmailValidator()
            }

            tool("check_existing_user") {
                implementation = DatabaseUserChecker(testDatabase)
            }

            tool("create_user") {
                implementation = UserCreator(testDatabase)
            }

            tool("send_welcome_email") {
                implementation = EmailSender()
            }

            strategy {
                node("validate") {
                    tool("validate_email")
                }

                node("check") {
                    tool("check_existing_user")
                }

                decision("user_exists") {
                    yes() to node("error")
                    no() to node("create")
                }

                node("create") {
                    tool("create_user")
                }

                node("notify") {
                    tool("send_welcome_email")
                }

                node("error") {
                    returnError("User already exists")
                }
            }
        }

        // Execute with valid new user
        val result = agent.execute(mapOf(
            "email" to "newuser@example.com",
            "name" to "New User"
        ))

        assertEquals("success", result.status)

        // Verify database state
        val user = testDatabase.findUser("newuser@example.com")
        assertNotNull(user)
        assertEquals("New User", user.name)
    }
}
```

### Testing Strategy Graphs

#### Testing Node Execution Order

```kotlin
class StrategyGraphTest {
    @Test
    fun `strategy graph should execute nodes in correct order`() {
        val executionOrder = mutableListOf<String>()

        val agent = agent("graph_test") {
            strategy {
                node("start") {
                    action {
                        executionOrder.add("start")
                    }
                }

                node("middle") {
                    action {
                        executionOrder.add("middle")
                    }
                }

                node("end") {
                    action {
                        executionOrder.add("end")
                    }
                }

                edge(node("start") onAction to node("middle"))
                edge(node("middle") onAction to node("end"))
            }
        }

        agent.execute("test")

        assertEquals(listOf("start", "middle", "end"), executionOrder)
    }
}
```

#### Testing Parallel Execution

```kotlin
class ParallelExecutionTest {
    @Test
    fun `parallel nodes should execute concurrently`() = runTest {
        val startTimes = mutableMapOf<String, Long>()
        val endTimes = mutableMapOf<String, Long>()

        val agent = agent("parallel_test") {
            strategy {
                node("parallel") {
                    parallel(
                        listOf(
                            node("task_1") {
                                action {
                                    startTimes["task_1"] = System.currentTimeMillis()
                                    delay(100)
                                    endTimes["task_1"] = System.currentTimeMillis()
                                }
                            },
                            node("task_2") {
                                action {
                                    startTimes["task_2"] = System.currentTimeMillis()
                                    delay(100)
                                    endTimes["task_2"] = System.currentTimeMillis()
                                }
                            },
                            node("task_3") {
                                action {
                                    startTimes["task_3"] = System.currentTimeMillis()
                                    delay(100)
                                    endTimes["task_3"] = System.currentTimeMillis()
                                }
                            }
                        )
                    )
                }
            }
        }

        val totalStart = System.currentTimeMillis()
        agent.execute("test")
        val totalEnd = System.currentTimeMillis()

        // If parallel, total time should be ~100ms, not 300ms
        val totalTime = totalEnd - totalStart
        assertTrue(totalTime < 200, "Expected parallel execution in ~100ms, got ${totalTime}ms")

        // All tasks should overlap in time
        val maxStart = maxOf(startTimes.values.max(), 0L)
        val minEnd = minOf(endTimes.values.min(), Long.MAX_VALUE)
        assertTrue(maxStart < minEnd, "Tasks should overlap in execution")
    }
}
```

### Testing Multimodal Agents

```kotlin
class MultimodalAgentTest {
    @Test
    fun `agent should handle image input correctly`() {
        val mockLLM = MockLLMProvider()
        mockLLM.mockVisionResponse(
            "What's in this image?",
            "A red car in a parking lot"
        )

        val agent = agent("image_analyzer") {
            llmProvider = mockLLM
            instruction("Analyze images")

            capabilities {
                vision = true
            }
        }

        val result = agent.execute(
            userMessage {
                text("What's in this image?")
                attachment(ImageAttachment(
                    url = "https://example.com/test-image.jpg"
                ))
            }
        )

        assertTrue(result.contains("red car"))
    }

    @Test
    fun `agent should process document with structured output`() {
        val agent = agent("document_processor") {
            instruction("Extract structured data from documents")
        }

        @Serializable
        data class InvoiceData(
            val invoiceNumber: String,
            val amount: Double,
            val date: String,
            val vendor: String
        )

        val result = agent.executeStructured<InvoiceData>(
            userMessage {
                text("Extract invoice data")
                attachment(DocumentAttachment(
                    path = "test-invoice.pdf"
                ))
            }
        )

        assertNotNull(result.invoiceNumber)
        assertTrue(result.amount > 0)
        assertNotNull(result.vendor)
    }
}
```

### Testing Structured Output

```kotlin
class StructuredOutputTest {
    @Serializable
    data class UserAnalysis(
        @LLMDescription("User's primary intention")
        val intention: String,

        @LLMDescription("Sentiment score from -1 to 1")
        val sentimentScore: Double,

        @LLMDescription("Extracted entities")
        val entities: List<String>,

        @LLMDescription("Confidence level 0-100")
        val confidence: Int
    )

    @Test
    fun `agent should return valid structured output`() {
        val agent = agent("analyzer") {
            instruction("Analyze user input")
        }

        val result = agent.executeStructured<UserAnalysis>(
            "I really love this new product, it's amazing!"
        )

        // Validate structure
        assertNotNull(result.intention)
        assertTrue(result.sentimentScore in -1.0..1.0)
        assertTrue(result.confidence in 0..100)
        assertTrue(result.sentimentScore > 0.5) // Positive sentiment
    }

    @Test
    fun `agent should retry on invalid structured output`() {
        val mockLLM = MockLLMProvider()
        var callCount = 0

        mockLLM.onRequest { request ->
            callCount++
            when (callCount) {
                1 -> """{"invalid": "structure"}""" // Invalid
                2 -> """{"intention": "purchase", "sentimentScore": "invalid"}""" // Invalid
                else -> """{"intention": "purchase", "sentimentScore": 0.8, "entities": ["product"], "confidence": 90}""" // Valid
            }
        }

        val agent = agent("analyzer") {
            llmProvider = mockLLM
        }

        val result = agent.executeStructured<UserAnalysis>(
            "Test input",
            retryCount = 3
        )

        assertEquals(3, callCount) // Should retry until valid
        assertEquals("purchase", result.intention)
    }
}
```

### Testing Sessions and State

```kotlin
class SessionTest {
    @Test
    fun `session should maintain conversation history`() {
        val agent = agent("conversational") {
            instruction("You are a helpful assistant")
        }

        val session = agent.createWriteSession()

        // First exchange
        session.appendPrompt(UserMessage("My name is Alice"))
        val response1 = session.requestLLM()

        // Second exchange should remember context
        session.appendPrompt(UserMessage("What's my name?"))
        val response2 = session.requestLLM()

        assertTrue(response2.contains("Alice"))
    }

    @Test
    fun `session should compress history when needed`() {
        val agent = agent("long_conversation") {
            instruction("Maintain conversation")
        }

        val session = agent.createWriteSession()

        // Add many messages
        repeat(50) { i ->
            session.appendPrompt(UserMessage("Message $i"))
            session.requestLLM()
        }

        val messagesBefore = session.prompt.messages.size

        // Compress
        session.replaceHistoryWithTLDR()

        val messagesAfter = session.prompt.messages.size

        assertTrue(messagesAfter < messagesBefore)
        assertTrue(messagesAfter > 0) // Still has summary
    }
}
```

## Patterns and Best Practices

### Pattern 1: Test Data Builders

```kotlin
class AgentTestDataBuilder {
    private var instruction: String = "Default instruction"
    private var tools: MutableList<Tool> = mutableListOf()
    private var llmProvider: LLMProvider? = null

    fun withInstruction(instruction: String) = apply {
        this.instruction = instruction
    }

    fun withTool(tool: Tool) = apply {
        this.tools.add(tool)
    }

    fun withMockLLM(responses: Map<String, String>) = apply {
        this.llmProvider = MockLLMProvider().apply {
            responses.forEach { (prompt, response) ->
                mockResponse(prompt, response)
            }
        }
    }

    fun build() = agent("test_agent") {
        instruction(this@AgentTestDataBuilder.instruction)
        tools.forEach { tool(it) }
        llmProvider?.let { this.llmProvider = it }
    }
}

@Test
fun `using test data builder`() {
    val agent = AgentTestDataBuilder()
        .withInstruction("Classify sentiment")
        .withMockLLM(mapOf(
            "I love it" to "positive",
            "I hate it" to "negative"
        ))
        .build()

    assertEquals("positive", agent.execute("I love it"))
}
```

### Pattern 2: Assertion Helpers

```kotlin
object AgentAssertions {
    fun assertValidJSON(text: String) {
        assertDoesNotThrow {
            Json.parseToJsonElement(text)
        }
    }

    fun assertContainsToolCall(execution: AgentExecution, toolName: String) {
        assertTrue(
            execution.toolCalls.any { it.name == toolName },
            "Expected tool call to '$toolName' but found: ${execution.toolCalls.map { it.name }}"
        )
    }

    fun assertExecutionTime(maxMillis: Long, block: () -> Unit) {
        val start = System.currentTimeMillis()
        block()
        val duration = System.currentTimeMillis() - start
        assertTrue(
            duration <= maxMillis,
            "Expected execution in ${maxMillis}ms but took ${duration}ms"
        )
    }
}

@Test
fun `using assertion helpers`() {
    val agent = agent("test") {
        instruction("Return JSON")
    }

    val result = agent.execute("test")

    AgentAssertions.assertValidJSON(result)
    AgentAssertions.assertExecutionTime(1000) {
        agent.execute("test")
    }
}
```

### Pattern 3: Test Fixtures

```kotlin
class AgentTestFixtures {
    companion object {
        fun createMockDatabase(): Database {
            return InMemoryDatabase().apply {
                insertUser(User("user1", "alice@example.com"))
                insertUser(User("user2", "bob@example.com"))
            }
        }

        fun createMockCache(): Cache {
            return InMemoryCache().apply {
                set("key1", "value1")
                set("key2", "value2")
            }
        }

        fun createTestAgent(
            database: Database = createMockDatabase(),
            cache: Cache = createMockCache()
        ) = agent("fixture_agent") {
            tool("db_query") {
                implementation = DatabaseTool(database)
            }
            tool("cache_get") {
                implementation = CacheTool(cache)
            }
        }
    }
}
```

## Common Pitfalls

### Pitfall 1: Over-Mocking
**Problem:** Mocking too many components makes tests fragile and disconnected from reality.

```kotlin
// ✗ Bad: Everything mocked
@Test
fun overMockedTest() {
    val mockLLM = mockk<LLMProvider>()
    val mockTool1 = mockk<Tool>()
    val mockTool2 = mockk<Tool>()
    val mockStorage = mockk<Storage>()
    val mockValidator = mockk<Validator>()
    // ... test becomes maintenance nightmare
}

// ✓ Good: Mock only external dependencies
@Test
fun balancedMockingTest() {
    val mockLLM = mockk<LLMProvider>() // External, expensive
    val realValidator = EmailValidator() // Fast, deterministic
    val realStorage = InMemoryStorage() // Fast, isolated
}
```

### Pitfall 2: Non-Deterministic Tests
**Problem:** Tests that sometimes pass and sometimes fail.

```kotlin
// ✗ Bad: Relies on timing
@Test
fun flakyTest() {
    val agent = agent("test")
    val result = agent.execute("test")
    Thread.sleep(100) // Race condition
    assertEquals("expected", result)
}

// ✓ Good: Deterministic with proper synchronization
@Test
fun deterministicTest() = runBlockingTest {
    val agent = agent("test")
    val result = agent.execute("test").await()
    assertEquals("expected", result)
}
```

### Pitfall 3: Testing Implementation Instead of Behavior
**Problem:** Tests that are coupled to implementation details.

```kotlin
// ✗ Bad: Tests internal implementation
@Test
fun implementationTest() {
    val agent = agent("test")
    verify { agent.internalMethod() } // Fragile
}

// ✓ Good: Tests observable behavior
@Test
fun behaviorTest() {
    val agent = agent("classifier")
    val result = agent.execute("positive text")
    assertEquals("positive", result) // Public contract
}
```

### Pitfall 4: Insufficient Edge Case Coverage
**Problem:** Only testing happy paths.

```kotlin
// ✗ Bad: Only happy path
@Test
fun happyPathOnly() {
    val tool = EmailValidator()
    assertEquals(true, tool.validate("valid@email.com"))
}

// ✓ Good: Comprehensive edge cases
@Test
fun comprehensiveValidation() {
    val tool = EmailValidator()

    // Valid cases
    assertTrue(tool.validate("user@example.com"))
    assertTrue(tool.validate("user+tag@example.co.uk"))

    // Invalid cases
    assertFalse(tool.validate("invalid"))
    assertFalse(tool.validate("@example.com"))
    assertFalse(tool.validate("user@"))

    // Edge cases
    assertFalse(tool.validate(""))
    assertFalse(tool.validate("   "))
    assertDoesNotThrow { tool.validate(null) }
}
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-tool-integration](/home/user/agents/plugins/kotlin-koog-development/skills/koog-tool-integration/SKILL.md)
- Related skill: [koog-workflow-orchestration](/home/user/agents/plugins/kotlin-koog-development/skills/koog-workflow-orchestration/SKILL.md)
- [Koog Testing Documentation](https://docs.koog.ai/testing/)
- [Kotlin Test Framework](https://kotlinlang.org/api/latest/kotlin.test/)
- [MockK Documentation](https://mockk.io/)
- [Kotest Property Testing](https://kotest.io/docs/proptest/property-based-testing.html)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
