# Knative Serving and Eventing Patterns

Advanced patterns and best practices for Knative Serving and Eventing in production environments.

## Knative Serving Patterns

### 1. Blue-Green Deployment

Deploy new version alongside old version, then switch traffic instantly:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
spec:
  traffic:
  # Blue (current production)
  - revisionName: my-service-00001
    percent: 100
    tag: blue
  # Green (new version, not receiving traffic yet)
  - revisionName: my-service-00002
    percent: 0
    tag: green
  - latestRevision: false
```

**Switch traffic to green:**
```bash
kn service update my-service \
  --traffic my-service-00001=0 \
  --traffic my-service-00002=100
```

**Instant rollback if issues:**
```bash
kn service update my-service \
  --traffic my-service-00001=100 \
  --traffic my-service-00002=0
```

### 2. Canary Deployment with Progressive Rollout

Gradually increase traffic to new version while monitoring metrics:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api-service
spec:
  traffic:
  - revisionName: api-service-v1
    percent: 90
    tag: stable
  - revisionName: api-service-v2
    percent: 10
    tag: canary
  - latestRevision: true
    percent: 0
    tag: latest
```

**Progressive rollout script:**
```bash
#!/bin/bash
SERVICE="api-service"
OLD_REV="api-service-v1"
NEW_REV="api-service-v2"

# Start with 10% canary
kn service update $SERVICE --traffic $OLD_REV=90,$NEW_REV=10
sleep 300  # Monitor for 5 minutes

# Check error rate
ERROR_RATE=$(kubectl exec -n monitoring prometheus-0 -- \
  promtool query instant http://localhost:9090 \
  'rate(http_requests_total{service="'$SERVICE'",code=~"5.."}[5m]) / rate(http_requests_total{service="'$SERVICE'"}[5m])')

if (( $(echo "$ERROR_RATE < 0.01" | bc -l) )); then
  # Increase to 25%
  kn service update $SERVICE --traffic $OLD_REV=75,$NEW_REV=25
  sleep 300
fi

# Continue progressive rollout...
# 50%
kn service update $SERVICE --traffic $OLD_REV=50,$NEW_REV=50
sleep 300

# 75%
kn service update $SERVICE --traffic $OLD_REV=25,$NEW_REV=75
sleep 300

# 100%
kn service update $SERVICE --traffic $OLD_REV=0,$NEW_REV=100
```

### 3. A/B Testing

Split traffic between versions for testing:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: frontend
spec:
  traffic:
  # Version A - 50% of traffic
  - revisionName: frontend-v1
    percent: 50
    tag: version-a
  # Version B - 50% of traffic
  - revisionName: frontend-v2
    percent: 50
    tag: version-b
```

**Header-based routing (using Istio):**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: frontend-ab-test
spec:
  hosts:
  - frontend.default.example.com
  http:
  - match:
    - headers:
        X-User-Group:
          exact: beta-testers
    route:
    - destination:
        host: version-b-frontend.default.svc.cluster.local
  - route:
    - destination:
        host: version-a-frontend.default.svc.cluster.local
```

### 4. Multi-Region Active-Active

Deploy same service across multiple regions:

```yaml
# us-east cluster
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "5"
        autoscaling.knative.dev/max-scale: "100"
      labels:
        region: us-east
    spec:
      containers:
      - image: myregistry/api-service:v1.0.0
        env:
        - name: REGION
          value: "us-east"
        - name: DATABASE_URL
          value: "postgres://us-east-db:5432/api"
---
# eu-west cluster
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "5"
        autoscaling.knative.dev/max-scale: "100"
      labels:
        region: eu-west
    spec:
      containers:
      - image: myregistry/api-service:v1.0.0
        env:
        - name: REGION
          value: "eu-west"
        - name: DATABASE_URL
          value: "postgres://eu-west-db:5432/api"
```

**Global load balancing (Cloudflare example):**
```javascript
// Cloudflare Worker for geo-routing
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const country = request.cf.country

  let region = 'us-east'
  if (['GB', 'FR', 'DE', 'IT', 'ES'].includes(country)) {
    region = 'eu-west'
  } else if (['JP', 'CN', 'KR', 'SG'].includes(country)) {
    region = 'ap-southeast'
  }

  const url = `https://api-service.${region}.example.com${new URL(request.url).pathname}`
  return fetch(url, request)
}
```

### 5. Schedule-Based Scaling

Scale services based on time of day:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-up-business-hours
spec:
  schedule: "0 8 * * 1-5"  # 8 AM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: scaler
          containers:
          - name: scaler
            image: bitnami/kubectl:latest
            command:
            - kubectl
            - annotate
            - ksvc/api-service
            - autoscaling.knative.dev/min-scale=10
            - --overwrite
          restartPolicy: OnFailure
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-off-hours
spec:
  schedule: "0 18 * * 1-5"  # 6 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: scaler
          containers:
          - name: scaler
            image: bitnami/kubectl:latest
            command:
            - kubectl
            - annotate
            - ksvc/api-service
            - autoscaling.knative.dev/min-scale=2
            - --overwrite
          restartPolicy: OnFailure
```

