# Runbook: инциденты Bedrock
- Триггеры: throttling/429, latency p99 рост, errors 5xx, guardrails outage, KB lag.
- Шаги: проверить Service Health, квоты, региональные проблемы; переключить на резервный регион/модель; снизить max_tokens, включить агрессивный кеш/батчинг.
- Rollback: перевести трафик на on-demand/другую модель, отключить новые фичи, включить degrade mode.
- Коммуникация: статус, ETA, алерты на on-call/прод.
- Пост-мортем: обновить квоты/конфиги, refresh runbooks, улучшить алерты.
