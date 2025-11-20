---
name: cost-finops
description: Kubernetes cost optimization and FinOps practices. Use when optimizing cloud costs, implementing cost allocation, setting up chargeback models, analyzing spending patterns, or establishing FinOps governance for Kubernetes workloads.
---

# Kubernetes Cost & FinOps

## When to Use This Skill

- Setting up cost monitoring and visibility tools (OpenCost, KubeCost)
- Implementing cost allocation strategies across teams, namespaces, or business units
- Establishing showback or chargeback models for Kubernetes resources
- Optimizing resource utilization and right-sizing workloads
- Implementing spot instances, reserved capacity, or savings plans
- Detecting and resolving cost anomalies
- Establishing FinOps governance and best practices
- Generating cost savings recommendations
- Multi-cloud cost management (AWS EKS, Azure AKS, GCP GKE)

## Core Concepts

### 1. Cost Visibility Architecture

**Three Pillars of Kubernetes Cost Management:**

```
┌─────────────────────────────────────────────────────┐
│                 Cost Visibility Layer                │
├─────────────────────────────────────────────────────┤
│  OpenCost/KubeCost   Prometheus   Cloud Billing API │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              Cost Allocation & Tagging               │
├─────────────────────────────────────────────────────┤
│  Namespace  Labels  Annotations  Cost Centers       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│            Optimization & Governance                 │
├─────────────────────────────────────────────────────┤
│  Right-sizing  Spot Instances  Reserved Capacity    │
└─────────────────────────────────────────────────────┘
```

**Key Components:**
- **Cost Monitoring**: Real-time tracking of resource consumption
- **Cost Allocation**: Mapping costs to teams, projects, environments
- **Cost Optimization**: Reducing waste and improving efficiency
- **Cost Governance**: Policies, budgets, and accountability

### 2. OpenCost / KubeCost Setup

**Installation Methods:**

**Helm Installation (OpenCost):**
```bash
# Add OpenCost repository
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm repo update

# Install with Prometheus integration
helm install opencost opencost/opencost \
  --namespace opencost --create-namespace \
  --set prometheus.internal.enabled=false \
  --set prometheus.external.url=http://prometheus-server.monitoring:80
```

**KubeCost Installation:**
```bash
# Install KubeCost with cloud integration
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost --create-namespace \
  --set kubecostToken="YOUR_TOKEN" \
  --set prometheus.server.global.external_labels.cluster_id=production
```

**Configuration Requirements:**
- Prometheus metrics (node, pod, container metrics)
- Cloud provider billing APIs (AWS Cost Explorer, Azure Cost Management, GCP Billing)
- Network egress tracking
- Persistent storage costs
- Load balancer costs

See `assets/opencost-config.yaml` for complete configuration.

### 3. Cost Allocation Strategies

**Multi-Dimensional Allocation:**

```yaml
# Cost allocation hierarchy
allocation:
  dimensions:
    - namespace        # Primary dimension
    - team            # Business unit (via labels)
    - environment     # dev/staging/prod
    - application     # Application identifier
    - cost_center     # Chargeback code

  # Allocation rules
  rules:
    - name: shared-costs
      type: proportional
      targets: [monitoring, logging, ingress]

    - name: idle-costs
      type: weighted
      algorithm: cpu-memory-weighted
```

**Labeling Strategy:**
```yaml
# Standard cost labels
metadata:
  labels:
    cost-center: "engineering-platform"
    team: "backend-team"
    project: "payments-api"
    environment: "production"
    budget-owner: "john.doe@company.com"
    cost-allocation: "direct"
```

**Namespace-Based Allocation:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-backend
  labels:
    cost-center: "CC-1001"
    team: "backend"
    chargeback: "enabled"
  annotations:
    cost.kubernetes.io/allocation-method: "direct"
    cost.kubernetes.io/budget-monthly: "5000"
    cost.kubernetes.io/alert-threshold: "80"
