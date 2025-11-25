# vGPU (виртуализация GPU)
- Типы: NVIDIA vGPU (лицензии), AMD MxGPU, Intel GVT-g.
- Требования: совместимые драйверы, лицензирование, профили vGPU (кол-во vCPU/FB).
- VM конфиг: `<hostdev mode='subsystem' type='mdev' managed='no' model='vfio-pci'>…</hostdev>`.
- Ограничения: perf < passthrough, миграция зависит от вендора, планирование профилей.
- Тесты: share fairness, latency/throughput ML/VDI, изоляция между тенантами.
