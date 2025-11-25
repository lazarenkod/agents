# perf: анализ vCPU задержек
- `perf kvm stat live`: VM-exit причины, TLB flush, io wait.
- `perf sched record -- sleep 10` + `perf sched latency`: задержки планировщика vCPU.
- `perf record -e 'kvm:*' -a -g -- sleep 30`: профилирование VM-exit, построить flamegraph.
- Ключевые метрики: vm-entry/exit count, avg exit cost, runqueue latency, irq time.
- Использование: найти частые VM-exit (ioapic, ept misconfig), скорректировать pinning/irq affinity.
