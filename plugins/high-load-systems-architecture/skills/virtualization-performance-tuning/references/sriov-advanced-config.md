# SR-IOV: продвинутые настройки
- VF driver: `vfio-pci` для passthrough; убедитесь в NUMA соответствии.
- Безопасность: VLAN/VF trust, анти-спуф, rate-limit VF.
- Interrupts: pin VF IRQ к локальным ядрам, включить RSS если поддерживается.
- Live migration: планировать fallback на virtio; подготовить detach/reattach скрипты.
- Мониторинг: VF errors/drops, pps, latency, PCI errors.
