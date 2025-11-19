#!/usr/bin/env python3
"""
Автоматическая генерация документации для Claude Code Plugins Marketplace
Сканирует все плагины, агенты, команды и скиллы и генерирует актуальную документацию
"""

import json
import os
from pathlib import Path
import re
from typing import Dict, List, Any
from collections import defaultdict

# Базовый путь к репозиторию
BASE_DIR = Path(__file__).parent.parent
PLUGINS_DIR = BASE_DIR / "plugins"
DOCS_DIR = BASE_DIR / "docs"
MARKETPLACE_FILE = BASE_DIR / ".claude-plugin" / "marketplace.json"


def read_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Читает YAML frontmatter из markdown файла"""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding='utf-8')

    # Ищем frontmatter между --- и ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter_text = match.group(1)
    result = {}

    # Простой парсер YAML (только базовые поля)
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"').strip("'")

    return result


def get_markdown_content(file_path: Path) -> str:
    """Получает содержимое markdown файла без frontmatter"""
    if not file_path.exists():
        return ""

    content = file_path.read_text(encoding='utf-8')

    # Удаляем frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Получаем первый параграф или описание
    lines = content.strip().split('\n')
    description_lines = []

    for line in lines:
        if line.startswith('#'):
            continue
        if line.strip():
            description_lines.append(line.strip())
            if len(description_lines) >= 3:
                break

    return ' '.join(description_lines)


def scan_plugins() -> Dict[str, Any]:
    """Сканирует все плагины и собирает информацию"""
    plugins_data = {
        'plugins': [],
        'agents': [],
        'skills': [],
        'commands': [],
        'stats': {
            'total_plugins': 0,
            'total_agents': 0,
            'total_skills': 0,
            'total_commands': 0,
            'agents_by_model': {'haiku': 0, 'sonnet': 0, 'opus': 0},
            'plugins_by_category': defaultdict(int)
        }
    }

    # Читаем marketplace.json если существует
    marketplace_data = {}
    if MARKETPLACE_FILE.exists():
        with open(MARKETPLACE_FILE, 'r', encoding='utf-8') as f:
            marketplace_data = json.load(f)

    marketplace_plugins = {p['name']: p for p in marketplace_data.get('plugins', [])}

    # Сканируем директорию plugins
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue

        plugin_name = plugin_dir.name
        plugin_info = {
            'name': plugin_name,
            'path': str(plugin_dir.relative_to(BASE_DIR)),
            'agents': [],
            'commands': [],
            'skills': [],
            'description': '',
            'version': '1.0.0',
            'category': 'general'
        }

        # Получаем информацию из marketplace.json если есть
        if plugin_name in marketplace_plugins:
            mp_plugin = marketplace_plugins[plugin_name]
            plugin_info['description'] = mp_plugin.get('description', '')
            plugin_info['version'] = mp_plugin.get('version', '1.0.0')
            plugin_info['category'] = mp_plugin.get('category', 'general')

        # Сканируем агентов
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            for agent_file in sorted(agents_dir.glob("*.md")):
                frontmatter = read_frontmatter(agent_file)
                agent_info = {
                    'name': frontmatter.get('name', agent_file.stem),
                    'file': str(agent_file.relative_to(BASE_DIR)),
                    'plugin': plugin_name,
                    'description': frontmatter.get('description', ''),
                    'model': frontmatter.get('model', 'sonnet')
                }
                plugin_info['agents'].append(agent_info)
                plugins_data['agents'].append(agent_info)

                # Статистика по моделям
                model = agent_info['model'].lower()
                if model in plugins_data['stats']['agents_by_model']:
                    plugins_data['stats']['agents_by_model'][model] += 1

        # Сканируем команды
        commands_dir = plugin_dir / "commands"
        if commands_dir.exists():
            for command_file in sorted(commands_dir.glob("*.md")):
                frontmatter = read_frontmatter(command_file)
                command_info = {
                    'name': frontmatter.get('name', command_file.stem),
                    'file': str(command_file.relative_to(BASE_DIR)),
                    'plugin': plugin_name,
                    'description': frontmatter.get('description', '')
                }
                plugin_info['commands'].append(command_info)
                plugins_data['commands'].append(command_info)

        # Сканируем скиллы
        skills_dir = plugin_dir / "skills"
        if skills_dir.exists():
            for skill_dir in sorted(skills_dir.iterdir()):
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        frontmatter = read_frontmatter(skill_file)
                        skill_info = {
                            'name': frontmatter.get('name', skill_dir.name),
                            'file': str(skill_file.relative_to(BASE_DIR)),
                            'plugin': plugin_name,
                            'description': frontmatter.get('description', '')
                        }
                        plugin_info['skills'].append(skill_info)
                        plugins_data['skills'].append(skill_info)

        # Добавляем плагин только если он имеет компоненты
        if plugin_info['agents'] or plugin_info['commands'] or plugin_info['skills']:
            plugins_data['plugins'].append(plugin_info)
            plugins_data['stats']['plugins_by_category'][plugin_info['category']] += 1

    # Обновляем статистику
    plugins_data['stats']['total_plugins'] = len(plugins_data['plugins'])
    plugins_data['stats']['total_agents'] = len(plugins_data['agents'])
    plugins_data['stats']['total_skills'] = len(plugins_data['skills'])
    plugins_data['stats']['total_commands'] = len(plugins_data['commands'])

    return plugins_data


def generate_plugins_md(data: Dict[str, Any]) -> str:
    """Генерирует docs/plugins.md"""
    content = f"""# Claude Code Plugins Catalog

