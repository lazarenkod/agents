# Оптимизация сетевой латентности
- Выбрать быстрые пути: SR-IOV/vDPA, vhost-net (kernel), vhost-user (dpdk) > virtio > emulated.
- IRQ/NUMA: pin VF/queues к локальным ядрам, уменьшить cross-NUMA.
- Offloads: включить TX/RX checksum/TSO/GSO где возможно; отключить если вызывает jitter.
- Coalescing: уменьшить `rx-usecs` для latency, следить за CPU.
- Тесты: ping/mtr (p99), sockperf/netperf latency, jitter; chaos: нагрузка на соседние VM.
