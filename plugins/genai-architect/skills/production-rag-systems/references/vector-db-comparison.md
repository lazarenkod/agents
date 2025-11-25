# Сравнение vector DB
- Критерии: latency p95/p99, recall, фильтры/ACL, масштабирование, стоимость хранения/запросов, multi-region.
- Кандидаты: Pinecone, Weaviate, Qdrant, Milvus, OpenSearch/AOSS, PGVector, Chroma.
- Use-cases: enterprise ACL (Pinecone/Weaviate), on-prem (Qdrant/Milvus), SQL + vectors (PGVector/OpenSearch).
- Таблица: поддержка HNSW/IVF, metadata filters, hybrid search, управление шардированием/репликами, оплата.
- Риски: горячие шарды, egress, ограничение на payload, совместимость с клирингом PII. 
