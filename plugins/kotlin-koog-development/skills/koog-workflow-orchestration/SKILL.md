---
name: koog-workflow-orchestration
description: Advanced workflow orchestration with strategy graphs, parallel execution, data transfer between nodes, conditional routing, and complex agent coordination. Use when designing multi-step workflows, implementing agentic loops, coordinating parallel tasks, managing data flow between nodes, or building complex decision trees.
---

# Koog Workflow Orchestration

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Designing complex multi-step agent workflows
- Implementing agentic loops and iterative refinement
- Orchestrating parallel task execution
- Managing data transfer between workflow nodes
- Building conditional routing and decision trees
- Creating state machines with AI agents
- Implementing error recovery strategies
- Coordinating multiple agents in workflows
- Building event-driven agent systems
- Creating adaptive workflows based on runtime conditions

## Core Concepts

### Strategy Graph Fundamentals

#### Basic Linear Workflow

```kotlin
import ai.koog.agent
import ai.koog.strategy.*

val linearWorkflow = agent("linear_processor") {
    instruction("Process data through sequential steps")

    strategy {
        // Step 1: Fetch data
        node("fetch") {
            tool("fetch_data") {
                // Fetch from API
            }
        }

        // Step 2: Transform data
        node("transform") {
            tool("transform_data") {
                // Process and clean
            }
        }

        // Step 3: Validate data
        node("validate") {
            tool("validate_data") {
                // Check quality
            }
        }

        // Step 4: Store data
        node("store") {
            tool("store_data") {
                // Save to database
            }
        }

        // Define edges (flow)
        edge(node("fetch") onToolResult to node("transform"))
        edge(node("transform") onToolResult to node("validate"))
        edge(node("validate") onToolResult to node("store"))
    }
}
```

#### Conditional Branching Workflow

```kotlin
val conditionalWorkflow = agent("conditional_processor") {
    instruction("Route requests based on analysis")

    strategy {
        // Analyze input
        node("analyze") {
            nodeLLMRequest(
                instruction = "Analyze the input and determine priority: high, medium, or low"
            )
        }

        // Branch based on priority
        decision("priority_router") {
            condition { response ->
                response.contains("high", ignoreCase = true)
            } to node("urgent_handler")

            condition { response ->
                response.contains("medium", ignoreCase = true)
            } to node("standard_handler")

            default() to node("low_priority_handler")
        }

        // Handler nodes
        node("urgent_handler") {
            tool("process_urgent")
        }

        node("standard_handler") {
            tool("process_standard")
        }

        node("low_priority_handler") {
            tool("process_low_priority")
        }

        // Define edges
        edge(node("analyze") onAssistantMessage to decision("priority_router"))
    }
}
```

#### Iterative Refinement Loop

```kotlin
val iterativeAgent = agent("iterative_researcher") {
    instruction("Research topics iteratively until complete understanding achieved")

    strategy {
        // Initial research
        node("initial_search") {
            nodeLLMRequest(
                instruction = "Search for information on the topic"
            )
            tool("web_search")
        }

        // Analyze completeness
        node("analyze_completeness") {
            nodeLLMRequest(
                instruction = """
                    Analyze the research findings.
                    Respond with:
                    - "COMPLETE" if findings are comprehensive
                    - "INCOMPLETE: <what's missing>" if more research needed
                """
            )
        }

        // Decision: continue or finish
        decision("is_complete") {
            condition { response ->
                response.contains("COMPLETE", ignoreCase = true)
            } to node("compile_report")

            condition { response ->
                storage.get<Int>("iterations") ?: 0 < 3
            } to node("additional_search")

            default() to node("compile_report")
        }

        // Additional research
        node("additional_search") {
            action {
                val iterations = storage.get<Int>("iterations") ?: 0
                storage.set("iterations", iterations + 1)
            }

            nodeLLMRequest(
                instruction = "Based on gaps, search for more specific information"
            )
            tool("web_search")
        }

        // Final compilation
        node("compile_report") {
            nodeLLMRequest(
                instruction = "Compile comprehensive final report"
            )
        }

        // Define edges
        edge(node("initial_search") onAssistantMessage to node("analyze_completeness"))
        edge(node("analyze_completeness") onAssistantMessage to decision("is_complete"))
        edge(node("additional_search") onAssistantMessage to node("analyze_completeness"))
    }
}
```

