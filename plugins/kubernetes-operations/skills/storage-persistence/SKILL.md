---
name: storage-persistence
description: Comprehensive storage and persistence solutions for Kubernetes including Rook-Ceph, Velero backup/restore, CSI drivers (AWS EBS, Azure Disk, GCP PD), StatefulSets, and disaster recovery strategies. Use when implementing persistent storage, configuring backups, deploying stateful applications, or designing disaster recovery for Kubernetes workloads.
---

# Kubernetes Storage & Persistence

Production-grade persistent storage and disaster recovery implementation for Kubernetes clusters using CNCF projects and cloud-native storage solutions following best practices from AWS, Google Cloud, Microsoft Azure, and leading cloud-native organizations.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

## When to Use This Skill

- Implement persistent storage solutions for stateful applications
- Deploy and configure Rook-Ceph for cloud-native storage
- Set up Velero for backup and disaster recovery
- Configure CSI drivers for AWS EBS, Azure Disk, GCP Persistent Disk
- Design StatefulSet patterns for databases and distributed systems
- Implement storage performance tuning and optimization
- Plan multi-region storage and disaster recovery strategies
- Manage persistent volume lifecycle and reclaim policies
- Implement snapshot and clone strategies
- Design storage capacity planning and monitoring

## Storage Fundamentals

### Kubernetes Storage Architecture

**Core Components:**
1. **PersistentVolume (PV)** - Cluster-level storage resource
2. **PersistentVolumeClaim (PVC)** - User request for storage
3. **StorageClass** - Dynamic provisioning template
4. **CSI Driver** - Container Storage Interface plugin
5. **VolumeSnapshot** - Point-in-time snapshot of volume

**Storage Provisioning Models:**
- **Static Provisioning** - Pre-created PVs by administrators
- **Dynamic Provisioning** - Automatic PV creation via StorageClass
- **Topology-Aware Provisioning** - Zone/region-aware volume placement

### Volume Lifecycle

```
Provisioning → Binding → Using → Releasing → Reclaiming
```

**Reclaim Policies:**
- `Retain` - Manual reclamation (data preserved)
- `Delete` - Automatic deletion (default for dynamic provisioning)
- `Recycle` - Deprecated (basic scrub and reuse)

## Rook-Ceph Storage Solution

### 1. Rook Operator Deployment

**Production Rook-Ceph cluster deployment:**

```bash
# Install Rook Operator
kubectl create -f https://raw.githubusercontent.com/rook/rook/v1.12.0/deploy/examples/crds.yaml
kubectl create -f https://raw.githubusercontent.com/rook/rook/v1.12.0/deploy/examples/common.yaml
kubectl create -f https://raw.githubusercontent.com/rook/rook/v1.12.0/deploy/examples/operator.yaml

# Verify operator is running
kubectl -n rook-ceph get pods
```

**Asset:** See `assets/rook-cluster.yaml` for complete production configuration

### 2. Ceph Storage Classes

**Block Storage (RBD):**

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-ceph-block
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering

  # Performance tuning
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph

  # Enable volume expansion
  csi.storage.k8s.io/fstype: ext4

allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

**Filesystem Storage (CephFS):**

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rook-cephfs
provisioner: rook-ceph.cephfs.csi.ceph.com
parameters:
  clusterID: rook-ceph
  fsName: myfs
  pool: myfs-replicated

  # Ceph credentials
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-cephfs-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-cephfs-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph

allowVolumeExpansion: true
reclaimPolicy: Delete
```

### 3. Ceph Dashboard Access

```bash
# Get dashboard password
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode

# Port forward to dashboard
kubectl -n rook-ceph port-forward service/rook-ceph-mgr-dashboard 7000:7000

# Access at https://localhost:7000
# Username: admin
```

### 4. Ceph Health Monitoring

```bash
# Enter toolbox pod
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash

# Check cluster status
ceph status
ceph health detail
ceph df

# Monitor OSD status
ceph osd status
ceph osd tree

# Check pool information
ceph osd pool ls
ceph osd pool stats

# Monitor placement groups
ceph pg stat
```

## Cloud Provider CSI Drivers

**Reference:** See `references/storage-classes.md` for detailed configurations
**Asset:** See `assets/csi-drivers.yaml` for complete examples

### 1. AWS EBS CSI Driver

**Installation:**

```bash
# Add IAM policy for EBS CSI driver
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve \
  --role-name AmazonEKS_EBS_CSI_DriverRole

