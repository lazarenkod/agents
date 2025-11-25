# Инструменты eBPF/BCC
- `bcc`: готовые утилиты (`execsnoop`, `opensnoop`, `tcplife`, `runqlat`, `biolatency`, `cachestat`).
- `bpftrace`: интерактивные скрипты, быстрая диагностика; требует BTF.
- `libbpf + CO-RE`: продакшн агенты, стабильность к версиям ядра.
- Практика: держите «golden» набор скриптов для CPU/IO/NET, сохраняйте вывод в артефакты.
- Безопасность: `unprivileged_bpf_disabled` контролировать, лимиты map sizes/stack size.
