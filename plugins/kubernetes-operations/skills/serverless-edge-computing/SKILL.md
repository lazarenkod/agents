---
name: serverless-edge-computing
description: Comprehensive serverless and edge computing for Kubernetes using Knative Serving/Eventing, OpenFaaS, K3s, MicroK8s, and KubeEdge. Implements production-grade serverless functions, event-driven architectures, edge deployments, and cold start optimization. Use when implementing serverless workloads, event-driven systems, edge computing deployments, or optimizing function performance.
---

# Kubernetes Serverless & Edge Computing

Production-grade serverless and edge computing implementation for Kubernetes using Knative, OpenFaaS, and lightweight Kubernetes distributions following best practices from AWS Lambda, Google Cloud Run, Azure Functions, and leading cloud-native companies.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

## When to Use This Skill

- Implement serverless functions on Kubernetes with Knative or OpenFaaS
- Design event-driven architectures with Knative Eventing
- Deploy applications to edge locations with K3s, MicroK8s, or KubeEdge
- Optimize cold start times for serverless functions
- Implement auto-scaling for serverless workloads (including scale-to-zero)
- Build event-driven systems with brokers, triggers, and channels
- Deploy lightweight Kubernetes clusters for IoT and edge computing
- Implement traffic splitting and blue-green deployments for functions
- Design distributed edge computing architectures
- Troubleshoot serverless and edge deployments

## Core Serverless Concepts

### Serverless Computing on Kubernetes

**Key characteristics:**
1. **Scale-to-zero** - Pods scale down to zero when idle, saving costs
2. **Event-driven** - Functions triggered by HTTP requests or events
3. **Auto-scaling** - Automatic scaling based on traffic or metrics
4. **Pay-per-use** - Resources consumed only during execution
5. **Rapid deployment** - Quick iteration and deployment cycles

### Serverless Frameworks

| Framework | Type | Best For | Scale-to-Zero | Language Support |
|-----------|------|----------|---------------|------------------|
| **Knative Serving** | Platform | HTTP workloads, containers | Yes | Any (container-based) |
| **Knative Eventing** | Platform | Event-driven architectures | N/A | Any (with Serving) |
| **OpenFaaS** | Framework | Simple functions, templates | Yes | 20+ languages |
| **Fission** | Framework | Fast cold starts, Python/Node | Yes | Python, Node.js, Go, Java |
| **Kubeless** | Framework | Simple functions | Yes | Python, Node.js, Ruby |

### Edge Computing on Kubernetes

**Key characteristics:**
1. **Distributed architecture** - Workloads run close to data sources
2. **Low latency** - Reduced network round-trip times
3. **Bandwidth optimization** - Process data locally, send only results
4. **Offline capability** - Continue operating without cloud connectivity
5. **Resource constraints** - Optimized for limited CPU/memory

## Knative Serving

### 1. Knative Installation

**Prerequisites:**
```bash
# Install cert-manager (required for webhook certificates)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=Available --timeout=300s deployment/cert-manager -n cert-manager
kubectl wait --for=condition=Available --timeout=300s deployment/cert-manager-webhook -n cert-manager
```

**Install Knative Serving:**
```bash
# Install Knative CRDs
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-crds.yaml

# Install Knative core components
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-core.yaml

# Install networking layer (Kourier - lightweight ingress)
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.12.0/kourier.yaml

# Configure Knative to use Kourier
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

# Configure DNS (use Magic DNS for development)
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.12.0/serving-default-domain.yaml
```

**Production DNS configuration:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-domain
  namespace: knative-serving
data:
  # Replace with your domain
  example.com: ""
```

### 2. Knative Service Deployment

**Reference:** See `assets/knative-service.yaml` for complete examples

**Basic service:**
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: hello-world
  namespace: default
spec:
  template:
    metadata:
      annotations:
        # Auto-scaling configuration
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "10"
        autoscaling.knative.dev/target: "100"
        autoscaling.knative.dev/metric: "concurrency"

        # Scale-down delay (default 0s for scale-to-zero)
        autoscaling.knative.dev/scale-down-delay: "30s"

        # Window for scaling decisions
        autoscaling.knative.dev/window: "60s"
    spec:
      containers:
      - name: user-container
        image: gcr.io/knative-samples/helloworld-go
        ports:
        - containerPort: 8080
        env:
        - name: TARGET
          value: "World"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 1000m
            memory: 512Mi
```

