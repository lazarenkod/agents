# Стратегии кеширования
- Prompt prefix cache, semantic cache, full-response cache; ключ = hash(prompt+context+tenant).
- TTL и инвалидация: по версиям данных/политик, warmup при релизах, eviction политика.
- Безопасность: tenant isolation, PII redaction, audit.
- Метрики: hit %, stale %, $/req до/после, latency улучшение.
- Риски: устаревшие данные, несогласованность версий, память/стоимость хранения.
