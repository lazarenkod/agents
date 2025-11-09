---
name: tarantool-testing-patterns
description: Comprehensive testing strategies for Tarantool applications including unit testing, integration testing, performance testing, and test automation. Use when implementing test suites, designing test strategies, or setting up CI/CD testing for Tarantool projects.
---

# Tarantool Testing Patterns

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## When to Use This Skill

- Designing test strategies for Tarantool applications
- Implementing unit tests for Lua business logic
- Creating integration tests for Tarantool spaces and indexes
- Setting up performance and load testing
- Configuring CI/CD test automation
- Testing replication and failover scenarios
- Validating data integrity and consistency

## Core Concepts

### Test Pyramid for Tarantool

```
        /\
       /  \       E2E Tests (Few)
      /____\      - Full cluster testing
     /      \     - Multi-node scenarios
    /        \    Integration Tests (Some)
   /__________\   - Space operations
  /            \  - Replication tests
 /______________\ Unit Tests (Many)
                  - Business logic
                  - Data validation
                  - Lua functions
```

### Testing Layers

1. **Unit Tests** - Test Lua functions in isolation
2. **Integration Tests** - Test spaces, indexes, and stored procedures
3. **System Tests** - Test full Tarantool instance behavior
4. **Performance Tests** - Load testing and benchmarking
5. **Replication Tests** - Multi-node cluster testing
6. **Chaos Tests** - Failure scenario testing

## Unit Testing Patterns

### Pattern: Testing Lua Functions

```lua
-- app/user_service.lua
local user_service = {}

function user_service.validate_email(email)
    if not email or email == '' then
        return false, 'Email is required'
    end

    if not string.match(email, '^[%w._%%-]+@[%w._%%-]+%.%w+$') then
        return false, 'Invalid email format'
    end

    return true
end

function user_service.create_user(name, email)
    local valid, err = user_service.validate_email(email)
    if not valid then
        return nil, err
    end

    local user = {
        id = box.sequence.user_id:next(),
        name = name,
        email = email,
        created_at = os.time()
    }

    box.space.users:insert(user)
    return user
end

return user_service
```

```lua
-- test/unit/user_service_test.lua
local tap = require('tap')
local user_service = require('app.user_service')

local test = tap.test('user_service')

test:plan(5)

-- Test email validation
test:test('validate_email', function(t)
    t:plan(4)

    local valid, err = user_service.validate_email('user@example.com')
    t:ok(valid, 'Valid email accepted')

    valid, err = user_service.validate_email('')
    t:is(valid, false, 'Empty email rejected')
    t:like(err, 'required', 'Error message for empty email')

    valid, err = user_service.validate_email('invalid-email')
    t:is(valid, false, 'Invalid format rejected')
end)

-- Test user creation
test:test('create_user', function(t)
    t:plan(3)

    -- Setup test space
    box.schema.sequence.create('user_id', {if_not_exists = true})
    box.schema.space.create('users', {if_not_exists = true, temporary = true})
    box.space.users:format{
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'created_at', type = 'number'}
    }
    box.space.users:create_index('primary', {parts = {'id'}})

    local user, err = user_service.create_user('John Doe', 'john@example.com')
    t:ok(user, 'User created successfully')
    t:is(user.name, 'John Doe', 'User name matches')
    t:is(user.email, 'john@example.com', 'User email matches')

    -- Cleanup
    box.space.users:drop()
    box.sequence.user_id:drop()
end)

os.exit(test:check() and 0 or 1)
```

### Pattern: Testing with Mocks

