# StatefulSet Design Patterns

Comprehensive guide to StatefulSet patterns for deploying stateful applications on Kubernetes including databases, distributed systems, and data processing frameworks.

## StatefulSet Fundamentals

### Key Characteristics

**StatefulSet Guarantees:**
1. **Stable, unique network identifiers** - Predictable pod names (app-0, app-1, app-2)
2. **Stable, persistent storage** - PVC per pod that survives pod rescheduling
3. **Ordered, graceful deployment and scaling** - Pods created/deleted in order
4. **Ordered, automated rolling updates** - Updates proceed in reverse ordinal order

**Comparison with Deployment:**

| Feature | StatefulSet | Deployment |
|---------|------------|------------|
| Pod naming | Predictable (app-0) | Random (app-7f9d8c-xyz) |
| Network identity | Stable DNS | Ephemeral |
| Storage | Persistent per pod | Shared or ephemeral |
| Scaling order | Sequential | Parallel |
| Update order | Reverse ordinal | Random |
| Use case | Databases, distributed systems | Stateless apps |

## Database Patterns

### Pattern 1: Single-Instance Database

**Use case:** PostgreSQL, MySQL single instance for development/testing

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  ports:
  - port: 5432
    name: postgres
  clusterIP: None  # Headless service
  selector:
    app: postgres

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres

  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
          name: postgres

        env:
        - name: POSTGRES_DB
          value: myapp
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata

        # Resource requests and limits
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        # Volume mounts
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data

        # Liveness probe
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - pg_isready -U $POSTGRES_USER -d $POSTGRES_DB
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3

      # Security context
      securityContext:
        fsGroup: 999
        runAsUser: 999
        runAsNonRoot: true

  # Volume claim templates
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi
```

### Pattern 2: Primary-Replica Database

**Use case:** PostgreSQL with streaming replication

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
data:
  primary.conf: |
    wal_level = replica
    max_wal_senders = 3
    max_replication_slots = 3
    hot_standby = on
    wal_log_hints = on

  replica.conf: |
    hot_standby = on
    hot_standby_feedback = on
    wal_level = replica

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  ports:
  - port: 5432
    name: postgres
  clusterIP: None
  selector:
    app: postgres

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-primary
  labels:
    app: postgres
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
    role: primary

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-replica
  labels:
    app: postgres
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
    role: replica

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres

  template:
    metadata:
      labels:
        app: postgres
    spec:
      # Anti-affinity for high availability
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - postgres
            topologyKey: kubernetes.io/hostname

      initContainers:
      # Initialize replica from primary
      - name: init-replica
        image: postgres:16
        command:
        - /bin/bash
        - -c
        - |
          if [ "$POD_NAME" != "postgres-0" ]; then
            until pg_isready -h postgres-0.postgres -U postgres; do
              echo "Waiting for primary..."
              sleep 2
            done
            if [ ! -f /var/lib/postgresql/data/pgdata/PG_VERSION ]; then
              echo "Initializing replica from primary..."
              pg_basebackup -h postgres-0.postgres -D /var/lib/postgresql/data/pgdata \
                -U replication -v -P -W --wal-method=stream
            fi
          fi
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: replication-password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data

      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
          name: postgres

        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-credentials
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata

        # Lifecycle hooks
        lifecycle:
          postStart:
            exec:
              command:
              - /bin/bash
              - -c
              - |
                if [ "$POD_NAME" = "postgres-0" ]; then
                  # Primary configuration
                  cat /config/primary.conf >> $PGDATA/postgresql.conf
                  kubectl label pod $POD_NAME role=primary --overwrite
                else
                  # Replica configuration
                  cat /config/replica.conf >> $PGDATA/postgresql.conf
                  kubectl label pod $POD_NAME role=replica --overwrite
                fi

        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        - name: config
          mountPath: /config

        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 10
          periodSeconds: 5

      volumes:
      - name: config
        configMap:
          name: postgres-config

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 200Gi
```

### Pattern 3: MongoDB Replica Set

**Use case:** MongoDB with replica set for high availability

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  labels:
    app: mongodb
