# PSI (Pressure Stall Information)
- Файлы: `/proc/pressure/{cpu,memory,io}`; метрики `some/full` avg10/60/300.
- Интерпретация: `some` = частичная задержка, `full` = полная блокировка всех задач.
- Алерты: `full` CPU >0.5% 5м, memory/io spikes → вероятно троттлинг/выбросы.
- Использование: autoscaling trigger, throttle фоновых задач, сигнализация SLO риска.
- Снимайте совместно с runqueue/oom/IO wait для диагностики.
