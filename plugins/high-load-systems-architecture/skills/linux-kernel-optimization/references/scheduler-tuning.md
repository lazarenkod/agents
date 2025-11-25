# Тюнинг планировщика (CFS/RT)
- `sched_latency_ns`, `sched_min_granularity_ns`, `sched_wakeup_granularity_ns` — баланс fairness vs latency; увеличивайте для throughput, уменьшайте для low-latency.
- `kernel.sched_migration_cost_ns` — меньше миграций → лучше кэш, хуже баланс.
- `kernel.numa_balancing=0/1` — отключить для детерминизма, включить при динамических нагрузках.
- RT: `sched_rt_runtime_us`, `sched_rt_period_us`, irqbalance тюн; не отключайте throttling без контроля.
- Проверка: `schedstat`, runqueue length, context switches; A/B с нагрузочными тестами.
