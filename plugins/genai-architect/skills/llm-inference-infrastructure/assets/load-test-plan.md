# Load Test Plan (LLM Inference)

## Цели
- Latency/throughput цели, SLO, критичные сценарии (батч/кеш/маршруты)

## Профили
- Нагрузки/спайки, длины промптов/ответов, mix моделей/маршрутов

## Тесты
- Load/soak/stress/spike, chaos (узлы/сеть), failure injection
- Метрики: latency p50/p95/p99, error/timeout, throughput, GPU util, batch efficiency, cache hit

## Критерии
- Успех/фейл, пороги, алерты, rollback

## Результаты
- Графики, bottlenecks, план улучшений
