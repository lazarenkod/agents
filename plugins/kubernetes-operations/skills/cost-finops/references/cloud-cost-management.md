# Cloud Provider Cost Management

## Overview

This guide provides cloud provider-specific cost optimization strategies for AWS EKS, Azure AKS, and Google Cloud GKE, including native tools, pricing models, and best practices.

## AWS EKS Cost Optimization

### 1. EKS Pricing Model

**Cost Components:**

```yaml
eks_costs:
  control_plane:
    cost: "$0.10/hour per cluster"
    monthly: "$73/cluster"
    notes: "Fixed cost regardless of size"

  worker_nodes:
    ec2_instances:
      on_demand: "Standard EC2 pricing"
      reserved: "40-60% discount"
      spot: "70-90% discount"
      savings_plans: "20-72% flexible discount"

  data_transfer:
    within_az: "Free"
    cross_az: "$0.01/GB"
    to_internet: "$0.09/GB"
    from_internet: "Free"

  storage:
    ebs_gp3: "$0.08/GB-month + $0.005/IOPS + $0.04/MB/s"
    ebs_gp2: "$0.10/GB-month"
    ebs_io2: "$0.125/GB-month + $0.065/IOPS"
    efs: "$0.30/GB-month (Standard)"

  load_balancers:
    alb: "$0.0225/hour + $0.008/LCU-hour"
    nlb: "$0.0225/hour + $0.006/NLCU-hour"
    clb: "$0.025/hour + $0.008/GB"
```

### 2. EC2 Instance Optimization

**Instance Type Selection:**

```python
#!/usr/bin/env python3
"""
AWS EC2 instance cost optimizer for EKS workloads.
"""

import boto3
from typing import Dict, List

# Cost-performance ratios (lower is better)
INSTANCE_EFFICIENCY = {
    # General Purpose
    'm5.xlarge': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.192, 'ratio': 0.012},
    'm5.2xlarge': {'vcpu': 8, 'memory': 32, 'cost_hour': 0.384, 'ratio': 0.012},
    'm5a.xlarge': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.172, 'ratio': 0.011},  # Better
    'm6i.xlarge': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.192, 'ratio': 0.012},

    # Compute Optimized
    'c5.xlarge': {'vcpu': 4, 'memory': 8, 'cost_hour': 0.170, 'ratio': 0.021},
    'c5a.xlarge': {'vcpu': 4, 'memory': 8, 'cost_hour': 0.154, 'ratio': 0.019},   # Better
    'c6i.xlarge': {'vcpu': 4, 'memory': 8, 'cost_hour': 0.170, 'ratio': 0.021},

    # Memory Optimized
    'r5.xlarge': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.252, 'ratio': 0.016},
    'r5a.xlarge': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.226, 'ratio': 0.014},  # Better
    'r6i.xlarge': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.252, 'ratio': 0.016},

    # ARM-based (Graviton) - 20% better price/performance
    'm6g.xlarge': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.154, 'ratio': 0.010},  # Best
    'c6g.xlarge': {'vcpu': 4, 'memory': 8, 'cost_hour': 0.136, 'ratio': 0.017},   # Best
    'r6g.xlarge': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.202, 'ratio': 0.013},  # Best
}

def recommend_instance_type(
    workload_type: str,
    cpu_required: int,
    memory_gb_required: int,
    spot_eligible: bool = False
) -> Dict:
    """
    Recommend optimal EC2 instance type for EKS workload.

    Args:
        workload_type: 'general', 'compute', or 'memory'
        cpu_required: Number of vCPUs needed
        memory_gb_required: Memory in GB needed
        spot_eligible: Whether workload can use spot instances

    Returns:
        Dict with recommendation and cost analysis
    """
    # Filter instances by workload type
    if workload_type == 'compute':
        candidates = {k: v for k, v in INSTANCE_EFFICIENCY.items() if k.startswith('c')}
    elif workload_type == 'memory':
        candidates = {k: v for k, v in INSTANCE_EFFICIENCY.items() if k.startswith('r')}
    else:
        candidates = {k: v for k, v in INSTANCE_EFFICIENCY.items() if k.startswith('m')}

    # Filter by resource requirements
    suitable = {
        k: v for k, v in candidates.items()
        if v['vcpu'] >= cpu_required and v['memory'] >= memory_gb_required
    }

    # Sort by cost efficiency
    sorted_instances = sorted(
        suitable.items(),
        key=lambda x: x[1]['ratio']
    )

    if not sorted_instances:
        return {'error': 'No suitable instance type found'}

    recommended = sorted_instances[0]
    instance_type, specs = recommended

    # Calculate costs
    hourly_cost = specs['cost_hour']
    monthly_cost = hourly_cost * 730

    if spot_eligible:
        spot_savings = 0.75  # Average 75% savings
        spot_monthly = monthly_cost * (1 - spot_savings)
    else:
        spot_monthly = None

    # Reserved instance options
    reserved_1yr = monthly_cost * 0.65 * 12
    reserved_3yr = monthly_cost * 0.48 * 36

    return {
        'recommended_instance': instance_type,
        'specs': specs,
        'costs': {
            'on_demand': {
                'hourly': hourly_cost,
                'monthly': monthly_cost,
                'annual': monthly_cost * 12
            },
            'spot': {
                'monthly': spot_monthly,
                'annual': spot_monthly * 12 if spot_monthly else None,
                'savings_percent': 75
            } if spot_eligible else None,
            'reserved_1yr': {
                'total': reserved_1yr,
                'monthly_equivalent': reserved_1yr / 12,
                'savings_percent': 35
            },
            'reserved_3yr': {
                'total': reserved_3yr,
                'monthly_equivalent': reserved_3yr / 36,
                'savings_percent': 52
            }
        },
        'alternatives': [
            {'type': k, 'cost_hour': v['cost_hour']}
            for k, v in sorted_instances[1:4]
        ]
    }

# Example usage
if __name__ == "__main__":
    recommendation = recommend_instance_type(
        workload_type='general',
        cpu_required=4,
        memory_gb_required=16,
        spot_eligible=True
    )
    print(f"Recommended: {recommendation['recommended_instance']}")
    print(f"Monthly cost (on-demand): ${recommendation['costs']['on_demand']['monthly']:.2f}")
    if recommendation['costs']['spot']:
        print(f"Monthly cost (spot): ${recommendation['costs']['spot']['monthly']:.2f}")
```

