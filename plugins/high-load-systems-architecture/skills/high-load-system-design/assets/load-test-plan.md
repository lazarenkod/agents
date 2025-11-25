# Load Test Plan

## Цели
- SLO проверки (latency/error), пропускная способность, деградации

## Профили
- Пики/рост/суточные паттерны, read/write mix, размер запросов/ответов

## Тесты
- Ramp/soak/stress/spike, fault injection/chaos (сеть/узлы/регион)
- Метрики: latency p50/p95/p99, error rate, throughput, saturation, queue depth, cache hit

## Критерии успеха/стопа
- Пороги, алерты, rollback условия

## Результаты
- Наблюдения, bottlenecks, план улучшений
