# Storage Class Configurations

Complete storage class configurations for AWS, Azure, and GCP with performance characteristics and use cases.

## AWS EBS Storage Classes

### GP3 (General Purpose SSD) - Recommended Default

**Characteristics:**
- Baseline: 3,000 IOPS and 125 MB/s throughput
- Configurable: Up to 16,000 IOPS and 1,000 MB/s
- Size: 1 GiB - 16 TiB
- Cost: ~$0.08/GB-month
- Use case: Boot volumes, dev/test, small-medium databases

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3-default
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### GP3 High Performance

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3-high-perf
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "16000"        # Maximum IOPS
  throughput: "1000"   # Maximum throughput
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### IO1/IO2 (Provisioned IOPS)

**Characteristics:**
- IOPS: Up to 64,000 IOPS (io2 Block Express: 256,000)
- Throughput: Up to 1,000 MB/s (io2 Block Express: 4,000 MB/s)
- Size: 4 GiB - 16 TiB (io2 Block Express: 64 TiB)
- Cost: ~$0.125/GB-month + $0.065/IOPS-month
- Use case: Mission-critical databases, high-performance workloads

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-io2-database
provisioner: ebs.csi.aws.com
parameters:
  type: io2
  iops: "10000"
  encrypted: "true"
  # Optional: io2 supports 99.999% durability SLA
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain  # Don't delete data on PVC deletion
```

### ST1 (Throughput Optimized HDD)

**Characteristics:**
- Baseline: 40 MB/s per TiB
- Burst: Up to 250 MB/s per TiB
- Size: 125 GiB - 16 TiB
- Cost: ~$0.045/GB-month
- Use case: Big data, data warehouses, log processing

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-st1-bigdata
provisioner: ebs.csi.aws.com
parameters:
  type: st1
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### SC1 (Cold HDD)

**Characteristics:**
- Baseline: 12 MB/s per TiB
- Burst: Up to 80 MB/s per TiB
- Size: 125 GiB - 16 TiB
- Cost: ~$0.015/GB-month
- Use case: Infrequently accessed data, archival

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc1-archive
provisioner: ebs.csi.aws.com
parameters:
  type: sc1
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Multi-AZ with Topology

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3-multi-az
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
allowedTopologies:
- matchLabelExpressions:
  - key: topology.ebs.csi.aws.com/zone
    values:
    - us-east-1a
    - us-east-1b
    - us-east-1c
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

## Azure Disk Storage Classes

### Premium SSD v2

**Characteristics:**
- IOPS: 3,000 - 80,000 configurable
- Throughput: 125 - 1,200 MB/s configurable
- Size: 1 GiB - 64 TiB
- Cost: $0.12/GB-month + IOPS + throughput charges
- Use case: Production databases, high-performance workloads

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium-ssd-v2
provisioner: disk.csi.azure.com
parameters:
  skuName: PremiumV2_LRS
  diskIOPSReadWrite: "5000"
  diskMBpsReadWrite: "200"
  cachingMode: None  # v2 doesn't support caching
  networkAccessPolicy: AllowAll
  publicNetworkAccess: Enabled
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Premium SSD (Managed)

**Characteristics:**
- IOPS: Up to 20,000 (depending on size)
- Throughput: Up to 900 MB/s
- Size: P4 (32 GiB) - P80 (32 TiB)
- Cost: $0.12-0.36/GB-month (size dependent)
- Use case: Production workloads, databases

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS  # or Premium_ZRS for zone-redundant
  cachingMode: ReadOnly  # None, ReadOnly, or ReadWrite
  kind: Managed
  # Optional: disk encryption set
  # diskEncryptionSetID: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/diskEncryptionSets/<des>
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Standard SSD

**Characteristics:**
- IOPS: Up to 6,000 (depending on size)
- Throughput: Up to 750 MB/s
- Size: E4 (32 GiB) - E80 (32 TiB)
- Cost: $0.05-0.19/GB-month
- Use case: Web servers, dev/test, lightly used apps

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-standard-ssd
provisioner: disk.csi.azure.com
parameters:
  skuName: StandardSSD_LRS  # or StandardSSD_ZRS
  cachingMode: ReadOnly
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Standard HDD

**Characteristics:**
- IOPS: Up to 2,000 (depending on size)
- Throughput: Up to 500 MB/s
- Size: S4 (32 GiB) - S80 (32 TiB)
- Cost: $0.04-0.12/GB-month
- Use case: Backup, archival, infrequent access

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-standard-hdd
provisioner: disk.csi.azure.com
parameters:
  skuName: Standard_LRS
  cachingMode: None
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Ultra Disk

**Characteristics:**
- IOPS: Up to 160,000
- Throughput: Up to 2,000 MB/s
- Latency: Sub-millisecond
- Size: 4 GiB - 64 TiB
- Cost: $0.12/GB-month + IOPS + throughput charges
- Use case: SAP HANA, mission-critical SQL, top-tier workloads

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-ultra
provisioner: disk.csi.azure.com
parameters:
  skuName: UltraSSD_LRS
  cachingMode: None
  diskIOPSReadWrite: "20000"
  diskMBpsReadWrite: "1000"
  # Ultra disk requires specific VM sizes and availability zones
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Zone-Redundant Storage

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium-zrs
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_ZRS  # Zone-redundant storage
  cachingMode: ReadOnly
allowedTopologies:
- matchLabelExpressions:
  - key: topology.disk.csi.azure.com/zone
    values:
    - eastus-1
    - eastus-2
    - eastus-3
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

## GCP Persistent Disk Storage Classes

### SSD Persistent Disk (pd-ssd)

**Characteristics:**
- IOPS: 30 read IOPS per GiB, 30 write IOPS per GiB
- Throughput: 0.48 MB/s per GiB (read), 0.48 MB/s per GiB (write)
- Size: 10 GiB - 64 TiB
- Cost: $0.17/GB-month
- Use case: Databases, high-performance workloads

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: none  # zonal disk
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Balanced Persistent Disk (pd-balanced)

**Characteristics:**
- IOPS: 6 read IOPS per GiB, 6 write IOPS per GiB
- Throughput: 0.28 MB/s per GiB
- Size: 10 GiB - 64 TiB
- Cost: $0.10/GB-month
- Use case: Most workloads, general purpose

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-balanced
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-balanced
  replication-type: none
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Standard Persistent Disk (pd-standard)

**Characteristics:**
- IOPS: 0.75 read IOPS per GiB, 1.5 write IOPS per GiB
- Throughput: 0.12 MB/s per GiB
- Size: 10 GiB - 64 TiB
- Cost: $0.04/GB-month
- Use case: Sequential workloads, backup, archival

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-standard
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-standard
  replication-type: none
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Extreme Persistent Disk (pd-extreme)

**Characteristics:**
- IOPS: Up to 120,000 read IOPS, 100,000 write IOPS
- Throughput: Up to 2,400 MB/s read, 1,200 MB/s write
- Size: 500 GiB - 64 TiB
- Cost: $0.125/GB-month + provisioned IOPS
- Use case: High-performance databases, Oracle, SAP HANA

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-extreme
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-extreme
  replication-type: none
  provisioned-iops-on-create: "100000"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Regional Persistent Disk

**Characteristics:**
- Synchronous replication across two zones
- Same performance as single-zone disks
- Higher availability and durability
- Cost: 2x the single-zone price
- Use case: Critical applications requiring high availability

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-ssd-regional
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
allowedTopologies:
- matchLabelExpressions:
  - key: topology.gke.io/zone
    values:
    - us-central1-a
    - us-central1-b
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### Hyperdisk Balanced

**Characteristics:**
- IOPS: Up to 80,000 configurable
- Throughput: Up to 1,200 MB/s configurable
- Size: 4 GiB - 64 TiB
- Cost: $0.09/GB-month + IOPS + throughput
- Use case: Modern high-performance workloads

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-hyperdisk-balanced
provisioner: pd.csi.storage.gke.io
parameters:
  type: hyperdisk-balanced
  provisioned-iops-on-create: "10000"
  provisioned-throughput-on-create: "300"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

## Performance Comparison Matrix

| Provider | Storage Type | IOPS Range | Throughput Range | Latency | Cost/GB-mo |
|----------|-------------|------------|------------------|---------|------------|
| AWS | EBS GP3 | 3K-16K | 125-1000 MB/s | <1ms | $0.08 |
| AWS | EBS IO2 | 100-64K | Up to 1000 MB/s | <1ms | $0.125 + IOPS |
| AWS | EBS ST1 | N/A | 40-250 MB/s/TiB | N/A | $0.045 |
| Azure | Premium SSD v2 | 3K-80K | 125-1200 MB/s | <1ms | $0.12 + IOPS |
| Azure | Premium SSD | Up to 20K | Up to 900 MB/s | <1ms | $0.12-0.36 |
| Azure | Ultra Disk | Up to 160K | Up to 2000 MB/s | <1ms | $0.12 + IOPS |
| GCP | PD-SSD | 30/GiB | 0.48 MB/s/GiB | <1ms | $0.17 |
| GCP | PD-Balanced | 6/GiB | 0.28 MB/s/GiB | <1ms | $0.10 |
| GCP | PD-Extreme | Up to 120K | Up to 2400 MB/s | <1ms | $0.125 + IOPS |

## Use Case Recommendations

### Databases (PostgreSQL, MySQL, MongoDB)

```yaml
# Production database - High IOPS
---
# AWS
metadata:
  name: database-storage
