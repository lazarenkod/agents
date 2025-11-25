# GCP: sole-tenant и изоляция
- Создавайте node template с `--cpu-overcommit-type none` для предсказуемости.
- Рекомендации: серии `C2/N2` для вычислительных нагрузок, sole-tenant для isolation.
- Миграции: включать `--maintenance-policy=MIGRATE` + live migrate окна.
- Лимиты: следить за quota на sole-tenant и placement policies (spread vs pack).
- Метрики: Ops Agent → steal time (guest), host maintenance events.
