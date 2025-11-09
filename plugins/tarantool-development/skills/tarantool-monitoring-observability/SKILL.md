---
name: tarantool-monitoring-observability
description: Master Tarantool monitoring and observability using Prometheus metrics, Grafana dashboards, alerting, distributed tracing, and SLA/SLO tracking. Use when implementing production monitoring, diagnosing performance issues, or setting up observability infrastructure.
---

# Tarantool Monitoring & Observability

Complete guide to implementing comprehensive monitoring, metrics, logging, and observability for Tarantool databases.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Implement production-grade observability to monitor Tarantool performance, diagnose issues, and ensure SLA compliance.

## When to Use This Skill

- Set up Prometheus metrics collection
- Create Grafana dashboards
- Configure alerting rules
- Implement distributed tracing
- Monitor replication lag
- Track query performance
- Set up logging infrastructure
- Define SLI/SLO/SLA metrics
- Debug production issues

## Core Concepts

### Prometheus Metrics Integration

**Install Metrics Module**
```lua
-- Install: tarantoolctl rocks install metrics
local metrics = require('metrics')

-- Initialize metrics
metrics.cfg{
    labels = {
        instance = box.info.name,
        cluster = os.getenv('CLUSTER_NAME') or 'default'
    }
}

-- Enable default metrics (memory, network, operations)
metrics.enable_default_metrics()
```

**Expose Prometheus Endpoint**
```lua
local http = require('http.server')
local metrics = require('metrics')

-- Create HTTP server for metrics
local httpd = http.new('0.0.0.0', 8081)

httpd:route({
    path = '/metrics',
    method = 'GET'
}, function(req)
    local prometheus = require('metrics.plugins.prometheus')
    return req:render{
        text = prometheus.collect_http()
    }
end)

httpd:start()
```

**Custom Business Metrics**
```lua
local metrics = require('metrics')

-- Counter: total number of operations
local order_counter = metrics.counter(
    'orders_total',
    'Total number of orders created',
    {labels = {'status'}}
)

-- Gauge: current active connections
local active_connections = metrics.gauge(
    'active_connections',
    'Number of active connections'
)

-- Histogram: request duration
local request_duration = metrics.histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    {buckets = {0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0}}
)

-- Summary: response size
local response_size = metrics.summary(
    'http_response_size_bytes',
    'HTTP response size',
    {quantiles = {0.5, 0.9, 0.99}}
)

-- Usage in application
function create_order(order_data)
    local start = fiber.time()

    box.begin()
    local order = box.space.orders:insert(order_data)
    box.commit()

    -- Record metrics
    order_counter:inc(1, {order.status})
    request_duration:observe(fiber.time() - start)

    return order
end
```

### Key Performance Indicators

**Memory Metrics**
```lua
local function collect_memory_metrics()
    local mem_gauge = metrics.gauge('tarantool_memory_bytes', 'Memory usage')

    -- Total memory used
    mem_gauge:set(box.info.memory().used, {type = 'used'})

    -- Arena memory
    mem_gauge:set(box.info.memory().arena_used, {type = 'arena_used'})

    -- Memtx memory
    local memtx_info = box.slab.info()
    mem_gauge:set(memtx_info.items_used_ratio * 100, {type = 'memtx_used_pct'})

    -- Vinyl memory
    mem_gauge:set(box.cfg.vinyl_memory, {type = 'vinyl_cache'})
end
```

**Operation Metrics**
```lua
local function collect_operation_metrics()
    local op_counter = metrics.counter('tarantool_operations_total', 'Operations by type')

    local stats = box.stat()
    op_counter:inc(stats.SELECT.total, {operation = 'select'})
    op_counter:inc(stats.INSERT.total, {operation = 'insert'})
    op_counter:inc(stats.UPDATE.total, {operation = 'update'})
    op_counter:inc(stats.DELETE.total, {operation = 'delete'})
    op_counter:inc(stats.REPLACE.total, {operation = 'replace'})
end
```

**Replication Metrics**
```lua
local function collect_replication_metrics()
    local repl_lag = metrics.gauge('tarantool_replication_lag_seconds', 'Replication lag')
    local repl_status = metrics.gauge('tarantool_replication_status', 'Replication status')

    local info = box.info.replication
    for replica_id, replica in pairs(info) do
        local labels = {
            replica_id = tostring(replica_id),
            upstream_uuid = replica.uuid or 'unknown'
        }

        if replica.upstream then
            -- Lag in seconds
            repl_lag:set(replica.upstream.lag or 0, labels)

            -- Status: 1 = follow, 0 = other
            local status = replica.upstream.status == 'follow' and 1 or 0
            repl_status:set(status, labels)
        end
    end
end
```

### Grafana Dashboard Configuration

