# DPDK vhost-user
- Use-case: быстрая передача пакетов между VM/контейнерами через userspace switch (OVS-DPDK).
- Настройка: включить `vhost-user` сокеты, hugepages, pin лупы на NUMA узел с NIC.
- Запуск ovs: `--dpdk -c 0x1f -n4 --vhost-owner libvirt-qemu:kvm`, `--socket-mem`.
- VM: `-chardev socket,id=char0,path=/var/run/openvswitch/vhost-user-1`, `-netdev type=vhost-user`.
- Метрики: pps, latency, packet loss; следите за vhost tx retries и dpdk poll mode нагрузкой.
