# Hybrid search шпаргалка
- Комбинации: BM25 + dense, term boosting, RRF, weighted sum, LTR.
- Настройки: top_k per modality, min_score, filter by metadata/time/tenant.
- Реранкеры: cross-encoder (monoT5, colbert-rerank), distillation в bi-encoder.
- Оптимизация: многоязычность, sparser embeddings (SPLADE), multi-vector store.
- Метрики: Recall@k, nDCG, latency budget, индекс размер/стоимость.