**Production service with optimization:**
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: api-service
  namespace: production
spec:
  template:
    metadata:
      annotations:
        # Auto-scaling
        autoscaling.knative.dev/min-scale: "2"
        autoscaling.knative.dev/max-scale: "100"
        autoscaling.knative.dev/target: "70"
        autoscaling.knative.dev/metric: "rps"
        autoscaling.knative.dev/target-utilization-percentage: "70"

        # Cold start optimization
        autoscaling.knative.dev/activation-scale: "3"
        autoscaling.knative.dev/scale-down-delay: "15m"

        # Request timeout
        serving.knative.dev/timeout: "300s"

        # Progress deadline
        serving.knative.dev/progress-deadline: "600s"
      labels:
        app: api-service
        version: v1
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300

      containers:
      - name: api
        image: myregistry.io/api-service:v1.2.0
        ports:
        - name: http1
          containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: CACHE_ENABLED
          value: "true"
        - name: POOL_SIZE
          value: "20"

        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          successThreshold: 1

        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        # Security context
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
```

### 3. Traffic Splitting and Blue-Green Deployments

**Reference:** See `references/knative-patterns.md` for advanced patterns

**Canary deployment (90/10 split):**
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
spec:
  traffic:
  - revisionName: my-service-v1
    percent: 90
    tag: stable
  - revisionName: my-service-v2
    percent: 10
    tag: canary
  - latestRevision: true
    percent: 0
    tag: latest
```

**Access specific revisions:**
```bash
# Access stable version
curl https://stable-my-service.default.example.com

# Access canary version
curl https://canary-my-service.default.example.com

# Access latest version (0% traffic but accessible by tag)
curl https://latest-my-service.default.example.com
```

**Progressive traffic migration:**
```bash
# Start with canary
kn service update my-service --traffic my-service-v1=90,my-service-v2=10

# Increase canary traffic
kn service update my-service --traffic my-service-v1=70,my-service-v2=30

# Full cutover
kn service update my-service --traffic my-service-v1=0,my-service-v2=100
```

### 4. Auto-Scaling Configuration

**Concurrency-based scaling:**
```yaml
annotations:
  autoscaling.knative.dev/metric: "concurrency"
  autoscaling.knative.dev/target: "100"
  # Scale up when average concurrency exceeds 100 requests per pod
```

**RPS-based scaling:**
```yaml
annotations:
  autoscaling.knative.dev/metric: "rps"
  autoscaling.knative.dev/target: "1000"
  # Scale up when requests per second exceeds 1000 per pod
```

**CPU-based scaling:**
```yaml
annotations:
  autoscaling.knative.dev/metric: "cpu"
  autoscaling.knative.dev/target: "80"
  # Scale up when CPU utilization exceeds 80%
```

**Custom metrics with HPA:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: custom-metric-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-service
  minReplicas: 1
  maxReplicas: 100
  metrics:
  - type: Pods
    pods:
      metric:
        name: queue_depth
      target:
        type: AverageValue
        averageValue: "50"
```

## Knative Eventing

### 1. Knative Eventing Installation

```bash
# Install Knative Eventing CRDs
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.12.0/eventing-crds.yaml

# Install Knative Eventing core
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.12.0/eventing-core.yaml

# Install in-memory channel (for development)
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.12.0/in-memory-channel.yaml

# Install broker
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.12.0/mt-channel-broker.yaml
```

**Production: Install Kafka channel (recommended):**
```bash
kubectl apply -f https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.12.0/eventing-kafka-controller.yaml
kubectl apply -f https://github.com/knative-sandbox/eventing-kafka-broker/releases/download/knative-v1.12.0/eventing-kafka-broker.yaml
```

### 2. Event Sources

**Reference:** See `references/knative-patterns.md` for event source patterns

**PingSource (scheduled events):**
```yaml
apiVersion: sources.knative.dev/v1
kind: PingSource
metadata:
  name: scheduled-task
  namespace: default
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes (cron format)
  contentType: "application/json"
  data: '{"message": "Scheduled task triggered"}'
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: task-processor
```

**ApiServerSource (Kubernetes events):**
```yaml
apiVersion: sources.knative.dev/v1
kind: ApiServerSource
metadata:
  name: pod-watcher
  namespace: default
