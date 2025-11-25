# Eval Plan (RAG)

## Цель и метрики
- Качество: groundedness/faithfulness/цитаты/accuracy/recall/rerank качество
- Производительность/стоимость: latency p50/p95, $/ответ, cache hit rate
- Безопасность: policy/PII violations

## Offline eval
- Датасет (размер, источники, обновление), метрики, пороги pass/fail
- LLM-as-judge/ручная проверка, регрессии

## Online eval
- A/B/канарейки, сегменты, длительность, критерии ship/kill, guardrails

## Алерты/мониторинг
- Пороги деградаций, каналы, владельцы, действия