```

### 4. Showback vs. Chargeback Models

**Showback Model (Informational):**
- **Purpose**: Visibility and awareness without financial transactions
- **Use Cases**: Teams understanding their consumption, cost trends
- **Implementation**: Monthly reports, dashboards, cost attribution

```yaml
# Showback configuration
showback:
  enabled: true
  reporting:
    frequency: weekly
    recipients:
      - team-leads@company.com
      - engineering-managers@company.com
    format:
      - email-summary
      - dashboard-link
    metrics:
      - total_cost
      - cost_per_namespace
      - cost_trends
      - efficiency_score
```

**Chargeback Model (Financial Accountability):**
- **Purpose**: Cost recovery through internal billing
- **Use Cases**: Mature FinOps organizations, cross-functional teams
- **Implementation**: Monthly invoices, budget enforcement, cost optimization incentives

```yaml
# Chargeback configuration
chargeback:
  enabled: true
  billing_period: monthly
  allocation_method: usage-based

  pricing:
    cpu:
      unit: core-hour
      rate: 0.031  # $/core-hour
    memory:
      unit: gb-hour
      rate: 0.004  # $/GB-hour
    storage:
      unit: gb-month
      rate: 0.10   # $/GB-month
    network:
      egress_rate: 0.09  # $/GB

  adjustments:
    - type: shared-costs
      allocation: proportional
      services: [ingress, dns, monitoring]
    - type: reserved-capacity-discount
      rate: 0.60  # 40% discount
```

See `references/finops-patterns.md` for detailed chargeback implementation.

### 5. Resource Optimization

**Right-Sizing Strategy:**

**Vertical Pod Autoscaler (VPA) Recommendations:**
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  updatePolicy:
    updateMode: "Off"  # Recommendation only
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 2Gi
      controlledResources: ["cpu", "memory"]
```

**Right-Sizing Analysis:**
```bash
# Analyze resource utilization
kubectl top pods --all-namespaces --containers | \
  awk '{if($3+0 < 50 || $5+0 < 50) print $0}' | \
  sort -k3 -n

# Get VPA recommendations
kubectl describe vpa --all-namespaces | \
  grep -A 10 "Recommendation:"

# Calculate potential savings
opencost-cli analyze --threshold=50 \
  --recommendation=downsize \
  --format=json
```

**Optimization Techniques:**
1. **Over-Provisioning Reduction**: Align requests with actual usage (P95)
2. **CPU Throttling Detection**: Identify CPU-bound workloads
3. **Memory Waste**: Find pods with high memory requests, low usage
4. **Idle Resources**: Detect consistently idle workloads

### 6. Spot Instances & Reserved Capacity

**Spot Instance Strategy:**

**Node Pool Configuration (GKE):**
```yaml
apiVersion: container.cnrm.cloud.google.com/v1beta1
kind: ContainerNodePool
metadata:
  name: spot-pool
spec:
  location: us-central1
  clusterRef:
    name: production
  nodeConfig:
    machineType: n2-standard-4
    spot: true  # Enable spot instances
    taints:
    - key: cloud.google.com/gke-spot
      value: "true"
      effect: NoSchedule
  autoscaling:
    minNodeCount: 0
    maxNodeCount: 20
```

**Workload Spot Tolerance:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  template:
    spec:
      tolerations:
      - key: "cloud.google.com/gke-spot"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      - key: "kubernetes.azure.com/scalesetpriority"
        operator: "Equal"
        value: "spot"
        effect: "NoSchedule"
      nodeSelector:
        workload-type: spot-eligible
      # Graceful handling of interruptions
      terminationGracePeriodSeconds: 120
```

**Spot/On-Demand Ratio:**
```yaml
# Cost optimization through hybrid approach
node_pools:
  on_demand:
    min_nodes: 3
    max_nodes: 10
    workloads: [critical, stateful, production]

  spot:
    min_nodes: 0
    max_nodes: 50
    workloads: [batch, ml-training, dev, test]
    savings: 70-90%

  reserved:
    committed_nodes: 5
    term: 1-year
    savings: 40-60%
    workloads: [baseline-load]