spec:
  serviceAccountName: pod-watcher-sa
  mode: Resource
  resources:
  - apiVersion: v1
    kind: Pod
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: pod-event-handler
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-watcher-sa
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-watcher-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: pod-watcher-binding
subjects:
- kind: ServiceAccount
  name: pod-watcher-sa
  namespace: default
roleRef:
  kind: ClusterRole
  name: pod-watcher-role
  apiGroup: rbac.authorization.k8s.io
```

**KafkaSource:**
```yaml
apiVersion: sources.knative.dev/v1beta1
kind: KafkaSource
metadata:
  name: kafka-events
  namespace: default
spec:
  consumerGroup: knative-consumer
  bootstrapServers:
  - kafka-broker:9092
  topics:
  - user-events
  - order-events
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-processor
```

### 3. Brokers and Triggers

**Create a broker:**
```yaml
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: default
  namespace: default
  annotations:
    eventing.knative.dev/broker.class: MTChannelBasedBroker
spec:
  config:
    apiVersion: v1
    kind: ConfigMap
    name: config-br-default-channel
    namespace: knative-eventing
```

**Or enable broker for namespace:**
```bash
kubectl label namespace default knative-eventing-injection=enabled
```

**Trigger (event filtering):**
```yaml
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-created-trigger
  namespace: default
spec:
  broker: default
  filter:
    attributes:
      type: com.example.order.created
      source: order-service
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: order-processor
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: payment-trigger
  namespace: default
spec:
  broker: default
  filter:
    attributes:
      type: com.example.payment.processed
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: payment-handler
```

### 4. Channels and Subscriptions

**In-Memory Channel (development only):**
```yaml
apiVersion: messaging.knative.dev/v1
kind: InMemoryChannel
metadata:
  name: events-channel
  namespace: default
```

**Kafka Channel (production):**
```yaml
apiVersion: messaging.knative.dev/v1beta1
kind: KafkaChannel
metadata:
  name: events-channel
  namespace: default
spec:
  numPartitions: 10
  replicationFactor: 3
  retentionDuration: "P7D"  # 7 days
```

**Subscription:**
```yaml
apiVersion: messaging.knative.dev/v1
kind: Subscription
metadata:
  name: event-subscription
  namespace: default
spec:
  channel:
    apiVersion: messaging.knative.dev/v1beta1
    kind: KafkaChannel
    name: events-channel
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-consumer
  delivery:
    deadLetterSink:
      ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: dlq-handler
    retry: 5
    backoffPolicy: exponential
    backoffDelay: "PT1S"
```

## OpenFaaS

### 1. OpenFaaS Installation

**Reference:** See `references/openfaas-guide.md` for complete guide

```bash
# Install arkade (OpenFaaS installer)
curl -sLS https://get.arkade.dev | sudo sh

# Install OpenFaaS
arkade install openfaas

# Or using Helm
helm repo add openfaas https://openfaas.github.io/faas-netes/
helm upgrade --install openfaas openfaas/openfaas \
  --namespace openfaas \
  --create-namespace \
  --set functionNamespace=openfaas-fn \
  --set generateBasicAuth=true \
  --set gateway.replicas=2 \
  --set queueWorker.replicas=2

# Get password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode)
echo "OpenFaaS password: $PASSWORD"

# Port forward to access gateway
kubectl port-forward -n openfaas svc/gateway 8080:8080 &

# Login
echo $PASSWORD | faas-cli login --username admin --password-stdin
```

### 2. Function Development

**Reference:** See `assets/openfaas-function.yaml` for examples

**Create function from template:**
```bash
# List available templates
faas-cli template store list

# Pull template
faas-cli template store pull python3-http

# Create new function
faas-cli new --lang python3-http image-processor

# Directory structure created:
# image-processor/
#   handler.py
#   requirements.txt
# image-processor.yml
```

**Function stack file (image-processor.yml):**
```yaml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080

