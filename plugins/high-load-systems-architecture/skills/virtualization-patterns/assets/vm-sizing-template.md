# VM Sizing Template

## Контекст
- Сервис/нагрузка: …
- SLO/SLA: latency p95/p99, throughput, uptime.
- Ограничения: лицензии/стоимость, NUMA/CPU модель, миграции/HA.

## Нагрузка и профиль
- Тип (web/api/db/cache/batch), тредов, concurrency, IO/NET профиль.
- Пики/суточные паттерны, рост.

## Рекомендация
| Опция | vCPU | RAM | Диск | Сеть | Особенности | Риски/стоимость |
|---|---|---|---|---|---|---|
| Low-latency | | | | | pinning, hugepages | |
| Balanced | | | | | | |
| Throughput | | | | | multiqueue, overcommit | |

## Тюнинг
- CPU: host-passthrough/модель, pinning/NUMA, SMT политика.
- Память: hugepages/balloon, memtune, swap policy.
- Storage: raw/qcow2, cache mode, io limits.
- Network: virtio vs SR-IOV/vDPA, queues, bandwidth.

## Метрики и тесты
- Met: CPU util, ready/steal, latency p99, IOPS/throughput, RTT/retrans, migration time.
- Тесты: fio, iperf/netperf, cyclictest, failover/migration.

## TODO
- Владельцы, сроки, open questions, rollback/канарейки.
