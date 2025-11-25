# virsh: основные команды
- Инфо: `virsh list --all`, `virsh dominfo NAME`, `virsh vcpuinfo`, `virsh dommemstat`.
- Управление: `virsh start/stop/suspend/resume`, `virsh destroy`, `virsh undefine`.
- Ресурсы: `virsh setvcpus NAME N --live`, `virsh setmem NAME 8G --live`, `virsh vcpupin`.
- Диски/сеть: `virsh domblklist`, `virsh domifstat`, attach/detach devices.
- Миграция: `virsh migrate --live NAME qemu+ssh://host/system`, `migrate-setmaxdowntime`.
