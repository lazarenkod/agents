# Guardrails Checklist (RAG)

- Safety/policy фильтры до/после генерации, self-critique
- PII детекция/редакция, хранение/логирование безопасно
- Grounding: ссылки/цитаты, проверка источников, анти-халлюцинации
- Контент фильтры по домену/регуляторике (HIPAA/FIN/дети)
- Rate limits/quotas, защита от prompt injection/длинных запросов
- Алёрты на policy/PII нарушения, fallback/rollback сценарии
