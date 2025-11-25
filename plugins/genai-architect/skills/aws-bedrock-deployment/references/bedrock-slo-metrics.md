# SLO/метрики для Bedrock
- Latency: p95/p99 per модель/маршрут, streaming и non-streaming.
- Доступность: success rate, throttling %, KB ingestion success, guardrail availability.
- Качество: groundedness (для KB), policy violation rate, fallback rate.
- Стоимость: $/1k токенов, MU util, кеш hit, egress.
- Алерты: p99>бюджет 5м, throttling>1%, guardrail errors, KB lag>порог, MU util>85%.
