# Шаблоны для Claude Code Plugins

Эта директория содержит шаблоны для создания русскоязычных агентов, скиллов и команд.

## Доступные шаблоны

### 1. Шаблон агента (`agent-template-ru.md`)

Используй этот шаблон для создания новых AI агентов на русском языке.

**Структура:**
- YAML frontmatter с метаданными
- Описание цели и назначения
- Возможности агента
- Система принятия решений
- Примеры использования
- Best practices

**Использование:**
```bash
# Скопируй шаблон
cp templates/agent-template-ru.md plugins/{plugin-name}/agents/{agent-name}.md

# Заполни метаданные и содержание
# Добавь агента в marketplace.json
```

### 2. Шаблон скилла (`skill-template-ru.md`)

Используй этот шаблон для создания новых скиллов (баз знаний) на русском языке.

**Структура:**
- YAML frontmatter с метаданными
- Триггеры активации
- Основные концепции
- Паттерны и практики
- Практические примеры
- Продвинутые техники

**Использование:**
```bash
# Создай директорию для скилла
mkdir -p plugins/{plugin-name}/skills/{skill-name}

# Скопируй шаблон
cp templates/skill-template-ru.md plugins/{plugin-name}/skills/{skill-name}/SKILL.md

# Создай дополнительные директории
mkdir -p plugins/{plugin-name}/skills/{skill-name}/references
mkdir -p plugins/{plugin-name}/skills/{skill-name}/assets

# Заполни содержание
# Добавь скилл в marketplace.json
```

### 3. Шаблон команды (`command-template-ru.md`)

Используй этот шаблон для создания новых команд на русском языке.

**Структура:**
- YAML frontmatter с метаданными
- Назначение команды
- Параметры и опции
- Сценарии использования
- Вывод команды
- Troubleshooting

**Использование:**
```bash
# Скопируй шаблон
cp templates/command-template-ru.md plugins/{plugin-name}/commands/{command-name}.md

# Заполни содержание
# Добавь команду в marketplace.json
```

## Процесс создания нового компонента

### 1. Определи цель

Четко определи:
- Какую проблему решает компонент
- Кто будет его использовать
- Когда он должен активироваться

### 2. Выбери правильный тип

- **Агент** - для рассуждения и принятия решений
- **Скилл** - для специализированных знаний
- **Команда** - для автоматизации и выполнения задач

### 3. Выбери модель (для агентов)

- **haiku** - быстрые, детерминированные задачи
- **sonnet** - сложное мышление, архитектура
- **opus** - критически сложные задачи

### 4. Заполни шаблон

Скопируй соответствующий шаблон и заполни все секции:
- Замени placeholder'ы на реальный контент
- Добавь конкретные примеры
- Убедись что описание включает триггеры активации

### 5. Добавь в marketplace.json

Зарегистрируй компонент в `.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "agents": [
    "./agents/agent-name.md"
  ],
  "commands": [
    "./commands/command-name.md"
  ],
  "skills": [
    "./skills/skill-name"
  ]
}
```

### 6. Регенерируй документацию

```bash
python scripts/generate-docs.py
```

Или используй команду:

```bash
/regenerate-docs
```

## Требования к frontmatter

### Агент

```yaml
---
name: agent-identifier          # hyphen-case, на английском
description: Описание на русском. Используй ПРОАКТИВНО когда [триггер].
model: sonnet|haiku|opus       # выбери подходящую модель
---
```

### Скилл

```yaml
---
name: skill-identifier          # hyphen-case, на английском
description: Описание на русском. Используй когда [триггер].
---
```

### Команда

```yaml
---
name: command-identifier        # hyphen-case, на английском
description: Описание на русском того, что делает команда
---
```

## Best Practices

### 1. Именование

- **Идентификаторы (name)**: hyphen-case, на английском
- **Описания**: на русском языке, четкие и конкретные
- **Файлы**: lowercase, hyphen-separated

### 2. Триггеры активации

Обязательно включай в описание когда использовать компонент:

