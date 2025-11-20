# Kubernetes Cost Optimization Guide

## Overview

This guide provides comprehensive strategies for optimizing Kubernetes costs through right-sizing, resource allocation, workload optimization, and automated cost reduction techniques.

## Right-Sizing Strategies

### 1. CPU Right-Sizing

**Problem Identification:**

```bash
# Find over-provisioned CPU
kubectl top pods --all-namespaces --containers | \
  awk 'NR>1 {
    cpu=$3;
    gsub(/m/, "", cpu);
    if (cpu+0 < 100) print $0
  }' | sort -k3 -n

# Get CPU requests vs usage
kubectl get pods --all-namespaces -o json | jq -r '
  .items[] |
  select(.status.phase == "Running") |
  {
    namespace: .metadata.namespace,
    pod: .metadata.name,
    container: .spec.containers[].name,
    cpu_request: .spec.containers[].resources.requests.cpu,
    cpu_limit: .spec.containers[].resources.limits.cpu
  }
'
```

**Analysis Methodology:**

```python
import pandas as pd
import numpy as np
from prometheus_api_client import PrometheusConnect

def analyze_cpu_utilization(namespace, deployment, days=14):
    """
    Analyze CPU utilization and generate right-sizing recommendations.

    Args:
        namespace: Kubernetes namespace
        deployment: Deployment name
        days: Historical data window

    Returns:
        dict: Right-sizing recommendations
    """
    prom = PrometheusConnect(url="http://prometheus:9090")

    # Query actual CPU usage (rate over 5m, averaged over period)
    usage_query = f'''
        avg_over_time(
            sum by (container) (
                rate(
                    container_cpu_usage_seconds_total{{
                        namespace="{namespace}",
                        pod=~"{deployment}-.*"
                    }}[5m]
                )
            )[{days}d:5m]
        )
    '''
    usage_data = prom.custom_query(usage_query)

    # Query CPU requests
    request_query = f'''
        avg(
            kube_pod_container_resource_requests{{
                namespace="{namespace}",
                pod=~"{deployment}-.*",
                resource="cpu"
            }}
        )
    '''
    request_data = prom.custom_query(request_query)

    # Calculate statistics
    p50_usage = np.percentile([float(d['value'][1]) for d in usage_data], 50)
    p95_usage = np.percentile([float(d['value'][1]) for d in usage_data], 95)
    p99_usage = np.percentile([float(d['value'][1]) for d in usage_data], 99)
    current_request = float(request_data[0]['value'][1])

    # Recommendation logic
    # Target: P95 usage + 20% headroom
    recommended_request = p95_usage * 1.2

    # Safety checks
    if recommended_request < 0.1:  # Minimum 100m
        recommended_request = 0.1
    if recommended_request > current_request * 1.5:  # Max 50% increase
        recommended_request = current_request * 1.5

    # Calculate savings
    cost_per_core_hour = 0.031
    hours_per_month = 730
    current_cost = current_request * hours_per_month * cost_per_core_hour
    recommended_cost = recommended_request * hours_per_month * cost_per_core_hour
    monthly_savings = current_cost - recommended_cost

    return {
        'current_request': current_request,
        'recommended_request': round(recommended_request, 3),
        'utilization': {
            'p50': round(p50_usage, 3),
            'p95': round(p95_usage, 3),
            'p99': round(p99_usage, 3)
        },
        'efficiency': round((p95_usage / current_request) * 100, 1),
        'savings': {
            'monthly_usd': round(monthly_savings, 2),
            'annual_usd': round(monthly_savings * 12, 2),
            'percentage': round(((current_cost - recommended_cost) / current_cost) * 100, 1)
        },
        'recommendation': 'downsize' if recommended_request < current_request else 'upsize'
    }
```

**Right-Sizing Best Practices:**

| Workload Type | Target Utilization | Headroom | P-Value |
|--------------|-------------------|----------|---------|
| Production (critical) | 60-70% | 30-40% | P95 |
| Production (standard) | 70-80% | 20-30% | P95 |
| Development | 80-90% | 10-20% | P99 |
| Batch/Jobs | 90-95% | 5-10% | P99 |

**Implementation:**

