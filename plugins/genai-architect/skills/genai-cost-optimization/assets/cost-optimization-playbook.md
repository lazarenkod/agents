# GenAI Cost Optimization Playbook

## Диагностика
- Токен-профили, $/req/$/user, SLA, модели/версии, кеш/батч, нагрузки/спайки

## Варианты оптимизации
- Prompt slim/контекст лимиты, системы подсказок
- Кеширование (semantic/cache of outputs), батчинг, сжатие/токенизация
- Tiered routing (simple→cheap, complex→strong), distillation, smaller модели
- Retrieval/фильтры до модели, truncation/резюме
- Self-check/stop-early/low-temp для стоимости

## План
- Экономия/риск, метрики, владельцы, фич-флаги, rollout/rollback

## Метрики/алерты
- $/req, tokens/req, cache hit, latency, качество, SLA нарушения, квоты
