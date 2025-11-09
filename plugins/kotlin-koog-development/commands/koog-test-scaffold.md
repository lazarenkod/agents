---
name: koog-test-scaffold
description: Interactive scaffolding for comprehensive Koog agent test suites including unit tests, integration tests, performance tests, mocks, and CI/CD automation. Use to rapidly create production-ready test infrastructure with best practices built-in.
---

# Koog Test Scaffolding Command

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Purpose

Provides an interactive workflow for creating comprehensive test suites for Koog AI agents. Automatically generates unit tests, integration tests, mock strategies, performance tests, and CI/CD pipeline configurations with complete coverage patterns.

## Quick Start

```bash
/koog-test-scaffold
```

Follow the interactive prompts to customize your test suite.

## Configuration Options

### Test Suite Type
```bash
--type unit             # Unit tests only (fast, isolated)
--type integration      # Integration tests (tools, workflows)
--type e2e              # End-to-end tests (full agent scenarios)
--type performance      # Performance and load tests
--type all              # Complete test suite (default)
```

### Test Framework
```bash
--framework junit5      # JUnit 5 (default, recommended)
--framework kotest      # Kotest for Kotlin-idiomatic tests
--framework spek        # Spek for BDD-style tests
```

### Mock Strategy
```bash
--mocking mockk         # MockK (default, Kotlin-friendly)
--mocking mockito       # Mockito (Java-style mocking)
--mocking none          # No mocking framework
```

### CI/CD Integration
```bash
--ci github             # GitHub Actions workflow
--ci gitlab             # GitLab CI pipeline
--ci jenkins            # Jenkins pipeline
--ci circleci           # CircleCI configuration
--ci none               # No CI configuration
```

### Coverage Tools
```bash
--coverage jacoco       # JaCoCo coverage (default)
--coverage kover        # Kover (Kotlin-native coverage)
--coverage both         # Both JaCoCo and Kover
```

### Project Configuration
```bash
--agent-path <path>              # Path to agent source code (required)
--test-path <path>               # Output path for tests (default: src/test)
--include-fixtures               # Include test data fixtures (default: true)
--include-testcontainers         # Include TestContainers setup (default: false)
--include-performance            # Include performance test suite (default: false)
--parallel-execution             # Enable parallel test execution (default: true)
```

## Execution Workflow

This command orchestrates test scaffolding through multiple specialized phases using the **koog-testing-specialist** agent.

### Phase 1: Test Strategy Planning

**Goal**: Analyze agent architecture and design comprehensive test strategy

**Actions**:
1. Analyze agent source code structure
2. Identify agent type (basic, functional, workflow)
3. Inventory all tools and external dependencies
4. Assess complexity and test coverage needs
5. Design test pyramid (unit, integration, e2e ratios)
6. Plan mock strategies for external systems

**Output**: Test strategy document with coverage plan

**Agent**: koog-testing-specialist (Haiku)

**Example Strategy**:
```yaml
Test Strategy:
  Agent Type: workflow_agent
  Tools Identified: 3 (database, API, queue)
  Test Distribution:
    Unit Tests: 60% (tool logic, validation)
    Integration Tests: 30% (workflow, tool integration)
    E2E Tests: 10% (complete scenarios)
  Mock Requirements:
    - Database: TestContainers PostgreSQL
    - External API: MockK with fixed responses
    - Message Queue: In-memory test queue
  Coverage Target: 85%
```

### Phase 2: Unit Test Generation

**Goal**: Generate unit tests for agent logic and tools

**Actions**:
1. Create test class structure matching source organization
2. Generate tests for each agent decision point
3. Create tool function tests with parameter validation
4. Add input/output validation tests
5. Generate error handling and edge case tests
6. Create state management tests (if applicable)

**Output**: Complete unit test suite with MockK setup

**Agent**: koog-testing-specialist (Haiku)

