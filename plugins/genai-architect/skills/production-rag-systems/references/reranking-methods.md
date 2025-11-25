# Реранкеры
- Модели: monoT5/monoBERT, Cohere Rerank, Voyage, Jina reranker, ColBERTv2 (late interaction).
- Критерии: качество (nDCG/MRR), latency/стоимость, языки, длина контекста, лицензия.
- Архитектуры: cross-encoder (лучшее качество), dual-encoder distill (быстрее), hybrid (rerank top-N).
- Настройки: top_k для rerank, max токены, batching, caching rerank scores.
- Метрики: uplift к основному retrieve (delta Recall@k, click/CTR), p95 latency, стоимость/req.