functions:
  image-processor:
    lang: python3-http
    handler: ./image-processor
    image: myregistry/image-processor:latest

    environment:
      read_timeout: "60s"
      write_timeout: "60s"
      exec_timeout: "60s"

    labels:
      com.openfaas.scale.min: "1"
      com.openfaas.scale.max: "20"
      com.openfaas.scale.factor: "5"
      com.openfaas.scale.type: "rps"
      com.openfaas.scale.target: "100"

    annotations:
      prometheus.io.scrape: "true"

    limits:
      cpu: "1000m"
      memory: "1Gi"
    requests:
      cpu: "100m"
      memory: "128Mi"

    secrets:
    - aws-credentials

    constraints:
    - "node.kubernetes.io/instance-type=c5.large"
```

**Function handler (handler.py):**
```python
import json
import os
from PIL import Image
import io
import base64

def handle(event, context):
    """
    Handle image processing request
    """
    try:
        # Parse request
        body = json.loads(event.body)
        image_data = base64.b64decode(body['image'])

        # Process image
        image = Image.open(io.BytesIO(image_data))

        # Resize
        width = int(body.get('width', 800))
        height = int(body.get('height', 600))
        resized = image.resize((width, height), Image.LANCZOS)

        # Convert to bytes
        output = io.BytesIO()
        resized.save(output, format='JPEG', quality=85)
        processed_data = base64.b64encode(output.getvalue()).decode()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "image": processed_data,
                "size": len(processed_data)
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
```

**Build and deploy:**
```bash
# Build function
faas-cli build -f image-processor.yml

# Push to registry
faas-cli push -f image-processor.yml

# Deploy to OpenFaaS
faas-cli deploy -f image-processor.yml

# Or all in one
faas-cli up -f image-processor.yml
```

**Invoke function:**
```bash
# Invoke function
echo '{"image": "base64_data...", "width": 1024, "height": 768}' | \
  faas-cli invoke image-processor
```

### 3. Auto-Scaling Configuration

**HPA-based scaling:**
```yaml
functions:
  my-function:
    labels:
      # Scale based on RPS
      com.openfaas.scale.type: "rps"
      com.openfaas.scale.target: "100"
      com.openfaas.scale.min: "1"
      com.openfaas.scale.max: "50"

      # Or scale based on capacity (concurrent requests)
      # com.openfaas.scale.type: "capacity"
      # com.openfaas.scale.target: "20"

      # Scale-to-zero
      com.openfaas.scale.zero: "true"
      com.openfaas.scale.zero-duration: "5m"
```

### 4. Secrets Management

```bash
# Create secret from file
faas-cli secret create aws-credentials --from-file=credentials.json

# Create secret from literal
echo "my-api-key" | faas-cli secret create api-key

# Use in function
faas-cli deploy -f function.yml --secret api-key

# Access in function
cat /var/openfaas/secrets/api-key
```

## Edge Computing

### 1. K3s - Lightweight Kubernetes

**Reference:** See `references/edge-computing.md` for deployment patterns

**Installation:**
```bash
# Install K3s server
curl -sfL https://get.k3s.io | sh -

# Install K3s agent (on edge nodes)
curl -sfL https://get.k3s.io | K3S_URL=https://myserver:6443 K3S_TOKEN=mytoken sh -

# Get kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config

# Disable default components (for minimal footprint)
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --disable servicelb --disable metrics-server" sh -
```

**Production deployment with high availability:**
```bash
# First server node
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san load-balancer.example.com \
  --datastore-endpoint="mysql://user:pass@tcp(mysql.example.com:3306)/k3s"

# Additional server nodes
curl -sfL https://get.k3s.io | sh -s - server \
  --server https://existing-server:6443 \
  --token TOKEN_FROM_EXISTING_SERVER \
  --datastore-endpoint="mysql://user:pass@tcp(mysql.example.com:3306)/k3s"

# Agent nodes
curl -sfL https://get.k3s.io | K3S_URL=https://load-balancer.example.com:6443 \
  K3S_TOKEN=TOKEN sh -
```

**Resource optimization for edge:**
```yaml
# Limit kubelet resources
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubelet-config
  namespace: kube-system