**Graviton (ARM) Migration:**

```yaml
# Migrate to Graviton instances for 20% cost savings
---
# Before: x86-based
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: production
nodeGroups:
  - name: general-x86
    instanceType: m5.xlarge    # $0.192/hour
    minSize: 5
    maxSize: 20

---
# After: ARM-based Graviton
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: production
nodeGroups:
  - name: general-graviton
    instanceType: m6g.xlarge   # $0.154/hour (20% cheaper)
    minSize: 5
    maxSize: 20
    # Require ARM-compatible images
    labels:
      arch: arm64

# Update deployments to use multi-arch images
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/arch: arm64
      containers:
      - name: app
        image: app:latest-arm64  # or multi-arch image
```

### 3. EBS Volume Optimization

**gp3 vs gp2 Savings:**

```yaml
# gp2 (older generation): $0.10/GB-month, 3 IOPS/GB (max 16,000)
# gp3 (newer): $0.08/GB-month, 3,000 IOPS baseline, configurable IOPS/throughput

# Migration recommendation
---
# Before: gp2
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp2-default
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
allowVolumeExpansion: true

---
# After: gp3 (20% cheaper, better performance)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3-default
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"        # Baseline (free)
  throughput: "125"   # Baseline (free)
  fsType: ext4
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

# High-performance: only pay for extra IOPS if needed
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3-high-perf
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "16000"       # +$0.005/IOPS above 3000 = $65/month
  throughput: "1000"  # +$0.04/MB/s above 125 = $35/month
  fsType: ext4
```

**EBS Snapshot Management:**