**Prometheus Configuration (prometheus.yml)**
```yaml
scrape_configs:
  - job_name: 'tarantool'
    static_configs:
      - targets:
          - 'tarantool-1:8081'
          - 'tarantool-2:8081'
          - 'tarantool-3:8081'
    scrape_interval: 15s
    scrape_timeout: 10s
```

**Key Dashboard Panels**
```lua
-- Query examples for Grafana panels

-- 1. Operations per second
rate(tarantool_operations_total[5m])

-- 2. Memory usage percentage
(tarantool_memory_bytes{type="used"} / tarantool_memory_bytes{type="arena_size"}) * 100

-- 3. Replication lag
max(tarantool_replication_lag_seconds) by (instance)

-- 4. Request latency (95th percentile)
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket[5m])
)

-- 5. Error rate
rate(tarantool_errors_total[5m])

-- 6. Active connections
tarantool_active_connections

-- 7. Transaction rate
rate(tarantool_transactions_total[5m])

-- 8. Space sizes
tarantool_space_size_bytes by (space_name)
```

### Alerting Rules

**Prometheus Alert Rules (alerts.yml)**
```yaml
groups:
  - name: tarantool_alerts
    interval: 30s
    rules:
      # High replication lag
      - alert: TarantoolHighReplicationLag
        expr: tarantool_replication_lag_seconds > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High replication lag on {{ $labels.instance }}"
          description: "Replication lag is {{ $value }}s"

      # Replica disconnected
      - alert: TarantoolReplicaDisconnected
        expr: tarantool_replication_status == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Replica {{ $labels.replica_id }} disconnected"

      # High memory usage
      - alert: TarantoolHighMemoryUsage
        expr: |
          (tarantool_memory_bytes{type="used"} /
           tarantool_memory_bytes{type="arena_size"}) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"

      # Error rate spike
      - alert: TarantoolHighErrorRate
        expr: rate(tarantool_errors_total[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.instance }}"

      # Slow queries
      - alert: TarantoolSlowQueries
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow queries detected on {{ $labels.instance }}"
```

### Logging Infrastructure

**Structured Logging Setup**
```lua
local log = require('log')
local json = require('json')

-- Configure log format
box.cfg{
    log_level = 5,  -- INFO level
    log_format = 'json',
    log = '/var/log/tarantool/instance.log'
}

-- Custom logger with context
local Logger = {}

function Logger:new(context)
    local obj = {context = context or {}}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function Logger:info(message, extra)
    local log_entry = {
        level = 'INFO',
        message = message,
        timestamp = os.time(),
        context = self.context
    }

    if extra then
        for k, v in pairs(extra) do
            log_entry[k] = v
        end
    end

    log.info(json.encode(log_entry))
end

function Logger:error(message, error_obj)
    log.error(json.encode{
        level = 'ERROR',
        message = message,
        error = tostring(error_obj),
        stack = debug.traceback(),
        timestamp = os.time(),
        context = self.context
    })
end

-- Usage
local logger = Logger:new{service = 'orders', instance = box.info.name}
logger:info('Order created', {order_id = 12345, user_id = 678})
```

**Centralized Logging with Fluentd**
```lua
local socket = require('socket')
local json = require('json')

local FluentdLogger = {}

function FluentdLogger:new(host, port, tag)
    local sock = socket.tcp_connect(host, port)
    return setmetatable({
        sock = sock,
        tag = tag
    }, {__index = self})
end

function FluentdLogger:log(level, message, data)
    local entry = {
        level = level,
        message = message,
        data = data,
        timestamp = fiber.time(),
        instance = box.info.name
    }

    local packet = json.encode({self.tag, fiber.time(), entry})
    self.sock:write(packet .. '\n')
end

-- Usage
local fluent = FluentdLogger:new('fluentd-host', 24224, 'tarantool')
fluent:log('INFO', 'Order processed', {order_id = 123})
```

### Distributed Tracing

**OpenTelemetry Integration**
```lua
local opentelemetry = require('opentelemetry')

-- Initialize tracer
local tracer = opentelemetry.tracer('tarantool-service')

function process_order_with_tracing(order_id)
    -- Start span
    local span = tracer:start_span('process_order', {
        attributes = {
            ['order.id'] = order_id,
            ['service.name'] = 'order-processor'
        }
    })

    -- Set span context
    local ctx = span:context()

    -- Child operation
    local validate_span = tracer:start_span('validate_order', {
        parent = ctx
    })

    -- Perform validation
    local is_valid = validate_order(order_id)
    validate_span:set_attribute('order.valid', is_valid)
    validate_span:finish()

    if is_valid then
        local save_span = tracer:start_span('save_order', {parent = ctx})
        box.space.orders:insert{order_id, 'pending'}
        save_span:finish()
    else
        span:set_status('ERROR', 'Invalid order')
    end

    span:finish()
end
```

