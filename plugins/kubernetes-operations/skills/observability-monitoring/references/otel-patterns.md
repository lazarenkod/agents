# OpenTelemetry Instrumentation Patterns

## Паттерны инструментирования с OpenTelemetry / Instrumentation Patterns

### Auto-Instrumentation vs Manual Instrumentation

**Auto-instrumentation** - Zero-code observability:
- Uses language-specific agents
- Automatic trace context propagation
- Minimal configuration
- Good for standard frameworks

**Manual instrumentation** - Fine-grained control:
- Custom spans and attributes
- Business logic tracking
- Performance optimization
- Custom metrics and events

## Language-Specific Instrumentation

### Python with FastAPI

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

# Configure resource attributes
resource = Resource.create({
    "service.name": "my-api",
    "service.version": "1.0.0",
    "deployment.environment": "production",
})

# Set up tracer provider
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure OTLP exporter to collector
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True,
)

# Add batch processor for efficiency
tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Auto-instrument FastAPI
from fastapi import FastAPI
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Manual instrumentation for custom spans
tracer = trace.get_tracer(__name__)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    with tracer.start_as_current_span("fetch_user") as span:
        # Add custom attributes
        span.set_attribute("user.id", user_id)
        span.set_attribute("user.tier", "premium")

        # Your business logic
        user = await fetch_user_from_db(user_id)

        # Add event
        span.add_event("user_fetched", {
            "user.country": user.country,
            "cache.hit": False,
        })

        return user
```

### Go with HTTP Server

```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func initTracer(ctx context.Context) (*sdktrace.TracerProvider, error) {
    // Configure resource
    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName("my-service"),
            semconv.ServiceVersion("1.0.0"),
            semconv.DeploymentEnvironment("production"),
        ),
    )
    if err != nil {
        return nil, err
    }

    // Configure OTLP exporter
    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    // Create tracer provider with batch processor
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.ParentBased(
            sdktrace.TraceIDRatioBased(0.1), // 10% sampling
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func main() {
    ctx := context.Background()
    tp, err := initTracer(ctx)
    if err != nil {
        panic(err)
    }
    defer tp.Shutdown(ctx)

    // Wrap HTTP handler with instrumentation
    handler := otelhttp.NewHandler(
        http.HandlerFunc(handleRequest),
        "my-service",
    )

    http.ListenAndServe(":8080", handler)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tracer := otel.Tracer("my-service")

    // Create custom span
    ctx, span := tracer.Start(ctx, "process_request")
    defer span.End()

    // Add attributes
    span.SetAttributes(
        attribute.String("user.id", r.Header.Get("X-User-ID")),
        attribute.String("request.path", r.URL.Path),
    )

    // Add event
    span.AddEvent("processing_started")

    // Your business logic here
    result := processRequest(ctx)

    span.AddEvent("processing_completed",
        trace.WithAttributes(
            attribute.Int("result.count", len(result)),
        ),
    )

    w.Write([]byte("OK"))
}
```

### Node.js with Express

```javascript
const opentelemetry = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

// Configure SDK
const sdk = new opentelemetry.NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-app',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4317',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': {
        enabled: false, // Disable high-cardinality instrumentation
      },
    }),
  ],
});

sdk.start();

// Manual instrumentation
const express = require('express');
const { trace } = require('@opentelemetry/api');

const app = express();
const tracer = trace.getTracer('my-app');

app.get('/api/users/:id', async (req, res) => {
  const span = tracer.startSpan('get_user');

  span.setAttributes({
    'user.id': req.params.id,
    'http.route': '/api/users/:id',
  });

  try {
    const user = await fetchUser(req.params.id);

    span.addEvent('user_fetched', {
      'user.country': user.country,
      'cache.hit': false,
    });

    res.json(user);
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    res.status(500).send('Error');
  } finally {
    span.end();
  }
});

app.listen(3000);

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('SDK shut down successfully'))
    .catch((error) => console.log('Error shutting down SDK', error))
    .finally(() => process.exit(0));
});
```

## Kubernetes Deployment Patterns

### Sidecar Injection Pattern

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        sidecar.opentelemetry.io/inject: "true"
    spec:
      containers:
      - name: app
        image: my-app:1.0.0
        env:
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://localhost:4317"
        - name: OTEL_SERVICE_NAME
          value: "my-app"
        - name: OTEL_RESOURCE_ATTRIBUTES
          value: "deployment.environment=production,service.version=1.0.0"
```

### DaemonSet Collector Pattern

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector-contrib:0.90.0
        args:
        - --config=/conf/otel-collector-config.yaml
        ports:
        - name: otlp-grpc
          containerPort: 4317
          hostPort: 4317
        - name: otlp-http
          containerPort: 4318
          hostPort: 4318
        volumeMounts:
        - name: config
          mountPath: /conf
      volumes:
      - name: config
        configMap:
          name: otel-collector-config
```

## Sampling Strategies

### Head-Based Sampling

**Always Decision (before creating span):**

```yaml
# otel-collector-config.yaml
processors:
  probabilistic_sampler:
    sampling_percentage: 10  # Keep 10% of traces
```

### Tail-Based Sampling

**After Decision (after span completes):**

```yaml
processors:
  tail_sampling:
    decision_wait: 30s  # Wait for complete trace
    num_traces: 100000
    expected_new_traces_per_sec: 1000
    policies:
    # Keep all error traces
    - name: errors
      type: status_code
      status_code:
        status_codes: [ERROR]

    # Keep slow traces (>1s)
    - name: slow-requests
      type: latency
      latency:
        threshold_ms: 1000

    # Keep specific endpoints
    - name: critical-endpoints
      type: string_attribute
      string_attribute:
        key: http.route
        values: ["/api/checkout", "/api/payment"]

    # Random sample of everything else
    - name: random-sample
      type: probabilistic
      probabilistic:
        sampling_percentage: 1
