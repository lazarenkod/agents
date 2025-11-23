---
name: platform-architecture-patterns
description: Архитектурные паттерны для облачных платформ. Use when designing platform architecture, implementing design patterns, solving scalability challenges, or establishing architectural standards.
---

# Паттерны платформенной архитектуры

Проверенные архитектурные паттерны для построения масштабируемых облачных платформ на базе AWS, Azure, GCP и Oracle Cloud.

## Когда использовать этот скилл

- Проектирование новых сервисов платформы
- Решение проблем масштабируемости
- Рефакторинг существующей архитектуры
- Установление архитектурных стандартов
- Code review архитектурных решений

## Control Plane Patterns

### Pattern: API Gateway с Rate Limiting

**Проблема**: Защита backend services от overload, fair usage enforcement

**Решение**:
```
[Client] → [API Gateway] → [Rate Limiter] → [Backend Services]
              ↓
         [Auth/AuthZ]
              ↓
         [Metrics/Logging]
```

**Implementation** (AWS API Gateway + Lambda):
```python
import time
from functools import wraps

class RateLimiter:
    """Token bucket algorithm"""
    def __init__(self, rate_limit, burst_size):
        self.rate = rate_limit  # tokens per second
        self.burst = burst_size  # max tokens in bucket
        self.tokens = burst_size
        self.last_update = time.time()

    def allow_request(self, cost=1):
        """Check if request is allowed"""
        now = time.time()
        elapsed = now - self.last_update

        # Refill bucket
        self.tokens = min(
            self.burst,
            self.tokens + elapsed * self.rate
        )
        self.last_update = now

        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

# Usage per API key
rate_limiters = {}  # {api_key: RateLimiter}

def rate_limit(rate=100, burst=200):
    """Decorator для API endpoints"""
    def decorator(func):
        @wraps(func)
        def wrapper(event, context):
            api_key = event['headers']['X-API-Key']

            if api_key not in rate_limiters:
                rate_limiters[api_key] = RateLimiter(rate, burst)

            if not rate_limiters[api_key].allow_request():
                return {
                    'statusCode': 429,
                    'body': json.dumps({
                        'error': 'Rate limit exceeded',
                        'retry_after': 1.0 / rate
                    })
                }

            return func(event, context)
        return wrapper
    return decorator

@rate_limit(rate=100, burst=200)  # 100 req/s, burst 200
def lambda_handler(event, context):
    # Your API logic
    return {'statusCode': 200, 'body': 'Success'}
```

**Tiered Rate Limits**:
```yaml
Free_Tier:
  rate: 10 req/s
  burst: 20
  daily_quota: 10000

Standard_Tier:
  rate: 100 req/s
  burst: 200
  daily_quota: 1000000

Premium_Tier:
  rate: 1000 req/s
  burst: 2000
  daily_quota: unlimited
```

### Pattern: Desired State Reconciliation (Controller Pattern)

**Проблема**: Обеспечение consistency между desired и actual state

**Решение**: Kubernetes-style control loop

```python
class ResourceController:
    """Generic controller для cloud resources"""

    def __init__(self, resource_type):
        self.resource_type = resource_type
        self.reconcile_interval = 30  # seconds

    def run(self):
        """Main control loop"""
        while True:
            try:
                self.reconcile_all()
            except Exception as e:
                logger.error(f"Reconciliation error: {e}")

            time.sleep(self.reconcile_interval)

    def reconcile_all(self):
        """Reconcile all resources"""
        resources = self.list_resources()

        for resource in resources:
            desired = resource.desired_state
            actual = self.get_actual_state(resource.id)

            if desired != actual:
                self.reconcile(resource, desired, actual)

    def reconcile(self, resource, desired, actual):
        """Bring actual state to desired state"""
        logger.info(f"Reconciling {resource.id}")

        # Compute diff
        actions = self.compute_actions(desired, actual)

        # Apply changes
        for action in actions:
            try:
                action.execute()
                resource.status = "Reconciling"
            except Exception as e:
                resource.status = "Failed"
                resource.error = str(e)
                raise

        resource.status = "Ready"
        resource.last_reconciled = datetime.now()

# Example: VM Controller
class VMController(ResourceController):
    def compute_actions(self, desired, actual):
        actions = []

        # Check instance state
        if desired.state == "running" and actual.state == "stopped":
            actions.append(StartInstanceAction(actual.id))
        elif desired.state == "stopped" and actual.state == "running":
            actions.append(StopInstanceAction(actual.id))

        # Check instance size
        if desired.instance_type != actual.instance_type:
            actions.append(ResizeInstanceAction(
                actual.id,
                desired.instance_type
            ))

        return actions
```

