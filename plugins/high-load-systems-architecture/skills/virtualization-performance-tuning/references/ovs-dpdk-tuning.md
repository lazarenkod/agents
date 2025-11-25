# OVS-DPDK тюнинг
- Hugepages и PMD pinning (по NUMA с NIC): `pmd-cpu-mask`, `dpdk-lcore-mask`.
- RX/TX queues per port, `n-dpdk-rxq`, RSS hash, offloads (tx-checksum, tso).
- Flow cache: `other_config:emc-insert-inv-prob`, `emc-insert-min`, `symmetric-rss`.
- Мониторинг: `ovs-appctl dpif-netdev/pmd-rxq-show`, pkt drop reasons, PMD idle cycles.
- Тесты: testpmd/iperf3, latency p99, packet loss; избегайте over-subscribe PMD ядра.
