---
name: tarantool-performance-audit
description: Comprehensive performance analysis command for Tarantool with bottleneck identification and optimization recommendations
---

# Tarantool Performance Audit & Optimization

Comprehensive performance analysis, bottleneck identification, and optimization recommendations for Tarantool applications:

[Extended thinking: This command performs deep performance analysis covering query optimization, memory management, index efficiency, replication lag, fiber scheduling, and storage engine tuning. It includes profiling, benchmarking, capacity planning, and actionable optimization recommendations with implementation guidance.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Audit Scope
- **quick**: Essential metrics and quick wins (30 min)
- **standard**: Comprehensive analysis of key areas (2-4 hours)
- **deep**: Deep dive with profiling and tracing (8+ hours)
- **focused**: Specific component analysis (custom duration)

### Focus Areas
- **queries**: Query performance and optimization
- **memory**: Memory usage and allocation patterns
- **indexes**: Index efficiency and coverage
- **replication**: Replication lag and throughput
- **storage**: Storage engine optimization (memtx/vinyl)
- **network**: Network I/O and connection pooling
- **fibers**: Fiber scheduling and concurrency
- **all**: Comprehensive audit of all areas

### Performance Profile
- **oltp**: OLTP workload optimization
- **olap**: OLAP/analytics workload optimization
- **mixed**: Mixed workload optimization
- **write-heavy**: Write-intensive optimization
- **read-heavy**: Read-intensive optimization

## Phase 1: Baseline & Discovery

1. **System Metrics Collection**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Collect baseline metrics for: $ARGUMENTS. Gather CPU, memory, disk I/O metrics. Collect Tarantool-specific metrics (operations/sec, latency, memory usage). Monitor fiber statistics. Check replication lag. Collect network statistics. Establish performance baseline."
   - Expected output: Baseline performance metrics report

2. **Configuration Review**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Review Tarantool configuration for: $ARGUMENTS. Profile: $PERFORMANCE_PROFILE. Analyze memtx_memory and vinyl settings. Review checkpoint and snapshot settings. Check WAL configuration. Analyze net_msg_max and other limits. Identify configuration bottlenecks."
   - Expected output: Configuration analysis with recommendations

3. **Workload Characterization**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Characterize workload for: $ARGUMENTS. Analyze read vs write ratio. Identify hot tables and operations. Analyze query patterns and complexity. Measure transaction rates and sizes. Identify peak load periods. Profile request distribution."
   - Expected output: Workload characterization report

4. **Resource Utilization Analysis**
   - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
   - Prompt: "Analyze resource utilization for: $ARGUMENTS. Monitor CPU usage patterns and saturation. Analyze memory allocation and fragmentation. Check disk I/O patterns and throughput. Monitor network bandwidth and packet rates. Identify resource bottlenecks. Create utilization dashboards."
   - Expected output: Resource utilization analysis with bottleneck identification

## Phase 2: Performance Analysis

5. **Query Performance Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Analyze query performance for: $ARGUMENTS. Focus: $FOCUS_AREAS. Profile slow queries using box.stat(). Analyze query execution plans. Identify full table scans. Measure query latency distribution. Identify N+1 query patterns. Analyze query complexity."
   - Expected output: Query performance analysis with slow query report

6. **Index Efficiency Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Analyze index efficiency for: $ARGUMENTS. Review all indexes usage statistics. Identify unused indexes. Find missing indexes for common queries. Analyze index selectivity and cardinality. Check index fragmentation. Measure index lookup performance. Identify composite index opportunities."
   - Expected output: Index efficiency report with optimization recommendations

7. **Memory Management Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Analyze memory management for: $ARGUMENTS. Monitor memtx memory usage and fragmentation. Analyze slab allocator efficiency. Check for memory leaks. Review tuple memory allocation patterns. Analyze memory quota utilization. Monitor snapshot and checkpoint memory impact."
   - Expected output: Memory analysis with optimization recommendations

8. **Replication Performance**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Analyze replication performance for: $ARGUMENTS. Measure replication lag across replicas. Analyze WAL writing and replication throughput. Identify replication bottlenecks. Monitor network latency between replicas. Analyze relay fiber performance. Check for replication conflicts."
   - Expected output: Replication performance analysis with tuning recommendations

9. **Storage Engine Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
   - Prompt: "Analyze storage engine performance for: $ARGUMENTS. Compare memtx vs vinyl performance characteristics. Analyze space fragmentation. Review compaction and garbage collection. Monitor LSM tree depth (vinyl). Analyze cache hit ratios. Measure storage I/O patterns."
   - Expected output: Storage engine analysis with configuration recommendations

10. **Fiber Scheduling Analysis**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Analyze fiber scheduling for: $ARGUMENTS. Monitor fiber creation and destruction rates. Analyze fiber pool utilization. Identify fiber starvation or contention. Check fiber yield behavior. Analyze cooperative multitasking efficiency. Identify long-running fibers blocking others."
    - Expected output: Fiber scheduling analysis with concurrency recommendations

## Phase 3: Bottleneck Identification

11. **CPU Bottleneck Analysis**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Identify CPU bottlenecks for: $ARGUMENTS. Profile CPU-intensive operations. Analyze Lua code hot paths. Identify excessive CPU usage patterns. Check for inefficient algorithms. Analyze serialization/deserialization overhead. Measure computational complexity."
    - Expected output: CPU bottleneck analysis with optimization opportunities

12. **I/O Bottleneck Analysis**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Identify I/O bottlenecks for: $ARGUMENTS. Analyze disk I/O wait times. Monitor snapshot and checkpoint I/O impact. Analyze WAL writing patterns and fsync behavior. Check for disk saturation. Identify sequential vs random I/O patterns. Measure I/O throughput limits."
    - Expected output: I/O bottleneck analysis with storage recommendations

13. **Network Bottleneck Analysis**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Identify network bottlenecks for: $ARGUMENTS. Analyze network latency and throughput. Monitor connection pool utilization. Check for network saturation. Analyze message sizes and batching. Identify chattiness in application protocol. Measure network overhead."
    - Expected output: Network bottleneck analysis with optimization recommendations

14. **Concurrency Bottleneck Analysis**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Identify concurrency bottlenecks for: $ARGUMENTS. Analyze lock contention and wait times. Identify transaction conflicts. Check for serialization bottlenecks. Analyze queue depths and backlog. Identify hot spots and contended resources. Measure concurrency scalability."
    - Expected output: Concurrency analysis with parallelization recommendations

## Phase 4: Optimization Recommendations

15. **Schema Optimization**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Design schema optimizations for: $ARGUMENTS. Recommend space format improvements. Suggest denormalization opportunities. Identify partition/sharding opportunities. Recommend data type optimizations. Suggest composite index strategies. Plan for data archival/purging."
    - Expected output: Schema optimization recommendations with implementation plan

16. **Query Optimization**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Design query optimizations for: $ARGUMENTS. Rewrite slow queries for better performance. Add strategic indexes for common patterns. Implement query result caching. Optimize batch operations. Reduce query complexity. Implement prepared statements pattern."
    - Expected output: Query optimization recommendations with code examples

17. **Configuration Tuning**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Recommend configuration tuning for: $ARGUMENTS. Profile: $PERFORMANCE_PROFILE. Tune memtx_memory and vinyl_memory limits. Optimize checkpoint and snapshot intervals. Tune WAL settings for performance vs durability. Adjust network buffer sizes. Configure fiber pool settings. Tune garbage collection."
    - Expected output: Configuration tuning recommendations with values

18. **Caching Strategy**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Design caching strategy for: $ARGUMENTS. Identify cacheable data and queries. Design cache invalidation strategies. Implement application-level caching in Tarantool. Configure vinyl cache settings. Design cache warming procedures. Measure cache hit ratios and effectiveness."
    - Expected output: Caching strategy with implementation guidance

## Phase 5: Validation & Testing

19. **Performance Benchmarking**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Design performance benchmarks for: $ARGUMENTS. Create benchmark scenarios for workload patterns. Design load testing for peak capacity. Benchmark optimization improvements. Measure latency percentiles (p50, p95, p99). Test scalability limits. Create performance regression tests."
    - Expected output: Benchmark suite with baseline comparisons

20. **Load Testing**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Execute load testing for: $ARGUMENTS. Setup load generation tools. Execute stress tests at various load levels. Measure system behavior under load. Identify breaking points and limits. Test optimization effectiveness. Document load testing results."
    - Expected output: Load test results with capacity analysis

21. **Optimization Validation**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Validate optimizations for: $ARGUMENTS. Measure before/after performance metrics. Validate query performance improvements. Verify memory usage reduction. Confirm replication lag improvement. Test under production-like load. Document improvement percentages."
    - Expected output: Optimization validation report with metrics

## Phase 6: Documentation & Monitoring

22. **Performance Monitoring Setup**
    - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
    - Prompt: "Setup performance monitoring for: $ARGUMENTS. Configure Prometheus metrics collection. Create Grafana performance dashboards. Setup performance alerting rules. Configure slow query logging. Create SLO/SLI monitoring. Setup automated performance reports."
    - Expected output: Monitoring configuration with dashboards

23. **Performance Documentation**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Create performance documentation for: $ARGUMENTS. Document performance audit findings. Create optimization implementation guide. Document tuning recommendations. Create performance troubleshooting guide. Document best practices. Create capacity planning guide."
    - Expected output: Comprehensive performance documentation

24. **Capacity Planning**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Create capacity plan for: $ARGUMENTS. Project growth based on current metrics. Estimate future resource requirements. Plan for scaling (vertical vs horizontal). Identify capacity constraints. Design scaling triggers and thresholds. Create capacity monitoring dashboards."
    - Expected output: Capacity planning report with growth projections

## Execution Parameters

### Required
- **--target**: Target Tarantool instance or cluster to audit
- **--audit-scope**: Scope of audit (quick|standard|deep|focused)

### Optional
- **--focus-areas**: Specific areas to analyze (queries|memory|indexes|replication|storage|network|fibers|all) - default: all
- **--performance-profile**: Workload type (oltp|olap|mixed|write-heavy|read-heavy) - default: mixed
- **--duration-hours**: Audit duration for metrics collection - default: 24
- **--baseline-period**: Baseline collection period in hours - default: 1
- **--load-percentile**: Performance percentile to optimize for (50|95|99) - default: 95
- **--enable-profiling**: Enable detailed profiling (true|false) - default: false
- **--generate-report**: Generate PDF report (true|false) - default: true

## Success Criteria

- Comprehensive baseline metrics collected
- All bottlenecks identified and documented
- Actionable optimization recommendations provided
- Performance improvements validated through testing
- Monitoring and alerting configured
- Capacity planning completed
- Complete documentation delivered
- Team trained on performance best practices

## Example Audit Scenarios

1. **Quick Performance Check**
   - 30-minute essential metrics review
   - Identify obvious bottlenecks
   - Quick-win optimization recommendations
   - Basic monitoring setup

2. **Standard OLTP Audit**
   - Comprehensive query and index analysis
   - Memory and configuration tuning
   - Replication lag optimization
   - Full performance documentation

3. **Deep Dive Analytics Audit**
   - Complex query optimization
   - Vinyl storage engine tuning
   - Memory optimization for large datasets
   - Comprehensive benchmarking

4. **Focused Replication Audit**
   - Detailed replication analysis
   - Network and WAL optimization
   - Replica lag reduction strategies
   - Replication monitoring setup

Tarantool performance audit for: $ARGUMENTS
