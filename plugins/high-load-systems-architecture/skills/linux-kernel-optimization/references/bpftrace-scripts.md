# bpftrace: полезные сниппеты
- syscalls latency:
```bash
bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[probe] = count(); }'
```
- runqueue latency:
```bash
bpftrace -e 'tracepoint:sched:sched_wakeup { @start[args->pid] = nsecs; }
tracepoint:sched:sched_switch /@start[args->next_pid]/ { @lat = hist((nsecs-@start[args->next_pid])/1000); delete(@start[args->next_pid]); }'
```
- TCP retrans:
```bash
bpftrace -e 'kprobe:tcp_retransmit_skb { @retrans[comm] = count(); }'
```
- IO latency:
```bash
bpftrace -e 'tracepoint:block:block_rq_issue { @start[args->rq] = nsecs; }
tracepoint:block:block_rq_complete /@start[args->rq]/ { @lat = hist((nsecs-@start[args->rq])/1000); delete(@start[args->rq]); }'
```
