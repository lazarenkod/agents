---
name: regenerate-docs
description: Автоматическая регенерация документации маркетплейса из структуры репозитория
---

# Регенерация документации

Эта команда автоматически сканирует структуру репозитория и обновляет всю документацию в директории `docs/`.

## Что обновляется

- `docs/plugins.md` - каталог всех плагинов
- `docs/agents.md` - справочник по всем агентам
- `docs/agent-skills.md` - руководство по скиллам
- `docs/usage.md` - руководство по использованию команд
- `docs/architecture.md` - архитектура маркетплейса

## Использование

```bash
/regenerate-docs
```

Или напрямую через Python:

```bash
python scripts/generate-docs.py
```

## Когда использовать

Запускайте эту команду после:

- Добавления нового плагина
- Создания нового агента
- Добавления нового скилла
- Создания новой команды
- Изменения описаний или метаданных

## Автоматизация

### Pre-commit hook

Для автоматической регенерации документации при коммите создайте `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python scripts/generate-docs.py
git add docs/*.md
```

### GitHub Actions

Добавьте в `.github/workflows/docs.yml`:

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

## Процесс генерации

1. Сканирование структуры `plugins/`
2. Чтение `.claude-plugin/marketplace.json`
3. Извлечение метаданных из frontmatter файлов
4. Группировка по категориям и плагинам
5. Генерация markdown документов с актуальной информацией

## Вывод

После выполнения команда показывает статистику:

- Количество найденных плагинов
- Количество агентов
- Количество скиллов
- Количество команд
- Список обновленных файлов