```bash
#!/bin/bash
# Optimize EBS snapshot costs

# Delete old snapshots (keep last 7 days)
aws ec2 describe-snapshots \
  --owner-ids self \
  --query "Snapshots[?StartTime<='$(date -d '7 days ago' --utc +%Y-%m-%dT%H:%M:%S.000Z)'].SnapshotId" \
  --output text | xargs -n 1 aws ec2 delete-snapshot --snapshot-id

# Move snapshots to S3 for cheaper storage (via Lifecycle policy)
aws dlm create-lifecycle-policy \
  --description "Move old snapshots to S3" \
  --state ENABLED \
  --execution-role-arn arn:aws:iam::ACCOUNT:role/DLMRole \
  --policy-details file://snapshot-lifecycle.json

# snapshot-lifecycle.json
{
  "PolicyType": "EBS_SNAPSHOT_MANAGEMENT",
  "ResourceTypes": ["VOLUME"],
  "TargetTags": [{
    "Key": "backup",
    "Value": "true"
  }],
  "Schedules": [{
    "Name": "Daily backups with 7-day retention",
    "CreateRule": {
      "Interval": 24,
      "IntervalUnit": "HOURS",
      "Times": ["03:00"]
    },
    "RetainRule": {
      "Count": 7
    }
  }]
}
```

### 4. VPC and Networking Optimization

**Use VPC Endpoints to Avoid NAT Gateway Costs:**

```bash
# NAT Gateway: $0.045/hour + $0.045/GB processed = ~$35/month + data
# VPC Endpoints: $0.01/hour + $0.01/GB = ~$7/month + data (Gateway endpoints free)

# Create S3 Gateway Endpoint (FREE for data transfer)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-xxx rtb-yyy

# Create ECR Interface Endpoints (reduces NAT Gateway usage)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxx \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.ecr.api \
  --subnet-ids subnet-xxx subnet-yyy \
  --security-group-ids sg-xxx

aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxx \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.ecr.dkr \
  --subnet-ids subnet-xxx subnet-yyy \
  --security-group-ids sg-xxx

# Cost comparison for 1TB/month data transfer to S3:
# Via NAT Gateway: $35 (NAT) + $45 (data processing) = $80/month
# Via VPC Endpoint (Gateway): $0/month
# Savings: $80/month per cluster
```

**Optimize ELB/ALB:**

```yaml
# Consolidate multiple ALBs into one (save $16-18/ALB/month)
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: consolidated-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    # Share single ALB across namespaces
    alb.ingress.kubernetes.io/group.name: shared-alb
    # Use IP targets (no extra ENI costs)
    alb.ingress.kubernetes.io/target-type: ip
    # Enable HTTP/2 for better efficiency
    alb.ingress.kubernetes.io/alpn-policy: HTTP2Preferred
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /v1
        pathType: Prefix
        backend:
          service:
            name: api-v1
            port:
              number: 80
  - host: web.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 80

# Cost savings example:
# Before: 5 ALBs × $16.20/month = $81/month
# After: 1 shared ALB = $16.20/month
# Savings: $64.80/month
```

### 5. AWS Savings Plans and Reserved Instances

**Compute Savings Plans (Most Flexible):**

```bash
# Compute Savings Plans: Up to 66% discount
# - Apply to EC2, Fargate, Lambda
# - Region and instance type flexible
# - 1 or 3 year commitment

# Analyze current usage
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days 30

# Purchase Savings Plan
aws savingsplans create-savings-plan \
  --savings-plan-type ComputeSavingsPlans \
  --commitment 100 \
  --upfront-payment-amount 0 \
  --term 1year
```

**Reserved Instances (Less Flexible, Deeper Discounts):**

```bash
# EC2 Reserved Instances: Up to 72% discount
# - Instance type, size, region locked
# - 1 or 3 year commitment
# - Convertible RIs allow some flexibility

# Find RI recommendations
aws ec2 describe-reserved-instances-offerings \
  --instance-type m5.xlarge \
  --product-description Linux/UNIX \
  --instance-tenancy default

# Purchase Reserved Instance
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id <offering-id> \
  --instance-count 10
```

