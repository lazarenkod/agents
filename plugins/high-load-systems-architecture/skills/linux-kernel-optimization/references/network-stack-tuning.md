# Тюнинг сетевого стека
- Буферы: `net.core.rmem_max/wmem_max`, `tcp_rmem/tcp_wmem` — увеличивать для throughput, с осторожностью для памяти.
- Очереди: `net.core.somaxconn`, `tcp_max_syn_backlog`, `tcp_tw_reuse/recycle` (не включать recycle).
- Congestion control: `bbr` для долгих RTT, `cubic` по умолчанию; проверьте аппарат offloads (GRO/LRO/TSO).
- NIC: RPS/RFS, IRQ affinity, ring buffers (`ethtool -G`), coalescing (`ethtool -C`), multiqueue.
- Диагностика: `ss -ti`, `netstat -s`, `tc -s qdisc`, pcap с `tcpdump` для подсчёта ретрансмитов/OWD.