### Parallel Execution Patterns

#### Parallel Tool Execution

```kotlin
val parallelAgent = agent("parallel_data_gatherer") {
    instruction("Gather data from multiple sources simultaneously")

    strategy {
        node("parallel_fetch") {
            parallel(
                listOf(
                    node("fetch_database") {
                        tool("query_database")
                    },
                    node("fetch_api") {
                        tool("call_external_api")
                    },
                    node("fetch_cache") {
                        tool("get_from_cache")
                    },
                    node("fetch_search") {
                        tool("web_search")
                    }
                ),
                mergeStrategy = MergeStrategy.Combine { results ->
                    // Combine all results into single context
                    results.flatten()
                }
            )
        }

        node("analyze_combined") {
            nodeLLMRequest(
                instruction = "Analyze all gathered data and create unified response"
            )
        }

        edge(node("parallel_fetch") onComplete to node("analyze_combined"))
    }
}
```

#### Parallel with Conditional Merge

```kotlin
val smartParallelAgent = agent("smart_parallel") {
    strategy {
        node("parallel_analysis") {
            parallel(
                listOf(
                    node("analyze_sentiment") {
                        nodeLLMRequest(instruction = "Analyze sentiment")
                    },
                    node("extract_entities") {
                        nodeLLMRequest(instruction = "Extract entities")
                    },
                    node("classify_intent") {
                        nodeLLMRequest(instruction = "Classify intent")
                    }
                ),
                mergeStrategy = MergeStrategy.SelectByMax { result ->
                    // Select result with highest confidence
                    result.metadata["confidence"] as? Double ?: 0.0
                }
            )
        }
    }
}
```

#### Racing Parallel Nodes

```kotlin
val racingAgent = agent("racing_fetcher") {
    instruction("Use fastest data source")

    strategy {
        node("race_sources") {
            parallel(
                listOf(
                    node("source_a") {
                        tool("fetch_from_source_a")
                    },
                    node("source_b") {
                        tool("fetch_from_source_b")
                    },
                    node("source_c") {
                        tool("fetch_from_source_c")
                    }
                ),
                mergeStrategy = MergeStrategy.FirstToComplete()
                // Returns as soon as first source completes
            )
        }
    }
}
```

### Data Transfer Between Nodes

#### Using Storage for Data Flow

```kotlin
import ai.koog.storage.*

// Define type-safe storage keys
val userDataKey = createStorageKey<UserData>("user_data")
val analysisResultKey = createStorageKey<AnalysisResult>("analysis_result")
val recommendationsKey = createStorageKey<List<String>>("recommendations")

val dataFlowAgent = agent("data_flow_example") {
    strategy {
        // Node 1: Fetch and store user data
        node("fetch_user") {
            action {
                val userId = input.get("user_id") as String
                val userData = fetchUserData(userId)

                // Store for later nodes
                storage.set(userDataKey, userData)
            }
        }

        // Node 2: Analyze using stored data
        node("analyze_user") {
            action {
                // Retrieve stored data
                val userData = storage.getValue(userDataKey)

                val analysis = analyzeUserBehavior(userData)

                // Store analysis result
                storage.set(analysisResultKey, analysis)
            }
        }

        // Node 3: Generate recommendations
        node("generate_recommendations") {
            action {
                val userData = storage.getValue(userDataKey)
                val analysis = storage.getValue(analysisResultKey)

                val recommendations = generateRecommendations(userData, analysis)

                // Store recommendations
                storage.set(recommendationsKey, recommendations)
            }
        }

        // Node 4: Format final response
        node("format_response") {
            action {
                val recommendations = storage.getValue(recommendationsKey)
                formatResponse(recommendations)
            }
        }

        // Define flow
        edge(node("fetch_user") onAction to node("analyze_user"))
        edge(node("analyze_user") onAction to node("generate_recommendations"))
        edge(node("generate_recommendations") onAction to node("format_response"))
    }
}
```

#### Context Accumulation Pattern

