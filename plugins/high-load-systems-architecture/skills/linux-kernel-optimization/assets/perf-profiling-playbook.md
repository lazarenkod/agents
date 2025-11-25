# Playbook: perf профилирование

1) Подготовка
- Убедитесь в наличии `perf`, `debug symbols`, достаточного `perf_event_paranoid`.
- Зафиксируйте ядро/конфиг, фоновые нагрузки, версию приложения.

2) CPU профилирование
```bash
perf record -F 99 -ag -- sleep 30
perf report --sort comm,dso,symbol
```
- Фокус: hot functions, контекстные переключения, syscalls.

3) Latency/IO
```bash
perf sched record -- sleep 10
perf sched latency
perf record -e 'block:block_rq_issue,block:block_rq_complete' -a -- sleep 30
```
- Метрики: runqueue latency, IO latency, blocked time.

4) Flamegraph (если доступно)
```bash
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

5) Отчёт
- Топ 10 функций, % CPU, рекомендации.
- Изменения параметров, ожидаемый эффект, риски.