**Benefits**:
- Self-healing (автоматическая коррекция drift)
- Declarative API (пользователи указывают "что", не "как")
- Eventual consistency
- Idempotent operations

## Data Plane Patterns

### Pattern: Multi-Tenant Isolation

**Проблема**: Изоляция tenant data и resources для security и performance

**Архитектура**: Несколько моделей

#### Model 1: Silo (Dedicated Infrastructure)
```
Tenant A → [VPC A] → [DB A] → [Storage A]
Tenant B → [VPC B] → [DB B] → [Storage B]
```

**Pros**:
- Максимальная изоляция
- Predictable performance (no noisy neighbor)
- Easy compliance (dedicated infrastructure для regulated tenants)

**Cons**:
- Highest cost (no resource sharing)
- Operational complexity (manage N stacks)

**Use case**: Enterprise customers, regulated industries (finance, healthcare)

#### Model 2: Bridge (Shared Infrastructure, Isolated Data)
```
Tenants A,B,C → [Shared VPC] → [Shared Compute]
                              → [DB - row-level security]
                              → [Storage - path prefixing]
```

**Implementation** (PostgreSQL Row-Level Security):
```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users only see their tenant's data
CREATE POLICY tenant_isolation ON users
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Application sets tenant context
SET app.current_tenant = 'tenant-uuid-here';

-- Now queries automatically filtered
SELECT * FROM users;  -- Only returns current tenant's users
```

**S3 Prefix Isolation**:
```python
def get_tenant_prefix(tenant_id):
    return f"tenants/{tenant_id}/"

def upload_file(tenant_id, filename, content):
    """Upload with tenant prefix"""
    key = get_tenant_prefix(tenant_id) + filename
    s3.put_object(Bucket='my-bucket', Key=key, Body=content)

def list_files(tenant_id):
    """List только tenant's files"""
    prefix = get_tenant_prefix(tenant_id)
    response = s3.list_objects_v2(Bucket='my-bucket', Prefix=prefix)
    return response.get('Contents', [])
```

**Pros**:
- Cost-effective (shared resources)
- Easier operations (single stack)
- Resource elasticity

**Cons**:
- Noisy neighbor риск
- Requires careful access control
- Application-level isolation (bugs = security issue)

**Use case**: SaaS platforms, SMB customers

#### Model 3: Pool (Fully Shared)
```
All Tenants → [Shared Everything]
```

**Use only for**:
- Multi-user applications (не multi-tenant businesses)
- Consumer apps (Gmail, Facebook)

### Pattern: Sharding для Horizontal Scalability

**Проблема**: Single database/service limits scalability

**Решение**: Partition data across multiple shards

```python
class ShardRouter:
    def __init__(self, num_shards):
        self.shards = [f"shard-{i}" for i in range(num_shards)]

    def get_shard(self, key):
        """Consistent hashing"""
        shard_index = hash(key) % len(self.shards)
        return self.shards[shard_index]

    def route_request(self, tenant_id, operation, **kwargs):
        """Route to correct shard"""
        shard = self.get_shard(tenant_id)
        connection = self.get_connection(shard)
        return operation(connection, **kwargs)

# Example usage
router = ShardRouter(num_shards=16)

def create_user(tenant_id, user_data):
    def _create(conn, user_data):
        return conn.execute("INSERT INTO users ...", user_data)

    return router.route_request(tenant_id, _create, user_data=user_data)
```

**Shard Rebalancing**:
```
Problem: Adding shards changes hash distribution

Solution: Consistent hashing с virtual nodes

from hashlib import md5

class ConsistentHashRouter:
    def __init__(self, shards, virtual_nodes=150):
        self.ring = {}
        self.shards = shards
        self.virtual_nodes = virtual_nodes
        self._build_ring()

    def _build_ring(self):
        for shard in self.shards:
            for i in range(self.virtual_nodes):
                key = f"{shard}:{i}"
                hash_val = int(md5(key.encode()).hexdigest(), 16)
                self.ring[hash_val] = shard

    def get_shard(self, key):
        hash_val = int(md5(key.encode()).hexdigest(), 16)
        # Find next shard in ring
        for ring_key in sorted(self.ring.keys()):
            if ring_key >= hash_val:
                return self.ring[ring_key]
        return self.ring[min(self.ring.keys())]  # Wrap around

    def add_shard(self, shard):
        """Add shard with minimal data movement"""
        self.shards.append(shard)
        self._build_ring()
```

**When to shard**:
- Database approaching limits (CPU, IOPS, connections)
- Storage growth predictably exceeds single instance
- Need geographic distribution

### Pattern: CQRS (Command Query Responsibility Segregation)

**Проблема**: Read и write patterns требуют разных optimizations