```kotlin
val contextAccumulatorAgent = agent("context_accumulator") {
    strategy {
        node("step_1") {
            action {
                val result = performStep1()
                storage.set("step_1_result", result)
                storage.set("context", listOf("Step 1 completed: $result"))
            }
        }

        node("step_2") {
            action {
                val step1Result = storage.get<String>("step_1_result")
                val result = performStep2(step1Result)

                storage.set("step_2_result", result)

                // Accumulate context
                val context = storage.get<List<String>>("context") ?: emptyList()
                storage.set("context", context + "Step 2 completed: $result")
            }
        }

        node("step_3") {
            action {
                val step2Result = storage.get<String>("step_2_result")
                val result = performStep3(step2Result)

                // Accumulate context
                val context = storage.get<List<String>>("context") ?: emptyList()
                storage.set("context", context + "Step 3 completed: $result")
            }
        }

        node("final_synthesis") {
            nodeLLMRequest {
                val fullContext = storage.get<List<String>>("context") ?: emptyList()
                instruction = """
                    Synthesize final response using accumulated context:
                    ${fullContext.joinToString("\n")}
                """
            }
        }
    }
}
```

### Complex Decision Trees

#### Multi-Level Decision Tree

```kotlin
val multiLevelDecisionAgent = agent("multi_level_router") {
    strategy {
        // Level 1: Classify request type
        node("classify_type") {
            nodeLLMRequest(
                instruction = "Classify request as: technical, business, or personal"
            )
        }

        decision("type_router") {
            condition { it.contains("technical") } to node("classify_technical_severity")
            condition { it.contains("business") } to node("classify_business_priority")
            condition { it.contains("personal") } to node("handle_personal")
            default() to node("handle_unknown")
        }

        // Level 2a: Technical severity
        node("classify_technical_severity") {
            nodeLLMRequest(
                instruction = "Classify technical issue severity: critical, high, medium, low"
            )
        }

        decision("technical_severity_router") {
            condition { it.contains("critical") } to node("handle_critical_technical")
            condition { it.contains("high") } to node("handle_high_technical")
            default() to node("handle_standard_technical")
        }

        // Level 2b: Business priority
        node("classify_business_priority") {
            nodeLLMRequest(
                instruction = "Classify business priority: urgent, important, routine"
            )
        }

        decision("business_priority_router") {
            condition { it.contains("urgent") } to node("handle_urgent_business")
            condition { it.contains("important") } to node("handle_important_business")
            default() to node("handle_routine_business")
        }

        // Handler nodes
        node("handle_critical_technical") { /* ... */ }
        node("handle_high_technical") { /* ... */ }
        node("handle_standard_technical") { /* ... */ }
        node("handle_urgent_business") { /* ... */ }
        node("handle_important_business") { /* ... */ }
        node("handle_routine_business") { /* ... */ }
        node("handle_personal") { /* ... */ }
        node("handle_unknown") { /* ... */ }

        // Define edges
        edge(node("classify_type") onAssistantMessage to decision("type_router"))
        edge(node("classify_technical_severity") onAssistantMessage to decision("technical_severity_router"))
        edge(node("classify_business_priority") onAssistantMessage to decision("business_priority_router"))
    }
}
```

### Error Handling and Recovery

#### Graceful Error Recovery

```kotlin
val resilientWorkflow = agent("resilient_workflow") {
    strategy {
        node("risky_operation") {
            tool("unreliable_api") {
                onError { error ->
                    logger.warn("API failed: ${error.message}")
                    storage.set("error_count", (storage.get<Int>("error_count") ?: 0) + 1)

                    // Branch to error handler
                    node("error_handler")
                }
            }
        }

        node("error_handler") {
            action {
                val errorCount = storage.get<Int>("error_count") ?: 0

                when {
                    errorCount < 3 -> {
                        // Retry with backoff
                        delay((errorCount * 1000).toLong())
                        node("risky_operation")
                    }
                    else -> {
                        // Use fallback
                        node("fallback_operation")
                    }
                }
            }
        }

        node("fallback_operation") {
            tool("fallback_api")
        }

        node("success_handler") {
            // Process successful result
        }

        edge(node("risky_operation") onToolResult to node("success_handler"))
    }
}
```

#### Timeout and Circuit Breaker

