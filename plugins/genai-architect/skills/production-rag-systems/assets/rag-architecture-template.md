# RAG Architecture Template

## Контекст
- Домен, цели (качество/latency/стоимость), требования к цитатам/ответственности

## Ингест и подготовка
- Источники, форматы, нормализация, chunking, версии, PII/редакция

## Индексация/хранение
- Vector/keyword/hybrid, схемы/метаданные, репликация/refresh, кеши

## Ранжирование/генерация
- Retrieval (k, фильтры), rerank (cross-encoder), генерация (модель/промпты), цитаты

## Guardrails
- Safety/policy, PII, модерация до/после, grounding checks

## Observability
- Метрики: качество/latency/cost, tracing, алерты, дрифт данных/индекса

## Операции
- Обновление данных, DR/rollback, тесты/регрессии, SLO/алерты, owners
