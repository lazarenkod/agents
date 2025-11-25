# PCI passthrough: best practices
- Включить IOMMU, убедиться в чистых IOMMU группах; использовать `vfio-pci`.
- NUMA: девайс и vCPU/мемория на одном узле; pin IRQ.
- Безопасность: отключить ACS override где возможно; ограничить DMA (iommu=pt при необходимости).
- Миграции: план fallback виртуальных устройств; предусмотреть drain трафика перед detach.
- Диагностика: `lspci -vv`, `dmesg | grep -i vfio`, проверка ошибок AER.