# Install EBS CSI driver
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.25"
```

**StorageClass Examples:**

```yaml
# GP3 (General Purpose SSD) - Recommended for most workloads
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"           # 3000-16000 IOPS
  throughput: "125"      # 125-1000 MB/s
  encrypted: "true"
  kmsKeyId: arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# IO2 (Provisioned IOPS) - High-performance databases
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-io2
provisioner: ebs.csi.aws.com
parameters:
  type: io2
  iops: "10000"          # Up to 64000 IOPS
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain

---
# ST1 (Throughput Optimized HDD) - Big data workloads
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-st1
provisioner: ebs.csi.aws.com
parameters:
  type: st1
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### 2. Azure Disk CSI Driver

**Installation:**

```bash
# Azure Disk CSI driver is pre-installed on AKS 1.21+
# Verify installation
kubectl get pods -n kube-system -l app=csi-azuredisk-controller
kubectl get pods -n kube-system -l app=csi-azuredisk-node
```

**StorageClass Examples:**

```yaml
# Premium SSD v2 - High performance
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium-ssd-v2
provisioner: disk.csi.azure.com
parameters:
  skuName: PremiumV2_LRS
  diskIOPSReadWrite: "3000"
  diskMBpsReadWrite: "125"
  cachingMode: None
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# Premium SSD - Production workloads
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  cachingMode: ReadOnly
  kind: Managed
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# Standard SSD - Development/test
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azure-disk-standard-ssd
provisioner: disk.csi.azure.com
parameters:
  skuName: StandardSSD_LRS
  cachingMode: ReadOnly
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
```

### 3. GCP Persistent Disk CSI Driver

**Installation:**

```bash
# GCP PD CSI driver is pre-installed on GKE 1.18+
# Enable CSI driver
gcloud container clusters update CLUSTER_NAME \
  --update-addons=GcePersistentDiskCsiDriver=ENABLED
```

**StorageClass Examples:**

```yaml
# SSD Persistent Disk - High performance
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd  # or none for zonal
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# Balanced Persistent Disk - Cost-performance balance
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gcp-pd-balanced
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-balanced
  replication-type: none
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete

---
# Standard Persistent Disk - Archival/backup
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

## StatefulSet Implementation

**Reference:** See `references/statefulset-patterns.md` for comprehensive patterns

### 1. Basic StatefulSet with Persistent Storage

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

  # Pod management policy
  podManagementPolicy: OrderedReady  # or Parallel

  # Update strategy
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0

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

      containers:
      - name: mongodb
        image: mongo:7.0
        command:
        - mongod
        - --replSet
        - rs0
        - --bind_ip_all
        ports:
        - containerPort: 27017
          name: mongo

        # Resource allocation
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi

        # Volume mounts
        volumeMounts:
        - name: data
          mountPath: /data/db

        # Liveness and readiness probes
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

### 2. StatefulSet Scaling

```bash
# Scale up
kubectl scale statefulset mongodb --replicas=5

# Scale down (deletes pods in reverse order)
kubectl scale statefulset mongodb --replicas=2

# Verify scaling
kubectl get pods -l app=mongodb -w
```

### 3. StatefulSet Updates

**Rolling Update:**

```yaml
# Update strategy in StatefulSet spec
updateStrategy:
  type: RollingUpdate
  rollingUpdate:
    partition: 0  # Update all pods (0 to N)
```

**Canary Update (Partition Strategy):**

```bash
# Update only pod-2 and pod-1 (partition=1 updates pods >= partition)
kubectl patch statefulset mongodb -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":1}}}}'

# Update image
kubectl set image statefulset/mongodb mongodb=mongo:7.0.1

# Verify pod-2 updated
kubectl get pods mongodb-2 -o jsonpath='{.spec.containers[0].image}'

# Roll out to all pods
kubectl patch statefulset mongodb -p '{"spec":{"updateStrategy":{"rollingUpdate":{"partition":0}}}}'
```

## Velero Backup & Disaster Recovery

**Asset:** See `assets/velero-schedule.yaml` for backup schedule examples
**Reference:** See `references/backup-strategies.md` for comprehensive strategies

### 1. Velero Installation

**AWS S3 Backend:**

```bash
# Create S3 bucket
aws s3 mb s3://velero-backups-production

# Create IAM user for Velero
cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::velero-backups-production/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::velero-backups-production"
            ]
        }
    ]
}
EOF

aws iam create-policy \
    --policy-name VeleroPolicy \
    --policy-document file://velero-policy.json