### 6. Request-Based Auto-Scaling with Queuing

Handle traffic spikes with queue-based scaling:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: batch-processor
spec:
  template:
    metadata:
      annotations:
        # Target queue depth per pod
        autoscaling.knative.dev/metric: "rps"
        autoscaling.knative.dev/target: "10"

        # Panic mode (rapid scale-up)
        autoscaling.knative.dev/panic-threshold-percentage: "200"
        autoscaling.knative.dev/panic-window-percentage: "10"

        # Stable window
        autoscaling.knative.dev/stable-window: "60s"

        # Scale bounds
        autoscaling.knative.dev/min-scale: "1"
        autoscaling.knative.dev/max-scale: "100"
    spec:
      containerConcurrency: 5  # Process 5 requests per pod
      containers:
      - image: myregistry/batch-processor
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
```

## Knative Eventing Patterns

### 1. Saga Pattern (Distributed Transactions)

Implement long-running distributed transactions with compensating actions:

```yaml
# Order service creates order and publishes event
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
      - image: myregistry/order-service
        env:
        - name: BROKER_URL
          value: http://broker-ingress.knative-eventing.svc.cluster.local/default/default
---
# Trigger: Reserve inventory
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: inventory-reservation
spec:
  broker: default
  filter:
    attributes:
      type: order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: inventory-service
---
# Trigger: Process payment
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: payment-processing
spec:
  broker: default
  filter:
    attributes:
      type: inventory.reserved
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: payment-service
---
# Trigger: Compensate if payment fails
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: inventory-compensation
spec:
  broker: default
  filter:
    attributes:
      type: payment.failed
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: inventory-compensator
```

**Saga coordinator (example):**
```python
from cloudevents.http import CloudEvent, to_structured
import requests

class SagaOrchestrator:
    def __init__(self, broker_url):
        self.broker_url = broker_url
        self.saga_state = {}

    def start_saga(self, order_id, order_data):
        """Start saga for order processing"""
        saga_id = f"saga-{order_id}"
        self.saga_state[saga_id] = {
            "status": "started",
            "steps_completed": [],
            "order_data": order_data
        }

        # Step 1: Reserve inventory
        self.publish_event("order.created", order_data)
        return saga_id

    def handle_event(self, event):
        """Handle saga events"""
        event_type = event['type']
        saga_id = event['data']['saga_id']

        if event_type == "inventory.reserved":
            self.saga_state[saga_id]["steps_completed"].append("inventory")
            # Trigger next step: payment
            self.publish_event("payment.process", event['data'])

        elif event_type == "payment.completed":
            self.saga_state[saga_id]["steps_completed"].append("payment")
            self.saga_state[saga_id]["status"] = "completed"
            self.publish_event("order.completed", event['data'])

        elif event_type == "payment.failed":
            # Compensate: release inventory
            self.saga_state[saga_id]["status"] = "compensating"
            self.publish_event("inventory.release", event['data'])

        elif event_type == "inventory.released":
            self.saga_state[saga_id]["status"] = "failed"
            self.publish_event("order.failed", event['data'])

    def publish_event(self, event_type, data):
        """Publish CloudEvent to broker"""
        event = CloudEvent({
            "type": event_type,
            "source": "saga-orchestrator",
        }, data)

        headers, body = to_structured(event)
        requests.post(self.broker_url, headers=headers, data=body)
```

### 2. Event Sourcing Pattern

Store all changes as sequence of events:

```yaml
# Event store service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: event-store
spec:
  template:
    spec:
      containers:
      - image: myregistry/event-store
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
---
# Aggregate events into current state
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: projection-updater
spec:
  broker: default
  filter:
    attributes:
      type: account.event.*
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: projection-service
```

**Event store implementation (Python example):**
```python
from datetime import datetime
import json

