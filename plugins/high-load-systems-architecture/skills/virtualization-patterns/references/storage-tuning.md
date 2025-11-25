# Тюнинг Storage для VM
- Форматы: raw (perf) vs qcow2 (гибкость/снапшоты); кеш: writethrough (безопасно), writeback (быстро), none (низкая латентность на быстрых дисках).
- IO scheduler: `none`/`mq-deadline` для NVMe/SSD; `bfq` для справедливости.
- IOTune: лимиты IOPS/MBps на диск/тенант; избегать noisy neighbor.
- Диск привязка: NUMA-aware, отдельные устройства для журналов, discard/trim.
- Метрики: await, svctm, iops, queue depth, cache hit/miss, dirty pages.