# Create credentials file
cat > credentials-velero <<EOF
[default]
aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_access_key=YOUR_SECRET_KEY
EOF

# Install Velero
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.8.0 \
    --bucket velero-backups-production \
    --backup-location-config region=us-east-1 \
    --snapshot-location-config region=us-east-1 \
    --secret-file ./credentials-velero
```

**Azure Blob Storage Backend:**

```bash
# Create resource group and storage account
AZURE_BACKUP_RESOURCE_GROUP=velero-backups
AZURE_STORAGE_ACCOUNT_ID=velerobackups
BLOB_CONTAINER=velero

az group create --name $AZURE_BACKUP_RESOURCE_GROUP --location eastus
az storage account create \
    --name $AZURE_STORAGE_ACCOUNT_ID \
    --resource-group $AZURE_BACKUP_RESOURCE_GROUP \
    --sku Standard_GRS \
    --encryption-services blob \
    --https-only true \
    --kind BlobStorage \
    --access-tier Hot

az storage container create -n $BLOB_CONTAINER --public-access off --account-name $AZURE_STORAGE_ACCOUNT_ID

# Install Velero
velero install \
    --provider azure \
    --plugins velero/velero-plugin-for-microsoft-azure:v1.8.0 \
    --bucket $BLOB_CONTAINER \
    --secret-file ./credentials-velero \
    --backup-location-config resourceGroup=$AZURE_BACKUP_RESOURCE_GROUP,storageAccount=$AZURE_STORAGE_ACCOUNT_ID \
    --snapshot-location-config apiTimeout=5m,resourceGroup=$AZURE_BACKUP_RESOURCE_GROUP
```

**GCP Cloud Storage Backend:**

```bash
# Create GCS bucket
gsutil mb gs://velero-backups-production/

# Create service account
gcloud iam service-accounts create velero \
    --display-name "Velero service account"

# Grant permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member serviceAccount:velero@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/compute.storageAdmin

gsutil iam ch serviceAccount:velero@PROJECT_ID.iam.gserviceaccount.com:objectAdmin gs://velero-backups-production

# Create key file
gcloud iam service-accounts keys create credentials-velero \
    --iam-account velero@PROJECT_ID.iam.gserviceaccount.com

# Install Velero
velero install \
    --provider gcp \
    --plugins velero/velero-plugin-for-gcp:v1.8.0 \
    --bucket velero-backups-production \
    --secret-file ./credentials-velero
```

### 2. Backup Strategies

**On-Demand Backup:**

```bash
# Backup entire cluster
velero backup create full-cluster-backup

# Backup specific namespace
velero backup create prod-backup --include-namespaces production

# Backup with label selector
velero backup create app-backup --selector app=my-app

# Backup with volume snapshots
velero backup create db-backup \
    --include-namespaces database \
    --snapshot-volumes=true \
    --volume-snapshot-locations=aws-us-east-1

# Exclude resources
velero backup create backup-no-secrets \
    --include-namespaces production \
    --exclude-resources secrets,configmaps
```

**Scheduled Backups:**

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-production-backup
  namespace: velero
spec:
  # Cron schedule (daily at 2 AM)
  schedule: "0 2 * * *"

  template:
    # Include namespaces
    includedNamespaces:
    - production
    - database

    # Exclude resources
    excludedResources:
    - events
    - events.events.k8s.io

    # Enable volume snapshots
    snapshotVolumes: true

    # TTL for backups
    ttl: 720h  # 30 days

    # Storage location
    storageLocation: default
    volumeSnapshotLocations:
    - aws-us-east-1

    # Hooks for backup
    hooks:
      resources:
      - name: postgres-backup-hook
        includedNamespaces:
        - database
        labelSelector:
          matchLabels:
            app: postgresql
        pre:
        - exec:
            command:
            - /bin/bash
            - -c
            - "PGPASSWORD=$POSTGRES_PASSWORD pg_dump -U postgres -d mydb > /backup/dump.sql"
            container: postgresql
            timeout: 5m
```

### 3. Restore Operations

```bash
# List available backups
velero backup get

# Restore from backup
velero restore create --from-backup daily-production-backup-20231120

# Restore specific namespace
velero restore create --from-backup full-cluster-backup \
    --include-namespaces production

# Restore with namespace mapping
velero restore create --from-backup prod-backup \
    --namespace-mappings production:production-restore

# Restore without volume data
velero restore create --from-backup db-backup \
    --restore-volumes=false

# Monitor restore progress
velero restore describe RESTORE_NAME
velero restore logs RESTORE_NAME
```