```yaml
# Before: Over-provisioned
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  template:
    spec:
      containers:
      - name: api
        resources:
          requests:
            cpu: "2000m"    # Over-provisioned
            memory: "4Gi"
          limits:
            cpu: "4000m"
            memory: "8Gi"

---
# After: Right-sized (based on P95 + 20%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  template:
    spec:
      containers:
      - name: api
        resources:
          requests:
            cpu: "800m"     # P95: 650m, Recommended: 780m
            memory: "1500Mi" # P95: 1200Mi, Recommended: 1440Mi
          limits:
            cpu: "1600m"    # 2x requests (allows bursting)
            memory: "3Gi"   # 2x requests
```

### 2. Memory Right-Sizing

**Memory Leak Detection:**

```promql
# Detect memory growth trend
deriv(
  container_memory_working_set_bytes{
    namespace="production"
  }[6h]
) > 0
and
rate(
  container_memory_working_set_bytes{
    namespace="production"
  }[1h]
) > 1e6  # Growing more than 1MB/sec
```

**Memory Optimization Checklist:**

```yaml
optimization_checklist:
  - name: application_tuning
    actions:
      - check_jvm_heap_size  # Java applications
      - optimize_buffer_sizes
      - implement_pagination  # Database queries
      - use_streaming_apis
      - enable_compression

  - name: kubernetes_settings
    actions:
      - set_appropriate_requests
      - set_limits_to_prevent_oom
      - use_quality_of_service_classes
      - enable_memory_limits

  - name: monitoring
    actions:
      - track_memory_usage_trends
      - set_oom_alerts
      - monitor_swap_usage
      - track_page_faults
```

**Memory Right-Sizing Example:**

```yaml
# Node.js application with proper memory configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: nodejs-app:1.0
        env:
        # Set Node.js heap size to 80% of memory limit
        - name: NODE_OPTIONS
          value: "--max-old-space-size=1536"  # 1.5GB * 0.8 = 1.2GB
        resources:
          requests:
            memory: "1536Mi"  # Based on P95 usage analysis
          limits:
            memory: "2Gi"     # OOM kill threshold
```

### 3. Vertical Pod Autoscaler (VPA)

**VPA Configuration:**

```yaml
# VPA in recommendation mode (safe)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-server-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  updatePolicy:
    updateMode: "Off"  # Recommendation only, no auto-updates

  resourcePolicy:
    containerPolicies:
    - containerName: api
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
      controlledResources:
        - cpu
        - memory
      # Use aggressive scaling for dev, conservative for prod
      mode: Auto
```

**VPA Recommendation Analysis:**

```bash
# Get VPA recommendations
kubectl get vpa api-server-vpa -o jsonpath='{.status.recommendation}' | jq

# Example output:
{
  "containerRecommendations": [
    {
      "containerName": "api",
      "lowerBound": {
        "cpu": "500m",
        "memory": "1Gi"
      },
      "target": {
        "cpu": "750m",
        "memory": "1.5Gi"
      },
      "uncappedTarget": {
        "cpu": "850m",
        "memory": "1.7Gi"
      },
      "upperBound": {
        "cpu": "1200m",
        "memory": "2.5Gi"
      }
    }
  ]
}

# Apply VPA recommendations
kubectl set resources deployment api-server \
  --containers=api \
  --requests=cpu=750m,memory=1536Mi \
  --limits=cpu=1500m,memory=3Gi
```

## Horizontal Pod Autoscaling (HPA)

### 1. CPU-Based HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Target 70% CPU utilization
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50  # Scale up by 50% of current replicas
        periodSeconds: 60
      - type: Pods
        value: 2   # Or add 2 pods
        periodSeconds: 60
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scale down
      policies:
      - type: Percent
        value: 25  # Scale down by 25%
        periodSeconds: 60
```

### 2. Custom Metrics HPA

```yaml
# Scale based on queue depth
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: queue-worker
  minReplicas: 1
  maxReplicas: 50
  metrics:
  - type: External
    external:
      metric:
        name: sqs_queue_depth
        selector:
          matchLabels:
            queue: production-jobs
      target:
        type: AverageValue
        averageValue: "30"  # Target 30 messages per pod

  # Multiple metrics (logical OR)
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

### 3. HPA with KEDA (Event-Driven Autoscaling)

