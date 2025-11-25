# GPU passthrough: оптимизация
- CPU mode `host-passthrough`, IOMMU включен, GPU и аудио-функции привязаны к `vfio-pci`.
- Запрещать power management в госте, фиксировать clocks (nvidia-smi -lgc) если допустимо.
- Изоляция: отключить первичный GPU хоста, использовать dummy HDMI для headless.
- Метрики: p99 latency графики/рендера, GPU utilization, PCIe errors, термопрофиль.
- Риски: миграция недоступна, лицензии, обновления драйверов требуют окна.
