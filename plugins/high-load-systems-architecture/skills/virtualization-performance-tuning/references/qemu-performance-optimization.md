# QEMU performance
- Запуск: `-cpu host`, `-smp sockets=1,cores=N,threads=1`, `-machine accel=kvm`.
- IO: `-drive cache=none,aio=native`, `-object iothread`, `-device virtio-blk-pci,iothread=ioth0`.
- Сеть: `-netdev tap,script=no,queues=4 -device virtio-net-pci,mq=on,vectors=10`.
- Таймеры: `-rtc base=utc,clock=host,driftfix=slew`, `-no-hpet` если нужно.
- Трэйсинг: `-trace events=file`, `-d guest_errors` для дебага.