spec:
  ports:
  - port: 27017
    name: mongo
  clusterIP: None
  selector:
    app: mongodb

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb

  template:
    metadata:
      labels:
        app: mongodb
    spec:
      # Anti-affinity for high availability
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - mongodb
            topologyKey: kubernetes.io/hostname

      # Termination grace period for clean shutdown
      terminationGracePeriodSeconds: 30

      containers:
      - name: mongodb
        image: mongo:7.0
        command:
        - mongod
        - --replSet
        - rs0
        - --bind_ip_all
        - --wiredTigerCacheSizeGB
        - "1"

        ports:
        - containerPort: 27017
          name: mongo

        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongodb-credentials
              key: username
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-credentials
              key: password

        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        volumeMounts:
        - name: data
          mountPath: /data/db

        livenessProbe:
          exec:
            command:
            - mongosh
            - --eval
            - "db.adminCommand('ping')"
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5

        readinessProbe:
          exec:
            command:
            - mongosh
            - --eval
            - "db.adminCommand('ping')"
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3

      # Sidecar for replica set initialization
      - name: mongo-sidecar
        image: cvallance/mongo-k8s-sidecar:latest
        env:
        - name: MONGO_SIDECAR_POD_LABELS
          value: "app=mongodb"
        - name: KUBERNETES_MONGO_SERVICE_NAME
          value: mongodb
        - name: MONGODB_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongodb-credentials
              key: username
        - name: MONGODB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-credentials
              key: password
        - name: MONGODB_DATABASE
          value: admin

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi
```

## Distributed System Patterns

### Pattern 4: Kafka Cluster

**Use case:** Apache Kafka with Zookeeper ensemble

```yaml
---
# Zookeeper for Kafka coordination
apiVersion: v1
kind: Service
metadata:
  name: zookeeper
  labels:
    app: zookeeper
spec:
  ports:
  - port: 2181
    name: client
  - port: 2888
    name: server
  - port: 3888
    name: leader-election
  clusterIP: None
  selector:
    app: zookeeper

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zookeeper
spec:
  serviceName: zookeeper
  replicas: 3
  selector:
    matchLabels:
      app: zookeeper

  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - zookeeper
            topologyKey: kubernetes.io/hostname

      containers:
      - name: zookeeper
        image: confluentinc/cp-zookeeper:7.5.0
        ports:
        - containerPort: 2181
          name: client
        - containerPort: 2888
          name: server
        - containerPort: 3888
          name: leader-election

        env:
        - name: ZOOKEEPER_SERVER_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: ZOOKEEPER_CLIENT_PORT
          value: "2181"
        - name: ZOOKEEPER_TICK_TIME
          value: "2000"
        - name: ZOOKEEPER_INIT_LIMIT
          value: "5"
        - name: ZOOKEEPER_SYNC_LIMIT
          value: "2"
        - name: ZOOKEEPER_SERVERS
          value: "zookeeper-0.zookeeper:2888:3888;zookeeper-1.zookeeper:2888:3888;zookeeper-2.zookeeper:2888:3888"

        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi

        volumeMounts:
        - name: data
          mountPath: /var/lib/zookeeper/data
        - name: logs
          mountPath: /var/lib/zookeeper/log

        livenessProbe:
          exec:
            command:
            - /bin/bash
            - -c
            - echo ruok | nc localhost 2181 | grep imok
          initialDelaySeconds: 30
          periodSeconds: 10

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: logs
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 10Gi

---
# Kafka brokers
apiVersion: v1
kind: Service
metadata:
  name: kafka
  labels:
    app: kafka
spec:
  ports:
  - port: 9092
    name: client
  clusterIP: None
  selector:
    app: kafka

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
spec:
  serviceName: kafka
  replicas: 3
  selector:
    matchLabels:
      app: kafka

  template:
    metadata:
      labels:
        app: kafka
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - kafka
            topologyKey: kubernetes.io/hostname

      containers:
      - name: kafka
        image: confluentinc/cp-kafka:7.5.0
        ports:
        - containerPort: 9092
          name: client

        env:
        - name: KAFKA_BROKER_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: KAFKA_ZOOKEEPER_CONNECT
          value: "zookeeper-0.zookeeper:2181,zookeeper-1.zookeeper:2181,zookeeper-2.zookeeper:2181"
        - name: KAFKA_ADVERTISED_LISTENERS
          value: "PLAINTEXT://$(POD_NAME).kafka:9092"
        - name: KAFKA_LISTENER_SECURITY_PROTOCOL_MAP
          value: "PLAINTEXT:PLAINTEXT"
        - name: KAFKA_INTER_BROKER_LISTENER_NAME
          value: "PLAINTEXT"
        - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR
          value: "3"
        - name: KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR
          value: "3"
        - name: KAFKA_TRANSACTION_STATE_LOG_MIN_ISR
          value: "2"
        - name: KAFKA_LOG_RETENTION_HOURS
          value: "168"
        - name: KAFKA_LOG_SEGMENT_BYTES
          value: "1073741824"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name

        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        volumeMounts:
        - name: data
          mountPath: /var/lib/kafka/data

        livenessProbe:
          tcpSocket:
            port: 9092
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          tcpSocket:
            port: 9092
          initialDelaySeconds: 10
          periodSeconds: 5

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 200Gi
```

### Pattern 5: Elasticsearch Cluster

**Use case:** Elasticsearch with master, data, and coordinator nodes

```yaml
---
# Master nodes
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-master
  labels:
    app: elasticsearch
    role: master
