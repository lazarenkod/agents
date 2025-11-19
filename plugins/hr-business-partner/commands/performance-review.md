---
name: performance-review
description: Conduct comprehensive performance review with OKR assessment, 360-degree feedback, and development planning. Generates structured review document in Russian markdown.
---

# Performance Review Command

Проведите комплексный performance review сотрудника с использованием лучших практик AWS, Google, Microsoft, Netflix.

## Использование

```
/performance-review [employee-name] [review-period]
```

## Что делает эта команда

1. **Собирает контекст**: Имя сотрудника, роль, период оценки, OKRs
2. **Анализирует performance**: Достижения, компетенции, 360-feedback
3. **Оценивает рейтинг**: По 5-балльной шкале с обоснованием
4. **Создает development plan**: Конкретные шаги для роста
5. **Сохраняет результат**: Markdown документ на русском языке

## Процесс

### Шаг 1: Сбор информации

Команда запросит у вас:
- ФИО сотрудника и должность
- Период review (например, "Q4 2024" или "2024 год")
- OKRs/цели на период
- Ключевые достижения
- Обратная связь от коллег (360-degree)

### Шаг 2: Анализ

Команда проанализирует:
- OKR achievement (% выполнения целей)
- Core competencies (технические, soft skills, leadership)
- Impact на команду и бизнес
- Strengths и growth areas

### Шаг 3: Рейтинг и рекомендации

Команда определит:
- Overall rating (1-5 scale)
- Обоснование рейтинга с примерами
- Readiness для следующего уровня
- Development план на следующий период

### Шаг 4: Генерация документа

Создается comprehensive review document:
```markdown
# Performance Review: {Имя Сотрудника}
**Период**: {Период}
**Должность**: {Должность}
**Менеджер**: {Ваше имя}
**Дата**: {Дата}

## Резюме
{Краткое описание performance}

## Достижения
{Ключевые достижения с impact}

## OKR Achievement
{Анализ выполнения целей}

## Компетенции
{Оценка по каждой компетенции}

## 360-Degree Feedback
{Обобщенная обратная связь}

## Рост и развитие
{Areas for growth и action plan}

## Карьерное развитие
{Readiness, promotion timeline}

## Общий рейтинг: {Рейтинг}
```

## Примеры использования

**Пример 1: Annual Review**
```
User: /performance-review Иван Петров Q4-2024

Agent: Проведу performance review для Ивана Петрова за Q4 2024.

Пожалуйста, предоставьте следующую информацию:
1. Должность Ивана: [Senior Software Engineer]
2. OKRs на Q4 2024: [...]
3. Ключевые достижения: [...]
4. Обратная связь от коллег: [...]

[После предоставления информации]

Agent: Анализирую performance...

[Генерирует comprehensive review document]

Документ сохранен: outputs/hr-business-partner/2024-12-18_performance-review-ivan-petrov-q4-2024.md
```

**Пример 2: Promotion Review**
```
User: /performance-review Мария Сидорова 2024-annual

Agent: Это годовой review. Фокусируется на promotion readiness?

User: Да, оцениваем готовность к Senior Manager.

Agent: Учту promotion criteria для Senior Manager при оценке.

[Проводит расширенный анализ leadership competencies]
```

## Лучшие практики

1. **Подготовка**: Соберите все данные ДО запуска команды (OKRs, projects, feedback)
2. **Specificity**: Используйте конкретные примеры и метрики
3. **Balance**: Включите как strengths, так и growth areas
4. **Forward-looking**: Фокус на development, а не только на прошлое
5. **Preparation for conversation**: Документ - это подготовка к разговору, не замена

## Навигация

После генерации review:
- Просмотрите документ
- Доработайте при необходимости
- Запланируйте 1-on-1 для обсуждения
- Используйте как основу для карьерного разговора

## См. также

- `team-motivation-excellence` skill - для работы с мотивацией
- `performance-review-mastery` skill - для глубокого понимания процесса
- `coaching-development-frameworks` skill - для career conversations
