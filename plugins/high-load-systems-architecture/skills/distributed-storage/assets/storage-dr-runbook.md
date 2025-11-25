# Runbook: DR/Fallover для распределённого хранилища

## 0) Паспорт
- Сервис/кластер: …
- Топология: регионы/AZ, репликация/EC, версии ПО.
- Цели: RPO …, RTO …, допустимая деградация (read-only/ограничение записи).
- Контакты: on-call, storage lead, SRE lead, бизнес-владелец.

## 1) Триггеры и классификация
- Region/AZ outage, quorum loss, мон/OSD down > X мин, rebalance stuck, corruption/scrub errors, replication lag > budget.
- Severity: SEV-1 (потеря записи/данных), SEV-2 (деградация latency/lag), SEV-3 (частичное влияние).

## 2) Немедленные действия (T0–T15)
- Назначить инцидент-командира, включить war-room.
- Зафиксировать SLO/SLA: текущие метрики (latency p99, error rate, lag, fullness).
- Включить защиту: rate-limit/traffic shaping, перевести клиентов в read-only (флаг/ACL), остановить шумные бэкенды.
- Заморозить рискованные операции: ребаланс/reshard/фоновые задачи, мажорные релизы.

## 3) Диагностика (T15–T45)
- Кворум/мониторы: `ceph -s`, `quorum_status`.
- Репликация/lag: `ceph health detail | grep lag`, `pg dump`.
- Пространство: `ceph osd df tree`, near/full ratio.
- Сеть: latency/loss между AZ/OSD, firewall/route изменения.
- Коррупция: `pg inconsistent`, scrub logs.
- Управление данными: bucket/placement anomalies, hotspot PG.

## 4) Ветвление решения
- **Loss of quorum/monitors:** поднять временный мон в здоровой AZ, восстановить монmap, удалить flapping мон.
- **OSD mass down:** приоритетные OSD, временное снижение full ratio, включить `recovery priority` + throttle клиентского трафика.
- **Replication lag:** увеличить backfills, выделить быстрые OSD, включить cache tier (если доступно), временно снизить нагрузку.
- **Corruption:** isolate PG, `pg repair`/`deep-scrub`, реконструкция из реплик/backup, блокировать запись на затронутые пулы.
- **Region failover:** promote standby, переключить клиентов (DNS/consul), включить write-block в поражённом регионе.

## 5) Выполнение failover/restore
- Активировать DR сайт: подготовить креденшелы, проверить версию и схемы.
- Применить write-block/geo policies, обновить роутинг.
- Поднять недостающие мон/OSD, восстановить CRUSH map, rebalance c лимитом IO.
- Проверить целостность: `pg clean`, отсутствие inconsistent PG, сверить хэши/объёмы ключевых бакетов.
- Постепенно снять блокировки записи (по сегментам/тенантам).

## 6) Валидация и выход
- Контрольные метрики: p99 latency, error rate, rebalance ETA, lag, fullness.
- Тест-кейсы: CRUD, листинг, ACL, multipart, TTL/GC, cross-region replication.
- Решение о выходе из инцидента: IC + владелец сервиса + SRE lead.

## 7) Пост-инцидентные действия
- Сохранить временную шкалу и логи (до/после).
- Обновить runbooks, risk log, decision log; оформить ретро.
- План профилактики: capacity/auto-scaling, алерты, тесты DR/chaos, обучение on-call.
