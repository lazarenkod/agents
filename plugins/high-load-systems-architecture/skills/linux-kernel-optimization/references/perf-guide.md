# perf: шпаргалка
- Основные команды: `perf list`, `perf stat`, `perf record`, `perf report`, `perf sched`, `perf c2c`.
- События: `cycles`, `instructions`, `cache-misses`, `branch-misses`, `cs`, `cpu-migrations`.
- Отбор по процессу/CPU: `perf stat -p $PID`, `perf stat -C 0-3`.
- Отладка latency: `perf sched latency`, `perf record -e sched:sched_switch -ag`.
- Советы: фиксируйте частоту (`perf stat -I 1000`), добавляйте `--clockid mono` для сопоставления с логами.
