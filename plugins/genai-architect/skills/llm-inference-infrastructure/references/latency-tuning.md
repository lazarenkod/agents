# Тюнинг латентности инференса
- Параметры: max_tokens, top_k/p, temperature, stop seq, `streaming` включать.
- Сервер: batching window, max batch size, concurrency, kv-cache reuse, paged attention.
- Сеть: близость к клиенту (edge POP), keep-alive, TLS reuse, gzip.
- Кеш: prompt/semantic/full response; warm cache per segment.
- Диагностика: распределение latency (p50/p95/p99), queue depth, GPU util, trace spans.
