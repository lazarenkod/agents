# Libvirt XML: шпаргалка
- CPU: `<cpu mode='host-passthrough|host-model|custom'>`, `<topology sockets='' cores='' threads=''>`, `<feature policy='require' name='invtsc'/>`.
- NUMA: `<numatune><memory mode='strict' nodeset='0'/><memnode .../></numatune>`.
- Hugepages: `<memoryBacking><hugepages><page size='1048576' unit='KiB'/></hugepages></memoryBacking>`.
- Disk: `<driver type='raw|qcow2' cache='none|writeback|writethrough' io='native|threads'>`, `<iotune>` лимиты.
- Network: `<model type='virtio'/>`, `<driver queues='4'/>`, `<bandwidth>`.
- Migration: `<features><hyperv><relaxed state='on'/></hyperv></features>`; `liveMigrationBandwidth`.
