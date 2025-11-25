# Bedrock pricing
- On-demand: оплата per 1k tokens, цены зависят от модели/региона; egress учитывайте.
- Provisioned Throughput: Model Units (MU) с помесячной оплатой, скидки при 6м+, гарантированная capacity.
- RAG KB: OpenSearch Serverless/AOSS хранение+запросы, S3 за исходники, ingestion cost.
- Оптимизация: Haiku для простых, Sonnet для сложных, кеш/батч, mix on-demand+PTU, краткосрочные PTU на пики.
- Мониторинг: $/req, MU util, throttling, KB ingestion cost; ежемесячный пересмотр.
