# SR-IOV: быстрый старт
- Включить IOMMU (`intel_iommu=on iommu=pt`), проверить `sriov_numvfs`.
- Создать VF: `echo 8 > /sys/class/net/eth0/device/sriov_numvfs`.
- Привязать VF к `vfio-pci`, добавить в VM `<hostdev>`; учесть NUMA.
- Ограничения: live migration обычно недоступна, планируйте fallback virtio.
- Тесты: iperf3/latency, проверки VF isolation, мониторинг drops/errs.
