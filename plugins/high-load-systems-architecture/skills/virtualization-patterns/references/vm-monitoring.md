# Мониторинг VM
- Метрики хоста: CPU util, ready/steal, runqueue, mem/caches, PSI, IO await, NIC drops, IRQ load.
- Метрики гостя: CPU/mem, st%, disk latency, network RTT/retrans, agent alive.
- Специфично миграции: downtime, dirty rate, remaining data, post-copy faults.
- Алерты: st%>5/10, ready time, p99 latency > бюджет, nearfull disk, VF errors, live migration > окно.
- Инструменты: libvirt exporter, node_exporter, collectd, qemu guest agent, tracing (perf/bpf).