```lua
-- test/unit/order_service_test.lua
local tap = require('tap')
local fiber = require('fiber')

local test = tap.test('order_service')

-- Mock external HTTP service
local http_mock = {
    requests = {},
    response = {status = 200, body = '{"success": true}'}
}

function http_mock.post(url, body, opts)
    table.insert(http_mock.requests, {url = url, body = body})
    return http_mock.response
end

-- Inject mock into service
local order_service = require('app.order_service')
order_service.http_client = http_mock

test:plan(2)

test:test('process_order', function(t)
    t:plan(3)

    local order = order_service.process_order({
        user_id = 123,
        amount = 100.50,
        items = {'item1', 'item2'}
    })

    t:ok(order, 'Order processed')
    t:is(#http_mock.requests, 1, 'HTTP request made')
    t:like(http_mock.requests[1].url, '/api/payment', 'Called payment API')
end)

os.exit(test:check() and 0 or 1)
```

## Integration Testing Patterns

### Pattern: Testing Spaces and Indexes

```lua
-- test/integration/space_test.lua
local tap = require('tap')
local test = tap.test('space_operations')

test:plan(4)

-- Setup test environment
box.cfg{
    listen = '127.0.0.1:0',  -- Random port
    wal_mode = 'none',       -- Disable WAL for tests
    log_level = 5
}

box.schema.space.create('products', {temporary = true})
box.space.products:format{
    {name = 'id', type = 'unsigned'},
    {name = 'name', type = 'string'},
    {name = 'category', type = 'string'},
    {name = 'price', type = 'number'}
}
box.space.products:create_index('primary', {parts = {'id'}})
box.space.products:create_index('category', {parts = {'category'}, unique = false})

test:test('insert and select', function(t)
    t:plan(2)

    box.space.products:insert{1, 'Laptop', 'Electronics', 999.99}
    local product = box.space.products:get(1)

    t:is(product[2], 'Laptop', 'Product name matches')
    t:is(product[4], 999.99, 'Product price matches')
end)

test:test('secondary index', function(t)
    t:plan(2)

    box.space.products:insert{2, 'Phone', 'Electronics', 699.99}
    box.space.products:insert{3, 'Desk', 'Furniture', 299.99}

    local electronics = {}
    for _, tuple in box.space.products.index.category:pairs('Electronics') do
        table.insert(electronics, tuple)
    end

    t:is(#electronics, 2, 'Found 2 electronics products')
    t:ok(electronics[1][2] == 'Laptop' or electronics[1][2] == 'Phone',
         'Electronics product found')
end)

test:test('update and delete', function(t)
    t:plan(2)

    box.space.products:update(1, {{'=', 4, 899.99}})
    local updated = box.space.products:get(1)
    t:is(updated[4], 899.99, 'Price updated')

    box.space.products:delete(1)
    local deleted = box.space.products:get(1)
    t:is(deleted, nil, 'Product deleted')
end)

-- Cleanup
box.space.products:drop()

os.exit(test:check() and 0 or 1)
```

### Pattern: Testing Transactions

```lua
-- test/integration/transaction_test.lua
local tap = require('tap')
local test = tap.test('transactions')

test:plan(3)

-- Setup
box.cfg{listen = '127.0.0.1:0', wal_mode = 'none'}
box.schema.space.create('accounts', {temporary = true})
box.space.accounts:format{
    {name = 'id', type = 'unsigned'},
    {name = 'balance', type = 'number'}
}
box.space.accounts:create_index('primary', {parts = {'id'}})

box.space.accounts:insert{1, 1000}
box.space.accounts:insert{2, 500}

test:test('successful transaction', function(t)
    t:plan(2)

    box.begin()
    box.space.accounts:update(1, {{'-', 2, 100}})
    box.space.accounts:update(2, {{'+', 2, 100}})
    box.commit()

    t:is(box.space.accounts:get(1)[2], 900, 'Sender balance decreased')
    t:is(box.space.accounts:get(2)[2], 600, 'Receiver balance increased')
end)

test:test('transaction rollback', function(t)
    t:plan(2)

    box.begin()
    box.space.accounts:update(1, {{'-', 2, 100}})
    box.space.accounts:update(2, {{'+', 2, 100}})
    box.rollback()

    t:is(box.space.accounts:get(1)[2], 900, 'Sender balance unchanged')
    t:is(box.space.accounts:get(2)[2], 600, 'Receiver balance unchanged')
end)

test:test('transaction isolation', function(t)
    t:plan(1)

    local fiber = require('fiber')
    local seen_values = {}

    box.begin()
    box.space.accounts:update(1, {{'=', 2, 1500}})

    local reader = fiber.create(function()
        -- Read from another fiber (should see old value)
        table.insert(seen_values, box.space.accounts:get(1)[2])
    end)

    fiber.sleep(0.01)
    box.commit()

    t:is(seen_values[1], 900, 'Isolation: reader saw old value')
end)

-- Cleanup
box.space.accounts:drop()

os.exit(test:check() and 0 or 1)
```

