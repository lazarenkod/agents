# Чек-лист метрик LLM inference
- Latency p50/p95/p99 (общая и по этапам: routing/batch/cache/model)
- Error/timeout rate, retry/fallback, success rate
- Throughput/QPS, GPU/CPU util, batch efficiency, cache hit rate
- Стоимость: $/req, tokens/req, $/model/маршрут, egress
- Надёжность: дрейф конфигов, health checks, rollout/rollback успех, DR тесты