> Автоматически сгенерировано из структуры репозитория

## Обзор

Маркетплейс содержит **{data['stats']['total_plugins']} плагинов**, организованных по категориям для эффективного использования.

### Статистика

- **Плагины:** {data['stats']['total_plugins']}
- **Агенты:** {data['stats']['total_agents']}
- **Скиллы:** {data['stats']['total_skills']}
- **Команды:** {data['stats']['total_commands']}

### Распределение агентов по моделям

- **Haiku:** {data['stats']['agents_by_model']['haiku']} (быстрые, детерминированные задачи)
- **Sonnet:** {data['stats']['agents_by_model']['sonnet']} (сложное мышление, архитектура)
- **Opus:** {data['stats']['agents_by_model']['opus']} (максимально сложные задачи)

## Плагины по категориям

"""

    # Группируем плагины по категориям
    by_category = defaultdict(list)
    for plugin in data['plugins']:
        by_category[plugin['category']].append(plugin)

    # Сортируем категории
    for category in sorted(by_category.keys()):
        plugins = by_category[category]
        content += f"\n### {category.title()} ({len(plugins)})\n\n"

        for plugin in sorted(plugins, key=lambda p: p['name']):
            content += f"#### {plugin['name']}\n\n"
            if plugin['description']:
                content += f"{plugin['description']}\n\n"

            content += f"**Версия:** {plugin['version']}  \n"
            content += f"**Путь:** `{plugin['path']}`\n\n"

            if plugin['agents']:
                content += f"**Агенты:** {len(plugin['agents'])}  \n"
            if plugin['commands']:
                content += f"**Команды:** {len(plugin['commands'])}  \n"
            if plugin['skills']:
                content += f"**Скиллы:** {len(plugin['skills'])}  \n"

            content += "\n"

    content += """
## Установка плагинов

Для установки конкретного плагина:

```bash
# Клонируйте репозиторий
git clone https://github.com/lazarenkod/agents.git

# Установите нужный плагин
cd agents
# Плагины устанавливаются автоматически при использовании
```

## Использование

После установки плагины доступны через:

1. **Агенты** - используются автоматически при соответствующих задачах
2. **Команды** - вызываются через slash-команды (например, `/command-name`)
3. **Скиллы** - загружаются по требованию для специфических знаний

## Разработка

Для добавления нового плагина см. [CONTRIBUTING.md](../.github/CONTRIBUTING.md)
"""

    return content


def generate_agents_md(data: Dict[str, Any]) -> str:
    """Генерирует docs/agents.md"""
    content = f"""# Claude Code Agents Reference

> Автоматически сгенерировано из структуры репозитория

## Обзор

Маркетплейс содержит **{data['stats']['total_agents']} специализированных агентов** для различных задач разработки.

### Распределение по моделям

- **Haiku ({data['stats']['agents_by_model']['haiku']})** - Быстрое выполнение, детерминированные задачи
- **Sonnet ({data['stats']['agents_by_model']['sonnet']})** - Сложное мышление, архитектурные решения
- **Opus ({data['stats']['agents_by_model']['opus']})** - Максимально сложные задачи

## Все агенты

