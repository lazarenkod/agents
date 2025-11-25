# Стратегии batching
- Adaptive batching: окна 10–50 мс, max batch size, приоритеты по SLA.
- Static batching: фиксированная пачка для throughput, risk latency.
- Token bucket per route, separate queues для коротких/длинных запросов.
- Guardrails: max prompt/response tokens, pre-flight estimation, drop/redirect при превышении.
- Метрики: batch fill %, latency vs size, ошибки/timeout, cost per token.
