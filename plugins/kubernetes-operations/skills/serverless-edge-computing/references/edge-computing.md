# Edge Computing Deployment Patterns

Complete guide to deploying and managing Kubernetes at the edge with K3s, MicroK8s, and KubeEdge.

## Table of Contents

1. [Edge Computing Architecture](#edge-computing-architecture)
2. [K3s Deployment](#k3s-deployment)
3. [MicroK8s Deployment](#microk8s-deployment)
4. [KubeEdge Deployment](#kubeedge-deployment)
5. [Edge Workload Patterns](#edge-workload-patterns)
6. [Data Synchronization](#data-synchronization)
7. [Security](#security)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

## Edge Computing Architecture

### Architecture Patterns

**1. Cloud-Edge Hierarchy:**
```
Cloud Datacenter
├── Region 1 (Central Hub)
│   ├── Edge Location 1 (K3s Cluster)
│   ├── Edge Location 2 (K3s Cluster)
│   └── Edge Location 3 (K3s Cluster)
└── Region 2 (Central Hub)
    ├── Edge Location 4 (MicroK8s)
    └── Edge Location 5 (KubeEdge)
```

**2. Distributed Edge:**
```
Manufacturing Plant
├── Factory Floor Gateway (KubeEdge)
│   ├── Production Line 1 (Edge Devices)
│   ├── Production Line 2 (Edge Devices)
│   └── Quality Control (Edge Devices)
└── Warehouse Gateway (K3s)
    ├── Inventory Scanners
    └── Robotics Control
```

### When to Use Each Solution

| Solution | Use Case | Hardware | Network |
|----------|----------|----------|---------|
| **K3s** | Edge clusters, IoT gateways, retail stores | 512MB+ RAM | Stable connectivity |
| **MicroK8s** | Developer workstations, CI/CD, small clusters | 1GB+ RAM | Stable connectivity |
| **KubeEdge** | IoT devices, intermittent connectivity, cloud-edge | 256MB+ RAM | Intermittent OK |

## K3s Deployment

### Single Node Installation

**Quick installation:**
```bash
# Install K3s server
curl -sfL https://get.k3s.io | sh -

# Check status
sudo systemctl status k3s

# Get kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config
sed -i 's/127.0.0.1/SERVER_IP/g' ~/.kube/config

# Check nodes
kubectl get nodes
```

**Custom installation:**
```bash
# Install with custom options
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server \
  --disable traefik \
  --disable servicelb \
  --disable local-storage \
  --write-kubeconfig-mode 644 \
  --node-name edge-gateway-1 \
  --node-label location=retail-store-1 \
  --node-label region=us-east" sh -
```

### High Availability Cluster

**External database (PostgreSQL):**
```bash
# Install PostgreSQL
apt-get install postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE k3s;
CREATE USER k3s WITH ENCRYPTED PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE k3s TO k3s;

# Install first server node
curl -sfL https://get.k3s.io | sh -s - server \
  --datastore-endpoint="postgres://k3s:secure-password@localhost:5432/k3s" \
  --tls-san load-balancer.example.com \
  --write-kubeconfig-mode 644

# Get token
sudo cat /var/lib/rancher/k3s/server/node-token

# Install additional server nodes
curl -sfL https://get.k3s.io | sh -s - server \
  --datastore-endpoint="postgres://k3s:secure-password@DB_HOST:5432/k3s" \
  --tls-san load-balancer.example.com
```

**Embedded etcd (3+ nodes):**
```bash
# First server node
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san load-balancer.example.com

# Get token
sudo cat /var/lib/rancher/k3s/server/node-token

# Additional server nodes
curl -sfL https://get.k3s.io | sh -s - server \
  --server https://FIRST_SERVER_IP:6443 \
  --token NODE_TOKEN
```

### Agent Nodes

```bash
# Install agent
curl -sfL https://get.k3s.io | K3S_URL=https://SERVER_IP:6443 \
  K3S_TOKEN=NODE_TOKEN \
  INSTALL_K3S_EXEC="agent \
    --node-name edge-device-1 \
    --node-label device-type=camera \
    --node-label location=entrance" sh -
```

### Production Configuration

**Server configuration (/etc/rancher/k3s/config.yaml):**
```yaml
write-kubeconfig-mode: "0644"
tls-san:
  - "k3s.example.com"
  - "10.0.0.100"

# Disable unnecessary components
disable:
  - traefik
  - servicelb
  - local-storage

# Resource limits
kube-apiserver-arg:
  - "max-requests-inflight=400"
  - "max-mutating-requests-inflight=200"

kube-controller-manager-arg:
  - "node-monitor-period=5s"
  - "node-monitor-grace-period=20s"
  - "pod-eviction-timeout=30s"

kubelet-arg:
  - "max-pods=50"
  - "eviction-hard=memory.available<100Mi,nodefs.available<5%"
  - "system-reserved=cpu=100m,memory=256Mi"
```

**Agent configuration (/etc/rancher/k3s/config.yaml):**
```yaml
server: https://k3s-server:6443
token: "your-token-here"
node-name: edge-device-1
node-label:
  - "location=retail-store-1"
  - "device-type=gateway"
  - "hardware=raspberry-pi-4"

kubelet-arg:
  - "max-pods=30"
  - "eviction-hard=memory.available<50Mi"
```

### Airgap Installation

**Download required files:**
```bash
# Download K3s binary
wget https://github.com/k3s-io/k3s/releases/download/v1.28.5+k3s1/k3s
chmod +x k3s
sudo mv k3s /usr/local/bin/

# Download images
wget https://github.com/k3s-io/k3s/releases/download/v1.28.5+k3s1/k3s-airgap-images-amd64.tar.gz
sudo mkdir -p /var/lib/rancher/k3s/agent/images/
sudo cp k3s-airgap-images-amd64.tar.gz /var/lib/rancher/k3s/agent/images/
```

**Install script:**
```bash
#!/bin/bash
# Install K3s in airgap mode
INSTALL_K3S_SKIP_DOWNLOAD=true \
INSTALL_K3S_EXEC="server --disable traefik" \
/path/to/install.sh
```

## MicroK8s Deployment

### Installation

```bash
# Install MicroK8s
sudo snap install microk8s --classic --channel=1.28/stable

# Add user to group
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s

# Check status
microk8s status --wait-ready

# Enable essential addons
microk8s enable dns
microk8s enable storage
microk8s enable ingress

# Get kubeconfig
microk8s config > ~/.kube/config
```

### High Availability Cluster

```bash
# On first node
microk8s add-node

# Copy join command and run on second node
microk8s join 10.0.0.1:25000/TOKEN

# Repeat for third node
microk8s add-node
# Run join command on third node
```

### Essential Addons

```bash
# DNS
microk8s enable dns

# Storage (local path)
microk8s enable storage

# Ingress (NGINX)
microk8s enable ingress

# Metrics server
microk8s enable metrics-server

# Prometheus
microk8s enable prometheus

# Registry
microk8s enable registry

# RBAC
microk8s enable rbac

# Cert-manager
microk8s enable cert-manager

# List all addons
microk8s status
```

### Production Configuration

**MicroK8s settings:**
```bash
# Configure kubelet
echo "--max-pods=50" >> /var/snap/microk8s/current/args/kubelet
echo "--eviction-hard=memory.available<100Mi" >> /var/snap/microk8s/current/args/kubelet

# Configure API server
echo "--max-requests-inflight=400" >> /var/snap/microk8s/current/args/kube-apiserver

# Restart MicroK8s
microk8s stop
microk8s start
```

### Resource Constraints

```bash
# Set memory limit for MicroK8s
sudo snap set microk8s memory=4096

# Set CPU limit
sudo snap set microk8s cpu=2
```

## KubeEdge Deployment

### Cloud Side Installation

**Install Kubernetes cluster:**
```bash
# Use any Kubernetes distribution
# For example, K3s
curl -sfL https://get.k3s.io | sh -
```

**Install CloudCore:**
```bash
# Download keadm
VERSION=v1.15.0
wget https://github.com/kubeedge/kubeedge/releases/download/$VERSION/keadm-$VERSION-linux-amd64.tar.gz
tar -zxvf keadm-$VERSION-linux-amd64.tar.gz
sudo cp keadm /usr/local/bin/

# Install CloudCore
sudo keadm init --advertise-address=CLOUD_NODE_IP \
  --kubeedge-version=$VERSION \
  --kube-config=/root/.kube/config

# Check CloudCore status
kubectl get pods -n kubeedge
```

**Get token for edge nodes:**
```bash
sudo keadm gettoken
```

**Configure CloudCore:**
```yaml
# /etc/kubeedge/config/cloudcore.yaml
apiVersion: cloudcore.config.kubeedge.io/v1alpha2
kind: CloudCore
kubeAPIConfig:
  kubeConfig: /root/.kube/config
  master: ""
  qps: 100
  burst: 200
modules:
  cloudHub:
    advertiseAddress:
      - CLOUD_NODE_IP
    nodeLimit: 1000
    websocket:
      enable: true
      port: 10000
    quic:
      enable: false
      port: 10001
  cloudStream:
    enable: true
    streamPort: 10003
  dynamicController:
    enable: true
```

### Edge Side Installation

**Install EdgeCore:**
```bash
# Download keadm
VERSION=v1.15.0
wget https://github.com/kubeedge/kubeedge/releases/download/$VERSION/keadm-$VERSION-linux-amd64.tar.gz
tar -zxvf keadm-$VERSION-linux-amd64.tar.gz
sudo cp keadm /usr/local/bin/

# Install container runtime (Docker or containerd)
sudo apt-get install docker.io

# Join edge node to cloud
sudo keadm join \
  --cloudcore-ipport=CLOUD_NODE_IP:10000 \
  --token=TOKEN \
  --edgenode-name=edge-node-1 \
  --kubeedge-version=$VERSION

# Check EdgeCore status
sudo systemctl status edgecore
```

**Configure EdgeCore:**
```yaml
# /etc/kubeedge/config/edgecore.yaml
apiVersion: edgecore.config.kubeedge.io/v1alpha2
kind: EdgeCore
modules:
  edged:
    enable: true
    tailoredKubeletConfig:
      maxPods: 50
      imageGCHighThresholdPercent: 80
      imageGCLowThresholdPercent: 40
  edgeHub:
    enable: true
    heartbeat: 15
    httpServer: https://CLOUD_NODE_IP:10002
    websocket:
      enable: true
      server: CLOUD_NODE_IP:10000
  eventBus:
    enable: true
    mqttMode: 0  # 0=internal, 1=external, 2=both
    mqttServerInternal: tcp://127.0.0.1:1883
```

### Device Management

**Define DeviceModel:**
```yaml
apiVersion: devices.kubeedge.io/v1alpha2
kind: DeviceModel
metadata:
  name: temperature-sensor-model
  namespace: default
spec:
  properties:
  - name: temperature
    description: Temperature reading in Celsius
    type:
      int:
        accessMode: ReadOnly
        maximum: 100
        minimum: -40
        unit: celsius
  - name: humidity
    description: Humidity percentage
    type:
      int:
        accessMode: ReadOnly
        maximum: 100
        minimum: 0
        unit: percentage
  - name: status
    description: Device status
    type:
      string:
        accessMode: ReadWrite
        defaultValue: active
```

**Create Device instance:**
```yaml
apiVersion: devices.kubeedge.io/v1alpha2
kind: Device
metadata:
  name: sensor-001
  namespace: default
spec:
  deviceModelRef:
    name: temperature-sensor-model
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
    common:
      com:
        serialPort: /dev/ttyUSB0
        baudRate: 9600
        dataBits: 8
        parity: "none"
        stopBits: 1
  propertyVisitors:
  - propertyName: temperature
    modbus:
      register: holding
      offset: 0
      limit: 1
      scale: 0.1
  - propertyName: humidity
    modbus:
      register: holding
      offset: 1
      limit: 1
```

**Read device data:**
```bash
# Get device status
kubectl get device sensor-001 -o yaml

# Get device twin (current values)
kubectl get device sensor-001 -o jsonpath='{.status.twins}'
```

## Edge Workload Patterns

### 1. Data Processing at Edge

**Local processing with cloud sync:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: video-analytics
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: video-analytics
  template:
    metadata:
      labels:
        app: video-analytics
    spec:
      nodeSelector:
        kubernetes.io/hostname: edge-gateway-1
      containers:
      - name: analytics
        image: myregistry/video-analytics:latest
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        env:
        - name: CAMERA_URL
          value: "rtsp://camera.local/stream"
        - name: CLOUD_ENDPOINT
          value: "https://cloud.example.com/api/events"
        - name: LOCAL_STORAGE
          value: "/data"
        - name: SYNC_INTERVAL
          value: "300"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: edge-storage
```

### 2. Offline-First Applications

**Application with local cache:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pos-system
  namespace: retail
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pos-system
  template:
    metadata:
      labels:
        app: pos-system
    spec:
      nodeSelector:
        location: retail-store-1
      containers:
      - name: pos
        image: myregistry/pos-system:latest
        env:
        - name: OFFLINE_MODE
          value: "true"
        - name: CACHE_SIZE
          value: "1000"
        - name: SYNC_ENDPOINT
          value: "https://central.example.com/api/sync"
        volumeMounts:
        - name: cache
          mountPath: /cache
      - name: redis
        image: redis:7-alpine
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: cache
        emptyDir: {}
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-storage
```

### 3. IoT Data Collection

**Collector deployment:**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: iot-collector
  namespace: iot
spec:
  selector:
    matchLabels:
      app: iot-collector
  template:
    metadata:
      labels:
        app: iot-collector
    spec:
      hostNetwork: true
      containers:
      - name: collector
        image: myregistry/iot-collector:latest
        securityContext:
          privileged: true
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        env:
        - name: MQTT_BROKER
          value: "tcp://mqtt.local:1883"
        - name: COLLECTION_INTERVAL
          value: "10"
        - name: BUFFER_SIZE
          value: "10000"
        volumeMounts:
        - name: dev
          mountPath: /dev
        - name: buffer
          mountPath: /buffer
      volumes:
      - name: dev
        hostPath:
          path: /dev
      - name: buffer
        emptyDir:
          medium: Memory
          sizeLimit: 128Mi
```

### 4. Edge AI Inference

**ML model inference:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: object-detection
  namespace: ai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: object-detection
  template:
    metadata:
      labels:
        app: object-detection
    spec:
      nodeSelector:
        hardware: nvidia-jetson
      containers:
      - name: inference
        image: myregistry/object-detection:latest
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
            nvidia.com/gpu: 1
          limits:
            cpu: 2000m
            memory: 4Gi
            nvidia.com/gpu: 1
        env:
        - name: MODEL_PATH
          value: "/models/yolov8n.onnx"
        - name: CONFIDENCE_THRESHOLD
          value: "0.5"
        - name: INPUT_SOURCE
          value: "/dev/video0"
        volumeMounts:
        - name: models
          mountPath: /models
          readOnly: true
        - name: dev
          mountPath: /dev
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: model-storage
      - name: dev
        hostPath:
          path: /dev
```

## Data Synchronization

### 1. Event-Driven Sync with MQTT

**MQTT broker deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mqtt-broker
  namespace: edge
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mqtt-broker
  template:
    metadata:
      labels:
        app: mqtt-broker
    spec:
      containers:
      - name: mosquitto
        image: eclipse-mosquitto:2
        ports:
        - containerPort: 1883
        - containerPort: 9001
        volumeMounts:
        - name: config
          mountPath: /mosquitto/config
        - name: data
          mountPath: /mosquitto/data
      volumes:
      - name: config
        configMap:
          name: mosquitto-config
      - name: data
        persistentVolumeClaim:
          claimName: mqtt-data
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mosquitto-config
  namespace: edge
data:
  mosquitto.conf: |
    listener 1883
    listener 9001
    protocol websockets
    allow_anonymous true
    persistence true
    persistence_location /mosquitto/data/
```

### 2. Database Replication

**PostgreSQL with replication:**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-edge
  namespace: database
spec:
  serviceName: postgres-edge
  replicas: 1
  selector:
    matchLabels:
      app: postgres-edge
  template:
    metadata:
      labels:
        app: postgres-edge
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: POSTGRES_DB
          value: edgedb
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        - name: replication-config
          mountPath: /docker-entrypoint-initdb.d
      volumes:
      - name: replication-config
        configMap:
          name: postgres-replication
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-replication
  namespace: database
data:
  setup-replication.sh: |
    #!/bin/bash
    # Configure logical replication to cloud
    psql -U postgres -d edgedb <<-EOSQL
      CREATE PUBLICATION edge_pub FOR ALL TABLES;
    EOSQL
```

### 3. Object Storage Sync

**Minio with sync:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: storage-sync
  namespace: edge
spec:
  schedule: "*/15 * * * *"  # Every 15 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: sync
            image: minio/mc:latest
            command:
            - /bin/sh
            - -c
            - |
              mc alias set edge http://minio-edge:9000 $MINIO_USER $MINIO_PASS
              mc alias set cloud https://s3.amazonaws.com $AWS_KEY $AWS_SECRET
              mc mirror --overwrite edge/bucket cloud/edge-bucket
            env:
            - name: MINIO_USER
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: user
            - name: MINIO_PASS
              valueFrom:
                secretKeyRef:
                  name: minio-credentials
                  key: password
            - name: AWS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key
            - name: AWS_SECRET
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-key
          restartPolicy: OnFailure
```

## Security

### 1. Network Segmentation

**NetworkPolicy for edge isolation:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: edge-isolation
  namespace: edge
spec:
  podSelector:
    matchLabels:
      tier: edge
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: edge
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # Allow DNS
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
  # Allow cloud sync
  - to:
    - podSelector:
        matchLabels:
          app: cloud-sync
    ports:
    - protocol: TCP
      port: 443
```

### 2. Certificate Management

**Cert-manager for edge certificates:**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: edge-ca-issuer
spec:
  ca:
    secretName: edge-ca-secret
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: edge-gateway-cert
  namespace: edge
spec:
  secretName: edge-gateway-tls
  issuerRef:
    name: edge-ca-issuer
    kind: ClusterIssuer
  dnsNames:
  - edge-gateway.local
  - edge-gateway.edge.svc.cluster.local
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days
```

### 3. Secrets Management

**Sealed Secrets for edge:**
```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Create sealed secret
kubeseal --controller-name=sealed-secrets-controller \
  --controller-namespace=kube-system \
  --format yaml < secret.yaml > sealed-secret.yaml

# Deploy sealed secret
kubectl apply -f sealed-secret.yaml
```

## Monitoring

### Edge Monitoring Stack

**Prometheus for edge:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 30s
      evaluation_interval: 30s
      external_labels:
        cluster: edge-location-1
        region: us-east

    scrape_configs:
    - job_name: 'kubernetes-nodes'
      kubernetes_sd_configs:
      - role: node
      relabel_configs:
      - source_labels: [__address__]
        regex: '(.*):10250'
        replacement: '${1}:9100'
        target_label: __address__

    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

    remote_write:
    - url: https://prometheus-cloud.example.com/api/v1/write
      basic_auth:
        username: edge-location-1
        password_file: /etc/prometheus/cloud-password
```

### Health Checks

**Edge connectivity monitor:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: connectivity-monitor
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: connectivity-monitor
  template:
    metadata:
      labels:
        app: connectivity-monitor
    spec:
      containers:
      - name: monitor
        image: alpine/curl:latest
        command:
        - /bin/sh
        - -c
        - |
          while true; do
            if curl -sf https://cloud.example.com/health > /dev/null; then
              echo "CONNECTED"
              echo "1" > /tmp/connectivity
            else
              echo "DISCONNECTED"
              echo "0" > /tmp/connectivity
            fi
            sleep 30
          done
        volumeMounts:
        - name: metrics
          mountPath: /tmp
      - name: exporter
        image: prom/node-exporter:latest
        args:
        - --collector.textfile.directory=/tmp
        volumeMounts:
        - name: metrics
          mountPath: /tmp
      volumes:
      - name: metrics
        emptyDir: {}
```

## Troubleshooting

### K3s Issues

```bash
# Check K3s logs
sudo journalctl -u k3s -f

# Check agent logs
sudo journalctl -u k3s-agent -f

# Check containerd
sudo k3s crictl ps
sudo k3s crictl logs <container-id>

# Reset K3s
sudo /usr/local/bin/k3s-killall.sh
sudo rm -rf /var/lib/rancher/k3s
```

### MicroK8s Issues

```bash
# Check MicroK8s status
microk8s inspect

# View logs
microk8s kubectl logs -n kube-system <pod-name>

# Reset MicroK8s
microk8s reset
```

### KubeEdge Issues

```bash
# Check CloudCore
kubectl logs -n kubeedge deployment/cloudcore

# Check EdgeCore
sudo journalctl -u edgecore -f

# Check edge node connection
kubectl get nodes
kubectl describe node edge-node-1

# Restart EdgeCore
sudo systemctl restart edgecore
```