```kotlin
val timeoutWorkflow = agent("timeout_workflow") {
    strategy {
        node("timed_operation") {
            action {
                withTimeout(5.seconds) {
                    try {
                        tool("slow_operation").execute()
                    } catch (e: TimeoutCancellationException) {
                        logger.warn("Operation timed out")
                        storage.set("timed_out", true)
                        node("timeout_handler")
                    }
                }
            }
        }

        decision("check_timeout") {
            condition { storage.get<Boolean>("timed_out") == true } to node("timeout_handler")
            default() to node("normal_flow")
        }

        node("timeout_handler") {
            // Handle timeout - maybe use cached data
            tool("use_cached_data")
        }

        node("normal_flow") {
            // Continue normal processing
        }
    }
}
```

### Multi-Agent Orchestration

#### Agent Delegation Pattern

```kotlin
// Orchestrator agent that delegates to specialized agents
val orchestratorAgent = agent("orchestrator") {
    instruction("""
        You are an orchestrator. Analyze requests and delegate to specialist agents:
        - Technical questions → technical_expert
        - Business questions → business_analyst
        - Creative tasks → creative_writer
    """)

    strategy {
        node("analyze_request") {
            nodeLLMRequest(
                instruction = "Analyze request and decide which specialist agent to use"
            )
        }

        decision("delegate") {
            condition { it.contains("technical_expert") } to node("call_technical_expert")
            condition { it.contains("business_analyst") } to node("call_business_analyst")
            condition { it.contains("creative_writer") } to node("call_creative_writer")
            default() to node("handle_general")
        }

        node("call_technical_expert") {
            action {
                val response = technicalExpertAgent.execute(input)
                storage.set("specialist_response", response)
            }
        }

        node("call_business_analyst") {
            action {
                val response = businessAnalystAgent.execute(input)
                storage.set("specialist_response", response)
            }
        }

        node("call_creative_writer") {
            action {
                val response = creativeWriterAgent.execute(input)
                storage.set("specialist_response", response)
            }
        }

        node("handle_general") {
            nodeLLMRequest(instruction = "Handle general request")
        }

        node("synthesize_response") {
            action {
                val specialistResponse = storage.get<String>("specialist_response")
                formatFinalResponse(specialistResponse)
            }
        }

        edge(node("analyze_request") onAssistantMessage to decision("delegate"))
        edge(node("call_technical_expert") onAction to node("synthesize_response"))
        edge(node("call_business_analyst") onAction to node("synthesize_response"))
        edge(node("call_creative_writer") onAction to node("synthesize_response"))
    }
}
```

#### Collaborative Multi-Agent Pattern

```kotlin
val collaborativeWorkflow = agent("collaborative") {
    strategy {
        // Parallel consultation with multiple agents
        node("consult_experts") {
            parallel(
                listOf(
                    node("technical_perspective") {
                        action {
                            val response = technicalAgent.execute(input)
                            storage.set("technical_view", response)
                        }
                    },
                    node("business_perspective") {
                        action {
                            val response = businessAgent.execute(input)
                            storage.set("business_view", response)
                        }
                    },
                    node("user_perspective") {
                        action {
                            val response = uxAgent.execute(input)
                            storage.set("ux_view", response)
                        }
                    }
                )
            )
        }

        node("synthesize_perspectives") {
            nodeLLMRequest {
                val technical = storage.get<String>("technical_view")
                val business = storage.get<String>("business_view")
                val ux = storage.get<String>("ux_view")

                instruction = """
                    Synthesize these expert perspectives into cohesive recommendation:

                    Technical: $technical
                    Business: $business
                    UX: $ux
                """
            }
        }

        edge(node("consult_experts") onComplete to node("synthesize_perspectives"))
    }
}
```

### Dynamic Workflow Construction

#### Runtime Workflow Generation

