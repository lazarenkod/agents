# Выбор embedding моделей
- Критерии: язык/мультиязык, размер векторов, latency/стоимость, лицензия, качество (MTEB).
- Популярные: BGE-large/m3, E5, GTE, NV-embed, Cohere Embed v3, OpenAI text-embedding-3.
- Стратегии: domain-tuned embeddings, multi-vector (colbert), distillation для latency.
- Метрики: Recall@k, nDCG, cosine distribution, дрейф эмбеддингов после обновлений.
- Совместимость: поддержка ускорителей, int8/fp16 квантование, фильтры/metadata per DB.