"""

    # Группируем агентов по плагинам
    by_plugin = defaultdict(list)
    for agent in data['agents']:
        by_plugin[agent['plugin']].append(agent)

    # Сортируем по плагинам
    for plugin_name in sorted(by_plugin.keys()):
        agents = by_plugin[plugin_name]
        content += f"\n### Плагин: {plugin_name}\n\n"

        for agent in sorted(agents, key=lambda a: a['name']):
            model_badge = agent['model'].upper()
            content += f"#### {agent['name']} `[{model_badge}]`\n\n"

            if agent['description']:
                content += f"{agent['description']}\n\n"

            content += f"**Файл:** `{agent['file']}`  \n"
            content += f"**Модель:** {agent['model']}\n\n"

    content += """
## Использование агентов

Агенты активируются автоматически на основе описания задачи. Для явного вызова агента:

```
Используй агента [agent-name] для [описание задачи]
```

## Модели агентов

### Haiku
Используется для:
- Генерация кода по спецификациям
- Создание тестов по шаблонам
- Генерация документации
- Операции с инфраструктурой

### Sonnet
Используется для:
- Проектирование архитектуры систем
- Принятие решений по выбору технологий
- Аудит безопасности
- Ревью качества кода
- Проектирование ML/AI пайплайнов

### Opus
Используется для:
- Критически сложные архитектурные решения
- Исследование и анализ больших кодовых баз
- Комплексная оптимизация производительности
"""

    return content


def generate_skills_md(data: Dict[str, Any]) -> str:
    """Генерирует docs/agent-skills.md"""
    content = f"""# Agent Skills Guide

> Автоматически сгенерировано из структуры репозитория

## Обзор

Маркетплейс содержит **{data['stats']['total_skills']} специализированных скиллов** с прогрессивным раскрытием знаний.

## Архитектура скиллов

Скиллы используют трехуровневую архитектуру:

1. **Метаданные** (всегда загружены) - имя и триггер активации
2. **Инструкции** (при активации) - основные концепции и паттерны
3. **Ресурсы** (по требованию) - примеры, шаблоны, продвинутые паттерны

## Все скиллы

"""

    # Группируем скиллы по плагинам
    by_plugin = defaultdict(list)
    for skill in data['skills']:
        by_plugin[skill['plugin']].append(skill)

    # Сортируем по плагинам
    for plugin_name in sorted(by_plugin.keys()):
        skills = by_plugin[plugin_name]
        content += f"\n### Плагин: {plugin_name}\n\n"

        for skill in sorted(skills, key=lambda s: s['name']):
            content += f"#### {skill['name']}\n\n"

            if skill['description']:
                content += f"{skill['description']}\n\n"

            content += f"**Файл:** `{skill['file']}`\n\n"

    content += """
## Использование скиллов

Скиллы активируются автоматически когда агенту нужны специализированные знания:

```
Claude Code автоматически загружает нужный скилл на основе контекста задачи
```

## Создание скиллов

Структура скилла:

```
plugins/{plugin}/skills/{skill-name}/
├── SKILL.md              # Основной файл с метаданными и инструкциями
├── references/           # Справочные материалы
│   └── patterns.md
└── assets/              # Шаблоны и примеры
    └── templates/
```

Frontmatter формат:

```yaml
---
name: skill-identifier
description: Что изучает скилл. Use when [триггер активации].
---
```

## Спецификация