**Recommendation Strategy:**

```yaml
commitment_strategy:
  # Baseline capacity: Reserved Instances (highest discount)
  reserved_instances:
    commitment: 30% of steady-state capacity
    term: 3-year convertible
    upfront: partial
    discount: ~50-55%

  # Flexible baseline: Compute Savings Plans
  savings_plans:
    commitment: 20% of average usage
    term: 1-year
    upfront: no
    discount: ~20-40%

  # Variable capacity: On-demand + Spot
  on_demand:
    usage: 20% (scaling buffer)
    discount: 0%

  spot_instances:
    usage: 30% (fault-tolerant workloads)
    discount: ~70-90%

# Expected blended discount: ~45-55%
```

### 6. AWS Cost Explorer and Budgets

**Set Up Cost Alerts:**

```bash
# Create budget with alerts
aws budgets create-budget \
  --account-id 123456789012 \
  --budget file://eks-budget.json \
  --notifications-with-subscribers file://notifications.json

# eks-budget.json
{
  "BudgetName": "EKS-Production-Monthly",
  "BudgetLimit": {
    "Amount": "10000",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {
    "TagKeyValue": [
      "kubernetes.io/cluster/production$true"
    ]
  }
}

# notifications.json
{
  "Notification": {
    "NotificationType": "ACTUAL",
    "ComparisonOperator": "GREATER_THAN",
    "Threshold": 80,
    "ThresholdType": "PERCENTAGE"
  },
  "Subscribers": [
    {
      "SubscriptionType": "EMAIL",
      "Address": "finops@company.com"
    }
  ]
}
```

## Azure AKS Cost Optimization

### 1. AKS Pricing Model

**Cost Components:**

```yaml
aks_costs:
  control_plane:
    free_tier: "Free (single availability zone)"
    standard_tier: "$0.10/hour ($73/month)"
    uptime_sla: "$0.10/hour with 99.95% SLA"

  worker_nodes:
    virtual_machines:
      pay_as_you_go: "Standard VM pricing"
      reserved: "Up to 72% discount (3-year)"
      spot: "Up to 90% discount"

  data_transfer:
    within_region: "Free"
    cross_region: "$0.02/GB"
    to_internet: "$0.05-0.087/GB (tiered)"

  storage:
    managed_disks:
      standard_hdd: "$0.04/GB-month"
      standard_ssd: "$0.10/GB-month"
      premium_ssd: "$0.18/GB-month"
      ultra_ssd: "$0.24/GB-month + IOPS/throughput"
    azure_files: "$0.06-0.30/GB-month"

  load_balancers:
    basic: "Free"
    standard: "$0.025/hour + $0.005/GB processed"
```

### 2. VM Instance Optimization

**Azure VM Series Cost Comparison:**

```python
AZURE_VM_EFFICIENCY = {
    # General Purpose
    'Standard_D4s_v5': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.192, 'ratio': 0.012},
    'Standard_D4as_v5': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.169, 'ratio': 0.011},  # AMD (12% cheaper)

    # Compute Optimized
    'Standard_F4s_v2': {'vcpu': 4, 'memory': 8, 'cost_hour': 0.169, 'ratio': 0.021},

    # Memory Optimized
    'Standard_E4s_v5': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.252, 'ratio': 0.016},
    'Standard_E4as_v5': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.221, 'ratio': 0.014},  # AMD (12% cheaper)

    # Burstable (Dev/Test)
    'Standard_B4ms': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.166, 'ratio': 0.010},  # Great for variable workloads
}

# AMD-based VMs: 10-15% cheaper than Intel equivalents
# Spot VMs: Up to 90% discount with eviction
# Reserved: Up to 72% discount (3-year commitment)
```

**Spot VM Configuration:**

```bash
# Create AKS node pool with Spot VMs
az aks nodepool add \
  --resource-group production-rg \
  --cluster-name production-aks \
  --name spotpool \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --node-count 3 \
  --min-count 0 \
  --max-count 20 \
  --enable-cluster-autoscaler \
  --node-taints kubernetes.azure.com/scalesetpriority=spot:NoSchedule \
  --node-labels workload=fault-tolerant
```