**Решение**: Separate read и write paths

```
Write Path:
[Client] → [Command API] → [Write DB (PostgreSQL)] → [Event Bus]
                                                           ↓
Read Path:                                     [Read Model Updater]
[Client] → [Query API] → [Read DB (Elasticsearch)]        ↓
                                              [Materialized Views]
```

**Implementation**:
```python
# Write side
class CommandHandler:
    def create_order(self, order_data):
        # Validate
        order = Order(**order_data)
        order.validate()

        # Save to write database
        db.session.add(order)
        db.session.commit()

        # Publish event
        event_bus.publish('order.created', {
            'order_id': order.id,
            'customer_id': order.customer_id,
            'total': order.total,
            'timestamp': datetime.now()
        })

        return order.id

# Read side
class EventProcessor:
    def handle_order_created(self, event):
        # Update read model (Elasticsearch)
        es.index(
            index='orders',
            id=event['order_id'],
            document={
                'order_id': event['order_id'],
                'customer_id': event['customer_id'],
                'total': event['total'],
                'status': 'pending',
                'created_at': event['timestamp']
            }
        )

        # Update customer view
        es.update(
            index='customers',
            id=event['customer_id'],
            doc={
                'total_orders': {'script': 'ctx._source.total_orders += 1'},
                'lifetime_value': {'script': f"ctx._source.lifetime_value += {event['total']}"}
            }
        )

# Query side
class QueryHandler:
    def search_orders(self, filters):
        # Fast search на optimized read model
        query = {
            'query': {
                'bool': {
                    'must': []
                }
            }
        }

        if 'customer_id' in filters:
            query['query']['bool']['must'].append({
                'term': {'customer_id': filters['customer_id']}
            })

        return es.search(index='orders', body=query)
```

**Benefits**:
- Optimized read models (denormalized, indexed)
- Write scalability (simplified write logic)
- Read scalability (scale read replicas independently)
- Flexibility (multiple read models для different use cases)

## Resilience Patterns

### Pattern: Circuit Breaker

**Проблема**: Cascading failures from failed dependencies

**Решение**: Stop calling failing service, fast-fail

```python
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,
        timeout=60,
        expected_exception=Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
breaker = CircuitBreaker(failure_threshold=3, timeout=30)

def call_external_api():
    return breaker.call(requests.get, 'https://api.example.com')
```

**States**:
- **CLOSED**: Normal, все requests проходят
- **OPEN**: Failing, reject immediately (fast-fail)
- **HALF_OPEN**: Testing recovery, single request через

**Metrics to monitor**:
- Circuit state changes (alert on OPEN)
- Rejection rate (requests blocked)
- Recovery time (OPEN → CLOSED duration)

### Pattern: Bulkhead Isolation

**Проблема**: One failing component exhausts shared resources

**Решение**: Partition resources into pools

```python
import threading
from queue import Queue

class BulkheadExecutor:
    """Isolate resource pools"""

    def __init__(self, pools_config):
        """
        pools_config = {
            'critical': {'size': 20, 'queue': 100},
            'standard': {'size': 50, 'queue': 200},
            'batch': {'size': 30, 'queue': 500}
        }
        """
        self.pools = {}

        for name, config in pools_config.items():
            self.pools[name] = {
                'semaphore': threading.Semaphore(config['size']),
                'queue': Queue(maxsize=config['queue']),
                'size': config['size']
            }

    def submit(self, pool_name, func, *args, **kwargs):
        """Submit task to pool"""
        pool = self.pools[pool_name]

        # Try to acquire slot
        if not pool['semaphore'].acquire(blocking=False):
            # Pool exhausted, check queue
            if pool['queue'].full():
                raise Exception(f"Pool {pool_name} exhausted")

            # Queue for later
            pool['queue'].put((func, args, kwargs))
            return None

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            pool['semaphore'].release()

            # Process queued item if any
            if not pool['queue'].empty():
                queued_func, queued_args, queued_kwargs = pool['queue'].get()
                self.submit(pool_name, queued_func, *queued_args, **queued_kwargs)

# Usage
executor = BulkheadExecutor({
    'payment': {'size': 10, 'queue': 50},  # Critical, limited capacity
    'analytics': {'size': 5, 'queue': 1000}  # Lower priority, large queue
})

# Payment processing (isolated)
executor.submit('payment', process_payment, payment_data)

# Analytics (won't affect payments)
executor.submit('analytics', update_analytics, event_data)
```

**Benefits**:
- Fault isolation (failure in one pool doesn't affect others)
- Priority management (critical pools protected)
- Resource guarantees (each pool guaranteed capacity)

---

**Все архитектурные паттерны документируются в Markdown на русском языке с диаграммами и примерами кода.**
