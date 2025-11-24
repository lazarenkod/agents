# Сниппеты Claude SDK для аналитики

## Получение метрик
```python
WebFetch(
    url="https://api.mixpanel.com/api/2.0/engage",
    prompt="Верни DAU/WAU/MAU и ретеншн за 30 дней, JSON"
)
```

## Автоматический отчёт
```python
report = Task(
    subagent_type="general-purpose",
    prompt="""
    Сформируй краткий отчёт:
    - тренды NSM и AARRR
    - аномалии
    - рекомендации (3 шт)
    Формат: markdown, русский язык.
    """
)

Write(
    file_path="outputs/product-management/skills/sdk-product-analytics/{timestamp}_weekly.md",
    content=report
)
```

## Анализ эксперимента
```bash
python scripts/ab_test_analysis.py --experiment data/exp.json --output reports/exp.md
```

## Алерт при деградации
```python
if dau_change < -0.05:
    Task(
        subagent_type="general-purpose",
        prompt="DAU упал на 5%. Проведи RCA по шаблону из assets/alert-runbook.md"
    )
```
