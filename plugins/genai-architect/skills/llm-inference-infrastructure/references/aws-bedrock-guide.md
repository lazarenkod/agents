# AWS Bedrock guide
- Модели: Claude, Llama, Mistral, Titan; провизионирование через on-demand или Provisioned Throughput.
- Сеть: VPC endpoints/PrivateLink, блокировка публичного доступа, KMS шифрование.
- Ops: CloudWatch метрики (latency, throttling, tokens), алерты на p99/throttling, MU util.
- Стоимость: сравнение on-demand vs PTU, выбор Haiku/Sonnet по сложности, кеш/батч для экономии.
- Безопасность: Guardrails, IAM least privilege, CloudTrail/Audit, KB с AOSS.