```yaml
# KEDA ScaledObject for event-driven autoscaling
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: rabbitmq-consumer-scaler
spec:
  scaleTargetRef:
    name: message-consumer
  minReplicaCount: 0   # Scale to zero when idle
  maxReplicaCount: 30
  pollingInterval: 15   # Check every 15 seconds
  cooldownPeriod: 300   # Wait 5 min before scaling to zero
  triggers:
  - type: rabbitmq
    metadata:
      host: amqp://rabbitmq:5672
      queueName: tasks
      queueLength: "20"  # Target 20 messages per pod
      protocol: auto

  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_per_second
      threshold: '100'
      query: |
        sum(rate(http_requests_total[2m]))
```

## Storage Optimization

### 1. Storage Class Selection

**Cost Comparison:**

| Storage Class | IOPS | Throughput | Cost (GB/month) | Use Case |
|--------------|------|------------|-----------------|----------|
| Standard HDD | 500 | 60 MB/s | $0.05 | Logs, backups |
| Standard SSD | 3000 | 125 MB/s | $0.17 | General purpose |
| Premium SSD | 5000+ | 200+ MB/s | $0.35 | Databases, high I/O |
| Ultra SSD | 20000+ | 1000+ MB/s | $0.70+ | Mission-critical |

**Right Storage Selection:**

```yaml
# Development: Standard HDD (cost-optimized)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dev-data
  namespace: development
spec:
  storageClassName: standard-hdd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi

---
# Production Database: Premium SSD (performance)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
  namespace: production
spec:
  storageClassName: premium-ssd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi

---
# Logs/Backups: Standard HDD with lifecycle
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: logs-archive
  namespace: logging
  annotations:
    # Transition to cheaper storage after 30 days
    backup.velero.io/storage-class: glacier
spec:
  storageClassName: standard-hdd
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Ti
```

### 2. Volume Sizing and Growth

**Dynamic Provisioning with Size Limits:**

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: dynamic-resize
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
allowVolumeExpansion: true  # Enable volume expansion

---
# PVC with initial conservative size
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
  annotations:
    # Alert when usage > 80%
    volume.kubernetes.io/storage-alert-threshold: "80"
spec:
  storageClassName: dynamic-resize
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi  # Start small, expand as needed
```

**Automated Volume Expansion:**

```python
def check_and_expand_volumes():
    """
    Monitor PVC usage and automatically expand when threshold reached.
    """
    for pvc in get_all_pvcs():
        usage_percent = get_pvc_usage_percentage(pvc)

        if usage_percent > 80:
            current_size = pvc.spec.resources.requests.storage
            new_size = increase_by_percent(current_size, 25)

            # Apply expansion
            pvc.spec.resources.requests.storage = new_size
            patch_pvc(pvc)

            send_notification(
                f"PVC {pvc.name} expanded from {current_size} to {new_size}"
            )
```

### 3. Snapshot and Backup Optimization

```yaml
# VolumeSnapshot with retention policy
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: db-backup-daily
  annotations:
    # Retention: 7 days
    backup.kubernetes.io/retention-days: "7"
    # Move to cheaper storage after 24 hours
    backup.kubernetes.io/storage-tier: "cold"
spec:
  volumeSnapshotClassName: csi-snapclass
  source:
    persistentVolumeClaimName: postgres-data

---
# Snapshot schedule with cost optimization
apiVersion: batch/v1
kind: CronJob
metadata:
  name: snapshot-manager
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: snapshot-manager
            image: bitnami/kubectl:latest
            command:
            - /bin/bash
            - -c
            - |
              # Create new snapshot
              kubectl create -f daily-snapshot.yaml

              # Delete snapshots older than 7 days
              kubectl get volumesnapshots \
                -o json | jq -r '
                  .items[] |
                  select(
                    (.metadata.creationTimestamp | fromdateiso8601) <
                    (now - (7 * 86400))
                  ) | .metadata.name
                ' | xargs kubectl delete volumesnapshot

              # Move 3+ day old snapshots to cold storage
              kubectl get volumesnapshots \
                -o json | jq -r '
                  .items[] |
                  select(
                    (.metadata.creationTimestamp | fromdateiso8601) <
                    (now - (3 * 86400))
                  ) | .metadata.name
                ' | xargs -I {} kubectl annotate volumesnapshot {} \
                  backup.kubernetes.io/storage-tier=cold --overwrite
          restartPolicy: OnFailure