class EventStore:
    def __init__(self, db_connection):
        self.db = db_connection

    def append_event(self, aggregate_id, event_type, event_data):
        """Append event to event stream"""
        self.db.execute("""
            INSERT INTO events (aggregate_id, event_type, event_data, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (aggregate_id, event_type, json.dumps(event_data), datetime.utcnow()))

        # Publish event to broker
        self.publish_to_broker(event_type, {
            "aggregate_id": aggregate_id,
            **event_data
        })

    def get_events(self, aggregate_id, from_version=0):
        """Get all events for aggregate"""
        result = self.db.execute("""
            SELECT event_type, event_data, version
            FROM events
            WHERE aggregate_id = %s AND version > %s
            ORDER BY version ASC
        """, (aggregate_id, from_version))
        return list(result)

    def rebuild_aggregate(self, aggregate_id):
        """Rebuild current state from events"""
        events = self.get_events(aggregate_id)
        state = {}

        for event in events:
            state = self.apply_event(state, event['event_type'], event['event_data'])

        return state

    def apply_event(self, state, event_type, event_data):
        """Apply event to state"""
        if event_type == "account.created":
            return {
                "id": event_data["account_id"],
                "balance": 0,
                "status": "active"
            }
        elif event_type == "account.credited":
            state["balance"] += event_data["amount"]
            return state
        elif event_type == "account.debited":
            state["balance"] -= event_data["amount"]
            return state
        # ... more event handlers
        return state
```

### 3. CQRS (Command Query Responsibility Segregation)

Separate read and write models:

```yaml
# Command service (writes)
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: command-service
spec:
  template:
    spec:
      containers:
      - image: myregistry/command-service
        env:
        - name: WRITE_DB_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: write-url
        - name: BROKER_URL
          value: http://broker-ingress.knative-eventing.svc.cluster.local/default/default
---
# Query service (reads)
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: query-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/min-scale: "3"
        autoscaling.knative.dev/max-scale: "50"
    spec:
      containers:
      - image: myregistry/query-service
        env:
        - name: READ_DB_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: read-url
---
# Projection builder (updates read model)
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: read-model-updater
spec:
  broker: default
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: projection-builder
```

### 4. Event Replay Pattern

Replay events for debugging or rebuilding state:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: event-replay
spec:
  template:
    spec:
      containers:
      - name: replay
        image: myregistry/event-replayer
        env:
        - name: EVENT_STORE_URL
          value: http://event-store.default.svc.cluster.local
        - name: BROKER_URL
          value: http://broker-ingress.knative-eventing.svc.cluster.local/default/default
        - name: START_TIME
          value: "2024-01-01T00:00:00Z"
        - name: END_TIME
          value: "2024-01-31T23:59:59Z"
        - name: AGGREGATE_ID
          value: "account-12345"
      restartPolicy: Never
```

**Event replayer implementation:**
```python
import requests
from datetime import datetime
from cloudevents.http import CloudEvent, to_structured

class EventReplayer:
    def __init__(self, event_store_url, broker_url):
        self.event_store_url = event_store_url
        self.broker_url = broker_url

    def replay_events(self, start_time, end_time, aggregate_id=None):
        """Replay events within time range"""
        params = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
        if aggregate_id:
            params["aggregate_id"] = aggregate_id

        response = requests.get(f"{self.event_store_url}/events", params=params)
        events = response.json()

        print(f"Replaying {len(events)} events...")

        for event in events:
            # Republish event with replay flag
            cloud_event = CloudEvent({
                "type": event["type"],
                "source": "event-replayer",
                "replay": "true",
                "original_timestamp": event["timestamp"]
            }, event["data"])

            headers, body = to_structured(cloud_event)
            requests.post(self.broker_url, headers=headers, data=body)

        print(f"Replay complete. {len(events)} events published.")
```

### 5. Event Filtering and Transformation

Filter and transform events in flight:

```yaml
# Event filter service
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: event-filter
spec:
  template:
    spec:
      containers:
      - image: myregistry/event-filter
        env:
        - name: FILTER_RULES
          value: |
            {
              "rules": [
                {
                  "match": {"type": "order.*", "source": "legacy-system"},
                  "transform": {
                    "type": "order.v2",
                    "add_fields": {"schema_version": "2.0"}
                  }
                }
              ]
            }
---
# Sequence for multi-step processing
apiVersion: flows.knative.dev/v1
kind: Sequence
metadata:
  name: event-processing-sequence
spec:
  steps:
  - ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-validator
  - ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-enricher
  - ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-transformer
  reply:
    ref:
      apiVersion: eventing.knative.dev/v1
      kind: Broker
      name: default
```

### 6. Event Aggregation Pattern

Aggregate multiple events into summary:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: event-aggregator
spec:
  template:
    spec:
      containers:
      - image: myregistry/event-aggregator
        env:
        - name: AGGREGATION_WINDOW
          value: "60s"
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-credentials
              key: url
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: metrics-aggregation
spec:
  broker: default
  filter:
    attributes:
      type: metric.recorded
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-aggregator
```

**Aggregator implementation:**
```python
import redis
import json
from datetime import datetime, timedelta

class EventAggregator:
    def __init__(self, redis_url, window_seconds=60):
        self.redis = redis.from_url(redis_url)
        self.window_seconds = window_seconds

    def aggregate_event(self, event):
        """Aggregate event into time window"""
        event_type = event['type']
        timestamp = datetime.fromisoformat(event['time'])

        # Calculate window key
        window_start = timestamp - timedelta(
            seconds=timestamp.second % self.window_seconds
        )
        window_key = f"agg:{event_type}:{window_start.isoformat()}"

        # Increment counter
        self.redis.hincrby(window_key, "count", 1)

        # Add to sum if numeric value
        if 'value' in event['data']:
            self.redis.hincrbyfloat(window_key, "sum", event['data']['value'])

        # Set expiry
        self.redis.expire(window_key, self.window_seconds * 2)

        # Check if window is complete
        if self.is_window_complete(window_start):
            return self.publish_aggregate(event_type, window_start)

    def is_window_complete(self, window_start):
        """Check if aggregation window has passed"""
        now = datetime.utcnow()
        window_end = window_start + timedelta(seconds=self.window_seconds)
        return now > window_end + timedelta(seconds=5)  # 5s grace period

    def publish_aggregate(self, event_type, window_start):
        """Publish aggregated metrics"""
        window_key = f"agg:{event_type}:{window_start.isoformat()}"
        data = self.redis.hgetall(window_key)

        aggregate_event = {
            "type": f"{event_type}.aggregated",
            "source": "event-aggregator",
            "data": {
                "window_start": window_start.isoformat(),
                "window_seconds": self.window_seconds,
                "count": int(data.get(b"count", 0)),
                "sum": float(data.get(b"sum", 0))
            }
        }

        # Publish to broker
        self.publish_to_broker(aggregate_event)

        # Clean up
        self.redis.delete(window_key)
```

## Advanced Auto-Scaling Patterns

### Custom Metrics Scaling

Scale based on queue depth, database connections, or custom metrics:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: custom-metrics-api
  namespace: custom-metrics
spec:
  ports:
  - port: 443
    targetPort: 443
  selector:
    app: custom-metrics-adapter
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: queue-based-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: worker
  minReplicas: 1
  maxReplicas: 100
  metrics:
  - type: External
    external:
      metric:
        name: queue_depth
        selector:
          matchLabels:
            queue: priority-tasks
      target:
        type: AverageValue
        averageValue: "30"
```

## Best Practices

### Event Design

1. **Include event metadata:**
   ```json
   {
     "specversion": "1.0",
     "type": "com.example.order.created",
     "source": "order-service",
     "id": "unique-event-id",
     "time": "2024-01-15T10:00:00Z",
     "datacontenttype": "application/json",
     "data": {
       "orderId": "12345",
       "customerId": "67890",
       "amount": 99.99
     }
   }
   ```

2. **Version your events:**
   - Use semantic versioning in event type: `com.example.order.created.v1`
   - Support multiple versions for backward compatibility

3. **Make events immutable:**
   - Never modify published events
   - Publish correction events if needed

4. **Design for idempotency:**
   - Include idempotency key in event
   - Handle duplicate events gracefully

### Monitoring and Observability

**Key metrics to track:**
```yaml
# Knative Serving
- knative_serving_revision_app_request_count
- knative_serving_revision_app_request_latencies
- knative_serving_autoscaler_actual_pods
- knative_serving_autoscaler_desired_pods

# Knative Eventing
- knative_eventing_broker_events_total
- knative_eventing_trigger_events_total
- knative_eventing_delivery_latency
```

**Grafana dashboard queries:**
```promql
# Request rate per service
sum(rate(knative_serving_revision_app_request_count[5m])) by (service_name)

# P95 latency
histogram_quantile(0.95,
  sum(rate(knative_serving_revision_app_request_latencies_bucket[5m])) by (le, service_name)
)

# Scale-from-zero latency
knative_serving_activator_request_latencies

# Event processing lag
knative_eventing_trigger_events_total{result="success"} -
knative_eventing_broker_events_total
```
