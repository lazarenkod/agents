# I/O threads (QEMU/libvirt)
- Включайте отдельные iothreads для дисков с высоким IOPS: `<iothreads>2</iothreads>` + `<disk ... iothread='1'>`.
- Разносите iothreads по CPU/NUMA (iothreadpin) для снижения contention.
- Используйте `io='native' cache='none'` на быстрых дисках, `writeback` если важна скорость с риском.
- Мониторинг: `virsh domstats --iothread`, `iostat`, host CPU per iothread.
- Риски: лишние контексты при малом IOPS, нарушенная NUMA локальность.
