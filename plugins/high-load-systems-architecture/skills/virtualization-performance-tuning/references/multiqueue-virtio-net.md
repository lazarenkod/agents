# Multi-queue virtio-net
- Включение: `<driver queues='N'/>`, `ethtool -L eth0 combined N`, RSS на госте.
- Требования: vhost-user/kerne-level поддержка, pin очередей к ядрам.
- Плюсы: масштаб pps, минусы: больше IRQ/контекстных переключений.
- Тесты: iperf3 (многопоточность), pktgen, проверка распределения очередей.
- Мониторинг: drops per queue, CPU per queue, IRQ баланс.
