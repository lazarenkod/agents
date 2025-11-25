# Checklist профилирования ядра/системы
- Цель и SLO (latency/throughput) сформулированы.
- Сбор базовых метрик: CPU/IO/NET/PSI, runqueue, irq load, THP/NUMA stats.
- Инструменты выбраны: perf/bcc/bpftrace, ftrace, sar/iostat/ss/pcpu.
- Наборы тестов: fio (IO), iperf/netperf (NET), cyclictest (RT), stress-ng (pressure).
- План выборки: длительность ≥10 мин, сэмплировать p99/p99.9.
- Хранение артефактов: perf.data, flamegraph.svg, sysctl diff, dmesg.
- Rollback/безопасность: параметры, которые откатить после тестов.