```

## Spot Instance Strategies

### 1. Spot Instance Node Pools

**AWS EKS Spot Configuration:**

```yaml
# eksctl cluster config with spot instances
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: production
  region: us-east-1

nodeGroups:
  # On-demand for critical workloads
  - name: on-demand-critical
    instanceType: m5.xlarge
    minSize: 3
    maxSize: 10
    desiredCapacity: 5
    labels:
      workload-type: critical
      node-lifecycle: on-demand
    taints:
      - key: workload-type
        value: critical
        effect: NoSchedule

  # Spot for fault-tolerant workloads
  - name: spot-general
    instancesDistribution:
      instanceTypes:
        - m5.xlarge
        - m5a.xlarge
        - m5n.xlarge
        - m5ad.xlarge
      onDemandBaseCapacity: 0
      onDemandPercentageAboveBaseCapacity: 0
      spotInstancePools: 4
      spotAllocationStrategy: capacity-optimized
    minSize: 0
    maxSize: 50
    desiredCapacity: 10
    labels:
      workload-type: fault-tolerant
      node-lifecycle: spot
    taints:
      - key: node-lifecycle
        value: spot
        effect: NoSchedule
```

**GKE Spot Configuration:**

```bash
# Create spot node pool
gcloud container node-pools create spot-pool \
  --cluster=production \
  --spot \
  --machine-type=n2-standard-4 \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=20 \
  --node-labels=workload-type=fault-tolerant,node-lifecycle=spot \
  --node-taints=node-lifecycle=spot:NoSchedule
```

### 2. Workload Spot Compatibility

**Spot-Tolerant Workloads:**

```yaml
# Batch processing job (spot-compatible)
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processing
spec:
  completions: 100
  parallelism: 10
  backoffLimit: 5  # Retry on spot interruption
  template:
    spec:
      restartPolicy: OnFailure
      tolerations:
      - key: node-lifecycle
        operator: Equal
        value: spot
        effect: NoSchedule
      nodeSelector:
        node-lifecycle: spot
      containers:
      - name: processor
        image: data-processor:1.0
        # Implement graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "kill -TERM 1; sleep 30"]
      terminationGracePeriodSeconds: 120
```

**Spot Interruption Handling:**

```yaml
# DaemonSet to handle spot termination notices
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: spot-interrupt-handler
spec:
  selector:
    matchLabels:
      app: spot-interrupt-handler
  template:
    metadata:
      labels:
        app: spot-interrupt-handler
    spec:
      nodeSelector:
        node-lifecycle: spot
      hostNetwork: true
      containers:
      - name: handler
        image: kubeaws/kube-spot-termination-notice-handler:1.15.0
        env:
        - name: POLL_INTERVAL
          value: "5"
        - name: NOTICE_URL
          value: "http://169.254.169.254/latest/meta-data/spot/instance-action"
        - name: DETACH_ASG
          value: "true"
        - name: DRAIN_TIMEOUT
          value: "120"
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
      volumes:
      - name: kubeconfig
        hostPath:
          path: /root/.kube
```

### 3. Spot/On-Demand Mix Strategy

**Cost-Optimized Deployment:**

```yaml
# Deployment with mixed spot/on-demand
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 10
  template:
    metadata:
      labels:
        app: web-app
    spec:
      # Prefer spot, fallback to on-demand
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: node-lifecycle
                operator: In
                values:
                - spot
          - weight: 50
            preference:
              matchExpressions:
              - key: node-lifecycle
                operator: In
                values:
                - on-demand
      tolerations:
      - key: node-lifecycle
        operator: Equal
        value: spot
        effect: NoSchedule
      # Pod topology spread for HA
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: node-lifecycle
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchLabels:
            app: web-app
      containers:
      - name: web
        image: web-app:1.0
