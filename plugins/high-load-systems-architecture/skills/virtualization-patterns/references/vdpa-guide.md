# vDPA: установка и тюнинг
- Требования: NIC с vDPA, ядро ≥5.7, модули `vdpa`, `vhost_vdpa`.
- Создание устройства: `vdpa dev add name vdpa0 mgmtdev pci/0000:03:00.0`.
- VM: `<interface type='vdpa'><source dev='/dev/vhost-vdpa-0'/><model type='virtio'/></interface>`.
- Преимущества: почти SR-IOV производительность + миграция через vhost.
- Проверки: pps/latency, поддержка live migration, NUMA местоположение.