data:
  kubelet: |
    apiVersion: kubelet.config.k8s.io/v1beta1
    kind: KubeletConfiguration
    maxPods: 50
    evictionHard:
      memory.available: "100Mi"
      nodefs.available: "5%"
    systemReserved:
      cpu: "100m"
      memory: "256Mi"
```

### 2. MicroK8s - Minimal Kubernetes

```bash
# Install MicroK8s
sudo snap install microk8s --classic

# Add user to group
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube

# Enable essential addons
microk8s enable dns storage

# Optional addons
microk8s enable ingress
microk8s enable metrics-server
microk8s enable prometheus

# Get kubeconfig
microk8s config > ~/.kube/config

# Create cluster
microk8s add-node
# Run the join command on other nodes
```

**Configure for edge deployment:**
```bash
# Disable unused services
microk8s disable dashboard
microk8s disable metallb

# Configure low resource profile
cat <<EOF | microk8s kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: edge-quota
  namespace: default
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 2Gi
    limits.cpu: "4"
    limits.memory: 4Gi
EOF
```

### 3. KubeEdge - Cloud-Edge Architecture

**Cloud side installation:**
```bash
# Download keadm
wget https://github.com/kubeedge/kubeedge/releases/download/v1.15.0/keadm-v1.15.0-linux-amd64.tar.gz
tar -zxvf keadm-v1.15.0-linux-amd64.tar.gz
sudo cp keadm /usr/local/bin/

# Initialize cloud core
keadm init --advertise-address=CLOUD_NODE_IP --kube-config=/root/.kube/config

# Get token for edge nodes
keadm gettoken
```

**Edge side installation:**
```bash
# Install edge core
keadm join --cloudcore-ipport=CLOUD_NODE_IP:10000 --token=TOKEN --edgenode-name=edge-node-1

# Verify
kubectl get nodes
```

**Deploy edge application:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edge-app
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: edge-app
  template:
    metadata:
      labels:
        app: edge-app
    spec:
      nodeSelector:
        node-role.kubernetes.io/edge: ""
      containers:
      - name: app
        image: myregistry/edge-app:latest
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        env:
        - name: EDGE_MODE
          value: "true"
        - name: SYNC_INTERVAL
          value: "300"
```

**Edge device management with DeviceModel:**
```yaml
apiVersion: devices.kubeedge.io/v1alpha2
kind: DeviceModel
metadata:
  name: temperature-sensor
  namespace: default
spec:
  properties:
  - name: temperature
    description: Current temperature reading
    type:
      int:
        accessMode: ReadOnly
        unit: celsius
  - name: humidity
    description: Current humidity reading
    type:
      int:
        accessMode: ReadOnly
        unit: percentage
---
apiVersion: devices.kubeedge.io/v1alpha2
kind: Device
metadata:
  name: sensor-001
  namespace: default
spec:
  deviceModelRef:
    name: temperature-sensor
  nodeSelector:
    nodeSelectorTerms:
    - matchExpressions:
      - key: kubernetes.io/hostname
        operator: In
        values:
        - edge-node-1
  protocol:
    modbus:
      slaveID: 1
```

## Cold Start Optimization

### 1. Container Optimization

**Multi-stage builds:**
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-s -w" -o main .

# Runtime stage (minimal image)
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/main /
EXPOSE 8080
ENTRYPOINT ["/main"]
```

**Image optimization:**
```dockerfile
# Use slim base images
FROM python:3.11-slim

# Combine RUN commands to reduce layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Use .dockerignore
# .git
# tests/
# *.md
```

### 2. Application Optimization

**Lazy initialization (Python example):**
```python
# Bad: Initialize on import
import tensorflow as tf
model = tf.keras.models.load_model('model.h5')  # Slow startup

def handle(req):
    return model.predict(req.data)

# Good: Lazy initialization
import tensorflow as tf

_model = None

def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model('model.h5')
    return _model

def handle(req):
    model = get_model()
    return model.predict(req.data)
```

**Connection pooling:**
```python
# Bad: Create connection per request
def handle(req):
    db = connect_to_database()  # Slow
    result = db.query(req.sql)
    db.close()
    return result