**Example Output**:
```kotlin
// test/kotlin/agents/SentimentAgentTest.kt
import ai.koog.agent
import io.mockk.*
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeEach
import kotlin.test.assertEquals

class SentimentAgentTest {

    private lateinit var mockLLMClient: LLMClient

    @BeforeEach
    fun setup() {
        mockLLMClient = mockk()
    }

    @Test
    fun `should classify positive sentiment correctly`() {
        // Given
        every { mockLLMClient.complete(any()) } returns
            LLMResponse("positive", Usage(10, 2))

        val agent = createSentimentAgent(mockLLMClient)

        // When
        val result = agent.run("I love this product!")

        // Then
        assertEquals("positive", result.trim())
        verify(exactly = 1) { mockLLMClient.complete(any()) }
    }

    @Test
    fun `should handle empty input with validation error`() {
        // Given
        val agent = createSentimentAgent()

        // When/Then
        assertThrows<IllegalArgumentException> {
            agent.run("")
        }
    }

    @Test
    fun `should classify negative sentiment correctly`() {
        // Given
        every { mockLLMClient.complete(any()) } returns
            LLMResponse("negative", Usage(12, 2))

        val agent = createSentimentAgent(mockLLMClient)

        // When
        val result = agent.run("This is terrible and broken")

        // Then
        assertEquals("negative", result.trim())
    }
}
```

### Phase 3: Integration Test Generation

**Goal**: Create integration tests for agent workflows and tool interactions

**Actions**:
1. Generate workflow orchestration tests
2. Create tool integration tests with real/mock backends
3. Add strategy graph execution tests
4. Create multi-tool coordination tests
5. Generate event handling tests
6. Add TestContainers configuration (if needed)

**Output**: Integration test suite with infrastructure setup

**Agent**: koog-testing-specialist (Haiku)

**Example Output**:
```kotlin
// test/kotlin/agents/OrderProcessingIntegrationTest.kt
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers
import org.junit.jupiter.api.Test

@Testcontainers
class OrderProcessingIntegrationTest {

    @Container
    private val postgres = PostgreSQLContainer<Nothing>("postgres:15").apply {
        withDatabaseName("test_orders")
        withUsername("test")
        withPassword("test")
    }

    @Test
    fun `should process order through complete workflow`() {
        // Given
        val dataSource = createDataSource(postgres)
        val agent = createOrderProcessingAgent(dataSource)

        val order = """
            {
                "items": [{"id": "p1", "quantity": 2}],
                "total": 99.99,
                "paymentMethod": "credit_card"
            }
        """

        // When
        val result = agent.run(order)

        // Then
        assertContains(result, "order_id")
        assertContains(result, "confirmed")

        // Verify database state
        val orderRecord = queryOrder(dataSource, extractOrderId(result))
        assertEquals("CONFIRMED", orderRecord.status)
    }
}
```

### Phase 4: Mock Strategy Implementation

**Goal**: Set up sophisticated mocking infrastructure

**Actions**:
1. Create mock factories for external dependencies
2. Generate realistic test data fixtures
3. Set up API response mocking
4. Create database mock/container configuration
5. Implement LLM response mocking
6. Add time and randomness mocking

**Output**: Mock utilities and test fixtures

**Agent**: koog-testing-specialist (Haiku)

**Example Output**:
```kotlin
// test/kotlin/mocks/TestFixtures.kt
object TestFixtures {

    fun mockLLMClient(responses: List<String>): LLMClient {
        val mock = mockk<LLMClient>()
        val iterator = responses.iterator()

        every { mock.complete(any()) } answers {
            LLMResponse(
                text = if (iterator.hasNext()) iterator.next() else "default",
                usage = Usage(promptTokens = 10, completionTokens = 5)
            )
        }

        return mock
    }

    fun createTestOrder(
        id: String = "order_${UUID.randomUUID()}",
        total: Double = 99.99,
        status: String = "PENDING"
    ): Order = Order(
        id = id,
        items = listOf(
            OrderItem("product_1", quantity = 2, price = 49.995)
        ),
        total = total,
        status = status,
        createdAt = Instant.now()
    )

    fun mockPaymentService(shouldSucceed: Boolean = true): PaymentService {
        val mock = mockk<PaymentService>()

        every { mock.charge(any(), any()) } returns
            if (shouldSucceed) {
                PaymentResult.Success("txn_${UUID.randomUUID()}")
            } else {
                PaymentResult.Failed("Insufficient funds")
            }

        return mock
    }
}
```

