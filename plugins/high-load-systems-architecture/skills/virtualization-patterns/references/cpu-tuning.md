# Тюнинг CPU для VM
- CPU mode: `host-passthrough` для perf, `host-model` для миграций, custom для совместимости.
- Pinning: vCPU→pCPU, NUMA alignment, избегать SMT siblings для low latency.
- Overcommit: правила 1.5–2x для non-critical; для базы/RT — 1:1.
- Features: включить `invtsc`, `pdpe1gb`, отключить `hypervisor` флаг если нужна маскировка.
- Метрики: ready/steal, runqueue, host CPU util, migrations; алерты на st%/p99 latency.