### 3. Managed Disk Optimization

**Standard SSD vs Premium SSD:**

```yaml
# Standard SSD: Better cost/performance for most workloads
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-ssd
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: StandardSSD_LRS  # $0.10/GB vs Premium $0.18/GB
  kind: Managed
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true

---
# Use Premium SSD only for high IOPS workloads (databases)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Premium_LRS
  kind: Managed
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

**Disk Snapshot Optimization:**

```bash
# Snapshots are incremental (only changed blocks)
# Standard snapshot: $0.05/GB-month
# Move old snapshots to cool storage

az snapshot create \
  --resource-group production-rg \
  --name daily-backup-$(date +%Y%m%d) \
  --source /subscriptions/.../disk-name \
  --incremental

# Cleanup old snapshots (keep 7 days)
az snapshot list \
  --resource-group production-rg \
  --query "[?timeCreated < '$(date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ)'].name" \
  --output tsv | xargs -I {} az snapshot delete --name {} --resource-group production-rg
```

### 4. Azure Reserved VM Instances

**Purchase Recommendations:**

```bash
# Get RI recommendations from Azure Advisor
az advisor recommendation list \
  --category Cost \
  --output table

# Purchase reserved capacity (via Azure portal or CLI)
# - 1-year: ~40% discount
# - 3-year: ~60-72% discount
# - Can be scoped to: Subscription, Resource Group, or Shared

# Example: Reserve 5× Standard_D4s_v5 for 3 years
# On-demand: $0.192/hour × 5 VMs × 8760 hours/year × 3 years = $25,272
# Reserved (3-year): $10,104 (60% savings = $15,168 saved)
```

### 5. Azure Cost Management

**Enable Cost Analysis for AKS:**

```bash
# Enable AKS cost analysis
az aks update \
  --resource-group production-rg \
  --name production-aks \
  --enable-cost-analysis

# Tag resources for cost allocation
az aks update \
  --resource-group production-rg \
  --name production-aks \
  --tags Environment=Production Team=Platform CostCenter=CC-1100

# Export cost data to storage account
az costmanagement export create \
  --name daily-costs \
  --type ActualCost \
  --dataset-granularity Daily \
  --timeframe MonthToDate \
  --storage-account-id /subscriptions/.../storageAccounts/costs \
  --storage-container costs \
  --schedule-status Active \
  --schedule-recurrence Daily
```

**Cost Alerts:**

```bash
# Create budget alert
az consumption budget create \
  --name AKS-Production-Budget \
  --category Cost \
  --amount 10000 \
  --time-grain Monthly \
  --start-date 2024-01-01 \
  --end-date 2025-12-31 \
  --resource-group production-rg \
  --filter resource-group=production-rg \
  --notifications \
    '[{
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["finops@company.com"],
      "contactRoles": ["Owner", "Contributor"]
    }]'
```

### 6. Azure Networking Cost Optimization

**Use Private Endpoints:**

```bash
# Private endpoint for Azure Container Registry (ACR)
# Avoids egress charges for image pulls

az network private-endpoint create \
  --name acr-private-endpoint \
  --resource-group production-rg \
  --vnet-name aks-vnet \
  --subnet private-endpoints \
  --private-connection-resource-id $(az acr show --name myregistry --query id -o tsv) \
  --group-id registry \
  --connection-name acr-connection