- **Агенты**: "Используй ПРОАКТИВНО когда..."
- **Скиллы**: "Используй когда..."
- **Команды**: Описание должно быть понятным без префикса

### 3. Структура контента

- Начинай с простого, переходи к сложному
- Используй конкретные примеры
- Добавляй code snippets где уместно
- Объясняй "почему", а не только "как"

### 4. Примеры

Всегда включай практические примеры:
- Реальные сценарии использования
- Рабочий код
- Ожидаемые результаты

### 5. Связи между компонентами

Указывай связанные ресурсы:
- Какие агенты используют этот скилл
- Какие команды работают вместе
- Какие скиллы дополняют друг друга

## Автоматизация

### Pre-commit hook

Создай `.git/hooks/pre-commit` для автоматической регенерации документации:

```bash
#!/bin/bash
python scripts/generate-docs.py
git add docs/*.md
```

### GitHub Actions

Автоматизируй обновление документации при изменениях:

```yaml
name: Update Documentation

on:
  push:
    paths:
      - 'plugins/**'
      - '.claude-plugin/marketplace.json'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate docs
        run: python scripts/generate-docs.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/*.md
          git commit -m "docs: auto-update documentation" || exit 0
          git push
```

## Валидация

Перед коммитом проверь:

- [ ] YAML frontmatter корректен
- [ ] Описание включает триггер активации
- [ ] Все секции шаблона заполнены
- [ ] Примеры работают и понятны
- [ ] Компонент добавлен в marketplace.json
- [ ] Документация регенерирована
- [ ] Нет опечаток и грамматических ошибок

## Примеры использования

### Создание нового агента

```bash
# 1. Определяем плагин
PLUGIN="backend-development"

# 2. Создаем агента из шаблона
cp templates/agent-template-ru.md plugins/$PLUGIN/agents/api-tester.md

# 3. Редактируем файл
# - Заменяем название-агента на api-tester
# - Заполняем описание: "API тестировщик. Используй ПРОАКТИВНО когда нужно протестировать API endpoints."
# - Выбираем model: haiku
# - Заполняем остальные секции

# 4. Добавляем в marketplace.json
# В секцию plugins[$PLUGIN].agents добавляем: "./agents/api-tester.md"

# 5. Регенерируем документацию
python scripts/generate-docs.py

# 6. Коммитим
git add plugins/$PLUGIN/agents/api-tester.md .claude-plugin/marketplace.json docs/
git commit -m "feat: add API tester agent"
```

### Создание нового скилла

```bash
# 1. Создаем структуру
PLUGIN="backend-development"
SKILL="rest-api-patterns"

mkdir -p plugins/$PLUGIN/skills/$SKILL/{references,assets}

# 2. Копируем шаблон
cp templates/skill-template-ru.md plugins/$PLUGIN/skills/$SKILL/SKILL.md

# 3. Редактируем SKILL.md
# - Заполняем frontmatter
# - Добавляем концепции и паттерны
# - Создаем примеры

# 4. Добавляем справочные материалы
# echo "# REST API Design Patterns" > plugins/$PLUGIN/skills/$SKILL/references/patterns.md

# 5. Добавляем в marketplace.json
# В секцию plugins[$PLUGIN].skills добавляем: "./skills/rest-api-patterns"

# 6. Регенерируем документацию
python scripts/generate-docs.py

# 7. Коммитим
git add plugins/$PLUGIN/skills/$SKILL .claude-plugin/marketplace.json docs/
git commit -m "feat: add REST API patterns skill"
```

## Поддержка

Если у тебя есть вопросы или предложения по улучшению шаблонов:

1. Открой issue в репозитории
2. Предложи pull request с улучшениями
3. Обсуди в discussions

## Дополнительные ресурсы

- [Anthropic Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Contributing Guidelines](../.github/CONTRIBUTING.md)
- [Architecture Documentation](../docs/architecture.md)

---

**Совет**: Начни с простых агентов и команд, затем переходи к более сложным скиллам с продвинутыми паттернами.
