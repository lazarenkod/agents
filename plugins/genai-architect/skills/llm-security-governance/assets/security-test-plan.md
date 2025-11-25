# План тестирования безопасности LLM
- Области: prompt injection, jailbreaks, PII leakage, toxicity, policy violations, data exfiltration.
- Метод: чек-листы + автоматизированные сценарии (fuzzing, red-team prompts), частота (каждый релиз, ежемесячно).
- Метрики: блокировки, false positive/negative, время реакции, coverage по OWASP LLM.
- Выход: отчёт с багами/рисками, владельцы/ETA, обновлённые guardrails.