# Cost savings:
# Without private endpoint: $0.087/GB egress × 500GB/month = $43.50/month
# With private endpoint: $0.01/hour × 730 hours = $7.30/month
# Savings: $36.20/month
```

## Google Cloud GKE Cost Optimization

### 1. GKE Pricing Model

**Cost Components:**

```yaml
gke_costs:
  control_plane:
    standard: "Free (single-zone)"
    autopilot: "$0.10/hour ($73/month) included in pod costs"
    regional: "$0.10/hour per cluster"

  worker_nodes:
    compute_engine:
      on_demand: "Standard Compute Engine pricing"
      committed_use: "Up to 57% discount (3-year)"
      preemptible: "Up to 80% discount"
      spot: "Up to 91% discount"

  data_transfer:
    within_zone: "Free"
    cross_zone_same_region: "$0.01/GB"
    cross_region: "$0.01-0.05/GB"
    to_internet: "$0.12/GB (first 1GB free)"

  storage:
    persistent_disks:
      standard_pd: "$0.04/GB-month"
      balanced_pd: "$0.10/GB-month"
      ssd_pd: "$0.17/GB-month"
    filestore:
      basic_hdd: "$0.20/GB-month"
      basic_ssd: "$0.30/GB-month"

  load_balancers:
    network_lb: "$0.025/hour + $0.008/GB"
    application_lb: "$0.025/hour + $0.008/GB (+ forwarding rules)"
```

### 2. Compute Engine Machine Type Optimization

**Cost-Effective Machine Types:**

```python
GCP_MACHINE_EFFICIENCY = {
    # General Purpose (N2)
    'n2-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.194, 'ratio': 0.012},
    'n2d-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.151, 'ratio': 0.009},  # AMD (22% cheaper)

    # Compute Optimized (C2)
    'c2-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.199, 'ratio': 0.012},
    'c2d-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.158, 'ratio': 0.010},  # AMD (21% cheaper)

    # Memory Optimized (N2 high-memory)
    'n2-highmem-4': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.290, 'ratio': 0.018},
    'n2d-highmem-4': {'vcpu': 4, 'memory': 32, 'cost_hour': 0.226, 'ratio': 0.014},  # AMD (22% cheaper)

    # E2 (Burstable - great for variable workloads)
    'e2-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.134, 'ratio': 0.008},  # Cheapest!

    # Tau T2D (Optimized for scale-out)
    't2d-standard-4': {'vcpu': 4, 'memory': 16, 'cost_hour': 0.135, 'ratio': 0.008},  # Excellent value
}

# AMD-based (N2D, C2D): 20-25% cheaper
# E2 shared-core: Up to 30% cheaper for variable workloads
# Tau T2D: Optimized for scale-out, ~30% cheaper
```

**Spot and Preemptible VMs:**

```bash
# Create GKE node pool with Spot VMs (up to 91% discount)
gcloud container node-pools create spot-pool \
  --cluster=production \
  --spot \
  --machine-type=n2d-standard-4 \
  --num-nodes=0 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=20 \
  --node-labels=workload-type=fault-tolerant \
  --node-taints=cloud.google.com/gke-spot=true:NoSchedule

# Legacy: Preemptible VMs (up to 80% discount)
gcloud container node-pools create preemptible-pool \
  --cluster=production \
  --preemptible \
  --machine-type=n2d-standard-4 \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=0 \
  --max-nodes=20
```

### 3. GKE Autopilot (Fully Managed)

**Autopilot vs Standard GKE Cost Comparison:**

```yaml
# Autopilot: Pay only for pod resources (no node overhead)
# - No node management fees
# - Automatic rightsizing
# - Better resource utilization
# - ~25-50% cost reduction vs. over-provisioned standard GKE

autopilot_pricing:
  compute:
    cpu: "$0.045/vCPU-hour"
    memory: "$0.005/GB-hour"
    spot_cpu: "$0.012/vCPU-hour (73% discount)"
    spot_memory: "$0.0013/GB-hour (73% discount)"

  # Example: 100 vCPU, 200GB memory, 50% spot-eligible
  monthly_cost_calculation:
    standard_compute: (50 vCPU × $0.045 × 730) + (100 GB × $0.005 × 730) = $2,007.50
    spot_compute: (50 vCPU × $0.012 × 730) + (100 GB × $0.0013 × 730) = $533.40
    total_monthly: $2,540.90

  # vs Standard GKE with 20% overhead
  standard_gke_cost:
    nodes: (120 vCPU × $0.031 × 730) + (240 GB × $0.004 × 730) = $3,422.40
    # Autopilot saves ~26% with better utilization
