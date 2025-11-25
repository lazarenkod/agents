# Batch + caching для снижения стоимости
- Semantic/full-response cache: TTL, tenant-aware ключи, hash prompt+context, запись в warmup.
- Batching: adaptive окна, max batch, разделение коротких/длинных запросов; токен бюджет.
- Guardrails: drop/redirect при переполнении, pre-flight estimation.
- Метрики: cache hit %, batch fill %, latency vs размер batch, $/req до/после.
- Риски: stale ответы, fairness между тенантами, деградация качества при агрессивном батчинге.
