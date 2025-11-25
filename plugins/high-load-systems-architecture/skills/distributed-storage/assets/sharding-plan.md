# План шардирования хранилища

## 1) Контекст и цели
- Продукт/сервис: …
- Данные: тип (объект/блок/файл), объём, рост, hot/cold зоны.
- SLO: p95/p99 latency (read/write), доступность, RPO/RTO.
- Регуляторика/гео: требования к локализации/PII/egress.

## 2) Ключевые решения
- Ключ шардирования: поле/составной ключ, защита от hot keys (salting/range bucketing/hash + random suffix).
- Стратегия: `hash | range | directory | geo | hybrid (range + hash)`.
- Балансировка: консистентный хеш, virtual nodes, весовые коэффициенты.
- Консистентность: CAP/PACELC обоснование, кворум/replication factor, lag budget.

## 3) Архитектура
- Топология: шард → реплика(и)/EC → AZ/Region → Router (LB/API/GW).
- Маршрутизация: клиентский SDK / сервисный роутер / smart proxy; кэширование метаданных.
- Метаданные: shard map (формат, TTL, источник), bootstrap/refresh стратегия.
- Изоляция: noisy-neighbor guardrails, лимиты IOPS/throughput per shard.

## 4) План ребалансировки и роста
- Триггеры: utilization > X%, p99 latency рост, hotspot alerts.
- Алгоритм: split/merge/reshard; шаги по 1–2 shard за итерацию; фоновая миграция с budget на RPS/latency.
- Контроль: шаговые метрики (lag, throttle %, errors), stop conditions, rollback.
- Headroom: target ≤ 65–70% CPU/IOPS/space, план прироста на 6–12 мес.

## 5) Тест-план и валидация
- Load test: профиль R/W, смешанные размеры объектов, burst.
- Chaos/failure: отключение shard node, network partition, replica lag.
- Консистентность: чтение после записи, read-your-writes, monotonic reads тесты.
- Дымовые проверки: CRUD, листинг, ACL, TTL/GC.

## 6) Операции и SRE
- Набор метрик: latency p50/p95/p99, IOPS/throughput, queue depth, replication lag, rebalance progress, cache hit.
- Алерты: tail latency рост, lag > budget, shard hotspot, disk full %, scrub errors.
- Бэкапы/DR: частота снапшотов, offsite копии, RPO/RTO, таблица контактов.
- Runbooks: hot shard, rebalance slowdown, disk/AZ failure (ссылка на DR runbook).

## 7) Риски и меры
- Hot keys / skew → salting + auto-split.
- Долгие миграции → throttle, окна, приоритизация холодных диапазонов.
- Сложность клиентов → тонкий smart proxy + версионирование shard map.
- Стоимость egress/replication → политика размещения, компрессия, TTL.

## 8) Rollout
- Канареечный rollout (1–2% трафика), dual-write/dual-read по флагу.
- Наблюдаемость: сравнение ошибок/latency до/после, diff по консистентности.
- Freeze/rollback: условия стопа, план возврата, кто утверждает.

## 9) TODO и владение
- Ответственные, сроки, зависимости.
- Таблица изменений vs предыдущей версии.
