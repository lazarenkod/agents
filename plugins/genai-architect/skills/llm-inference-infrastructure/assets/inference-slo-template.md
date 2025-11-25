# SLO для LLM inference (шаблон)
- Latency: p95 ≤ … ms, p99 ≤ … ms (per model/route).
- Availability: ≥ 99.9%, error rate < …%.
- Quality: success rate (non-toxicity/guardrail pass), fallback hit rate.
- Cost: $/1k токенов, GPU час/1000 запросов, cache hit ≥ …%.
- Alert policies: p99>budget 5м, error>1%, cost spike>20%/день.
