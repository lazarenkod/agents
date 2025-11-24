# Ключевые фреймворки для AI/LLM продуктов

## Стратегия и приоритизация
- **PRFAQ (Working Backwards):** формулирует ценность и ожидания до разработки.
- **RICE / ICE / WSJF:** сравнение инициатив с учётом Reach/Impact/Confidence/Effort и задержанных затрат (latency/$).
- **JTBD + Kano + HEART:** понимание работы пользователя, классификация фич, измерение UX.
- **AARRR/North Star:** связывает модельные метрики с бизнес-результатами.

## Ответственный AI
- **Constitutional AI:** принципы поведения + self-critique; прозрачная конституция.
- **Model Cards:** документирование данных, ограничений, метрик, версий, владельцев.
- **Safety Stack:** модерация до/после генерации, red teaming, policy enforcement, PII scrub.
- **Privacy by Design:** минимизация данных, маскирование, явное согласие.

## Оценка и качество
- **Offline Eval:** golden datasets, автоматические регрессии, LLM-as-judge, метрики hallucination/bias.
- **Online Experiments:** A/B, canary, shadow; критерии ship/kill; guardrails на деградацию.
- **Cost Governance:** $/вызов, $/сессия, $/конверсию; аллокация бюджета на эксперименты.

## Операции и масштабирование
- **Release Stages:** sandbox → beta → GA с чёткими порогами качества/безопасности.
- **Observability:** трассировка промтов, мониторинг latency/quality/cost, алерты.
- **Feedback Loops:** пользовательский фидбек, human-in-the-loop метки, continuous learning.