```

## Correlation Between Signals

### Trace-Metrics Correlation

```yaml
# Exemplars in Prometheus metrics
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: "app"
    enable_open_metrics: true  # Enable exemplars

  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]

    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

**Query with exemplars:**

```promql
# Get trace IDs for high latency requests
http_request_duration_seconds_bucket{le="1.0"}
```

### Trace-Logs Correlation

**Add trace context to logs:**

```python
import logging
from opentelemetry import trace

# Configure logger to include trace context
logging.basicConfig(
    format='%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] - %(message)s'
)

# In your code
span = trace.get_current_span()
logger.info(
    "User action completed",
    extra={
        "otelTraceID": format(span.get_span_context().trace_id, '032x'),
        "otelSpanID": format(span.get_span_context().span_id, '016x'),
        "user.id": user_id,
    }
)
```

## Best Practices

### 1. Resource Attributes

**Always include:**

```python
resource = Resource.create({
    # Service identification
    "service.name": "my-api",
    "service.version": "1.0.0",
    "service.namespace": "production",

    # Deployment
    "deployment.environment": "production",
    "deployment.id": os.getenv("DEPLOYMENT_ID"),

    # Infrastructure
    "cloud.provider": "aws",
    "cloud.region": "us-east-1",
    "k8s.cluster.name": "prod-cluster",
    "k8s.namespace.name": "default",
    "k8s.pod.name": os.getenv("HOSTNAME"),
    "k8s.container.name": "api",
})
```

### 2. Span Attributes

**Follow semantic conventions:**

```python
# HTTP attributes
span.set_attributes({
    "http.method": "GET",
    "http.route": "/api/users/:id",
    "http.status_code": 200,
    "http.url": "https://api.example.com/api/users/123",
})

# Database attributes
span.set_attributes({
    "db.system": "postgresql",
    "db.name": "users_db",
    "db.statement": "SELECT * FROM users WHERE id = ?",
    "db.operation": "SELECT",
})

# RPC attributes
span.set_attributes({
    "rpc.system": "grpc",
    "rpc.service": "UserService",
    "rpc.method": "GetUser",
})

# Custom business attributes
span.set_attributes({
    "user.id": "123",
    "user.tier": "premium",
    "cart.item_count": 5,
    "order.total": 99.99,
})
```

### 3. Context Propagation

**Ensure trace context propagates across services:**

```python
from opentelemetry.propagate import inject, extract

# Outgoing HTTP request
headers = {}
inject(headers)  # Inject trace context into headers
requests.get("http://backend-service/api", headers=headers)

# Incoming HTTP request (in backend service)
ctx = extract(request.headers)  # Extract trace context
with tracer.start_as_current_span("process_request", context=ctx):
    # Process request
    pass
```

### 4. Span Lifecycle

```python
tracer = trace.get_tracer(__name__)

def process_order(order_id):
    # Start span
    with tracer.start_as_current_span("process_order") as span:
        # Set attributes
        span.set_attribute("order.id", order_id)

        try:
            # Add events at key points
            span.add_event("validation_started")
            validate_order(order_id)
            span.add_event("validation_completed")

            span.add_event("payment_processing")
            payment = process_payment(order_id)
            span.add_event("payment_completed", {
                "payment.amount": payment.amount,
                "payment.method": payment.method,
            })

            # Span automatically ends when exiting context
            return payment

        except ValidationError as e:
            # Record exception
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, "Validation failed"))
            raise
```

## Performance Optimization

### 1. Reduce Span Overhead

**Avoid creating spans in hot paths:**

```python
# Bad: Creates span for every iteration
for item in items:
    with tracer.start_as_current_span(f"process_{item.id}"):
        process_item(item)

# Good: Single span for batch operation
with tracer.start_as_current_span("process_items") as span:
    span.set_attribute("item.count", len(items))
    for item in items:
        process_item(item)
```

### 2. Batch Export

```yaml
processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
    send_batch_max_size: 2048
```

### 3. Resource Limits

```yaml
spec:
  containers:
  - name: otel-collector
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 2000m
        memory: 4Gi
```

## Troubleshooting

### Trace Not Appearing

1. **Check collector is receiving spans:**
```bash
kubectl logs -n monitoring otel-collector | grep "Trace ID"
```

2. **Verify exporter configuration:**
```bash
# Check collector metrics
curl http://otel-collector:8888/metrics | grep otelcol_exporter
```

3. **Check sampling decision:**
```python
span = trace.get_current_span()
if span.get_span_context().trace_flags.sampled:
    print("Span is sampled")
else:
    print("Span is not sampled")
```

### High Cardinality

**Avoid:**
```python
# BAD: User ID as span attribute (millions of unique values)
span.set_attribute("user.id", user_id)
```

**Use instead:**
```python
# GOOD: User tier (limited cardinality)
span.set_attribute("user.tier", user_tier)

# Or use events for high-cardinality data
span.add_event("user_action", {"user.id": user_id})
```

## References

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Semantic Conventions](https://opentelemetry.io/docs/reference/specification/trace/semantic_conventions/)
- [Sampling Documentation](https://opentelemetry.io/docs/reference/specification/trace/sdk/#sampling)
- [Auto-Instrumentation](https://opentelemetry.io/docs/instrumentation/)
