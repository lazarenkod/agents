# Velero Backup Strategies

Comprehensive backup and disaster recovery strategies using Velero for Kubernetes workloads.

## Backup Strategy Fundamentals

### The 3-2-1 Backup Rule

**Rule Definition:**
- **3** copies of your data
- **2** different storage types
- **1** off-site copy

**Kubernetes Implementation:**
1. **Primary copy** - Live data in PersistentVolumes
2. **Secondary copy** - Volume snapshots in same region
3. **Tertiary copy** - Velero backups in object storage (different region)

### Recovery Time Objective (RTO) & Recovery Point Objective (RPO)

| Application Tier | RTO Target | RPO Target | Backup Frequency | Retention |
|-----------------|------------|------------|------------------|-----------|
| Critical | < 1 hour | < 5 minutes | Every 5 minutes | 30 days |
| High Priority | < 4 hours | < 1 hour | Hourly | 14 days |
| Standard | < 8 hours | < 6 hours | Every 6 hours | 7 days |
| Low Priority | < 24 hours | < 1 day | Daily | 7 days |
| Development | < 48 hours | < 1 day | Daily | 3 days |

## Backup Scope Strategies

### 1. Full Cluster Backup

**Use case:** Complete disaster recovery, cluster migration

```bash
# Create full cluster backup
velero backup create full-cluster-$(date +%Y%m%d-%H%M%S) \
  --snapshot-volumes=true \
  --include-cluster-resources=true

# Exclude system namespaces
velero backup create full-cluster-$(date +%Y%m%d-%H%M%S) \
  --exclude-namespaces kube-system,kube-public,kube-node-lease,velero
```

**Scheduled full cluster backup:**

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: full-cluster-daily
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  template:
    excludedNamespaces:
    - kube-system
    - kube-public
    - kube-node-lease
    - velero
    includeClusterResources: true
    snapshotVolumes: true
    ttl: 720h  # 30 days
```

### 2. Namespace-Specific Backup

**Use case:** Application-specific backups, team isolation

```bash
# Backup single namespace
velero backup create production-backup \
  --include-namespaces production \
  --snapshot-volumes=true

# Backup multiple namespaces
velero backup create app-stack-backup \
  --include-namespaces frontend,backend,database \
  --snapshot-volumes=true
```

**Scheduled namespace backup:**

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: production-hourly
  namespace: velero
spec:
  schedule: "0 * * * *"  # Hourly
  template:
    includedNamespaces:
    - production
    snapshotVolumes: true
    ttl: 168h  # 7 days

    # Backup hooks for application consistency
    hooks:
      resources:
      - name: postgres-backup-hook
        includedNamespaces:
        - production
        labelSelector:
          matchLabels:
            app: postgresql
        pre:
        - exec:
            command:
            - /bin/bash
            - -c
            - "pg_dumpall -U postgres > /backup/dump.sql"
            container: postgresql
            timeout: 10m
```

### 3. Label-Based Backup

**Use case:** Backup specific resources across namespaces

```bash
# Backup all resources with specific label
velero backup create critical-apps \
  --selector tier=critical \
  --snapshot-volumes=true

# Backup stateful applications
velero backup create stateful-apps \
  --selector stateful=true \
  --snapshot-volumes=true
```

**Scheduled label-based backup:**

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: critical-apps-frequent
  namespace: velero
spec:
  schedule: "*/15 * * * *"  # Every 15 minutes
  template:
    labelSelector:
      matchLabels:
        tier: critical
    snapshotVolumes: true
    ttl: 72h  # 3 days
```

### 4. Resource-Specific Backup

**Use case:** Backup only specific Kubernetes resources

```bash
# Backup only PVCs and ConfigMaps
velero backup create data-config-backup \
  --include-resources pvc,configmap \
  --all-namespaces

# Exclude secrets
velero backup create app-no-secrets \
  --include-namespaces production \
  --exclude-resources secrets
```

## Backup Frequency Patterns

### Critical Applications - High Frequency

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: critical-every-5min
  namespace: velero
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  template:
    includedNamespaces:
    - critical-prod
    snapshotVolumes: true
    ttl: 48h  # 2 days (frequent backups = shorter retention)

    # Incremental backups for efficiency
    defaultVolumesToRestic: true  # Use restic for incremental
```