# Good: Connection pool
from sqlalchemy import create_engine, pool

engine = create_engine(
    'postgresql://user:pass@host/db',
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

def handle(req):
    with engine.connect() as conn:
        result = conn.execute(req.sql)
    return result
```

### 3. Knative Cold Start Optimization

```yaml
spec:
  template:
    metadata:
      annotations:
        # Keep minimum replicas warm
        autoscaling.knative.dev/min-scale: "1"

        # Aggressive scale-up during cold start
        autoscaling.knative.dev/activation-scale: "3"

        # Longer grace period before scale-down
        autoscaling.knative.dev/scale-down-delay: "10m"

        # Target utilization to trigger scale-up early
        autoscaling.knative.dev/target-utilization-percentage: "70"
    spec:
      containers:
      - name: app
        # Fast startup probe
        startupProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 1
          failureThreshold: 30

        # Quick readiness check
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 1
```

### 4. Pre-warming Strategies

**Scheduled warmup:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: function-warmer
  namespace: default
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: warmer
            image: curlimages/curl:latest
            command:
            - sh
            - -c
            - |
              curl -s https://my-function.default.example.com/health
          restartPolicy: OnFailure
```

**Predictive scaling:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: predictive-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-function
  minReplicas: 1
  maxReplicas: 100
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
```

## Event-Driven Patterns

### 1. Fan-Out Pattern

**Single event triggers multiple handlers:**
```yaml
# Event source publishes to broker
apiVersion: sources.knative.dev/v1
kind: PingSource
metadata:
  name: order-events
spec:
  schedule: "*/1 * * * *"
  data: '{"orderId": "12345", "amount": 100}'
  sink:
    ref:
      apiVersion: eventing.knative.dev/v1
      kind: Broker
      name: default
---
# Multiple triggers subscribe to same event type
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: inventory-update
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
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: notification-send
spec:
  broker: default
  filter:
    attributes:
      type: order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: notification-service
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: analytics-track
spec:
  broker: default
  filter:
    attributes:
      type: order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: analytics-service
```

### 2. Event Chaining Pattern

**Output of one function triggers another:**
```yaml
# First function processes and emits new event
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-processor
spec:
  template:
    spec:
      containers:
      - image: myregistry/order-processor
        env:
        - name: K_SINK
          value: http://broker-ingress.knative-eventing.svc.cluster.local/default/default
---
# Trigger for next step in chain
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: payment-processor
spec:
  broker: default
  filter:
    attributes:
      type: order.validated
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: payment-processor
---
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: shipment-creator
spec:
  broker: default
  filter:
    attributes:
      type: payment.completed
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: shipment-service
```

### 3. Dead Letter Queue Pattern

```yaml
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: order-trigger
spec:
  broker: default
  filter:
    attributes:
      type: order.created
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: order-processor
  delivery:
    deadLetterSink:
      ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: dlq-handler
    retry: 5
    backoffPolicy: exponential
    backoffDelay: PT1S
```

## Best Practices

### 1. Serverless Function Design

- **Single responsibility** - Each function should do one thing well
- **Stateless** - Store state in external systems (databases, caches)
- **Idempotent** - Handle duplicate events gracefully
- **Fast startup** - Optimize container images and initialization
- **Connection reuse** - Use connection pools, cache clients
- **Graceful degradation** - Handle downstream failures
- **Proper timeouts** - Set realistic execution timeouts
- **Resource limits** - Define CPU/memory requests and limits

### 2. Event-Driven Architecture

- **Event versioning** - Include version in event type
- **Schema validation** - Validate event payloads
- **Dead letter queues** - Handle failed events
- **Idempotency keys** - Prevent duplicate processing
- **Event ordering** - Consider ordering guarantees
- **Retry policies** - Implement exponential backoff
- **Observability** - Add tracing and logging
- **Event documentation** - Document event schemas

### 3. Edge Computing

- **Offline capability** - Design for intermittent connectivity
- **Local storage** - Cache critical data locally
- **Bandwidth optimization** - Compress data, batch updates
- **Security** - Encrypt data at rest and in transit
- **Resource constraints** - Optimize for limited CPU/memory
- **Remote management** - Enable remote updates and monitoring
- **Failover** - Handle cloud connectivity loss
- **Data synchronization** - Implement sync strategies

### 4. Auto-Scaling

- **Appropriate metrics** - Choose RPS, concurrency, or custom metrics
- **Min/max replicas** - Set realistic boundaries
- **Scale-down delay** - Balance cost vs. cold starts
- **Target utilization** - Leave headroom for traffic spikes
- **Activation scale** - Warm up multiple instances during cold start
- **HPA configuration** - Tune stabilization windows
- **Load testing** - Validate scaling behavior

## Troubleshooting

### Knative Issues

**Service not accessible:**
```bash
# Check service status
kubectl get ksvc

# Check revision status
kubectl get revision

# Check route configuration
kubectl get route

# Check configuration
kubectl get configuration

# Describe service for events
kubectl describe ksvc my-service

# Check activator logs (for scale-from-zero)
kubectl logs -n knative-serving -l app=activator

# Check autoscaler logs
kubectl logs -n knative-serving -l app=autoscaler
```

**Scaling issues:**
```bash
# Check current metrics
kubectl get podautoscaler

# Check HPA status
kubectl get hpa

# View scaling events
kubectl get events --sort-by='.lastTimestamp'

# Check metrics server
kubectl top pods
```

### OpenFaaS Issues

**Function deployment failures:**
```bash
# Check function status
faas-cli list

# Describe function
faas-cli describe my-function

# Check logs
faas-cli logs my-function

# Check gateway logs
kubectl logs -n openfaas deploy/gateway

# Check queue worker logs
kubectl logs -n openfaas deploy/queue-worker
```

**Scaling issues:**
```bash
# Check auto-scaling labels
kubectl get deploy -n openfaas-fn my-function -o yaml | grep -A 5 labels

# Check Prometheus metrics
kubectl port-forward -n openfaas svc/prometheus 9090:9090
# Visit http://localhost:9090

# Query function metrics
gateway_function_invocation_total{function_name="my-function"}
```

### Edge Computing Issues

**K3s issues:**
```bash
# Check K3s status
sudo systemctl status k3s

# View K3s logs
sudo journalctl -u k3s -f

# Check agent connection
kubectl get nodes

# View agent logs
sudo journalctl -u k3s-agent -f
```

**KubeEdge connectivity:**
```bash
# Check edge node status
kubectl get nodes

# Check cloudcore logs
kubectl logs -n kubeedge deployment/cloudcore

# Check edgecore logs (on edge node)
journalctl -u edgecore -f

# Test connectivity
curl http://CLOUDCORE_IP:10002/readyz
```

## Performance Optimization

### 1. Cold Start Reduction

**Measured improvements:**
- Distroless images: 40-60% faster startup
- Connection pooling: 70% reduction in initialization time
- Lazy loading: 50-80% improvement in cold start
- Min scale > 0: Eliminates cold starts (at cost of resources)

### 2. Resource Optimization

**Right-sizing:**
```yaml
# Under-provisioned (frequent OOM)
requests:
  memory: 64Mi
limits:
  memory: 128Mi

# Right-sized (optimal)
requests:
  memory: 256Mi
limits:
  memory: 512Mi

# Over-provisioned (wasted resources)
requests:
  memory: 2Gi
limits:
  memory: 4Gi
```

### 3. Network Optimization

**Keep-alive connections:**
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
session.mount('http://', adapter)
session.mount('https://', adapter)

def handle(req):
    # Reuse session across requests
    response = session.get('https://api.example.com/data')
    return response.json()
```

## References

- `references/knative-patterns.md` - Advanced Knative serving and eventing patterns
- `references/openfaas-guide.md` - Complete OpenFaaS function development guide
- `references/edge-computing.md` - Edge deployment patterns and architectures

## Assets

- `assets/knative-service.yaml` - Knative service examples with various configurations
- `assets/openfaas-function.yaml` - OpenFaaS function templates and examples

## Related Skills

- `observability-monitoring` - Monitoring serverless and edge deployments
- `k8s-security-policies` - Securing serverless functions
- `service-mesh-patterns` - Service mesh integration with serverless
- `cicd-pipelines` - CI/CD for serverless functions