parameters:
  type: io2
  iops: "10000"
---
# Azure
parameters:
  skuName: PremiumV2_LRS
  diskIOPSReadWrite: "10000"
  diskMBpsReadWrite: "500"
---
# GCP
parameters:
  type: pd-ssd
  replication-type: regional-pd
```

### Web Applications

```yaml
# Web app storage - Balanced performance/cost
---
# AWS
parameters:
  type: gp3
  iops: "3000"
---
# Azure
parameters:
  skuName: StandardSSD_LRS
---
# GCP
parameters:
  type: pd-balanced
```

### Data Analytics / Big Data

```yaml
# High throughput for sequential access
---
# AWS
parameters:
  type: st1  # Throughput optimized
---
# Azure
parameters:
  skuName: Premium_LRS
  cachingMode: ReadOnly
---
# GCP
parameters:
  type: pd-standard
```

### Backup / Archive

```yaml
# Low-cost storage for infrequent access
---
# AWS
parameters:
  type: sc1
---
# Azure
parameters:
  skuName: Standard_LRS
---
# GCP
parameters:
  type: pd-standard
```

## Advanced Features

### Volume Expansion

All modern CSI drivers support volume expansion:

```yaml
allowVolumeExpansion: true
```

**Expand PVC:**
```bash
kubectl patch pvc data-mongodb-0 -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'
```

### Volume Snapshots

Enable snapshot support:

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-snapclass
driver: ebs.csi.aws.com  # or disk.csi.azure.com, pd.csi.storage.gke.io
deletionPolicy: Delete
```

### Volume Cloning

Clone volumes for testing:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
  dataSource:
    name: original-pvc
    kind: PersistentVolumeClaim
```

### Encryption

**AWS KMS:**
```yaml
parameters:
  encrypted: "true"
  kmsKeyId: arn:aws:kms:region:account:key/key-id
```

**Azure Disk Encryption Set:**
```yaml
parameters:
  diskEncryptionSetID: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/diskEncryptionSets/<des>
```

**GCP Customer-Managed Keys:**
```yaml
parameters:
  disk-encryption-kms-key: projects/<project>/locations/<location>/keyRings/<keyring>/cryptoKeys/<key>
```