### Database Applications - Consistent Backups

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: database-consistent-backup
  namespace: velero
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  template:
    includedNamespaces:
    - database
    snapshotVolumes: true
    ttl: 720h  # 30 days

    hooks:
      resources:
      # PostgreSQL backup hook
      - name: postgres-pre-backup
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
            - |
              echo "Starting PostgreSQL backup..."
              PGPASSWORD=$POSTGRES_PASSWORD pg_dump \
                -U postgres \
                -h localhost \
                -d $POSTGRES_DB \
                --format=custom \
                --blobs \
                --verbose \
                --file=/var/lib/postgresql/backup/dump.backup
              echo "PostgreSQL backup completed"
            container: postgresql
            timeout: 30m
            onError: Fail
        post:
        - exec:
            command:
            - /bin/bash
            - -c
            - rm -f /var/lib/postgresql/backup/dump.backup
            container: postgresql

      # MySQL backup hook
      - name: mysql-pre-backup
        includedNamespaces:
        - database
        labelSelector:
          matchLabels:
            app: mysql
        pre:
        - exec:
            command:
            - /bin/bash
            - -c
            - |
              mysqldump \
                -u root \
                -p$MYSQL_ROOT_PASSWORD \
                --all-databases \
                --single-transaction \
                --quick \
                --lock-tables=false \
                > /var/lib/mysql/backup/dump.sql
            container: mysql
            timeout: 30m

      # MongoDB backup hook
      - name: mongodb-pre-backup
        includedNamespaces:
        - database
        labelSelector:
          matchLabels:
            app: mongodb
        pre:
        - exec:
            command:
            - /bin/bash
            - -c
            - |
              mongodump \
                --host=localhost:27017 \
                --username=$MONGO_INITDB_ROOT_USERNAME \
                --password=$MONGO_INITDB_ROOT_PASSWORD \
                --authenticationDatabase=admin \
                --out=/data/backup/dump
            container: mongodb
            timeout: 30m
```

### Multi-Tier Backup Strategy

```yaml
---
# Tier 1: Critical - Every 5 minutes
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: tier1-critical
  namespace: velero
spec:
  schedule: "*/5 * * * *"
  template:
    labelSelector:
      matchLabels:
        backup-tier: "1"
    snapshotVolumes: true
    ttl: 48h

---
# Tier 2: High Priority - Hourly
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: tier2-high-priority
  namespace: velero
spec:
  schedule: "0 * * * *"
  template:
    labelSelector:
      matchLabels:
        backup-tier: "2"
    snapshotVolumes: true
    ttl: 336h  # 14 days

---
# Tier 3: Standard - Every 6 hours
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: tier3-standard
  namespace: velero
spec:
  schedule: "0 */6 * * *"
  template:
    labelSelector:
      matchLabels:
        backup-tier: "3"
    snapshotVolumes: true
    ttl: 168h  # 7 days

---
# Tier 4: Low Priority - Daily
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: tier4-low-priority
  namespace: velero
spec:
  schedule: "0 3 * * *"  # 3 AM daily
  template:
    labelSelector:
      matchLabels:
        backup-tier: "4"
    snapshotVolumes: true
    ttl: 168h  # 7 days
```

## Multi-Region Backup Strategy

### Primary and Secondary Backup Locations

```yaml
---
# Primary backup location (same region as cluster)
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: primary-us-east-1
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-backups-us-east-1
    prefix: production-cluster
  config:
    region: us-east-1
    s3ForcePathStyle: "false"
  default: true

---
# Secondary backup location (different region for DR)
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: secondary-us-west-2
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-backups-us-west-2
    prefix: production-cluster
  config:
    region: us-west-2
    s3ForcePathStyle: "false"

---
# Backup to both locations
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
    snapshotVolumes: true
    storageLocation: primary-us-east-1
    ttl: 720h  # 30 days

---
# Copy to secondary location (daily)
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: secondary-region-backup
  namespace: velero
spec:
  schedule: "0 4 * * *"  # 4 AM daily
  template:
    includedNamespaces:
    - production
    snapshotVolumes: false  # Don't duplicate snapshots
    storageLocation: secondary-us-west-2
    ttl: 2160h  # 90 days
```

## Restore Procedures

### Full Cluster Restore

**Scenario:** Complete cluster failure, restore to new cluster

```bash
# 1. Install Velero on new cluster with same configuration
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups-us-east-1 \
  --backup-location-config region=us-east-1 \
  --secret-file ./credentials-velero

# 2. Wait for Velero to sync backups
velero backup get

# 3. Identify latest backup
LATEST_BACKUP=$(velero backup get --output json | \
  jq -r '.items | sort_by(.status.startTimestamp) | last | .metadata.name')
echo "Latest backup: $LATEST_BACKUP"

