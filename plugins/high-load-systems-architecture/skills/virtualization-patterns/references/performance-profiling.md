# Профилирование производительности VM
- CPU: `perf kvm stat`, `perf sched`, runqueue/steal; внутри гостя `perf top`.
- IO: `fio` с `libaio/io_uring`, `iostat -x`, `blkio` cgroup stats, `qemu-iothread` pinning.
- Network: `iperf3`, `ethtool -S`, `ss -ti`, XDP/vhost stats.
- Трейсинг: `bpftrace` на `kvm_vcpu_block`, `block_rq*`, `tcp_retransmit_skb`.
- Отчёт: таблица метрик до/после, конфиги (XML/sysctl), риски/rollback.
