# KSM (Kernel Samepage Merging)
- Цель: экономия памяти путём дедупликации страниц; полезно для множества одинаковых VM.
- Настройки: `/sys/kernel/mm/ksm/run`, `sleep_millisecs`, `pages_to_scan`.
- Риски: накладные расходы CPU, потенциальные side-channel; отключать для чувствительных данных.
- Мониторинг: `pages_shared`, `pages_sharing`, CPU load; алерты на рост CPU от ksmd.
- Используйте на хостах с гомогенными VM и не критичной латентностью.
