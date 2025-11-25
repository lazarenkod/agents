# Bedrock Deployment Plan

## Контекст
- Цели/трафик/latency/стоимость, модели/версии, регионы, PII/регуляторика

## Архитектура/конфиг
- VPC/privatelink, IAM/политики, endpoints, Provisioned Throughput
- Кеш/батч/роутинг, контроль контекста/токенов, Guardrails
- Observability: метрики/logs/traces, алерты, квоты

## Тесты и rollout
- Load/latency/safety тесты, канареек/фич-флаги, rollback

## Метрики/алерты
- Latency/error, $/req/tokens, квоты, policy/PII violations

## TODO
- Действия, владельцы, сроки, зависимости