# 4. Restore entire cluster
velero restore create full-cluster-restore \
  --from-backup $LATEST_BACKUP \
  --wait

# 5. Verify restoration
kubectl get all --all-namespaces
velero restore describe full-cluster-restore
velero restore logs full-cluster-restore
```

### Namespace Restore

**Scenario:** Accidental namespace deletion or corruption

```bash
# Restore specific namespace
velero restore create prod-namespace-restore \
  --from-backup production-backup-20231120 \
  --include-namespaces production \
  --wait

# Restore to different namespace (testing)
velero restore create prod-test-restore \
  --from-backup production-backup-20231120 \
  --namespace-mappings production:production-test \
  --wait

# Restore without services (for data recovery only)
velero restore create data-only-restore \
  --from-backup production-backup-20231120 \
  --include-namespaces production \
  --exclude-resources services,ingresses \
  --wait
```

### Selective Resource Restore

**Scenario:** Restore specific resources (ConfigMaps, Secrets, PVCs)

```bash
# Restore only PVCs
velero restore create pvc-restore \
  --from-backup production-backup-20231120 \
  --include-resources pvc \
  --include-namespaces production

# Restore ConfigMaps and Secrets
velero restore create config-restore \
  --from-backup production-backup-20231120 \
  --include-resources configmap,secret \
  --include-namespaces production

# Restore specific resource by label
velero restore create app-restore \
  --from-backup production-backup-20231120 \
  --selector app=my-app
```

### Point-in-Time Recovery

**Scenario:** Rollback to specific point in time

```bash
# List backups with timestamps
velero backup get

# Restore from specific time
velero restore create pit-restore-20231120 \
  --from-backup production-backup-20231120-0200 \
  --include-namespaces production

# Verify restore time
kubectl get pods -n production -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.creationTimestamp}{"\n"}{end}'
```

### Cross-Cluster Migration

**Scenario:** Migrate workloads from one cluster to another

```bash
# Source cluster: Create backup
velero backup create migration-backup \
  --include-namespaces production,staging \
  --snapshot-volumes=true

# Wait for completion
velero backup describe migration-backup

# Target cluster: Install Velero with same backup location
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups-us-east-1 \
  --backup-location-config region=us-east-1 \
  --secret-file ./credentials-velero

# Wait for sync
velero backup get migration-backup

# Restore on target cluster
velero restore create migration-restore \
  --from-backup migration-backup \
  --wait

# Verify migration
kubectl get all -n production
kubectl get all -n staging
```

## Backup Validation and Testing

### Automated Backup Verification

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-verification
  namespace: velero
spec:
  schedule: "0 6 * * *"  # Daily at 6 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: velero
          containers:
          - name: verify-backup
            image: velero/velero:v1.12.0
            command:
            - /bin/sh
            - -c
            - |
              # Get latest backup
              LATEST=$(velero backup get --output json | \
                jq -r '.items | sort_by(.status.startTimestamp) | last | .metadata.name')

              # Check backup status
              STATUS=$(velero backup describe $LATEST --details | grep "Phase:" | awk '{print $2}')

              if [ "$STATUS" != "Completed" ]; then
                echo "ERROR: Latest backup $LATEST failed with status $STATUS"
                exit 1
              fi

              # Verify backup size
              SIZE=$(velero backup describe $LATEST | grep "Total items" | awk '{print $4}')
              if [ "$SIZE" -lt 10 ]; then
                echo "WARNING: Backup $LATEST has only $SIZE items"
              fi

              echo "Backup verification successful: $LATEST"
          restartPolicy: OnFailure
```

### Restore Testing

```bash
# Create test namespace
kubectl create namespace restore-test

# Perform test restore
velero restore create restore-test-$(date +%Y%m%d) \
  --from-backup production-backup-latest \
  --namespace-mappings production:restore-test \
  --wait

# Validate restored resources
kubectl get all -n restore-test

# Run application tests
kubectl run test-pod -n restore-test --image=curlimages/curl:latest -- \
  curl http://app-service.restore-test.svc.cluster.local

# Cleanup
kubectl delete namespace restore-test
velero restore delete restore-test-$(date +%Y%m%d)
```

## Backup Monitoring and Alerting

### Prometheus Alerts for Velero

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: velero-alerts
  namespace: monitoring
