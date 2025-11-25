# DPDK: быстрая настройка
- Требования: поддерживаемая NIC, hugepages, отключить irqbalance/питч offload конфликты.
- Шаги: установить DPDK, выделить hugepages (`echo 1024 > /sys/.../nr_hugepages`), привязать VF/PF к `vfio-pci` (`dpdk-devbind.py`).
- Запуск теста: `./dpdk-app --vdev=net_pcap0,iface=eth0 --lcores 0-3 --proc-type=primary`.
- Метрики: pps, latency, packet loss; следить за NUMA (lcores и память на одном узле).
- Риски: loss SR-IOV функций, сложность управления; держите fallback конфиг.