Скиллы следуют [Anthropic Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
"""

    return content


def generate_usage_md(data: Dict[str, Any]) -> str:
    """Генерирует docs/usage.md"""
    content = f"""# Usage Guide - Руководство по использованию

> Автоматически сгенерировано из структуры репозитория

## Обзор

Маркетплейс предоставляет **{data['stats']['total_commands']} команд** для автоматизации различных задач разработки.

## Команды по плагинам

"""

    # Группируем команды по плагинам
    by_plugin = defaultdict(list)
    for command in data['commands']:
        by_plugin[command['plugin']].append(command)

    # Сортируем по плагинам
    for plugin_name in sorted(by_plugin.keys()):
        commands = by_plugin[plugin_name]
        content += f"\n### Плагин: {plugin_name}\n\n"

        for command in sorted(commands, key=lambda c: c['name']):
            content += f"#### /{command['name']}\n\n"

            if command['description']:
                content += f"{command['description']}\n\n"

            content += f"**Файл:** `{command['file']}`\n\n"
            content += f"**Использование:**\n```\n/{command['name']}\n```\n\n"

    content += """
## Общие workflow

### Разработка новой функции

```bash
# 1. Используйте агента для проектирования
"Спроектируй архитектуру для [описание функции]"

# 2. Сгенерируйте код
"Реализуй спроектированную архитектуру"

# 3. Добавьте тесты
/generate-tests

# 4. Запустите проверки
/run-tests
/lint-code
```

### Рефакторинг кода

```bash
# 1. Анализ кода
"Проанализируй текущую структуру [компонента]"

# 2. Рефакторинг
"Отрефактори с применением [паттерн]"

# 3. Проверка
/run-tests
```

### Деплой

```bash
# 1. Подготовка
/build

# 2. Проверка
/validate-deployment

# 3. Деплой
/deploy [environment]
```

## Интеграция с Git

Для работы с Git доступны команды:

```bash
/create-branch [name]
/commit [message]
/create-pr [title]
```

## Конфигурация

Настройка плагинов через `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "...",
      "commands": ["./commands/command.md"],
      "agents": ["./agents/agent.md"],
      "skills": ["./skills/skill"]
    }
  ]
}
```

## Расширение функциональности

Для добавления собственных команд:

1. Создайте файл `plugins/{plugin}/commands/{command}.md`
2. Добавьте frontmatter с описанием
3. Опишите логику команды в markdown
4. Обновите `marketplace.json`
5. Запустите `/regenerate-docs` для обновления документации
"""

    return content


def generate_architecture_md(data: Dict[str, Any]) -> str:
    """Генерирует docs/architecture.md"""
    content = f"""# Architecture - Архитектура маркетплейса

> Автоматически сгенерировано из структуры репозитория

## Обзор системы

Claude Code Plugins Marketplace - это production-ready система для организации и оркестрации AI агентов.

### Текущая статистика

- **Плагины:** {data['stats']['total_plugins']}
- **Агенты:** {data['stats']['total_agents']}
- **Скиллы:** {data['stats']['total_skills']}
- **Команды:** {data['stats']['total_commands']}

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

Среднее количество компонентов на плагин: **{(data['stats']['total_agents'] + data['stats']['total_skills'] + data['stats']['total_commands']) / max(data['stats']['total_plugins'], 1):.1f}**

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

- **Haiku агенты ({data['stats']['agents_by_model']['haiku']})** - Быстрая генерация кода, тесты, документация
- **Sonnet агенты ({data['stats']['agents_by_model']['sonnet']})** - Архитектура, дизайн, аудит
- **Opus агенты ({data['stats']['agents_by_model']['opus']})** - Критически сложные задачи

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
{{
  "name": "claude-agents",
  "metadata": {{
    "description": "...",
    "version": "1.4.0"
  }},
  "plugins": [...]
}}
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

1. Создайте директорию: `plugins/{{plugin-name}}/`
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

"""

    # Добавляем статистику по категориям
    for category, count in sorted(data['stats']['plugins_by_category'].items()):
        content += f"- **{category}**: {count} плагинов\n"

    content += """

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
"""

    return content


def main():
    """Основная функция генерации документации"""
    print("🔍 Сканирую структуру репозитория...")
    data = scan_plugins()

    print(f"✅ Найдено:")
    print(f"   - Плагинов: {data['stats']['total_plugins']}")
    print(f"   - Агентов: {data['stats']['total_agents']}")
    print(f"   - Скиллов: {data['stats']['total_skills']}")
    print(f"   - Команд: {data['stats']['total_commands']}")

    # Создаем директорию docs если не существует
    DOCS_DIR.mkdir(exist_ok=True)

    print("\n📝 Генерирую документацию...")

    # Генерируем документы
    docs_to_generate = [
        ('plugins.md', generate_plugins_md),
        ('agents.md', generate_agents_md),
        ('agent-skills.md', generate_skills_md),
        ('usage.md', generate_usage_md),
        ('architecture.md', generate_architecture_md)
    ]

    for filename, generator_func in docs_to_generate:
        filepath = DOCS_DIR / filename
        content = generator_func(data)
        filepath.write_text(content, encoding='utf-8')
        print(f"   ✅ {filename}")

    print("\n✨ Документация успешно сгенерирована!")
    print(f"\nФайлы обновлены в: {DOCS_DIR}")


if __name__ == "__main__":
    main()
