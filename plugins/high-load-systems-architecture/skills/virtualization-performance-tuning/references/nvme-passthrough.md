# NVMe passthrough
- Требует свободный NVMe девайс; привязать к `vfio-pci`, убедиться в NUMA локальности.
- VM: `<hostdev>` PCI device, cache=none, io=linux; внутри гостя обычный NVMe.
- Преимущества: почти native latency/IOPS, минусы: нет live migration, управление диском в госте.
- Тесты: fio (randread/write, 4k/128k), tail latency, queue depth.
- Мониторинг: SMART/health, PCIe AER errors, температура.