spec:
  ports:
  - port: 9300
    name: transport
  clusterIP: None
  selector:
    app: elasticsearch
    role: master

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch-master
spec:
  serviceName: elasticsearch-master
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
      role: master

  template:
    metadata:
      labels:
        app: elasticsearch
        role: master
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - elasticsearch
              - key: role
                operator: In
                values:
                - master
            topologyKey: kubernetes.io/hostname

      initContainers:
      - name: increase-vm-max-map
        image: busybox
        command: ["sysctl", "-w", "vm.max_map_count=262144"]
        securityContext:
          privileged: true

      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        ports:
        - containerPort: 9300
          name: transport

        env:
        - name: cluster.name
          value: "elasticsearch-cluster"
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: node.roles
          value: "master"
        - name: discovery.seed_hosts
          value: "elasticsearch-master-0.elasticsearch-master,elasticsearch-master-1.elasticsearch-master,elasticsearch-master-2.elasticsearch-master"
        - name: cluster.initial_master_nodes
          value: "elasticsearch-master-0,elasticsearch-master-1,elasticsearch-master-2"
        - name: ES_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        - name: xpack.security.enabled
          value: "false"

        resources:
          requests:
            cpu: 500m
            memory: 2Gi
          limits:
            cpu: 1000m
            memory: 2Gi

        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 50Gi

---
# Data nodes
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-data
  labels:
    app: elasticsearch
    role: data
spec:
  ports:
  - port: 9300
    name: transport
  clusterIP: None
  selector:
    app: elasticsearch
    role: data

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch-data
spec:
  serviceName: elasticsearch-data
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
      role: data

  template:
    metadata:
      labels:
        app: elasticsearch
        role: data
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - elasticsearch
              - key: role
                operator: In
                values:
                - data
            topologyKey: kubernetes.io/hostname

      initContainers:
      - name: increase-vm-max-map
        image: busybox
        command: ["sysctl", "-w", "vm.max_map_count=262144"]
        securityContext:
          privileged: true

      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
        ports:
        - containerPort: 9300
          name: transport

        env:
        - name: cluster.name
          value: "elasticsearch-cluster"
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: node.roles
          value: "data,ingest"
        - name: discovery.seed_hosts
          value: "elasticsearch-master-0.elasticsearch-master,elasticsearch-master-1.elasticsearch-master,elasticsearch-master-2.elasticsearch-master"
        - name: ES_JAVA_OPTS
          value: "-Xms2g -Xmx2g"
        - name: xpack.security.enabled
          value: "false"

        resources:
          requests:
            cpu: 1000m
            memory: 4Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data

  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 500Gi
```

## Scaling Patterns

### Horizontal Scaling (Adding/Removing Pods)

```bash
# Scale up (creates pods in order: N, N+1, N+2...)
kubectl scale statefulset mongodb --replicas=5

# Scale down (deletes pods in reverse order: N, N-1, N-2...)
kubectl scale statefulset mongodb --replicas=3

# Wait for scaling to complete
kubectl rollout status statefulset mongodb
```

### Vertical Scaling (Resize PVC)

```bash
# 1. Ensure StorageClass allows volume expansion
kubectl get storageclass fast-ssd -o yaml | grep allowVolumeExpansion

# 2. Edit PVC to increase size
kubectl patch pvc data-mongodb-0 -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'

# 3. Verify expansion
kubectl get pvc data-mongodb-0

# 4. Restart pod if filesystem doesn't auto-expand
kubectl delete pod mongodb-0
```

### Pod Management Policies

**OrderedReady (default):**
```yaml
spec:
  podManagementPolicy: OrderedReady  # Pods created/deleted sequentially
```

**Parallel:**
```yaml
spec:
  podManagementPolicy: Parallel  # Pods created/deleted in parallel
```

## Update Strategies

### Rolling Update (Default)

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0  # Update all pods (pods >= partition)
```

**Update process:**
```bash
# Update image
kubectl set image statefulset/mongodb mongodb=mongo:7.0.1

# Monitor rollout
kubectl rollout status statefulset mongodb

# Check pod versions
kubectl get pods -l app=mongodb -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
```

