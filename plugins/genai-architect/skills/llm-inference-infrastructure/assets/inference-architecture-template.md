# LLM Inference Architecture Template

## Требования
- Latency/качество/стоимость, SLA, PII/регуляторика, self-host/API гибрид

## Компоненты
- Gateway/API, auth/quotas, routing/tiering, batching, caching
- Models/versions (GPU/CPU), autoscale, schedulers, storage
- Observability: metrics/logs/traces, алерты, дрифт/health checks
- DR/rollback, feature flags, config management

## Метрики/алерты
- Latency p50/p95/p99, error/timeout, throughput, GPU util, $/req, cache hit, batch efficiency

## Операции
- Deploy/rollback, tests (load/chaos), change control, runbooks
