# RAG Ops Checklist
- Ингест: SLA обновлений, очередь, dead-letter, мониторинг ошибок парсинга.
- Индексация: время индексации, lag, pg errors, checksum сверка, версия схемы.
- Поиск: latency p95/p99, hit rate, hybrid fusion веса, rerank success rate.
- Генерация: groundedness, цитаты, отказ при отсутствии фактов, guardrail срабатывания.
- Безопасность: PII redaction, policy фильтры, audit лог.
- DR/Runbooks: refresh rollback, index rebuild, модельный fallback, feature flags.