```

**Reserved Capacity (AWS EKS):**
```bash
# Purchase Reserved Instances for baseline
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id <offering-id> \
  --instance-count 10 \
  --instance-type m5.xlarge \
  --region us-east-1

# Savings Plans (more flexible)
aws savingsplans purchase-savingsplan \
  --savings-plan-type ComputeSavingsPlans \
  --commitment 100 \
  --upfront-payment-amount 0 \
  --term 1year
```

### 7. Cloud Provider Cost Management

**AWS EKS Cost Optimization:**

```yaml
# Tag-based cost allocation
aws:
  tags:
    - key: kubernetes.io/cluster/production
      propagate_to_volumes: true
    - key: CostCenter
      value: "engineering"
    - key: Environment
      value: "production"

# Cost allocation tags
cost_allocation_tags:
  - kubernetes.io/created-for/pvc/namespace
  - kubernetes.io/created-for/pvc/name
  - eks:cluster-name
  - eks:nodegroup-name
```

**EKS Cost Optimization Checklist:**
- ✅ Use EC2 Spot for fault-tolerant workloads (70% savings)
- ✅ Reserved Instances for baseline capacity (40% savings)
- ✅ Savings Plans for flexible commitment (20-72% savings)
- ✅ Graviton-based instances (20% cost reduction)
- ✅ EBS volume optimization (gp3 vs gp2)
- ✅ S3 lifecycle policies for logs and backups
- ✅ VPC endpoint for S3/ECR (reduce data transfer costs)

**Azure AKS Cost Optimization:**

```bash
# Enable cost analysis
az aks update \
  --resource-group production-rg \
  --name production-aks \
  --enable-cost-analysis

# Use Azure Spot VMs
az aks nodepool add \
  --resource-group production-rg \
  --cluster-name production-aks \
  --name spotpool \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --node-count 3 \
  --min-count 0 \
  --max-count 10
```

**GCP GKE Cost Optimization:**

```bash
# Enable GKE cost allocation
gcloud container clusters update production \
  --enable-cost-allocation \
  --resource-labels=team=backend,env=prod

# Use preemptible nodes
gcloud container node-pools create preemptible-pool \
  --cluster=production \
  --preemptible \
  --num-nodes=5 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=20
```

See `references/cloud-cost-management.md` for provider-specific details.

### 8. Cost Anomaly Detection

**Automated Anomaly Detection:**

```yaml
# PrometheusRule for cost spikes
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cost-anomaly-detection
spec:
  groups:
  - name: cost.alerts
    interval: 5m
    rules:
    - alert: NamespaceCostSpike
      expr: |
        (
          sum by (namespace) (
            rate(container_cpu_usage_seconds_total[1h])
          )
          /
          avg_over_time(
            sum by (namespace) (
              rate(container_cpu_usage_seconds_total[1h])
            )[7d:1h]
          )
        ) > 1.5
      for: 30m
      labels:
        severity: warning
        category: cost-anomaly
      annotations:
        summary: "Cost spike in namespace {{ $labels.namespace }}"
        description: "Namespace {{ $labels.namespace }} cost increased by {{ $value | humanizePercentage }} above 7-day average"

    - alert: UnexpectedPodScaling
      expr: |
        count by (namespace, deployment) (kube_pod_info)
        >
        avg_over_time(count by (namespace, deployment) (kube_pod_info)[24h:1h]) * 2
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: "Unexpected pod count increase in {{ $labels.namespace }}/{{ $labels.deployment }}"

    - alert: StorageCostIncrease
      expr: |
        sum by (namespace) (kube_persistentvolumeclaim_resource_requests_storage_bytes)
        >
        sum by (namespace) (kube_persistentvolumeclaim_resource_requests_storage_bytes offset 7d) * 1.3
      labels:
        severity: info
      annotations:
        summary: "Storage costs increased 30% in {{ $labels.namespace }}"
```

**Machine Learning-Based Detection:**
```python
# Cost anomaly detection with Prophet
from prophet import Prophet
import pandas as pd

