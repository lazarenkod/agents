# Hugepages: подбор размера
- Выбор: 2MB для гибкости, 1GB для минимальной TLB нагрузки (но сложнее выделить).
- Расчёт: (RAM гостя + резерв под QEMU/IO/cache) округлить вверх; плюс 10–20% запас.
- NUMA: выделять по узлам, `vm.nr_hugepages` + `vm.hugetlb_shm_group` для qemu.
- Проверка: `/proc/meminfo | grep Huge`, `cat /proc/self/maps | grep huge`.
- Риски: фрагментация, сложности с миграцией/overcommit, невозможность подкачки.