## Performance Testing Patterns

### Pattern: Load Testing with Benchmarking

```lua
-- test/performance/load_test.lua
local fiber = require('fiber')
local clock = require('clock')
local log = require('log')

-- Configuration
local NUM_FIBERS = 100
local OPERATIONS_PER_FIBER = 1000
local TARGET_RPS = 10000

-- Setup
box.cfg{
    listen = '127.0.0.1:3301',
    wal_mode = 'write'
}

box.schema.space.create('benchmark', {if_not_exists = true})
box.space.benchmark:format{
    {name = 'id', type = 'unsigned'},
    {name = 'value', type = 'string'},
    {name = 'timestamp', type = 'number'}
}
box.space.benchmark:create_index('primary', {parts = {'id'}, if_not_exists = true})

-- Benchmark function
local function worker(fiber_id, results)
    local start = clock.monotonic()
    local ops = 0
    local errors = 0

    for i = 1, OPERATIONS_PER_FIBER do
        local id = fiber_id * OPERATIONS_PER_FIBER + i
        local ok, err = pcall(function()
            box.space.benchmark:insert{id, 'test_value_' .. id, clock.realtime()}
        end)

        if not ok then
            errors = errors + 1
        else
            ops = ops + 1
        end

        -- Rate limiting
        if i % 100 == 0 then
            fiber.sleep(0.001)
        end
    end

    local duration = clock.monotonic() - start
    results[fiber_id] = {
        ops = ops,
        errors = errors,
        duration = duration,
        rps = ops / duration
    }
end

-- Run load test
log.info('Starting load test with %d fibers', NUM_FIBERS)
local results = {}
local fibers = {}
local test_start = clock.monotonic()

for i = 1, NUM_FIBERS do
    fibers[i] = fiber.create(worker, i, results)
end

-- Wait for completion
for _, f in ipairs(fibers) do
    f:join()
end

local test_duration = clock.monotonic() - test_start

-- Calculate statistics
local total_ops = 0
local total_errors = 0
local min_rps = math.huge
local max_rps = 0

for _, result in pairs(results) do
    total_ops = total_ops + result.ops
    total_errors = total_errors + result.errors
    min_rps = math.min(min_rps, result.rps)
    max_rps = math.max(max_rps, result.rps)
end

local overall_rps = total_ops / test_duration

-- Print results
log.info('=== Load Test Results ===')
log.info('Total operations: %d', total_ops)
log.info('Total errors: %d', total_errors)
log.info('Test duration: %.2f seconds', test_duration)
log.info('Overall RPS: %.2f', overall_rps)
log.info('Min RPS: %.2f', min_rps)
log.info('Max RPS: %.2f', max_rps)
log.info('Error rate: %.2f%%', (total_errors / (total_ops + total_errors)) * 100)

-- Check if target RPS was met
if overall_rps >= TARGET_RPS then
    log.info('✓ Target RPS achieved')
    os.exit(0)
else
    log.error('✗ Target RPS not met (target: %d, actual: %.2f)', TARGET_RPS, overall_rps)
    os.exit(1)
end
```

### Pattern: Latency Profiling

