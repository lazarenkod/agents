# GPU passthrough
- IOMMU включён, GPU отвязан от host драйвера (`vfio-pci`).
- VM XML: `<hostdev mode='subsystem' type='pci' managed='yes'>…</hostdev>`, CPU `host-passthrough`, Hyper-V `vendor_id` скрыт для NVIDIA (Error 43).
- Дополнительно: audio функция GPU тоже передаётся, включить rombar при необходимости.
- Риски: миграция недоступна, энергопотребление/тепло, лицензии.
- Тесты: `nvidia-smi`, cuda samples, графика/latency при нагрузке.
