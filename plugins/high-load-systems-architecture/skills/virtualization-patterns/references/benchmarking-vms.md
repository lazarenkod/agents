# Бенчмаркинг VM
- Сценарии: fio (randread/write, mixed), iperf3/netperf (pps/throughput), cyclictest (latency), sysbench/pgbench (CPU/DB).
- Метод: baseline → вариант A/B → повторяемость (3 прогона), фиксировать конфиги/NUMA/pinning.
- Метрики: p99/p99.9 latency, throughput, CPU ready/steal, jitter, migrations, host load.
- Артефакты: команды запуска, версии, графики, табличка результатов (см. asset benchmark-results.md).
- Guardrails: прогрев, стабильность температуры/частоты, нет фоновых задач.