```

## Reserved Capacity Optimization

### 1. Commitment Analysis

**Reserved Instance Planning:**

```python
def analyze_reserved_capacity(cluster_metrics, forecast_months=12):
    """
    Analyze usage patterns to recommend reserved capacity purchase.

    Returns optimal reserved capacity commitment.
    """
    # Get baseline usage (minimum usage over past 6 months)
    baseline_usage = calculate_baseline_usage(
        cluster_metrics,
        percentile=10,  # Use P10 as baseline
        lookback_months=6
    )

    # Calculate steady-state capacity
    steady_state = {
        'cpu_cores': baseline_usage['cpu'] * 0.9,  # 90% of baseline
        'memory_gb': baseline_usage['memory'] * 0.9,
        'storage_gb': baseline_usage['storage'] * 0.9
    }

    # Cost analysis
    on_demand_cost = calculate_on_demand_cost(steady_state, forecast_months)

    reserved_options = [
        {
            'term': '1-year',
            'upfront': 'no',
            'cost': on_demand_cost * 0.65,
            'savings': 0.35
        },
        {
            'term': '1-year',
            'upfront': 'partial',
            'cost': on_demand_cost * 0.60,
            'savings': 0.40
        },
        {
            'term': '3-year',
            'upfront': 'partial',
            'cost': on_demand_cost * 0.48,
            'savings': 0.52
        }
    ]

    # Risk analysis
    growth_forecast = forecast_growth(cluster_metrics)
    risk = 'low' if growth_forecast < 0.2 else 'medium' if growth_forecast < 0.5 else 'high'

    return {
        'steady_state_capacity': steady_state,
        'on_demand_annual_cost': on_demand_cost,
        'reserved_options': reserved_options,
        'recommended': reserved_options[1] if risk == 'low' else reserved_options[0],
        'risk_level': risk
    }
```

### 2. Reserved Capacity Mix

**Optimal Mix Strategy:**

```yaml
# Capacity planning
capacity_strategy:
  # Baseline: Reserved (40-60% savings)
  reserved:
    percentage: 40%
    term: 1-year
    upfront: partial
    workloads:
      - control-plane-nodes
      - database-nodes
      - core-services

  # Variable: On-demand (flexibility)
  on_demand:
    percentage: 30%
    workloads:
      - production-web-apps
      - api-services
      - scaling-buffer

  # Burst: Spot (70-90% savings)
  spot:
    percentage: 30%
    workloads:
      - batch-jobs
      - ml-training
      - ci-cd
      - development
```

## Network Cost Optimization

### 1. Data Transfer Costs

**Minimize Cross-AZ Traffic:**

```yaml
# Topology-aware routing
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    service.kubernetes.io/topology-aware-hints: auto
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: api
  # Prefer same-AZ routing
  internalTrafficPolicy: Local
```

**Pod Topology Spread:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 9
  template:
    spec:
      # Spread evenly across AZs
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: api
      containers:
      - name: api
        image: api:1.0
```

### 2. Egress Cost Reduction

**Use VPC Endpoints:**

```yaml
# AWS VPC endpoints for S3, ECR (no internet egress charges)
vpc_endpoints:
  - service: com.amazonaws.us-east-1.s3
    type: Gateway
    route_tables: [rtb-xxx, rtb-yyy]

  - service: com.amazonaws.us-east-1.ecr.api
    type: Interface
    subnets: [subnet-xxx, subnet-yyy]

  - service: com.amazonaws.us-east-1.ecr.dkr
    type: Interface
    subnets: [subnet-xxx, subnet-yyy]
```

**CDN for Static Content:**

```yaml
# Use CloudFront/CDN to reduce direct egress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: website
  annotations:
    # CloudFront distribution
    external-dns.alpha.kubernetes.io/hostname: www.example.com
    alb.ingress.kubernetes.io/scheme: internet-facing
    # Cache static assets at edge
    alb.ingress.kubernetes.io/cache-control: "public, max-age=31536000"
spec:
  rules:
  - host: www.example.com
    http:
      paths:
      - path: /static/*
        pathType: Prefix
        backend:
          service:
            name: static-content
            port:
              number: 80
```

### 3. Load Balancer Optimization

**Consolidate Load Balancers:**