### 4. Disaster Recovery Procedures

**Full Cluster Recovery:**

```bash
# 1. Install Velero on new cluster
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.8.0 \
    --bucket velero-backups-production \
    --backup-location-config region=us-east-1 \
    --secret-file ./credentials-velero

# 2. Wait for Velero to sync backups
velero backup get

# 3. Restore latest backup
LATEST_BACKUP=$(velero backup get --output json | jq -r '.items | sort_by(.status.startTimestamp) | last | .metadata.name')
velero restore create disaster-recovery-restore --from-backup $LATEST_BACKUP

# 4. Verify restoration
kubectl get all --all-namespaces
velero restore describe disaster-recovery-restore
```

## Volume Snapshots

### 1. VolumeSnapshot CRD

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: mongodb-snapshot
  namespace: production
spec:
  volumeSnapshotClassName: csi-snapclass
  source:
    persistentVolumeClaimName: data-mongodb-0
```

### 2. VolumeSnapshotClass

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-snapclass
driver: ebs.csi.aws.com  # or disk.csi.azure.com, pd.csi.storage.gke.io
deletionPolicy: Delete
parameters:
  tagSpecification_1: "Name=production-snapshot"
  tagSpecification_2: "Environment=production"
```

### 3. Restore from Snapshot

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-restore
  namespace: production
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
  dataSource:
    name: mongodb-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
```

## Storage Performance Tuning

### 1. I/O Optimization

**Block Size Tuning:**

```yaml
# For databases (4k-8k blocks)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: high-iops
  resources:
    requests:
      storage: 500Gi
```

**Read/Write Performance:**

```bash
# Test sequential write
kubectl run -it fio --image=dmonakhov/alpine-fio --restart=Never -- \
  fio --name=seqwrite --rw=write --bs=1M --size=10G --numjobs=1

# Test random read/write
kubectl run -it fio --image=dmonakhov/alpine-fio --restart=Never -- \
  fio --name=randwrite --rw=randwrite --bs=4k --size=10G --numjobs=4 --iodepth=16

# Test IOPS
kubectl run -it fio --image=dmonakhov/alpine-fio --restart=Never -- \
  fio --name=iops --rw=randread --bs=4k --size=10G --numjobs=4 --iodepth=32
```

### 2. Capacity Management

**PVC Expansion:**

```bash
# Expand PVC (StorageClass must allow volume expansion)
kubectl patch pvc data-mongodb-0 -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'

# Verify expansion
kubectl get pvc data-mongodb-0 -w

# For filesystem expansion, may need to restart pod
kubectl rollout restart statefulset mongodb
```

**Storage Quota:**

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: storage-quota
  namespace: production
spec:
  hard:
    requests.storage: "1Ti"
    persistentvolumeclaims: "50"
```

### 3. Monitoring Storage

**Prometheus Metrics:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kubelet-storage-metrics
  namespace: monitoring
spec:
  endpoints:
  - port: https-metrics
    scheme: https
    tlsConfig:
      caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    metricRelabelings:
    # Keep only storage-related metrics
    - sourceLabels: [__name__]
      regex: kubelet_volume_stats.*
      action: keep
  selector:
    matchLabels:
      app.kubernetes.io/name: kubelet
```

**Key Metrics to Monitor:**
- `kubelet_volume_stats_capacity_bytes` - Volume capacity
- `kubelet_volume_stats_used_bytes` - Volume usage
- `kubelet_volume_stats_available_bytes` - Available space
- `kubelet_volume_stats_inodes` - Inode capacity
- `kubelet_volume_stats_inodes_used` - Inode usage

## Multi-Region Storage Strategy

### 1. Cross-Region Replication

**Velero Multi-Region Backup:**

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: aws-us-east-1
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-backups-us-east-1
  config:
    region: us-east-1

---
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: aws-us-west-2
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-backups-us-west-2
  config:
    region: us-west-2

---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: multi-region-backup
  namespace: velero
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  template:
    includedNamespaces:
    - production
    storageLocation: aws-us-east-1
    volumeSnapshotLocations:
    - aws-us-east-1
```

### 2. Regional Storage Classes

```yaml
# US-East-1 storage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: regional-ssd-us-east-1
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
allowedTopologies:
- matchLabelExpressions:
  - key: topology.ebs.csi.aws.com/zone
    values:
    - us-east-1a
    - us-east-1b
    - us-east-1c
volumeBindingMode: WaitForFirstConsumer

---
# US-West-2 storage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: regional-ssd-us-west-2
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
allowedTopologies:
- matchLabelExpressions:
  - key: topology.ebs.csi.aws.com/zone
    values:
    - us-west-2a
    - us-west-2b
    - us-west-2c
volumeBindingMode: WaitForFirstConsumer
```