### SLA/SLO Monitoring

**SLI (Service Level Indicators)**
```lua
local sli_tracker = {}

function sli_tracker.track_request(duration, success)
    -- Latency SLI
    local latency_histogram = metrics.histogram(
        'request_duration_seconds',
        'Request duration',
        {buckets = {0.01, 0.05, 0.1, 0.5, 1.0, 5.0}}
    )
    latency_histogram:observe(duration)

    -- Availability SLI
    local availability_counter = metrics.counter(
        'requests_total',
        'Total requests',
        {labels = {'status'}}
    )
    availability_counter:inc(1, {status = success and 'success' or 'error'})
end

-- Calculate SLO compliance
function sli_tracker.check_slo()
    -- Target: 99% of requests under 100ms
    local query = [[
        sum(rate(request_duration_seconds_bucket{le="0.1"}[7d])) /
        sum(rate(request_duration_seconds_count[7d]))
    ]]

    -- Target: 99.9% availability
    local availability_query = [[
        sum(rate(requests_total{status="success"}[7d])) /
        sum(rate(requests_total[7d]))
    ]]
end
```

## Monitoring Patterns

### Pattern 1: Health Check Endpoint

```lua
local http = require('http.server')
local httpd = http.new('0.0.0.0', 8080)

httpd:route({path = '/health', method = 'GET'}, function(req)
    local health = {
        status = 'UP',
        checks = {}
    }

    -- Check database
    local db_ok, db_err = pcall(function()
        box.space.users:count()
    end)
    health.checks.database = {
        status = db_ok and 'UP' or 'DOWN',
        error = db_err
    }

    -- Check replication
    local repl_ok = true
    for _, replica in pairs(box.info.replication) do
        if replica.upstream and replica.upstream.status ~= 'follow' then
            repl_ok = false
        end
    end
    health.checks.replication = {
        status = repl_ok and 'UP' or 'DOWN'
    }

    -- Check memory
    local mem_usage = box.info.memory().used / box.cfg.memtx_memory
    health.checks.memory = {
        status = mem_usage < 0.9 and 'UP' or 'WARN',
        usage_percent = mem_usage * 100
    }

    local status_code = health.status == 'UP' and 200 or 503
    return req:render{json = health, status = status_code}
end)
```

### Pattern 2: Performance Profiling

```lua
local fiber = require('fiber')
local clock = require('clock')

local profiler = {}

function profiler.profile(name, fn, ...)
    local start = clock.monotonic()
    local cpu_start = clock.proc()

    local ok, result = pcall(fn, ...)

    local duration = clock.monotonic() - start
    local cpu_time = clock.proc() - cpu_start

    -- Record metrics
    metrics.histogram('function_duration_seconds', name):observe(duration)
    metrics.histogram('function_cpu_seconds', name):observe(cpu_time)

    if not ok then
        metrics.counter('function_errors_total', name):inc(1)
        error(result)
    end

    return result
end

-- Usage
local result = profiler.profile('create_order', create_order, order_data)
```

## Best Practices

1. **Metric Naming**
   - Use descriptive names: `http_requests_total` not `requests`
   - Include units: `_seconds`, `_bytes`, `_total`
   - Follow Prometheus conventions
   - Use consistent labels

2. **Cardinality Control**
   - Limit label values (avoid user IDs, timestamps)
   - Use histograms for distribution metrics
   - Aggregate high-cardinality data

3. **Alert Design**
   - Alert on symptoms, not causes
   - Set appropriate thresholds
   - Include actionable context
   - Avoid alert fatigue

4. **Dashboard Organization**
   - Group related metrics
   - Use consistent time ranges
   - Include SLO indicators
   - Add annotations for deployments

5. **Log Management**
   - Use structured logging (JSON)
   - Include correlation IDs
   - Set appropriate log levels
   - Implement log rotation

## Common Pitfalls

- **Too Many Metrics**: High cardinality kills Prometheus
- **Missing Context**: Include instance, cluster labels
- **Ignoring Replication**: Monitor lag on all replicas
- **Alert Spam**: Too many alerts = ignored alerts
- **No Retention Policy**: Logs and metrics fill disks
- **Synchronous Logging**: Impacts performance

## Related Skills

- `tarantool-architecture` - Understanding metrics sources
- `tarantool-performance` - Performance tuning based on metrics
- `lua-development` - Implementing custom metrics
- `cartridge-framework` - Cluster-wide monitoring
- `prometheus-grafana` - Visualization and alerting

## References

- [Tarantool Metrics Module](https://www.tarantool.io/en/doc/latest/book/monitoring/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Examples](https://grafana.com/grafana/dashboards/)
- [OpenTelemetry Lua](https://opentelemetry.io/docs/instrumentation/lua/)
