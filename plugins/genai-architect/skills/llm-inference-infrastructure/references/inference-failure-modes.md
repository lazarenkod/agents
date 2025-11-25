# Failure modes LLM inference
- Throttling/quotas: превышение RPS/tokens → queue build-up, latency рост.
- Model cold starts: p99 всплески; решение — warm pools, prewarming.
- Batching regрессии: oversize batch → timeout/quality drop.
- GPU память: OOM/fragmentation → evictions/restarts.
- Dependency: embedding/rerank endpoints down → fallback route, degrade quality.
- Network/egress: cross-region latency, DNS failures; добавить локальные резервы.
