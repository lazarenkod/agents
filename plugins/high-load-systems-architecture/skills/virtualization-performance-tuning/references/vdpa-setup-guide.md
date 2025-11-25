# vDPA настройка
- Поддерживаемые NIC: Mellanox/Broadcom с vDPA; ядро ≥5.7.
- Шаги: `modprobe vdpa vhost_vdpa`, `vdpa dev add name vdpa0 mgmtdev pci/0000:af:00.0`.
- Libvirt: `<interface type='vdpa'><source dev='/dev/vhost-vdpa-0'/><model type='virtio'/></interface>`.
- Преимущества: hw data path + совместимость virtio + миграция (зависит от backend).
- Метрики: pps/latency, vhost stats, миграция downtime, VF errors.