### Phase 5: Performance Test Setup

**Goal**: Create performance and load testing infrastructure

**Actions**:
1. Generate latency measurement tests
2. Create throughput tests (requests per second)
3. Add concurrent execution tests
4. Generate memory usage tests
5. Create token usage tracking tests
6. Set up load testing scripts (K6/Gatling)

**Output**: Performance test suite and benchmarking tools

**Agent**: koog-testing-specialist (Haiku)

**Example Output**:
```kotlin
// test/kotlin/performance/AgentPerformanceTest.kt
import kotlin.system.measureTimeMillis
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Tag
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking

@Tag("performance")
class AgentPerformanceTest {

    @Test
    fun `agent should respond within 500ms latency budget`() {
        // Given
        val agent = createProductionAgent()
        val maxLatency = 500L

        // When
        val latency = measureTimeMillis {
            agent.run("Classify sentiment: This is great!")
        }

        // Then
        assertTrue(latency < maxLatency,
            "Agent took ${latency}ms, budget was ${maxLatency}ms")
    }

    @Test
    fun `agent should handle 100 concurrent requests`() = runBlocking {
        // Given
        val agent = createProductionAgent()
        val requests = 100

        // When
        val startTime = System.currentTimeMillis()

        val results = (1..requests).map { i ->
            async {
                agent.run("Request $i")
            }
        }.awaitAll()

        val duration = System.currentTimeMillis() - startTime
        val throughput = (requests * 1000.0) / duration

        // Then
        assertEquals(requests, results.size)
        assertTrue(results.all { it.isNotEmpty() })
        println("Throughput: ${"%.2f".format(throughput)} req/sec")
        assertTrue(throughput > 50.0, "Expected > 50 req/sec, got $throughput")
    }
}
```

### Phase 6: CI/CD Pipeline Configuration

**Goal**: Set up automated test execution in CI/CD

**Actions**:
1. Generate CI workflow configuration
2. Add test execution jobs (unit, integration, performance)
3. Configure coverage report generation
4. Set up test result publishing
5. Add failure notifications
6. Configure test caching for speed

**Output**: Complete CI/CD pipeline configuration

**Agent**: koog-testing-specialist (Haiku)

**Example Output**:
```yaml
# .github/workflows/test.yml
name: Koog Agent Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Cache Gradle packages
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}

      - name: Run Unit Tests
        run: ./gradlew test --parallel

      - name: Generate Coverage Report
        run: ./gradlew jacocoTestReport

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: build/reports/jacoco/test/jacocoTestReport.xml
          fail_ci_if_error: true

  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run Integration Tests
        run: ./gradlew integrationTest
        env:
          DB_URL: postgresql://localhost:5432/test_db
          DB_USER: test
          DB_PASSWORD: test

      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: build/test-results/**/*.xml
```

## Execution Parameters

### Required Parameters
- `agent-path`: Path to the agent source code directory
- `agent-type`: Type of agent (basic, functional, workflow)

### Optional Parameters
- `test-path`: Output directory for tests (default: `src/test`)
- `coverage-target`: Minimum coverage percentage (default: 80)
- `framework`: Test framework choice (default: junit5)
- `mocking`: Mocking library (default: mockk)
- `ci`: CI/CD platform (default: github)
- `include-fixtures`: Generate test data fixtures (default: true)
- `include-performance`: Include performance tests (default: false)
- `parallel-execution`: Enable parallel test execution (default: true)

## Success Criteria

