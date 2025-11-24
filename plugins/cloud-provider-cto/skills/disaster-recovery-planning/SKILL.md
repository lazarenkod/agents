---
name: disaster-recovery-planning
description: Планирование disaster recovery для облачных платформ. Use when designing DR strategy, calculating RPO/RTO, implementing backup solutions, or planning failover procedures.
---

# Disaster Recovery Planning

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/cloud-provider-cto/skills/disaster-recovery-planning/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: цель/контекст → риски/критичные сервисы → RTO/RPO/стратегии → план/тесты/алерты → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Диагностика (1–2 ч):** критичные сервисы/данные, BIA, RTO/RPO требования, текущие меры/брешь, регуляторика. Черновой бриф + risk log.
2) **Дизайн (2–4 ч):** стратегии (pilot light/warm/hot, multi-AZ/region), данные (backup/snap/replication), runbooks, тест-план, метрики/алерты, коммуникации. Таблицы сервисов/стратегий/владельцев.
3) **Верификация (1–2 ч):** провести/запланировать тесты, go/no-go, контрольные точки, обновить TODO/логи/изменения.

## Когда использовать

- Разработка DR стратегии
- Расчет RPO/RTO requirements
- Проектирование backup solutions
- Планирование failover процедур
- DR testing и validation

## DR Strategies

### 4 Стратегии (по стоимости)

**1. Backup & Restore (Lowest cost)**
```
RPO: Hours, RTO: 24+ hours
Cost: ~1-2% производства

Architecture:
[Production] → [Daily Snapshots] → [S3 Glacier]
                                  → [Cross-Region Replication]

Recovery: Restore from backup на новую инфраструктуру
```

**2. Pilot Light (Low cost)**
```
RPO: Minutes, RTO: Hours
Cost: ~10% производства

Architecture:
Production:
[Web Tier] → [App Tier] → [DB Primary (Multi-AZ)]
                             ↓
DR Region:                [DB Replica (stopped)]
                          [AMIs ready]
                          [Scripts для launch]

Recovery: Start instances, switch DNS
```

**3. Warm Standby (Medium cost)**
```
RPO: Seconds, RTO: Minutes
Cost: ~50% производства

Architecture:
Production: Full stack running
DR Region: Reduced capacity running (20-50%)

Recovery: Auto-scale DR, switch traffic
```

**4. Multi-Site Active-Active (Highest cost)**
```
RPO: 0, RTO: Seconds (automatic)
Cost: ~200% производства

Architecture:
Region A: 50% capacity, serving traffic
Region B: 50% capacity, serving traffic
Global Load Balancer distributes

Recovery: Automatic (no action needed)
```

## RPO/RTO Calculation

```python
# Business Impact Analysis
services = {
    'payment_processing': {
        'revenue_per_hour': 100000,  # $100K/hour
        'max_acceptable_downtime': '5 minutes',
        'rpo': '0',  # No data loss acceptable
        'rto': '5 minutes',
        'dr_strategy': 'active-active'
    },
    'customer_portal': {
        'revenue_per_hour': 10000,
        'max_acceptable_downtime': '1 hour',
        'rpo': '15 minutes',
        'rto': '1 hour',
        'dr_strategy': 'warm_standby'
    },
    'reporting': {
        'revenue_per_hour': 0,  # Not revenue-generating
        'max_acceptable_downtime': '24 hours',
        'rpo': '24 hours',
        'rto': '24 hours',
        'dr_strategy': 'backup_restore'
    }
}
```

## Multi-Region Failover

### Database Replication

```python
# Aurora Global Database (cross-region)
resource "aws_rds_global_cluster" "main" {
  global_cluster_identifier = "global-db"
  engine = "aurora-postgresql"
  engine_version = "13.7"
  database_name = "prod"
}

# Primary cluster (us-east-1)
resource "aws_rds_cluster" "primary" {
  provider = aws.us_east_1

  cluster_identifier = "primary-cluster"
  global_cluster_identifier = aws_rds_global_cluster.main.id

  engine = "aurora-postgresql"
  engine_version = "13.7"

  master_username = "admin"
  master_password = var.db_password

  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
}

# Secondary cluster (eu-west-1)
resource "aws_rds_cluster" "secondary" {
  provider = aws.eu_west_1

  cluster_identifier = "secondary-cluster"
  global_cluster_identifier = aws_rds_global_cluster.main.id

  engine = "aurora-postgresql"
  engine_version = "13.7"

  # Replica lag: < 1 second typically
}
```

**Failover Process**:
```python
def failover_to_dr_region():
    """Promote secondary DB to primary"""

    print("1. Stop writes to primary")
    set_primary_read_only()

    print("2. Wait для replication lag = 0")
    wait_for_replication()

    print("3. Promote secondary")
    rds.modify_current_db_cluster_primary(
        GlobalClusterIdentifier='global-db',
        TargetDbClusterIdentifier='secondary-cluster'
    )

    print("4. Update DNS")
    route53.change_resource_record_sets(
        HostedZoneId='Z123',
        ChangeBatch={
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'db.example.com',
                    'Type': 'CNAME',
                    'TTL': 60,
                    'ResourceRecords': [
                        {'Value': 'secondary-cluster.eu-west-1.rds.amazonaws.com'}
                    ]
                }
            }]
        }
    )

    print("5. Resume writes")
    set_secondary_read_write()

    print("Failover complete!")
```

## Testing DR Plans

```python
# DR Drill Runbook
class DRDrill:
    def __init__(self, service):
        self.service = service
        self.results = []

    def execute_drill(self):
        """Run quarterly DR drill"""

        self.results.append(self.test_backup_restore())
        self.results.append(self.test_failover())
        self.results.append(self.test_recovery_time())
        self.results.append(self.test_data_integrity())

        self.generate_report()

    def test_backup_restore(self):
        """Verify backups are restorable"""
        start = time.time()

        # Restore latest backup to test environment
        snapshot = self.get_latest_snapshot()
        restored_db = self.restore_snapshot(snapshot)

        # Validate data
        assert self.validate_data(restored_db)

        duration = time.time() - start

        return {
            'test': 'backup_restore',
            'passed': True,
            'duration': duration,
            'rpo_achieved': snapshot.age
        }

    def test_failover(self):
        """Test failover procedure"""
        start = time.time()

        # Trigger failover
        self.initiate_failover()

        # Wait для completion
        self.wait_for_healthy_state()

        duration = time.time() - start

        return {
            'test': 'failover',
            'passed': True,
            'duration': duration,
            'rto_achieved': duration
        }
```

---

**Все DR plans сохраняются в Markdown на русском языке.**
