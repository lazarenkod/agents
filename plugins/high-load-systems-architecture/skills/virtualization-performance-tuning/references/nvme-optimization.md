# NVMe оптимизация
- Очереди: увеличить `nr_requests`, `queue_depth` в госте; multi-queue в хосте.
- IRQ affinity: pin NVMe IRQ к локальным ядрам, irqbalance настроить.
- Scheduler: `none` или `mq-deadline`, отключить merge для NVMe, включить `noatime`.
- Мониторинг: `nvme smart-log`, latency per queue, AER errors, temp.
- Тесты: fio randread/write, смешанный профиль, p99/p99.9, queue depth, verify NUMA локальность.
