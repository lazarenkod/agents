# Миграция на cgroups v2 (unified)
- Требования: системд ≥ 226, ядро ≥ 5.x, включить `systemd.unified_cgroup_hierarchy=1` или `systemd.legacy_systemd_cgroup_controller=no`.
- Отличия: единый иерарх, новые контроллеры (`cpu.max`, `memory.high/max`, `io.max`), PSI per cgroup.
- План: инвентаризация сервисов, совместимость контейнеров, тест на стейдже, dual-mount период, обновление мониторинга.
- Риски: несовместимость со старыми докер/CRI, отсутствие некоторых v1 контроллеров.
- Проверка: `cat /sys/fs/cgroup/cgroup.controllers`, `systemd-cgls`, psi файлы.