def detect_cost_anomalies(cost_data):
    """
    Detect cost anomalies using time series forecasting.

    Args:
        cost_data: DataFrame with 'ds' (date) and 'y' (cost) columns
    """
    model = Prophet(
        changepoint_prior_scale=0.05,
        yearly_seasonality=True,
        weekly_seasonality=True,
        interval_width=0.95
    )
    model.fit(cost_data)

    forecast = model.predict(cost_data)

    # Identify anomalies (outside 95% confidence interval)
    anomalies = cost_data[
        (cost_data['y'] > forecast['yhat_upper']) |
        (cost_data['y'] < forecast['yhat_lower'])
    ]

    return anomalies
```

### 9. FinOps Best Practices

**The FinOps Framework:**

```
┌─────────────────────────────────────────────────────┐
│                   INFORM Phase                       │
│  • Cost visibility    • Allocation    • Benchmarks  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                  OPTIMIZE Phase                      │
│  • Right-sizing    • Spot usage    • Reservations   │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                  OPERATE Phase                       │
│  • Governance    • Automation    • Culture           │
└─────────────────────────────────────────────────────┘
```

**FinOps Maturity Model:**

| Crawl | Walk | Run |
|-------|------|-----|
| Basic visibility | Cost allocation | Automated optimization |
| Manual reporting | Showback model | Chargeback implementation |
| Ad-hoc optimization | Reserved capacity planning | Continuous optimization |
| No governance | Team budgets | Policy enforcement |
| Centralized management | Federated accountability | Self-service with guardrails |

**Key Performance Indicators (KPIs):**

```yaml
finops_kpis:
  efficiency:
    - name: cluster_utilization
      target: ">65%"
      formula: "(allocated / capacity) * 100"

    - name: waste_percentage
      target: "<15%"
      formula: "(requested - used) / requested * 100"

  cost:
    - name: cost_per_namespace
      unit: USD/month
      tracking: monthly_trend

    - name: cost_per_request
      unit: USD/million requests
      benchmark: industry_average

  optimization:
    - name: spot_instance_coverage
      target: ">50%"
      workloads: [non-critical]

    - name: reserved_capacity_utilization
      target: ">90%"

    - name: savings_from_rightsizing
      target: ">20%"
      calculation: monthly
```

**Governance Policies:**

```yaml
# Budget enforcement
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-backend-quota
  namespace: team-backend
spec:
  hard:
    requests.cpu: "50"
    requests.memory: "100Gi"
    persistentvolumeclaims: "20"
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["medium", "low"]
```

```yaml
# LimitRange for cost control
apiVersion: v1
kind: LimitRange
metadata:
  name: cost-limits
  namespace: development
spec:
  limits:
  - max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "10m"
      memory: "16Mi"
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

### 10. Cost Optimization Recommendations

**Automated Recommendation Engine:**

```yaml
# Cost optimization recommendations
recommendations:
  high_priority:
    - type: rightsizing
      resource: deployment/api-server
      namespace: production
      current:
        cpu_request: 2000m
        memory_request: 4Gi
      recommended:
        cpu_request: 800m
        memory_request: 1.5Gi
      reasoning: "P95 usage: CPU 750m, Memory 1.2Gi"
      savings: "$145/month (65% reduction)"

    - type: storage_optimization
      resource: pvc/logs-volume
      namespace: logging
      current:
        storage_class: standard-ssd
        size: 500Gi
      recommended:
        storage_class: standard
        size: 200Gi
      reasoning: "Usage: 180Gi, growth: 2GB/month"
      savings: "$80/month"

  medium_priority:
    - type: spot_migration
      resource: deployment/batch-processor
      namespace: batch
      current:
        node_type: on-demand
        monthly_cost: "$450"
      recommended:
        node_type: spot
        monthly_cost: "$135"
      reasoning: "Fault-tolerant workload, no SLA requirements"
      savings: "$315/month (70% reduction)"
      risk: "low"

  low_priority:
    - type: image_optimization
      resource: deployment/web-app
      namespace: production
      current:
        image_size: 2.4GB
      recommended:
        base_image: "distroless"
        image_size: 450MB
      savings: "$15/month (registry + transfer costs)"
```

