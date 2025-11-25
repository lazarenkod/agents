# Live migration: чеклист
- Подготовка: одинаковые версии libvirt/QEMU, совместимые CPU модели, общий сторидж или `--copy-storage-all`.
- Параметры: `migrate-setmaxdowntime`, `--postcopy` (если допустимо), компрессия/xbzrle.
- Сеть: MTU/доступность между хостами, bandwidth caps, firewall.
- Валидация: p99 latency, packet loss, дисковая консистентность, guest agent жив.
- Риски: dirty pages при write-heavy, зависание из-за bandwidth, несовместимость устройств (GPU/SR-IOV).