```yaml
# Single ALB with multiple ingress rules (vs. one ALB per service)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: consolidated-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    # Share single ALB across multiple services
    alb.ingress.kubernetes.io/group.name: shared-alb
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
  - host: web.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

## Idle Resource Cleanup

### 1. Automated Cleanup Policies

**Development Environment Cleanup:**

```yaml
# CronJob to stop dev/test environments after hours
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dev-environment-cleanup
spec:
  schedule: "0 20 * * 1-5"  # 8 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cleanup-sa
          containers:
          - name: cleanup
            image: bitnami/kubectl:latest
            command:
            - /bin/bash
            - -c
            - |
              # Scale down development deployments
              kubectl scale deployment --all \
                --namespace=development \
                --replicas=0

              # Delete idle pods (no activity for 8 hours)
              kubectl get pods --all-namespaces \
                -o json | jq -r '
                  .items[] |
                  select(
                    .metadata.namespace == "development" and
                    (.status.startTime | fromdateiso8601) <
                    (now - 28800)
                  ) | .metadata.name
                ' | xargs kubectl delete pod

              # Suspend CronJobs in dev
              kubectl get cronjobs -n development \
                -o name | xargs kubectl patch -p '{"spec":{"suspend":true}}'

              echo "Dev environments stopped. Will restart at 6 AM."
          restartPolicy: OnFailure

---
# Morning restart
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dev-environment-restart
spec:
  schedule: "0 6 * * 1-5"  # 6 AM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cleanup-sa
          containers:
          - name: restart
            image: bitnami/kubectl:latest
            command:
            - /bin/bash
            - -c
            - |
              # Scale up to original replicas
              kubectl scale deployment --all \
                --namespace=development \
                --replicas=1

              # Resume CronJobs
              kubectl get cronjobs -n development \
                -o name | xargs kubectl patch -p '{"spec":{"suspend":false}}'
          restartPolicy: OnFailure
```

### 2. Orphaned Resource Detection

```python
#!/usr/bin/env python3
"""
Detect and clean up orphaned Kubernetes resources.
"""

def find_orphaned_pvcs():
    """Find PVCs not attached to any pod."""
    pvcs = kubectl("get pvc --all-namespaces -o json")
    pods = kubectl("get pods --all-namespaces -o json")

    attached_pvcs = set()
    for pod in pods['items']:
        for volume in pod.get('spec', {}).get('volumes', []):
            if 'persistentVolumeClaim' in volume:
                pvc_name = volume['persistentVolumeClaim']['claimName']
                namespace = pod['metadata']['namespace']
                attached_pvcs.add(f"{namespace}/{pvc_name}")

    orphaned = []
    for pvc in pvcs['items']:
        namespace = pvc['metadata']['namespace']
        name = pvc['metadata']['name']
        full_name = f"{namespace}/{name}"

        if full_name not in attached_pvcs:
            # Check age (only flag if older than 7 days)
            creation_time = parse_timestamp(pvc['metadata']['creationTimestamp'])
            age_days = (datetime.now() - creation_time).days

            if age_days > 7:
                size_gi = parse_storage_size(pvc['spec']['resources']['requests']['storage'])
                cost_per_month = calculate_storage_cost(size_gi, pvc['spec']['storageClassName'])

                orphaned.append({
                    'namespace': namespace,
                    'name': name,
                    'age_days': age_days,
                    'size_gi': size_gi,
                    'monthly_cost_usd': cost_per_month
                })

    return orphaned

def find_unused_configmaps_secrets():
    """Find ConfigMaps and Secrets not referenced by any pod."""
    # Similar logic to orphaned PVCs
    pass

def find_stale_images():
    """Find container images not used by any deployment."""
    pass

if __name__ == "__main__":
    orphaned_pvcs = find_orphaned_pvcs()
    total_savings = sum(pvc['monthly_cost_usd'] for pvc in orphaned_pvcs)

    print(f"Found {len(orphaned_pvcs)} orphaned PVCs")
    print(f"Potential monthly savings: ${total_savings:.2f}")

    for pvc in orphaned_pvcs:
        print(f"  - {pvc['namespace']}/{pvc['name']}: "
              f"{pvc['size_gi']}Gi, ${pvc['monthly_cost_usd']:.2f}/month")
```

## Continuous Optimization

### 1. Daily Optimization Workflow

```bash
#!/bin/bash
# daily-cost-optimization.sh

set -euo pipefail