```

**Deploy to Autopilot:**

```bash
# Create Autopilot cluster
gcloud container clusters create-auto production-auto \
  --region=us-central1 \
  --release-channel=regular

# Deploy workload (automatic bin-packing and rightsizing)
kubectl apply -f deployment.yaml

# Use spot pods for fault-tolerant workloads
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
spec:
  template:
    metadata:
      annotations:
        # Request spot capacity
        cloud.google.com/compute-class: "Spot"
    spec:
      containers:
      - name: processor
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          # Autopilot enforces limits = requests
```

### 4. Persistent Disk Optimization

**Choose Right Disk Type:**

```yaml
# Standard PD: $0.04/GB-month (magnetic, legacy)
# Balanced PD: $0.10/GB-month (SSD, best value)
# SSD PD: $0.17/GB-month (high performance)

---
# Use Balanced PD for most workloads (best cost/performance)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: balanced-rwo
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-balanced
  replication-type: regional-pd  # HA across zones
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true

---
# Use SSD PD only for databases needing high IOPS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ssd-rwo
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### 5. Committed Use Discounts (CUDs)

**Purchase Recommendations:**

```bash
# Get CUD recommendations
gcloud recommender recommendations list \
  --project=my-project \
  --location=us-central1 \
  --recommender=google.compute.commitment.UsageCommitmentRecommender

# Purchase 1-year or 3-year commitment
# - 1-year: ~37% discount
# - 3-year: ~55-57% discount
# - Applies to CPU, memory, or both

# Example: Commit to 50 vCPUs for 3 years
gcloud compute commitments create cpu-commitment \
  --project=my-project \
  --region=us-central1 \
  --plan=36-month \
  --resources=vcpu=50

# Cost savings:
# On-demand: 50 vCPU × $0.031/hour × 8760 hours/year × 3 years = $40,716
# 3-year CUD: $40,716 × 0.45 = $18,322 (57% discount = $22,394 saved)
```

### 6. GCP Cost Management

**Enable Cost Allocation:**

```bash
# Enable GKE cost allocation
gcloud container clusters update production \
  --enable-cost-allocation \
  --resource-usage-export-dataset-id=gke_costs \
  --resource-usage-export-project-id=my-project \
  --enable-network-egress-metering

# Tag resources for cost allocation
gcloud container clusters update production \
  --resource-labels=team=platform,env=prod,cost-center=cc-1100

# Set up billing exports to BigQuery
gcloud beta billing accounts update BILLING_ACCOUNT_ID \
  --export-to-bigquery \
  --bigquery-project=my-project \
  --bigquery-dataset=billing_export
```

**Cost Alerts:**

```bash
# Create budget alert
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="GKE Production Monthly Budget" \
  --budget-amount=10000 \
  --threshold-rule=percent=80,basis=current-spend \
  --threshold-rule=percent=100,basis=current-spend \
  --notification-channels=CHANNEL_ID \
  --filter-projects=my-project \
  --filter-labels=env:prod
```

### 7. GCP Networking Cost Optimization

**Regional Cluster (vs Zonal):**

```bash
# Regional clusters: Better availability, higher cross-zone traffic costs
# Consider zonal clusters for dev/test to save on cross-zone traffic

# Zonal cluster (cheaper for dev/test)
gcloud container clusters create dev \
  --zone=us-central1-a \
  --machine-type=e2-standard-4 \
  --num-nodes=3

# Regional cluster (production)
gcloud container clusters create prod \
  --region=us-central1 \
  --machine-type=n2d-standard-4 \
  --num-nodes=1 \
  --node-locations=us-central1-a,us-central1-b,us-central1-c

# Cost impact:
# Cross-zone traffic: $0.01/GB
# For 1TB/month cross-zone: $10/month additional cost
```

**Private GKE with VPC Peering:**

