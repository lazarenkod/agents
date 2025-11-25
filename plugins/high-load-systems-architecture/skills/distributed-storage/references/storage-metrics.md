# Метрики и алерты для распределённого хранилища

## 1) Основные SLI
- Latency p50/p95/p99 (read/write, control path), tail spikes.
- Throughput/IOPS, queue depth, parallel ops.
- Error rate: 4xx/5xx, timeouts, throttling.
- Replication lag, scrub/repair duration, rebalance ETA.
- Durability: несоответствие/коррупция, количество inconsistent PG/objects.

## 2) Использование ресурсов
- Disk: util %, await, svctm, fs fragmentation.
- Network: bw usage, retransmits, drops, RTT межузловой.
- CPU/Memory: OSD/ RGW процессы, cache hit/miss, allocator fragmentation.
- Space: used/avail, nearfull/full, growth rate, hot/cold distribution.

## 3) Пулы/кластер
- PG states: active+clean vs degraded/inconsistent/stuck.
- Balancer/reshard progress, amount moved GB/h.
- MDS (CephFS): cache hit, caps per client, req/s.
- RGW: req/s, bucket ops, shard ops, 5xx/4xx, latency.

## 4) Алерты (SLO-aware)
- p99 latency > бюджет X мин.
- Error rate/timeout > Y%.
- Replication lag > Z сек/минут, rebalance ETA > окно.
- PG degraded/inconsistent > 0, stuck > 0.
- Nearfull/full ratio превышен; рост > план; scrub failures.
- DR: cross-region lag > бюджет, replication suspended.

## 5) Дашборды
- RED/USE: Rate, Errors, Duration + Utilization/Saturation/Errors.
- Heatmap latency per shard/PG/bucket.
- Capacity forecast: 30/60/90 дней.
- Recovery/backfill speed, client throttling.

## 6) Тесты и верификация метрик
- Нагрузочные тесты с сэмплингом p99.9 и гистограмм.
- Chaos: отключение OSD/AZ, измерение деградации и восстановления.
- Консистентность: long-tail проверки после failover/reshard.
