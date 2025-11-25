# eBPF latency probe (шаблон)

## Цель
Собрать латентность системных вызовов/IO/сетевых путей без существенной нагрузки.

## Шаги
1. Проверить BTF/CO-RE поддержку (`/sys/kernel/btf/vmlinux`).
2. Выбрать точки: `tcp_sendmsg`, `blk_account_io_completion`, `sys_enter/exit`.
3. Сгенерировать скрипт bpftrace:
```bash
bpftrace -e 'tracepoint:syscalls:sys_enter_read { @start[tid] = nsecs; }
tracepoint:syscalls:sys_exit_read /@start[tid]/ { @lat = hist((nsecs-@start[tid])/1000); delete(@start[tid]); }'
```
4. Сбор 1–5 мин, сохранить гистограмму в артефакт.
5. Интерпретация: tail latency, outliers, корреляция с IO/CPU.

## Хранение
- Сохранить скрипт, вывод, контекст (ядро/нагрузка/время), изменения параметров.
