# Cost comparison (LLM inference)
- Сравнивайте: $/1k input/output tokens, контекст, concurrency/quotas, региональные цены.
- Провайдеры: Bedrock, Azure OpenAI, Vertex AI, Anthropic API, self-host (Triton/vLLM).
- Паттерны оптимизации: tiered routing, кеш/батч, короткие промпты, max_tokens лимиты.
- Отчёт: таблица цен, фактический $/req из мониторинга, рекомендации по маршрутам.
- Пересмотр: ежемесячно и при релизе новых моделей/цен.
