# OpenFaaS Function Development and Deployment Guide

Complete guide to developing, deploying, and operating OpenFaaS functions in production.

## Table of Contents

1. [Function Templates](#function-templates)
2. [Function Development](#function-development)
3. [Configuration](#configuration)
4. [Secrets and Configuration](#secrets-and-configuration)
5. [Auto-Scaling](#auto-scaling)
6. [Monitoring](#monitoring)
7. [Advanced Patterns](#advanced-patterns)
8. [Production Best Practices](#production-best-practices)

## Function Templates

### Available Templates

```bash
# List all available templates
faas-cli template store list

# Popular templates:
- python3-flask          # Python with Flask
- python3-http          # Python with HTTP context
- python3-debian        # Python on Debian
- node18                # Node.js 18
- node18-express        # Node.js with Express
- golang-http           # Go with HTTP context
- golang-middleware     # Go with middleware support
- java11                # Java 11
- csharp                # C# .NET
- ruby                  # Ruby
- php8                  # PHP 8
- rust                  # Rust
```

### Pull Templates

```bash
# Pull specific template
faas-cli template store pull python3-http

# Pull multiple templates
faas-cli template store pull python3-http golang-http node18

# Pull custom template from Git
faas-cli template pull https://github.com/custom/templates
```

### Custom Templates

Create custom template:

```bash
# Create template directory structure
mkdir -p template/python3-custom
cd template/python3-custom

# Create Dockerfile
cat > Dockerfile <<'EOF'
FROM python:3.11-slim

RUN pip install --no-cache-dir flask gunicorn

WORKDIR /home/app

COPY index.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY function function

ENV fprocess="python index.py"
EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["python", "index.py"]
EOF

# Create template.yml
cat > template.yml <<'EOF'
language: python3-custom
fprocess: python index.py
EOF

# Create handler wrapper
cat > index.py <<'EOF'
import sys
from function import handler

def handle(req):
    """OpenFaaS handler wrapper"""
    return handler.handle(req)

if __name__ == "__main__":
    st = sys.stdin.read()
    ret = handle(st)
    sys.stdout.write(ret)
EOF
```

## Function Development

### Python Examples

**Simple HTTP function (python3-http):**

```python
# handler.py
def handle(event, context):
    """
    Handle HTTP request

    Args:
        event: Request event with body, headers, method, query
        context: OpenFaaS context

    Returns:
        Response dict with statusCode, body, headers
    """
    import json

    # Access request data
    body = json.loads(event.body) if event.body else {}
    method = event.method
    headers = event.headers
    query = event.query
    path = event.path

    # Process request
    result = {
        "message": "Hello from OpenFaaS",
        "method": method,
        "input": body
    }

    # Return response
    return {
        "statusCode": 200,
        "body": json.dumps(result),
        "headers": {
            "Content-Type": "application/json",
            "X-Custom-Header": "value"
        }
    }
```

**Database function with connection pooling:**

```python
# handler.py
import json
import psycopg2
from psycopg2 import pool

# Initialize connection pool at module level (reused across requests)
connection_pool = None

def get_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host="postgres.default.svc.cluster.local",
            port=5432,
            database="mydb",
            user="user",
            password="password"
        )
    return connection_pool

def handle(event, context):
    """Query database with connection pooling"""
    pool = get_pool()
    conn = pool.getconn()

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (event.body,))
        result = cur.fetchone()
        cur.close()

        return {
            "statusCode": 200,
            "body": json.dumps({"user": result})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    finally:
        pool.putconn(conn)

# requirements.txt
# psycopg2-binary==2.9.9
```

**Async function:**

```python
# handler.py
import asyncio
import json
import aiohttp

async def fetch_data(session, url):
    """Fetch data from URL"""
    async with session.get(url) as response:
        return await response.json()

async def process_async(urls):
    """Process multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

def handle(event, context):
    """Handle async requests"""
    body = json.loads(event.body)
    urls = body.get("urls", [])

    # Run async code
    results = asyncio.run(process_async(urls))

    return {
        "statusCode": 200,
        "body": json.dumps({"results": results})
    }

# requirements.txt
# aiohttp==3.9.1
```

### Node.js Examples

**Simple HTTP function (node18-express):**

```javascript
// handler.js
module.exports = async (event, context) => {
  const body = JSON.parse(event.body);
  const method = event.method;
  const headers = event.headers;

  // Process request
  const result = {
    message: "Hello from OpenFaaS",
    method: method,
    input: body
  };

  return context
    .status(200)
    .succeed(result);
};

// package.json
{
  "name": "function",
  "version": "1.0.0",
  "main": "handler.js",
  "dependencies": {
    "axios": "^1.6.0"
  }
}
```

**Database function with connection pooling:**

```javascript
// handler.js
const { Pool } = require('pg');

// Initialize pool at module level (reused across requests)
const pool = new Pool({
  host: 'postgres.default.svc.cluster.local',
  port: 5432,
  database: 'mydb',
  user: 'user',
  password: 'password',
  max: 10,
  idleTimeoutMillis: 30000
});

module.exports = async (event, context) => {
  const userId = event.body;

  try {
    const client = await pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE id = $1',
        [userId]
      );
      return context.status(200).succeed({
        user: result.rows[0]
      });
    } finally {
      client.release();
    }
  } catch (error) {
    return context.status(500).succeed({
      error: error.message
    });
  }
};

// package.json
{
  "dependencies": {
    "pg": "^8.11.0"
  }
}
```

### Go Examples

**Simple HTTP function (golang-http):**

```go
// handler.go
package function

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type Request struct {
    Message string `json:"message"`
}

type Response struct {
    Result string `json:"result"`
    Status string `json:"status"`
}

func Handle(w http.ResponseWriter, r *http.Request) {
    // Read request body
    body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // Parse JSON
    var req Request
    if err := json.Unmarshal(body, &req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // Process request
    response := Response{
        Result: fmt.Sprintf("Processed: %s", req.Message),
        Status: "success",
    }

    // Return JSON response
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(response)
}
```

**Database function with connection pooling:**

```go
// handler.go
package function

import (
    "database/sql"
    "encoding/json"
    "net/http"
    "sync"

    _ "github.com/lib/pq"
)

var (
    db   *sql.DB
    once sync.Once
)

func initDB() {
    connStr := "host=postgres.default.svc.cluster.local port=5432 user=user password=password dbname=mydb sslmode=disable"
    var err error
    db, err = sql.Open("postgres", connStr)
    if err != nil {
        panic(err)
    }

    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
}

func Handle(w http.ResponseWriter, r *http.Request) {
    // Initialize DB connection once
    once.Do(initDB)

    // Query database
    var name string
    err := db.QueryRow("SELECT name FROM users WHERE id = $1", 1).Scan(&name)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Return response
    response := map[string]string{"name": name}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

// go.mod
module function

go 1.21

require github.com/lib/pq v1.10.9
```

## Configuration

### Stack File (YAML)

**Complete example:**

```yaml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  my-function:
    lang: python3-http
    handler: ./my-function
    image: myregistry.io/my-function:latest

    # Build options
    build_args:
      PYTHON_VERSION: "3.11"
      ADDITIONAL_PACKAGE: "opencv-python"
    build_options:
    - name: dev
      platforms: linux/amd64,linux/arm64

    # Resource limits
    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "100m"
      memory: "128Mi"

    # Environment variables
    environment:
      DATABASE_HOST: postgres.default.svc.cluster.local
      CACHE_ENABLED: "true"
      LOG_LEVEL: info
      read_timeout: "60s"
      write_timeout: "60s"
      exec_timeout: "60s"

    # Environment variables from secrets
    environment_file:
    - database.env

    # Secrets (mounted at /var/openfaas/secrets/)
    secrets:
    - db-password
    - api-key

    # Labels for auto-scaling
    labels:
      com.openfaas.scale.min: "2"
      com.openfaas.scale.max: "50"
      com.openfaas.scale.factor: "5"
      com.openfaas.scale.type: "rps"
      com.openfaas.scale.target: "100"
      com.openfaas.scale.zero: "false"
      com.openfaas.scale.zero-duration: "5m"

    # Annotations
    annotations:
      prometheus.io.scrape: "true"
      prometheus.io.port: "8080"
      prometheus.io.path: "/metrics"
      kubernetes.io/ingress.class: "nginx"

    # Node selection
    constraints:
    - "node.kubernetes.io/instance-type=c5.large"

    # Readiness probe
    readiness_probe:
      initial_delay_seconds: 5
      timeout_seconds: 3
      period_seconds: 10

    # Liveness probe
    liveness_probe:
      initial_delay_seconds: 15
      timeout_seconds: 3
      period_seconds: 10
```

### Multi-Function Stack

```yaml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  api-gateway:
    lang: node18-express
    handler: ./api-gateway
    image: myregistry.io/api-gateway:latest
    labels:
      com.openfaas.scale.min: "3"
      com.openfaas.scale.max: "20"
    environment:
      AUTH_SERVICE_URL: http://gateway.openfaas:8080/function/auth-service

  auth-service:
    lang: python3-http
    handler: ./auth-service
    image: myregistry.io/auth-service:latest
    secrets:
    - jwt-secret
    labels:
      com.openfaas.scale.min: "2"
      com.openfaas.scale.max: "10"

  data-processor:
    lang: golang-http
    handler: ./data-processor
    image: myregistry.io/data-processor:latest
    limits:
      cpu: "2000m"
      memory: "4Gi"
    labels:
      com.openfaas.scale.type: "capacity"
      com.openfaas.scale.target: "20"
      com.openfaas.scale.min: "1"
      com.openfaas.scale.max: "100"
```

## Secrets and Configuration

### Create Secrets

```bash
# Create secret from file
faas-cli secret create db-password --from-file=./db-password.txt

# Create secret from stdin
echo "my-secret-value" | faas-cli secret create api-key

# Create secret from literal (Kubernetes)
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password=secret123 \
  -n openfaas-fn
```

### Access Secrets in Function

**Python:**
```python
# handler.py
import os

def handle(event, context):
    # Read secret from file
    with open('/var/openfaas/secrets/db-password', 'r') as f:
        db_password = f.read().strip()

    # Use secret
    connection_string = f"postgresql://user:{db_password}@host/db"

    return {"status": "connected"}
```

**Node.js:**
```javascript
// handler.js
const fs = require('fs');

module.exports = async (event, context) => {
  // Read secret from file
  const apiKey = fs.readFileSync('/var/openfaas/secrets/api-key', 'utf8').trim();

  // Use secret
  const response = await fetch('https://api.example.com', {
    headers: {
      'Authorization': `Bearer ${apiKey}`
    }
  });

  return context.status(200).succeed({status: 'ok'});
};
```

**Go:**
```go
// handler.go
package function

import (
    "io/ioutil"
    "strings"
)

func Handle(w http.ResponseWriter, r *http.Request) {
    // Read secret from file
    secretBytes, err := ioutil.ReadFile("/var/openfaas/secrets/api-key")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    apiKey := strings.TrimSpace(string(secretBytes))

    // Use secret
    // ...
}
```

### Environment Files

Create environment file:
```bash
# database.env
DATABASE_HOST=postgres.default.svc.cluster.local
DATABASE_PORT=5432
DATABASE_NAME=mydb
DATABASE_USER=user
```

Reference in stack file:
```yaml
functions:
  my-function:
    environment_file:
    - database.env
```

## Auto-Scaling

### Scaling Configuration

**RPS-based scaling (Requests Per Second):**
```yaml
labels:
  com.openfaas.scale.type: "rps"
  com.openfaas.scale.target: "100"    # Scale when RPS exceeds 100 per pod
  com.openfaas.scale.min: "1"
  com.openfaas.scale.max: "50"
  com.openfaas.scale.factor: "5"      # Scale up/down by 5 pods at a time
```

**Capacity-based scaling (Concurrent Requests):**
```yaml
labels:
  com.openfaas.scale.type: "capacity"
  com.openfaas.scale.target: "20"     # Scale when concurrent requests exceed 20
  com.openfaas.scale.min: "1"
  com.openfaas.scale.max: "50"
```

**CPU-based scaling:**
```yaml
labels:
  com.openfaas.scale.type: "cpu"
  com.openfaas.scale.target: "80"     # Scale when CPU exceeds 80%
  com.openfaas.scale.min: "1"
  com.openfaas.scale.max: "50"
```

### Scale-to-Zero

```yaml
labels:
  com.openfaas.scale.zero: "true"
  com.openfaas.scale.zero-duration: "5m"  # Idle time before scaling to zero
  com.openfaas.scale.min: "0"
```

**Enable scale-to-zero in OpenFaaS:**
```bash
# Install with scale-to-zero enabled
helm upgrade --install openfaas openfaas/openfaas \
  --namespace openfaas \
  --set faasnetes.imagePullPolicy=Always \
  --set gateway.scaleFromZero=true \
  --set gateway.readTimeout=60s \
  --set gateway.writeTimeout=60s
```

### Custom HPA

Create custom HPA for advanced scaling:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-function-hpa
  namespace: openfaas-fn
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-function
  minReplicas: 2
  maxReplicas: 100
  metrics:
  # CPU-based
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Memory-based
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # Custom metric (queue depth)
  - type: External
    external:
      metric:
        name: queue_depth
        selector:
          matchLabels:
            queue: my-function-queue
      target:
        type: AverageValue
        averageValue: "30"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

## Monitoring

### Prometheus Metrics

OpenFaaS exposes metrics at `/metrics`:

```promql
# Request rate
sum(rate(gateway_function_invocation_total[1m])) by (function_name)

# Request duration
histogram_quantile(0.95,
  sum(rate(gateway_functions_seconds_bucket[5m])) by (le, function_name)
)

# Error rate
sum(rate(gateway_function_invocation_total{code!="200"}[5m])) by (function_name)

# Replica count
gateway_service_count{function_name="my-function"}

# Invocations in flight
gateway_functions_invocation_inflight{function_name="my-function"}
```

### Grafana Dashboard

**Key metrics dashboard:**
```json
{
  "dashboard": {
    "title": "OpenFaaS Functions",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(gateway_function_invocation_total[5m])) by (function_name)"
          }
        ]
      },
      {
        "title": "P95 Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(gateway_functions_seconds_bucket[5m])) by (le, function_name))"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "sum(rate(gateway_function_invocation_total{code!=\"200\"}[5m])) by (function_name) / sum(rate(gateway_function_invocation_total[5m])) by (function_name)"
          }
        ]
      },
      {
        "title": "Active Replicas",
        "targets": [
          {
            "expr": "gateway_service_count"
          }
        ]
      }
    ]
  }
}
```

### Custom Metrics in Functions

**Python with Prometheus client:**
```python
# handler.py
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

# Define metrics
REQUEST_COUNT = Counter(
    'function_requests_total',
    'Total function requests',
    ['status']
)

REQUEST_DURATION = Histogram(
    'function_request_duration_seconds',
    'Function request duration'
)

def handle(event, context):
    import time
    start_time = time.time()

    try:
        # Process request
        result = process_request(event.body)

        REQUEST_COUNT.labels(status='success').inc()
        return {"statusCode": 200, "body": result}
    except Exception as e:
        REQUEST_COUNT.labels(status='error').inc()
        return {"statusCode": 500, "body": str(e)}
    finally:
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)

# requirements.txt
# prometheus-client==0.19.0
```

## Advanced Patterns

### Function Chaining

Call one function from another:

```python
# handler.py
import requests
import json

GATEWAY_URL = "http://gateway.openfaas:8080"

def handle(event, context):
    # Process initial request
    data = json.loads(event.body)

    # Call another function
    response = requests.post(
        f"{GATEWAY_URL}/function/data-transformer",
        json=data,
        timeout=30
    )

    transformed = response.json()

    # Call third function
    response = requests.post(
        f"{GATEWAY_URL}/function/data-saver",
        json=transformed,
        timeout=30
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "completed"})
    }
```

### Async Function with Queue

Use NATS queue for async processing:

```yaml
# Install NATS
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm install nats nats/nats

# Configure OpenFaaS to use NATS
helm upgrade --install openfaas openfaas/openfaas \
  --set queueWorker.nats.enabled=true \
  --set queueWorker.nats.address=nats.default.svc.cluster.local
```

**Invoke function asynchronously:**
```bash
# Async invocation
curl http://gateway:8080/async-function/my-function \
  -d '{"data": "value"}' \
  -H "X-Callback-Url: http://callback-service/webhook"
```

**Python async handler:**
```python
# handler.py
import json

def handle(event, context):
    """Long-running task"""
    data = json.loads(event.body)

    # Process data (may take minutes)
    result = long_running_task(data)

    # If callback URL provided, call it
    callback_url = event.headers.get('X-Callback-Url')
    if callback_url:
        import requests
        requests.post(callback_url, json={"result": result})

    return {
        "statusCode": 202,
        "body": json.dumps({"status": "processing"})
    }
```

### Middleware Pattern

Add middleware for auth, logging, etc.:

```python
# middleware.py
import functools
import time
import json

def require_auth(func):
    """Authentication middleware"""
    @functools.wraps(func)
    def wrapper(event, context):
        # Check auth token
        auth_header = event.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Unauthorized"})
            }

        # Validate token
        token = auth_header[7:]
        if not validate_token(token):
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "Invalid token"})
            }

        # Call actual handler
        return func(event, context)
    return wrapper

def log_requests(func):
    """Logging middleware"""
    @functools.wraps(func)
    def wrapper(event, context):
        start_time = time.time()

        print(f"Request: {event.method} {event.path}")

        result = func(event, context)

        duration = time.time() - start_time
        print(f"Response: {result.get('statusCode')} ({duration:.3f}s)")

        return result
    return wrapper

# handler.py
from middleware import require_auth, log_requests

@require_auth
@log_requests
def handle(event, context):
    """Protected endpoint"""
    return {
        "statusCode": 200,
        "body": json.dumps({"data": "secret"})
    }
```

## Production Best Practices

### 1. Error Handling

```python
# handler.py
import json
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle(event, context):
    try:
        # Validate input
        if not event.body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing request body"})
            }

        # Parse and validate
        try:
            data = json.loads(event.body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON"})
            }

        # Process
        result = process_data(data)

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        logger.error(f"Internal error: {e}\n{traceback.format_exc()}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
```

### 2. Timeouts

```yaml
environment:
  read_timeout: "60s"      # Client read timeout
  write_timeout: "60s"     # Client write timeout
  exec_timeout: "60s"      # Function execution timeout
  upstream_timeout: "50s"  # Backend timeout (should be less than exec_timeout)
```

### 3. Health Checks

```python
# handler.py
def handle(event, context):
    # Health check endpoint
    if event.path == "/_/health":
        # Check dependencies
        if not check_database():
            return {
                "statusCode": 503,
                "body": json.dumps({"status": "unhealthy", "reason": "database"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "healthy"})
        }

    # Normal request handling
    return process_request(event)
```

### 4. Request ID Tracing

```python
# handler.py
import uuid
import logging

def handle(event, context):
    # Get or generate request ID
    request_id = event.headers.get('X-Request-ID', str(uuid.uuid4()))

    # Add to logger
    logger = logging.LoggerAdapter(
        logging.getLogger(__name__),
        {'request_id': request_id}
    )

    logger.info("Processing request")

    # Include in response
    return {
        "statusCode": 200,
        "body": json.dumps({"data": "value"}),
        "headers": {
            "X-Request-ID": request_id
        }
    }
```

### 5. Rate Limiting

Use Kubernetes NetworkPolicy or Istio for rate limiting:

```yaml
# Istio rate limit
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-function-rate-limit
spec:
  host: my-function.openfaas-fn.svc.cluster.local
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 100
        maxRequestsPerConnection: 1
```

### 6. Resource Management

```yaml
# Right-size resources
limits:
  cpu: "1000m"
  memory: "1Gi"
requests:
  cpu: "100m"
  memory: "256Mi"

# Set appropriate timeout
environment:
  exec_timeout: "30s"

# Configure auto-scaling
labels:
  com.openfaas.scale.min: "2"
  com.openfaas.scale.max: "50"
  com.openfaas.scale.target: "100"
```

### 7. CI/CD Integration

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - cd my-function
    - pip install -r requirements.txt
    - pytest tests/

build:
  stage: build
  script:
    - faas-cli build -f my-function.yml

deploy:
  stage: deploy
  script:
    - faas-cli login --gateway $OPENFAAS_GATEWAY --password $OPENFAAS_PASSWORD
    - faas-cli push -f my-function.yml
    - faas-cli deploy -f my-function.yml
  only:
    - main
```

## Troubleshooting

### Function Not Starting

```bash
# Check function logs
faas-cli logs my-function

# Describe function (Kubernetes)
kubectl describe deploy -n openfaas-fn my-function

# Check events
kubectl get events -n openfaas-fn --sort-by='.lastTimestamp'
```

### High Latency

```bash
# Check metrics
curl http://gateway:8080/system/metrics

# Check concurrent requests
kubectl get hpa -n openfaas-fn

# Increase resources or replicas
faas-cli deploy -f my-function.yml \
  --label com.openfaas.scale.min=5
```

### Memory Issues

```bash
# Check memory usage
kubectl top pods -n openfaas-fn

# Increase memory limit
faas-cli deploy -f my-function.yml \
  --limit-memory 2Gi \
  --request-memory 1Gi
```