```kotlin
class DynamicWorkflowBuilder {

    fun buildWorkflow(config: WorkflowConfig): Agent {
        return agent("dynamic_workflow") {
            instruction(config.instruction)

            strategy {
                val nodes = buildNodes(config.steps)
                val edges = buildEdges(config.steps, nodes)

                nodes.forEach { addNode(it) }
                edges.forEach { addEdge(it) }
            }
        }
    }

    private fun buildNodes(steps: List<WorkflowStep>): List<Node> {
        return steps.map { step ->
            when (step.type) {
                StepType.LLM -> node(step.id) {
                    nodeLLMRequest(instruction = step.instruction)
                }

                StepType.TOOL -> node(step.id) {
                    tool(step.toolName)
                }

                StepType.DECISION -> decision(step.id) {
                    step.conditions.forEach { condition ->
                        condition(condition.predicate) to node(condition.targetNode)
                    }
                }

                StepType.PARALLEL -> node(step.id) {
                    parallel(step.parallelNodes.map { node(it) })
                }
            }
        }
    }

    private fun buildEdges(steps: List<WorkflowStep>, nodes: List<Node>): List<Edge> {
        return steps.flatMap { step ->
            step.nextSteps.map { nextId ->
                edge(node(step.id) to node(nextId))
            }
        }
    }
}

// Usage
val config = WorkflowConfig(
    instruction = "Process customer requests",
    steps = listOf(
        WorkflowStep(id = "analyze", type = StepType.LLM, nextSteps = listOf("route")),
        WorkflowStep(id = "route", type = StepType.DECISION, nextSteps = listOf("handle_a", "handle_b")),
        WorkflowStep(id = "handle_a", type = StepType.TOOL, toolName = "handler_a"),
        WorkflowStep(id = "handle_b", type = StepType.TOOL, toolName = "handler_b")
    )
)

val workflow = DynamicWorkflowBuilder().buildWorkflow(config)
```

### Advanced Patterns

#### State Machine Pattern

```kotlin
enum class State {
    INITIAL, PROCESSING, VALIDATING, COMPLETED, FAILED
}

val stateMachineAgent = agent("state_machine") {
    strategy {
        node("initial") {
            action {
                storage.set("state", State.INITIAL)
            }
        }

        decision("state_router") {
            condition { storage.get<State>("state") == State.INITIAL } to node("start_processing")
            condition { storage.get<State>("state") == State.PROCESSING } to node("validate")
            condition { storage.get<State>("state") == State.VALIDATING } to node("check_validation")
            condition { storage.get<State>("state") == State.COMPLETED } to node("finalize")
            condition { storage.get<State>("state") == State.FAILED } to node("handle_failure")
        }

        node("start_processing") {
            action {
                processData()
                storage.set("state", State.PROCESSING)
                node("state_router")
            }
        }

        node("validate") {
            action {
                validateData()
                storage.set("state", State.VALIDATING)
                node("state_router")
            }
        }

        node("check_validation") {
            action {
                if (isValid()) {
                    storage.set("state", State.COMPLETED)
                } else {
                    storage.set("state", State.FAILED)
                }
                node("state_router")
            }
        }

        node("finalize") {
            // Complete workflow
        }

        node("handle_failure") {
            // Handle failure
        }
    }
}
```

#### Event-Driven Workflow

```kotlin
class EventDrivenAgent(private val eventBus: EventBus) {

    val agent = agent("event_driven") {
        strategy {
            node("listen_for_events") {
                action {
                    val event = eventBus.waitForEvent()
                    storage.set("current_event", event)
                }
            }

            decision("route_event") {
                condition {
                    storage.get<Event>("current_event")?.type == EventType.USER_ACTION
                } to node("handle_user_action")

                condition {
                    storage.get<Event>("current_event")?.type == EventType.SYSTEM_EVENT
                } to node("handle_system_event")

                condition {
                    storage.get<Event>("current_event")?.type == EventType.ERROR
                } to node("handle_error")
            }

            node("handle_user_action") {
                action {
                    val event = storage.get<Event>("current_event")!!
                    processUserAction(event)

                    // Continue listening
                    node("listen_for_events")
                }
            }

            node("handle_system_event") {
                action {
                    val event = storage.get<Event>("current_event")!!
                    processSystemEvent(event)

                    node("listen_for_events")
                }
            }

            node("handle_error") {
                action {
                    val event = storage.get<Event>("current_event")!!
                    handleError(event)

                    node("listen_for_events")
                }
            }

            edge(node("listen_for_events") onAction to decision("route_event"))
        }
    }
}
```

