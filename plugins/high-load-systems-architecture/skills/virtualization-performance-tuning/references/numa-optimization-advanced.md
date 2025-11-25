# NUMA: продвинутая оптимизация
- Топология: pin vCPU и память на один узел; избегать cross-node IO/NIC.
- Libvirt: `<numatune>` + `<cputune>` + hugepages per node.
- IRQ: affinity VF/NVMe к локальным ядрам, `irqbalance --ban` изолированных ядер.
- Автоматизация: `numactl --hardware`, `hwloc`, скрипты пиннинга под лейблы.
- Метрики: numa_miss, remote memory %, latency, p99/ps99.9.