NAMESPACE="${1:-production}"
THRESHOLD_SAVINGS=50  # Minimum $50/month savings to recommend

echo "=== Daily Cost Optimization Report ==="
echo "Date: $(date)"
echo "Namespace: $NAMESPACE"
echo ""

# 1. Right-sizing recommendations
echo "1. Right-sizing Analysis"
kubectl opencost recommendations \
  --namespace="$NAMESPACE" \
  --type=rightsizing \
  --min-savings="$THRESHOLD_SAVINGS" \
  --format=table

# 2. Idle resource detection
echo "2. Idle Resources"
kubectl get pods -n "$NAMESPACE" -o json | jq -r '
  .items[] |
  select(
    .status.phase == "Running" and
    (.metadata.creationTimestamp | fromdateiso8601) < (now - 604800)
  ) |
  [.metadata.name, .spec.containers[0].resources.requests] |
  @tsv
' | while read pod resources; do
  # Check if pod has low CPU usage
  cpu_usage=$(kubectl top pod "$pod" -n "$NAMESPACE" --no-headers | awk '{print $2}')
  if [[ "${cpu_usage%m}" -lt 10 ]]; then
    echo "  - Low usage pod: $pod (CPU: $cpu_usage)"
  fi
done

# 3. Storage optimization
echo "3. Storage Optimization"
kubectl get pvc -n "$NAMESPACE" -o json | jq -r '
  .items[] |
  {
    name: .metadata.name,
    size: .spec.resources.requests.storage,
    storageClass: .spec.storageClassName
  } |
  [.name, .size, .storageClass] |
  @tsv
' | while read name size class; do
  if [[ "$class" == "premium-ssd" ]]; then
    echo "  - Consider downgrading $name from premium-ssd to standard-ssd"
  fi
done

# 4. Spot migration candidates
echo "4. Spot Migration Candidates"
kubectl get deployments -n "$NAMESPACE" -o json | jq -r '
  .items[] |
  select(
    .spec.template.spec.nodeSelector["node-lifecycle"] != "spot" and
    .metadata.labels.criticality != "high"
  ) |
  .metadata.name
' | while read deployment; do
  echo "  - $deployment can potentially use spot instances"
done

# 5. Generate report
kubectl opencost report \
  --namespace="$NAMESPACE" \
  --window=7d \
  --format=json > /tmp/cost-report.json

# Send to Slack/Email
curl -X POST "$SLACK_WEBHOOK" \
  --data-binary @/tmp/cost-report.json

echo ""
echo "Optimization report complete."
```

### 2. Weekly Optimization Review

```yaml
# Kubernetes CronJob for weekly review
apiVersion: batch/v1
kind: CronJob
metadata:
  name: weekly-cost-review
spec:
  schedule: "0 9 * * 1"  # Monday 9 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cost-analyzer
            image: cost-analyzer:1.0
            env:
            - name: PROMETHEUS_URL
              value: "http://prometheus:9090"
            - name: OPENCOST_URL
              value: "http://opencost:9003"
            command:
            - /bin/bash
            - -c
            - |
              # Generate comprehensive weekly report
              python3 /scripts/weekly-review.py \
                --output=/reports/weekly-$(date +%Y%m%d).pdf \
                --email=finops-team@company.com \
                --include-recommendations \
                --include-trends
          restartPolicy: OnFailure
```

## Cost Optimization KPIs

### Key Metrics to Track

```yaml
cost_optimization_kpis:
  efficiency:
    - metric: cluster_utilization
      target: ">65%"
      current: calculate_utilization()

    - metric: resource_waste
      target: "<15%"
      current: calculate_waste_percentage()

  savings:
    - metric: monthly_savings_from_rightsizing
      target: ">$5000"
      current: sum_implemented_recommendations()

    - metric: spot_instance_coverage
      target: ">40%"
      current: calculate_spot_coverage()

  automation:
    - metric: auto_optimization_rate
      target: ">70%"
      description: "% of recommendations auto-applied"

    - metric: time_to_implement_recommendation
      target: "<7 days"
      description: "Average time from recommendation to implementation"
```

---

**Related References:**
- finops-patterns.md — Cost allocation and chargeback models
- cloud-cost-management.md — Cloud provider-specific optimizations