## Best Practices

### 1. Storage Selection

**Guidelines:**
- **Databases** - Use block storage (RBD, EBS io2, Azure Premium SSD v2)
- **Shared filesystems** - Use CephFS, EFS, Azure Files, GCP Filestore
- **Big data** - Use object storage (S3, Azure Blob, GCS) with CSI
- **Logs/temporary** - Use ephemeral volumes or emptyDir
- **High-performance** - Use local SSDs with data replication at app level

### 2. Backup Strategy

**3-2-1 Rule:**
- **3** copies of data
- **2** different storage types
- **1** off-site backup

**Implementation:**
- Primary data in cluster (PVs)
- Volume snapshots (same region)
- Velero backups to object storage (cross-region)

### 3. Disaster Recovery Planning

**Recovery Time Objective (RTO) & Recovery Point Objective (RPO):**

```yaml
# Critical applications: RTO < 1h, RPO < 5min
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: critical-app-backup
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  template:
    includedNamespaces:
    - critical-app
    snapshotVolumes: true

---
# Standard applications: RTO < 4h, RPO < 1h
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: standard-app-backup
spec:
  schedule: "0 * * * *"  # Hourly
  template:
    includedNamespaces:
    - standard-app
    snapshotVolumes: true
```

### 4. Security

**Encryption at Rest:**
- Enable encryption for all StorageClasses
- Use KMS for key management (AWS KMS, Azure Key Vault, GCP KMS)
- Encrypt backup storage buckets

**Access Control:**
- Use PodSecurityPolicies or PodSecurityStandards
- Implement RBAC for PV/PVC operations
- Restrict Velero access to backup admins

### 5. Cost Optimization

**Storage Tiering:**
- Use appropriate storage types for workload
- Implement lifecycle policies for backups
- Clean up unused PVs with `Retain` policy

```bash
# Find unused PVs
kubectl get pv --all-namespaces -o json | \
  jq -r '.items[] | select(.status.phase=="Released") | .metadata.name'

# Delete released PVs
kubectl delete pv <pv-name>
```

## Troubleshooting

### Common Issues

**1. PVC Stuck in Pending:**

```bash
# Check PVC events
kubectl describe pvc <pvc-name>

# Common causes:
# - No available PVs (static provisioning)
# - StorageClass not found
# - Insufficient capacity
# - Node selector mismatch

# Check StorageClass
kubectl get storageclass

# Check node topology
kubectl get nodes --show-labels
```

**2. Volume Mount Failures:**

```bash
# Check pod events
kubectl describe pod <pod-name>

# Check volume attachments
kubectl get volumeattachment

# For CSI issues, check driver pods
kubectl get pods -n kube-system -l app=ebs-csi-controller
kubectl logs -n kube-system <csi-driver-pod>
```

**3. Velero Backup Failures:**

```bash
# Check backup status
velero backup describe <backup-name> --details

# Check Velero logs
kubectl logs -n velero deployment/velero

# Common issues:
# - Insufficient IAM permissions
# - S3 bucket not accessible
# - Volume snapshot timeout
# - Resource quota exceeded
```

**4. StatefulSet Pod Stuck:**

```bash
# Check pod status
kubectl get pods -l app=<statefulset-app>

# Force delete stuck pod (careful!)
kubectl delete pod <pod-name> --grace-period=0 --force

# Check PVC binding
kubectl get pvc

# Check node resources
kubectl describe node <node-name>
```

## References

- `references/storage-classes.md` - Complete storage class configurations for AWS/Azure/GCP
- `references/backup-strategies.md` - Velero backup strategies, schedules, and restore procedures
- `references/statefulset-patterns.md` - StatefulSet design patterns, scaling, and update strategies

## Assets

- `assets/rook-cluster.yaml` - Production Rook-Ceph cluster configuration
- `assets/velero-schedule.yaml` - Backup schedule examples for different scenarios
- `assets/csi-drivers.yaml` - CSI driver configurations for major cloud providers

## Related Skills

- `observability-monitoring` - Storage metrics and alerting
- `k8s-security-policies` - Storage encryption and access control
- `gitops-workflow` - Storage configuration management
- `cicd-pipelines` - Backup automation and validation
