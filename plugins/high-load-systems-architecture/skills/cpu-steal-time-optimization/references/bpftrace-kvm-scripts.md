# bpftrace для диагностики steal time

- **kvm_vcpu_block latency**:
```bash
bpftrace -e 'kprobe:kvm_vcpu_block {@lat = hist(nsecs/1000);}'
```
- **noisy neighbor detector**: считать CPU time других VM по threads `qemu-system`.
- **scheduler delays**:
```bash
bpftrace -e 'tracepoint:sched:sched_wakeup { @wait[args->pid] = nsecs; }
tracepoint:sched:sched_switch /@wait[args->next_pid]/ {
  printf("pid %d wait %d us\\n", args->next_pid, (nsecs-@wait[args->next_pid])/1000);
  delete(@wait[args->next_pid]);
}'
```
- **IRQ storms**: `tracepoint:irq:irq_handler_entry` + latency hist.
- Рекомендации: запускайте ≤ 60 c, на стенде с debuginfo/BTF, сохраняйте результаты в артефакт.
