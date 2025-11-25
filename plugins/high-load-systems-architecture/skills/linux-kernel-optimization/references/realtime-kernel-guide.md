# Реалтай ядро и тюнинг
- Используйте PREEMPT_RT ядра для жёстких требований; проверка `uname -a | grep PREEMPT_RT`.
- Параметры: отключить `intel_pstate` (performance governor), `isolcpus/nohz_full/rcu_nocbs`, pin IRQ на housekeeping ядра.
- cyclictest/hwlatdetect для измерения; цели: max latency, не средние.
- Планировщики: SCHED_FIFO/DEADLINE для критичных тредов, ограничить RT throttling разумно.
- Проверка: `trace-cmd record -e irqoff` для поиска длительных отключений прерываний.
