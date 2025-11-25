# SPDK integration
- Userspace NVMe/TCP/iSCSI, минимизация syscalls/interrupts.
- Требования: hugepages, `vfio-pci` для NVMe, DPDK mempool.
- Пример: `spdk_tgt` + vhost-blk для VM: экспорт блочного девайса, в VM использовать vhost-blk (virtio-scsi).
- Плюсы: низкая латентность, высокий IOPS; минусы: сложность управления, выделенные ядра.
- Метрики: latency p99, IOPS, CPU utilization на poller threads; pin pollers к NUMA с NVMe.