## Patterns and Best Practices

### Pattern 1: Workflow Visualization

```kotlin
class WorkflowVisualizer {
    fun visualize(agent: Agent): String {
        val graph = agent.strategy.graph

        return buildString {
            appendLine("Workflow: ${agent.name}")
            appendLine("=" repeat 50)

            graph.nodes.forEach { node ->
                appendLine("Node: ${node.id}")
                val outgoingEdges = graph.edges.filter { it.from == node }
                outgoingEdges.forEach { edge ->
                    appendLine("  -> ${edge.to.id} (${edge.condition})")
                }
            }
        }
    }
}
```

### Pattern 2: Workflow Testing

```kotlin
class WorkflowTester {
    suspend fun testWorkflow(agent: Agent, testCases: List<TestCase>): TestResults {
        val results = testCases.map { testCase ->
            val result = agent.execute(testCase.input)

            TestResult(
                input = testCase.input,
                expected = testCase.expected,
                actual = result,
                passed = result == testCase.expected,
                nodesVisited = extractVisitedNodes(agent)
            )
        }

        return TestResults(results)
    }

    private fun extractVisitedNodes(agent: Agent): List<String> {
        // Track which nodes were executed
        return agent.executionTrace.map { it.nodeId }
    }
}
```

### Pattern 3: Monitoring and Observability

```kotlin
class WorkflowMonitor(private val agent: Agent) {

    fun attachMonitoring() {
        agent.addFeatureMessageProcessor(object : FeatureMessageProcessor {
            override fun process(message: FeatureMessage) {
                when (message) {
                    is NodeStartedEvent -> {
                        logger.info("Node started: ${message.nodeId}")
                        metrics.nodeExecutions.increment()
                    }

                    is NodeCompletedEvent -> {
                        logger.info("Node completed: ${message.nodeId} in ${message.duration}ms")
                        metrics.nodeDuration.record(message.duration)
                    }

                    is EdgeTraversedEvent -> {
                        logger.debug("Edge traversed: ${message.fromNode} -> ${message.toNode}")
                    }

                    is WorkflowErrorEvent -> {
                        logger.error("Workflow error at ${message.nodeId}: ${message.error}")
                        metrics.errors.increment()
                    }
                }
            }
        })
    }
}
```

## Common Pitfalls

### Pitfall 1: Circular Dependencies

```kotlin
// ✗ Bad: Circular flow
edge(node("a") to node("b"))
edge(node("b") to node("c"))
edge(node("c") to node("a")) // Infinite loop!

// ✓ Good: Add exit condition
edge(node("a") to node("b"))
edge(node("b") to decision("should_continue") {
    condition { iterations < 3 } to node("c")
    default() to node("exit")
})
edge(node("c") to node("a"))
```

### Pitfall 2: Missing Error Handling

```kotlin
// ✗ Bad: No error handling
node("risky") {
    tool("unreliable_api")
}

// ✓ Good: Handle errors
node("risky") {
    tool("unreliable_api") {
        onError { error ->
            node("fallback")
        }
    }
}
```

### Pitfall 3: Data Not Transferred

```kotlin
// ✗ Bad: Data lost between nodes
node("fetch") {
    val data = fetchData()
    // Data not stored!
}

node("process") {
    // How to access data from previous node?
}

// ✓ Good: Use storage
node("fetch") {
    val data = fetchData()
    storage.set("data", data)
}

node("process") {
    val data = storage.get<Data>("data")
    processData(data)
}
```

## References

- Related skill: [kotlin-koog-agent-development](/home/user/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md)
- Related skill: [koog-performance-optimization](/home/user/agents/plugins/kotlin-koog-development/skills/koog-performance-optimization/SKILL.md)
- [Koog Strategy Graphs](https://docs.koog.ai/predefined-agent-strategies/)
- [Koog Custom Graphs](https://docs.koog.ai/custom-strategy-graphs/)
- [Koog Parallel Execution](https://docs.koog.ai/parallel-node-execution/)
- [Koog Data Transfer](https://docs.koog.ai/data-transfer-between-nodes/)
- [Koog Nodes and Components](https://docs.koog.ai/nodes-and-components/)