```bash
# Use private GKE to avoid egress costs to GCR
gcloud container clusters create private-prod \
  --region=us-central1 \
  --enable-private-nodes \
  --enable-private-endpoint \
  --master-ipv4-cidr=172.16.0.0/28 \
  --enable-ip-alias

# Use Private Google Access for free egress to GCS/GCR
gcloud compute networks subnets update subnet-name \
  --region=us-central1 \
  --enable-private-ip-google-access
```

## Multi-Cloud Cost Comparison

### Equivalent Instance Comparison

| Specs | AWS | Azure | GCP | Cheapest |
|-------|-----|-------|-----|----------|
| 4 vCPU, 16GB (x86) | m5.xlarge ($0.192/hr) | Standard_D4s_v5 ($0.192/hr) | n2-standard-4 ($0.194/hr) | AWS/Azure |
| 4 vCPU, 16GB (AMD) | m5a.xlarge ($0.172/hr) | Standard_D4as_v5 ($0.169/hr) | n2d-standard-4 ($0.151/hr) | **GCP (22% cheaper)** |
| 4 vCPU, 16GB (ARM) | m6g.xlarge ($0.154/hr) | N/A | N/A | **AWS (ARM)** |
| 4 vCPU, 16GB (Spot) | $0.052/hr (73% off) | $0.019/hr (90% off) | $0.017/hr (91% off) | **GCP Spot** |

### Storage Cost Comparison

| Type | AWS EBS | Azure Managed Disk | GCP Persistent Disk | Cheapest |
|------|---------|--------------------|--------------------|----------|
| HDD | N/A | $0.04/GB | $0.04/GB | **Azure/GCP** |
| Standard SSD | gp3: $0.08/GB | Standard: $0.10/GB | Balanced: $0.10/GB | **AWS gp3** |
| Premium SSD | gp3: $0.08/GB + IOPS | Premium: $0.18/GB | SSD: $0.17/GB | **AWS gp3** |

### Data Transfer Cost Comparison

| Transfer Type | AWS | Azure | GCP | Cheapest |
|---------------|-----|-------|-----|----------|
| Within AZ/Zone | Free | Free | Free | All equal |
| Cross AZ/Zone | $0.01/GB | Free (within region) | $0.01/GB | **Azure** |
| Internet Egress | $0.09/GB | $0.05-0.087/GB | $0.12/GB | **Azure** |

## Cost Optimization Checklist

### AWS EKS

- [ ] Use Graviton (ARM) instances for 20% savings
- [ ] Migrate gp2 → gp3 volumes for 20% storage savings
- [ ] Implement Compute Savings Plans (~40% discount)
- [ ] Use Spot instances for 70-90% savings on fault-tolerant workloads
- [ ] Deploy VPC endpoints for S3/ECR to eliminate NAT Gateway costs
- [ ] Consolidate ALBs with shared ingress
- [ ] Enable EKS cost allocation tags
- [ ] Set up AWS Cost Explorer and budgets

### Azure AKS

- [ ] Use AMD-based VMs for 10-15% savings
- [ ] Implement Azure Spot VMs for up to 90% savings
- [ ] Use Standard SSD instead of Premium SSD where possible
- [ ] Purchase Reserved VM Instances (up to 72% discount)
- [ ] Deploy Private Endpoints for ACR to reduce egress
- [ ] Enable AKS cost analysis
- [ ] Set up Azure Cost Management budgets and alerts
- [ ] Use Azure Hybrid Benefit if available

### Google Cloud GKE

- [ ] Use AMD-based (N2D) or E2 instances for 20-30% savings
- [ ] Consider GKE Autopilot for automatic optimization
- [ ] Implement Spot VMs for up to 91% savings
- [ ] Use Balanced PD instead of SSD PD where possible
- [ ] Purchase Committed Use Discounts (up to 57% discount)
- [ ] Enable GKE cost allocation and BigQuery export
- [ ] Set up Cloud Billing budgets and alerts
- [ ] Use Private Google Access to avoid egress costs

---

**Related References:**
- finops-patterns.md — Cost allocation and FinOps governance
- optimization-guide.md — Right-sizing and resource optimization
