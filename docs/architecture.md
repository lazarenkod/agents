# Architecture - Архитектура маркетплейса

> Автоматически сгенерировано из структуры репозитория

## Обзор системы

Claude Code Plugins Marketplace - это production-ready система для организации и оркестрации AI агентов.

### Текущая статистика

- **Плагины:** 82
- **Агенты:** 204
- **Скиллы:** 154
- **Команды:** 123

## Принципы проектирования

### 1. Гранулярность и фокус

Каждый плагин фокусируется на одной предметной области:

```
plugins/
├── backend-development/     # Backend разработка
├── frontend-mobile/         # Frontend/Mobile
├── database-design/         # Database проектирование
└── ...
```

Среднее количество компонентов на плагин: **5.9**

### 2. Изоляция компонентов

Каждый плагин содержит все необходимые компоненты:

```
plugin/
├── agents/          # Агенты для рассуждения
├── commands/        # Команды для выполнения
└── skills/          # Скиллы для знаний
```

### 3. Оптимизация использования токенов

- Минимальный размер плагинов
- Прогрессивное раскрытие в скиллах
- Ленивая загрузка компонентов
- Установка только необходимых плагинов

### 4. Специализация агентов

Агенты оптимизированы под конкретные задачи:

- **Haiku агенты (52)** - Быстрая генерация кода, тесты, документация
- **Sonnet агенты (152)** - Архитектура, дизайн, аудит
- **Opus агенты (0)** - Критически сложные задачи

## Паттерны архитектуры

### Паттерн 1: Domain-Focused Plugin

Каждый плагин сфокусирован на домене с со-расположенной экспертизой:

```
backend-development/
├── agents/
│   ├── backend-architect.md      # Архитектура
│   ├── api-developer.md          # Разработка
│   └── tdd-orchestrator.md       # Тестирование
├── commands/
│   └── feature-development.md     # Workflow
└── skills/
    ├── api-design-principles/     # Знания по API
    └── architecture-patterns/     # Паттерны архитектуры
```

### Паттерн 2: Workflow Orchestration

Сложные workflow координируют несколько агентов:

```
User request
  ↓
Orchestrator Agent (backend-architect)
  ↓
Database Architect → Frontend Developer → Test Automator
  ↓
Security Auditor → Deployment Engineer
  ↓
Result
```

### Паттерн 3: Progressive Skill Disclosure

Скиллы загружают знания поэтапно:

1. **Метаданные** (всегда) - название, триггер
2. **Инструкции** (при активации) - основы, паттерны
3. **Ресурсы** (по требованию) - примеры, шаблоны

## Структура данных

### Marketplace Manifest

`.claude-plugin/marketplace.json` - центральный реестр:

```json
{
  "name": "claude-agents",
  "metadata": {
    "description": "...",
    "version": "1.4.0"
  },
  "plugins": [...]
}
```

### Plugin Structure

```
plugin-name/
├── agents/              # AI агенты с system prompts
│   └── agent.md        # YAML frontmatter + Markdown
├── commands/            # Исполняемые команды
│   └── command.md      # YAML frontmatter + Markdown
└── skills/             # Базы знаний
    └── skill-name/     # Директория скилла
        ├── SKILL.md    # Основной файл
        ├── references/ # Справка
        └── assets/     # Шаблоны
```

### Frontmatter Format

**Агенты:**
```yaml
---
name: agent-identifier
description: What it does. Use PROACTIVELY when [trigger].
model: sonnet|haiku|opus
---
```

**Скиллы:**
```yaml
---
name: skill-identifier
description: What it teaches. Use when [trigger].
---
```

**Команды:**
```yaml
---
name: command-identifier
description: What it does
---
```

## Стратегия выбора модели

### Haiku - Скорость и детерминизм

Использование:
- Генерация кода по спецификации
- Создание тестов по шаблонам
- Генерация документации
- Операции с инфраструктурой
- Scaffolding инструменты

### Sonnet - Сложное мышление

Использование:
- Проектирование системной архитектуры
- Принятие решений по технологиям
- Аудит безопасности и ревью
- Ревью качества кода
- ML/AI pipeline дизайн
- Язык-специфичная экспертиза
- Оркестрация workflow

### Opus - Максимальная сложность

Использование:
- Критически сложные архитектурные решения
- Исследование больших кодовых баз
- Комплексная оптимизация

## Расширяемость

### Добавление нового плагина

1. Создайте директорию: `plugins/{plugin-name}/`
2. Добавьте компоненты (agents/commands/skills)
3. Зарегистрируйте в `marketplace.json`
4. Запустите `/regenerate-docs`

### Автоматизация документации

Документация автоматически генерируется из структуры:

```bash
python scripts/generate-docs.py
```

Обновляет:
- `docs/plugins.md`
- `docs/agents.md`
- `docs/agent-skills.md`
- `docs/usage.md`
- `docs/architecture.md`

## Категории плагинов

- **accessibility**: 1 плагинов
- **ai-architecture**: 1 плагинов
- **ai-development**: 1 плагинов
- **ai-ml**: 5 плагинов
- **api**: 2 плагинов
- **blockchain**: 1 плагинов
- **business**: 8 плагинов
- **cloud**: 1 плагинов
- **code-analysis**: 1 плагинов
- **data**: 2 плагинов
- **database**: 3 плагинов
- **development**: 4 плагинов
- **documentation**: 2 плагинов
- **enterprise**: 1 плагинов
- **executive-leadership**: 1 плагинов
- **finance**: 2 плагинов
- **gaming**: 1 плагинов
- **infrastructure**: 6 плагинов
- **languages**: 8 плагинов
- **leadership**: 1 плагинов
- **marketing**: 5 плагинов
- **modernization**: 2 плагинов
- **operations**: 5 плагинов
- **payments**: 1 плагинов
- **performance**: 2 плагинов
- **quality**: 3 плагинов
- **security**: 4 плагинов
- **testing**: 1 плагинов
- **utilities**: 4 плагинов
- **workflows**: 3 плагинов


## Best Practices

1. **Один плагин = одна область** - избегайте смешивания доменов
2. **Минимальный размер** - только необходимые компоненты
3. **Четкие триггеры** - описывайте когда использовать агента/скилл
4. **Правильная модель** - выбирайте модель по сложности задачи
5. **Прогрессивное раскрытие** - структурируйте скиллы поэтапно
6. **Документация** - поддерживайте актуальность через автогенерацию

## Интеграция и CI/CD

### Pre-commit хук

Автоматическая регенерация документации:

```bash
#!/bin/bash
# .git/hooks/pre-commit
python scripts/generate-docs.py
git add docs/*.md
```

### GitHub Actions

Проверка актуальности документации:

```yaml
- name: Generate docs
  run: python scripts/generate-docs.py

- name: Check for changes
  run: git diff --exit-code docs/
```

## Производительность

### Оптимизация токенов

- Средний размер плагина: ~3-5 компонентов
- Lazy loading скиллов
- Избирательная установка плагинов

### Время активации

- Haiku агенты: ~1-2 сек
- Sonnet агенты: ~3-5 сек
- Opus агенты: ~10-15 сек

## Roadmap

- [ ] Автоматическая валидация структуры плагинов
- [ ] Система версионирования плагинов
- [ ] Dependency management между плагинами
- [ ] Метрики использования агентов
- [ ] A/B тестирование промптов