spec:
  groups:
  - name: velero.backups
    interval: 5m
    rules:
    # Backup failure alert
    - alert: VeleroBackupFailed
      expr: |
        velero_backup_failure_total > 0
      for: 5m
      labels:
        severity: critical
        component: velero
      annotations:
        summary: "Velero backup failed"
        description: "Velero backup {{ $labels.schedule }} failed in the last 5 minutes."
        runbook_url: "https://runbooks.example.com/velero-backup-failed"

    # No recent backups
    - alert: VeleroBackupTooOld
      expr: |
        time() - velero_backup_last_successful_timestamp{schedule!=""} > 7200
      for: 10m
      labels:
        severity: warning
        component: velero
      annotations:
        summary: "Velero backup is too old"
        description: "No successful backup for schedule {{ $labels.schedule }} in the last 2 hours."

    # Backup duration too long
    - alert: VeleroBackupDurationHigh
      expr: |
        velero_backup_duration_seconds > 3600
      for: 5m
      labels:
        severity: warning
        component: velero
      annotations:
        summary: "Velero backup duration is high"
        description: "Backup {{ $labels.schedule }} took {{ $value }}s to complete."

    # Backup size anomaly
    - alert: VeleroBackupSizeAnomaly
      expr: |
        abs(
          velero_backup_total_items -
          avg_over_time(velero_backup_total_items{schedule!=""}[7d])
        ) / avg_over_time(velero_backup_total_items{schedule!=""}[7d]) > 0.5
      for: 10m
      labels:
        severity: warning
        component: velero
      annotations:
        summary: "Velero backup size anomaly detected"
        description: "Backup {{ $labels.schedule }} size differs by >50% from 7-day average."
```

## Backup Retention Policies

### Automated Backup Cleanup

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: velero-backup-cleanup
  namespace: velero
spec:
  schedule: "0 0 * * 0"  # Weekly on Sunday
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: velero
          containers:
          - name: cleanup
            image: velero/velero:v1.12.0
            command:
            - /bin/sh
            - -c
            - |
              # Delete backups older than 30 days
              velero backup get --output json | \
                jq -r '.items[] | select(.status.expiration < now) | .metadata.name' | \
                xargs -I {} velero backup delete {} --confirm

              # Delete failed backups older than 7 days
              velero backup get --output json | \
                jq -r '.items[] |
                  select(.status.phase == "Failed") |
                  select(.status.startTimestamp < (now - 604800)) |
                  .metadata.name' | \
                xargs -I {} velero backup delete {} --confirm
          restartPolicy: OnFailure
```

### Tiered Retention Strategy

```yaml
---
# Critical: 30 days full retention
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: critical-retention-30d
spec:
  schedule: "*/5 * * * *"
  template:
    labelSelector:
      matchLabels:
        backup-tier: "1"
    ttl: 720h  # 30 days

---
# Standard: 14 days full retention
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: standard-retention-14d
spec:
  schedule: "0 * * * *"
  template:
    labelSelector:
      matchLabels:
        backup-tier: "2"
    ttl: 336h  # 14 days

---
# Archive: Monthly backups for 1 year
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: monthly-archive
spec:
  schedule: "0 0 1 * *"  # First day of month
  template:
    includedNamespaces:
    - production
    snapshotVolumes: true
    ttl: 8760h  # 365 days
```

## Best Practices Summary

### Backup Strategy Checklist

- [ ] Implement 3-2-1 backup rule
- [ ] Define RTO/RPO for each application tier
- [ ] Use multiple backup locations (cross-region)
- [ ] Enable volume snapshots for stateful workloads
- [ ] Implement backup hooks for database consistency
- [ ] Set appropriate TTL based on retention requirements
- [ ] Exclude unnecessary resources (events, temporary data)
- [ ] Use label selectors for flexible backup policies
- [ ] Encrypt backup storage buckets
- [ ] Monitor backup success/failure with alerts
- [ ] Test restore procedures regularly (monthly minimum)
- [ ] Document restore procedures and runbooks
- [ ] Implement automated backup verification
- [ ] Use separate backup storage accounts/subscriptions
- [ ] Version control Velero configurations

### Common Pitfalls to Avoid

1. **Single backup location** - Always use cross-region replication
2. **No restore testing** - Test restores regularly, not just during disasters
3. **Ignoring backup hooks** - Databases need application-consistent backups
4. **Excessive retention** - Balance retention with storage costs
5. **Backing up everything** - Exclude non-critical resources to reduce costs
6. **No monitoring** - Always monitor backup success and failures
7. **Hardcoded credentials** - Use IAM roles or managed identities
8. **Ignoring volume snapshots** - Enable for stateful workloads
9. **No documentation** - Document restore procedures and test them
10. **One backup schedule** - Different apps need different backup frequencies