```lua
-- test/performance/latency_test.lua
local clock = require('clock')
local log = require('log')

local NUM_SAMPLES = 10000

-- Setup
box.cfg{listen = '127.0.0.1:3301'}
box.schema.space.create('latency_test', {if_not_exists = true, temporary = true})
box.space.latency_test:format{{name = 'id', type = 'unsigned'}}
box.space.latency_test:create_index('primary', {parts = {'id'}})

-- Measure operation latencies
local latencies = {}

for i = 1, NUM_SAMPLES do
    local start = clock.monotonic()
    box.space.latency_test:insert{i}
    local duration = (clock.monotonic() - start) * 1000000  -- Convert to microseconds
    table.insert(latencies, duration)
end

-- Calculate percentiles
table.sort(latencies)
local function percentile(p)
    local index = math.ceil((p / 100) * #latencies)
    return latencies[index]
end

log.info('=== Latency Statistics ===')
log.info('Samples: %d', NUM_SAMPLES)
log.info('Min: %.2f μs', latencies[1])
log.info('P50: %.2f μs', percentile(50))
log.info('P95: %.2f μs', percentile(95))
log.info('P99: %.2f μs', percentile(99))
log.info('P99.9: %.2f μs', percentile(99.9))
log.info('Max: %.2f μs', latencies[#latencies])

-- Calculate average
local sum = 0
for _, lat in ipairs(latencies) do
    sum = sum + lat
end
log.info('Average: %.2f μs', sum / #latencies)

-- Cleanup
box.space.latency_test:drop()
```

## CI/CD Testing Integration

### Pattern: GitHub Actions Test Workflow

```yaml
# .github/workflows/test.yml
name: Tarantool Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Tarantool
        run: |
          curl -L https://tarantool.io/release/2/installer.sh | sudo bash
          sudo apt-get install -y tarantool tarantool-dev

      - name: Run Unit Tests
        run: tarantool test/unit/*.lua

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Tarantool
        run: |
          curl -L https://tarantool.io/release/2/installer.sh | sudo bash
          sudo apt-get install -y tarantool tarantool-dev

      - name: Run Integration Tests
        run: tarantool test/integration/*.lua

  performance-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Install Tarantool
        run: |
          curl -L https://tarantool.io/release/2/installer.sh | sudo bash
          sudo apt-get install -y tarantool tarantool-dev

      - name: Run Performance Tests
        run: tarantool test/performance/*.lua

      - name: Upload Performance Results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: test/performance/results/*.log
```

## Best Practices

### Test Organization
- Separate unit, integration, and performance tests
- Use descriptive test names
- Keep tests independent and isolated
- Clean up resources after tests

### Test Data
- Use temporary spaces for tests
- Generate realistic test data
- Test edge cases and boundaries
- Validate error conditions

### Performance Testing
- Test under realistic load
- Measure multiple metrics (RPS, latency, memory)
- Run tests on production-like hardware
- Monitor resource utilization

### Continuous Testing
- Run tests on every commit
- Fail fast on test failures
- Track test coverage
- Monitor test execution time

## Common Pitfalls

❌ **Not cleaning up test data** - Use temporary spaces or drop spaces after tests
✓ Use `temporary = true` for test spaces

❌ **Tests depending on each other** - Each test should be independent
✓ Set up and tear down in each test

❌ **Not testing error conditions** - Test failures, not just success paths
✓ Test validation, constraints, and error handling

❌ **Ignoring performance tests** - Performance regressions are bugs
✓ Run performance tests regularly

## Related Skills

- **tarantool-architecture** - Understanding data structures for testing
- **lua-development** - Lua programming patterns for test code
- **tarantool-performance** - Performance benchmarking and profiling
- **cartridge-framework** - Testing Cartridge applications

## References

- [Tarantool TAP Testing](https://www.tarantool.io/en/doc/latest/reference/reference_lua/tap/)
- [Tarantool Testing Best Practices](https://www.tarantool.io/en/doc/latest/book/app_server/testing/)
- [Lua Unit Testing](https://github.com/bluebird75/luaunit)
- [Performance Testing Methodologies](https://www.tarantool.io/en/doc/latest/book/app_server/profiling/)
