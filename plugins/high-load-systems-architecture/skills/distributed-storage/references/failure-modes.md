# Failure Modes: распределённое хранилище

## 1) Узловые/диск
- OSD down/flapping → detect: `ceph osd tree`, `osd perf`; mitigate: restart, reweight, replace disk, throttle recovery.
- Disk latency/jitter → detect: iostat/latency; mitigate: drain/rebalance, NVMe journal, QoS лимиты.
- Journal/DB corruption → detect: bluestore errors; mitigate: recreate with backup, scrub/repair, rehydrate from replicas.

## 2) Сеть
- Partition между AZ/мон → detect: quorum loss, mon down; mitigate: временный мон в здоровой AZ, туннель, настроить public/cluster сеть.
- Packet loss/RTT spike → detect: mtr/iperf, OSD heartbeat; mitigate: reroute, NIC failover, QoS.
- MTU/fragmentation → detect: drops, PMTU errors; mitigate: унифицировать MTU, проверить jumbo frames.

## 3) Балансировка/PG
- Hot PG/shard → detect: perf skew; mitigate: split/reshard, reweight, cache tier, throttle clients.
- Too many/few PG → detect: mem overhead/uneven dist; mitigate: recalibrate PG num, staged increase.
- Stuck PG (stale/inactive/unclean) → detect: `pg dump_stuck`; mitigate: fix down OSD, force create, repair.

## 4) Репликация/EC
- Replication lag → detect: health detail; mitigate: bump backfills, isolate noisy clients, add bandwidth.
- Backfill starvation → detect: recovery stalled; mitigate: tune `osd_max_backfills`, dedicated window.
- EC decode storms → detect: CPU spikes; mitigate: cache hot objects, place parity on faster media.

## 5) Контроль/конфигурация
- Drift/несогласованные конфиги → detect: config audit; mitigate: IaC, template enforcement.
- Неправильные crush rules (AZ awareness) → detect: uneven failure domains; mitigate: fix rules, simulate placement.
- ACL/тенант misconfig → detect: access errors; mitigate: policy audit, staged rollout.

## 6) DR/replication geo
- Cross-region lag/outage → detect: replication metrics, health; mitigate: promote standby, rate-limit writes, freeze risky ops.
- Split-brain между регионами → detect: divergent versions; mitigate: authoritative region, reconcile logs, conflict resolution.

## 7) Операционные ошибки
- Aggressive rebalance в пике → impact latency/errors; mitigate: guardrails, approvals, throttle.
- Массовое удаление/TTL → detect: delete rate spike; mitigate: soft-delete, bucket policy, backups.

## 8) Тестирование отказов
- Регулярные DR/chaos игры: OSD down, AZ down, mon quorum loss, lag injection.
- Критерии успеха: RTO/RPO, latency/error budget, отсутствие silent data loss.
