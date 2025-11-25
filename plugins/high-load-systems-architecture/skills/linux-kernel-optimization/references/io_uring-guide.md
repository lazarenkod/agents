# io_uring: краткое руководство
- Режимы: `IORING_SETUP_IOPOLL` (низкая латентность NVMe), `IORING_SETUP_SQPOLL` (меньше syscall), fixed buffers/files для минимизации оверхеда.
- Лимиты: `ulimit -l` для pinned memory, `fs.nr_open`, `io_uring_disabled` флаг.
- Мониторинг: `cat /proc/sys/kernel/io_uring_disabled`, bpftrace на `io_uring_enter/complete`, perf на `io_uring`.
- Паттерны: батчи (меньше syscalls), zero-copy, временные таймауты, affinity к CPU/NVMe queue.
- Тесты: `fio --ioengine=io_uring`, следить за latency p99, submission/completion queue overflow.