### Test Suite Quality
- ✓ 80%+ code coverage achieved
- ✓ All agent decision paths tested
- ✓ Tool integration tests passing
- ✓ Edge cases and error scenarios covered
- ✓ Mock strategies properly isolated
- ✓ Tests run in < 5 minutes locally

### Test Organization
- ✓ Clear test class naming and structure
- ✓ Descriptive test method names (BDD style)
- ✓ Proper setup/teardown lifecycle
- ✓ Independent, non-flaky tests
- ✓ Test fixtures well-organized
- ✓ Performance tests properly tagged

### CI/CD Integration
- ✓ Tests run automatically on PR/push
- ✓ Coverage reports generated and tracked
- ✓ Test results published and visible
- ✓ Failures trigger notifications
- ✓ Test execution parallelized
- ✓ Dependencies cached for speed

## Example Use Cases

### Use Case 1: Basic Agent Test Suite
```bash
/koog-test-scaffold \
  --agent-path src/main/kotlin/agents/SentimentAgent.kt \
  --type all \
  --framework junit5 \
  --mocking mockk \
  --ci github
```

**Generated**:
- Unit tests for sentiment classification logic
- Mock LLM client for deterministic tests
- Input validation tests
- Error handling tests
- GitHub Actions workflow

### Use Case 2: Workflow Agent with Database
```bash
/koog-test-scaffold \
  --agent-path src/main/kotlin/agents/OrderProcessor.kt \
  --type all \
  --include-testcontainers \
  --include-performance \
  --ci gitlab
```

**Generated**:
- Unit tests for workflow nodes
- Integration tests with TestContainers PostgreSQL
- Workflow orchestration tests
- Performance tests for throughput
- GitLab CI pipeline configuration

### Use Case 3: Performance-Critical Agent
```bash
/koog-test-scaffold \
  --agent-path src/main/kotlin/agents/RealtimeAnalyzer.kt \
  --type performance \
  --include-performance \
  --coverage-target 90
```

**Generated**:
- Latency measurement tests
- Concurrent execution tests
- Memory usage tests
- Token consumption tracking
- Load testing scripts

## Integration with Other Plugins

### kotlin-koog-development
- Works with `koog-agent-scaffold` for full project setup
- Complements `koog-production-deploy` for production readiness

### backend-development
- Integrates with `api-testing` for REST endpoint testing
- Shares patterns with `database-testing` for data layer tests

### devops-automation
- CI/CD configurations compatible with infrastructure pipelines
- Test results integrate with monitoring dashboards

## Troubleshooting

**Q: Tests fail with "Cannot resolve agent class"**
A: Ensure `agent-path` points to the correct source directory. Check that the agent is compiled before running tests.

**Q: MockK fails with verification errors**
A: Verify mock setup in `@BeforeEach`. Ensure `every` blocks match actual invocations. Use `relaxed = true` for lenient mocking.

**Q: TestContainers fail to start**
A: Ensure Docker is running. Check Docker daemon accessibility. Verify container image availability.

**Q: Coverage is lower than expected**
A: Review uncovered branches with coverage report. Add tests for error paths. Test private methods through public API.

**Q: Tests are slow (> 5 minutes)**
A: Enable parallel execution. Use in-memory databases instead of containers for unit tests. Cache dependencies in CI.

**Q: Flaky tests failing intermittently**
A: Remove timing dependencies. Use deterministic mocks. Avoid shared state between tests. Fix race conditions.

## Next Steps After Scaffolding

1. **Review Generated Tests** — Understand test coverage and patterns
2. **Customize Test Data** — Update fixtures with realistic scenarios
3. **Run Test Suite** — Execute locally and verify all tests pass
4. **Integrate CI/CD** — Push to repository and verify pipeline execution
5. **Monitor Coverage** — Track coverage trends over time
6. **Add Scenarios** — Expand tests for new features and edge cases
7. **Performance Baseline** — Establish performance benchmarks
8. **Document Tests** — Explain complex test scenarios in comments