### Canary Update (Partition Strategy)

```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 2  # Only update pods >= 2 (keep 0 and 1 on old version)
```

**Canary rollout:**
```bash
# Step 1: Update only pod-2 (latest pod)
kubectl patch statefulset mongodb -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":2}}}}'
kubectl set image statefulset/mongodb mongodb=mongo:7.0.1

# Step 2: Verify pod-2 health
kubectl logs mongodb-2
kubectl exec mongodb-2 -- mongosh --eval "db.adminCommand('ping')"

# Step 3: Roll out to pod-1
kubectl patch statefulset mongodb -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":1}}}}'

# Step 4: Roll out to all pods
kubectl patch statefulset mongodb -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":0}}}}'
```

### OnDelete Strategy

```yaml
spec:
  updateStrategy:
    type: OnDelete  # Manual pod deletion triggers update
```

**Manual update process:**
```bash
# Update StatefulSet spec
kubectl set image statefulset/mongodb mongodb=mongo:7.0.1

# Manually delete pods to trigger update
kubectl delete pod mongodb-2
kubectl wait --for=condition=Ready pod/mongodb-2

kubectl delete pod mongodb-1
kubectl wait --for=condition=Ready pod/mongodb-1

kubectl delete pod mongodb-0
kubectl wait --for=condition=Ready pod/mongodb-0
```

## Best Practices

### 1. Storage Configuration

**Always use volumeClaimTemplates:**
```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    accessModes: ["ReadWriteOnce"]
    storageClassName: fast-ssd  # Specify appropriate storage class
    resources:
      requests:
        storage: 100Gi
```

**Multiple volumes per pod:**
```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    storageClassName: fast-ssd
    resources:
      requests:
        storage: 500Gi
- metadata:
    name: logs
  spec:
    storageClassName: standard
    resources:
      requests:
        storage: 50Gi
```

### 2. High Availability

**Use pod anti-affinity:**
```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - myapp
      topologyKey: kubernetes.io/hostname  # Different nodes
```

**Spread across zones:**
```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - myapp
        topologyKey: topology.kubernetes.io/zone  # Different zones
```

### 3. Resource Management

**Set resource requests and limits:**
```yaml
resources:
  requests:
    cpu: 1000m
    memory: 2Gi
  limits:
    cpu: 2000m
    memory: 4Gi
```

**Use PriorityClass for critical workloads:**
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority for databases"

---
spec:
  priorityClassName: high-priority
```

### 4. Health Checks

**Liveness probe (restart unhealthy pods):**
```yaml
livenessProbe:
  exec:
    command:
    - /health-check
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

**Readiness probe (remove from service endpoints):**
```yaml
readinessProbe:
  exec:
    command:
    - /ready-check
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 2
```

### 5. Graceful Termination

**Set appropriate grace period:**
```yaml
terminationGracePeriodSeconds: 60  # Longer for databases

lifecycle:
  preStop:
    exec:
      command:
      - /bin/bash
      - -c
      - |
        # Drain connections, flush buffers, etc.
        my-graceful-shutdown-script
```

### 6. Security

**Use Pod Security Standards:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
      - ALL
    readOnlyRootFilesystem: true
```

**Use secrets for credentials:**
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-credentials
      key: password
```

## Troubleshooting

### Pod Stuck in Pending

```bash
# Check PVC status
kubectl get pvc

# Check events
kubectl describe pod <pod-name>

# Common issues:
# - No available PVs (static provisioning)
# - StorageClass not found
# - Insufficient node resources
# - Volume attachment failed
```

### Pod Stuck in Terminating

```bash
# Check pod status
kubectl get pod <pod-name> -o yaml

# Force delete (use with caution)
kubectl delete pod <pod-name> --grace-period=0 --force

# Check finalizers
kubectl patch pod <pod-name> -p '{"metadata":{"finalizers":null}}'
```

### Update Stuck

```bash
# Check rollout status
kubectl rollout status statefulset <name>

# Check pod status
kubectl get pods -l app=<app>

# Check for errors
kubectl describe statefulset <name>

# Rollback if needed
kubectl rollout undo statefulset <name>
```

### Data Loss After Scale Down

**Important:** StatefulSet does NOT delete PVCs when scaling down!

```bash
# List orphaned PVCs after scale down
kubectl get pvc | grep <statefulset-name>

# Re-attach by scaling up
kubectl scale statefulset <name> --replicas=<previous-count>

# Manually delete PVC (permanent data loss!)
kubectl delete pvc data-<statefulset-name>-<ordinal>
```