**Continuous Optimization Workflow:**

```bash
#!/bin/bash
# Daily cost optimization check

# 1. Generate recommendations
kubectl opencost recommendations \
  --threshold=20 \
  --output=json > /tmp/recommendations.json

# 2. Filter by potential savings
jq '.recommendations[] | select(.savings_monthly > 50)' \
  /tmp/recommendations.json

# 3. Auto-apply safe recommendations
kubectl opencost apply-recommendation \
  --type=rightsizing \
  --auto-approve \
  --max-change=30 \
  --rollback-on-error

# 4. Send report
kubectl opencost report \
  --format=email \
  --recipients=finops-team@company.com
```

### 11. Multi-Cluster Cost Management

**Centralized Cost Dashboard:**

```yaml
# Thanos for multi-cluster metrics aggregation
apiVersion: monitoring.coreos.com/v1
kind: ThanosQuery
metadata:
  name: cost-aggregator
spec:
  replicas: 2
  stores:
    - dnssrv+_grpc._tcp.thanos-store.cluster-prod.svc.cluster.local
    - dnssrv+_grpc._tcp.thanos-store.cluster-staging.svc.cluster.local
    - dnssrv+_grpc._tcp.thanos-store.cluster-dev.svc.cluster.local
  queryTimeout: 5m
```

**Cross-Cluster Cost Comparison:**

```promql
# Total cost by cluster
sum by (cluster) (
  opencost_namespace_cpu_cost +
  opencost_namespace_memory_cost +
  opencost_namespace_storage_cost
)

# Cost efficiency by cluster
sum by (cluster) (
  opencost_namespace_cpu_cost
) / sum by (cluster) (
  kube_pod_container_resource_requests{resource="cpu"}
)
```

## Bilingual Support

### Русский (Russian)

**Основные концепции FinOps:**

1. **Видимость затрат** — отслеживание расходов на ресурсы Kubernetes
2. **Аллокация затрат** — распределение расходов по командам, проектам, средам
3. **Оптимизация** — снижение затрат через правильное sizing, spot-инстансы, резервирование
4. **Управление** — политики, бюджеты, автоматизация

**Ключевые метрики:**
- Utilization (использование) — процент используемых ресурсов от запрошенных
- Waste (потери) — разница между запрошенными и используемыми ресурсами
- Cost per namespace — затраты на namespace
- Savings percentage — процент экономии от оптимизации

**Модели распределения затрат:**
- **Showback** — информирование о затратах без финансовых транзакций
- **Chargeback** — внутренний биллинг с реальными переводами между бюджетами

## References

- **[finops-patterns.md](references/finops-patterns.md)** — FinOps practices, cost allocation models, chargeback implementation
- **[optimization-guide.md](references/optimization-guide.md)** — Resource optimization strategies, right-sizing, spot instances
- **[cloud-cost-management.md](references/cloud-cost-management.md)** — AWS/Azure/GCP specific cost optimization techniques

## Configuration Assets

- **[opencost-config.yaml](assets/opencost-config.yaml)** — Production-ready OpenCost configuration
- **[cost-allocation-policies.yaml](assets/cost-allocation-policies.yaml)** — Cost allocation rules and policies

## Key Takeaways

1. **Start with visibility** — Deploy OpenCost/KubeCost before optimization
2. **Implement allocation early** — Tag resources consistently from day one
3. **Begin with showback** — Build cost awareness before chargeback
4. **Optimize continuously** — Automate recommendations and right-sizing
5. **Use hybrid strategies** — Combine spot, reserved, and on-demand capacity
6. **Set budgets and alerts** — Prevent cost overruns proactively
7. **Measure and iterate** — Track KPIs and improve over time

## Related Skills

- **observability-monitoring** — Metrics collection for cost tracking
- **policy-compliance** — Resource quotas and limits enforcement
- **gitops-workflow** — Infrastructure as Code for cost policies
