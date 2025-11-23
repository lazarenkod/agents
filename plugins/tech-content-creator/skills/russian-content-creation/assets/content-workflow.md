# Russian Content Creation Workflow

## Overview

This comprehensive workflow guide demonstrates the complete process for creating, validating, and auto-saving Russian technical content. Follow these steps to produce publication-ready articles that meet professional editorial standards.

---

## Table of Contents

1. [Pre-Writing Phase](#pre-writing-phase)
2. [Content Creation Phase](#content-creation-phase)
3. [Russian Language Validation](#russian-language-validation)
4. [Auto-Save Process](#auto-save-process)
5. [Quality Assurance](#quality-assurance)
6. [Publishing Preparation](#publishing-preparation)

---

## Pre-Writing Phase

### Step 1: Define Parameters

Before writing, clearly define these parameters:

```yaml
# Content Parameters
topic: "Конкретная тема статьи"
target_publication: "habr | vc-ru | rbc | vedomosti"
content_type: "article | case-study | tutorial | research"
target_audience: "developers | founders | executives | general-business"
technical_depth: "beginner | intermediate | advanced"
estimated_length: "1500-3000 words"
```

**Questions to answer:**

- [ ] What is the main topic/problem?
- [ ] Who is the target reader?
- [ ] Which platform will this be published on?
- [ ] What type of content is this?
- [ ] What's the key takeaway or value proposition?
- [ ] Do I have metrics/data to support claims?

### Step 2: Research and Gather Materials

Collect necessary materials:

**For Technical Articles:**
- Code examples (tested and working)
- Performance metrics
- Architecture diagrams
- Screenshots or demos
- References to documentation

**For Business Content:**
- Business metrics (MRR, CAC, LTV, churn, etc.)
- Before/after comparisons
- Expert quotes
- Market data or research
- Charts and visualizations

**For Case Studies:**
- Project timeline
- Team composition
- Problem description with impact
- Solution details
- Concrete results with numbers
- Lessons learned

### Step 3: Create Outline

Structure your content:

```markdown
# Working Title

## Preview/Lead (before <cut /> for Habr)
- Hook
- Problem statement
- Value proposition

## Introduction
- Context
- Why it matters
- What reader will learn

## Main Content
### Section 1: [Topic]
### Section 2: [Topic]
### Section 3: [Topic]

## Practical Recommendations
- Actionable advice
- Best practices
- Common mistakes

## Conclusion
- Summary
- Key takeaways
- Next steps

## Resources
- Links
- References
- Additional reading
```

---

## Content Creation Phase

### Step 4: Write Initial Draft

Write content following platform-specific guidelines:

**For Habr (Technical):**
- Informal «ты» tone
- Heavy code examples with Russian comments
- Personal experience and stories
- Detailed technical explanations
- Include `<cut />` tag after preview

**For VC.ru (Business):**
- TL;DR at the top with metrics
- Business-focused language
- Before/after comparisons
- Actionable insights
- Charts and data visualizations

**For RBC/Vedomosti (Journalistic):**
- Formal third-person perspective
- Multiple expert quotes
- Objective reporting style
- Data-driven analysis
- Conservative formatting

### Step 5: Add Code Examples (if applicable)

**Write tested code with Russian comments:**

```python
# Создаем подключение к базе данных
connection = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="postgres",
    password="password"
)

# Выполняем запрос с использованием prepared statement
with connection.cursor() as cursor:
    # Используем %s для параметризации (защита от SQL injection)
    cursor.execute(
        "SELECT * FROM users WHERE created_at > %s",
        (datetime.now() - timedelta(days=7),)
    )

    # Получаем результаты
    users = cursor.fetchall()
    print(f"Найдено пользователей: {len(users)}")
```

**Best practices:**
- Test all code before including
- Add comments in Russian
- Show expected output
- Keep examples concise and focused
- Use syntax highlighting with language specification

### Step 6: Create Frontmatter

Generate YAML frontmatter with all metadata:

```yaml
---
title: "Заголовок статьи: конкретный и информативный"
subtitle: "Опциональный подзаголовок"
author: "Имя Фамилия"
date: "2025-11-20"
publication: "habr"
category: "Backend Development"
tags: ["python", "performance", "optimization", "microservices"]
language: "ru"
seo:
  description: "Краткое описание статьи для поисковых систем (150-160 символов)"
  keywords: ["ключевое слово 1", "ключевое слово 2", "ключевое слово 3"]
reading_time: "12 мин"
difficulty: "intermediate"
---
```

---

## Russian Language Validation

### Step 7: Apply Russian Typography Rules

**Replace all quotation marks:**

```python
def fix_quotes(text: str) -> str:
    """
    Заменяет английские кавычки на русские « ».

    Args:
        text: Исходный текст

    Returns:
        Текст с русскими кавычками
    """
    # Заменяем прямые кавычки
    text = text.replace('"', '«')
    text = text.replace('"', '»')

    # Обрабатываем парные кавычки
    quote_count = 0
    result = []

    for char in text:
        if char == '"':
            if quote_count % 2 == 0:
                result.append('«')
            else:
                result.append('»')
            quote_count += 1
        else:
            result.append(char)

    return ''.join(result)
```

**Replace dashes:**

```python
def fix_dashes(text: str) -> str:
    """
    Заменяет дефисы на длинные тире где необходимо.

    Args:
        text: Исходный текст

    Returns:
        Текст с правильными тире
    """
    # Паттерны для замены дефиса на длинное тире
    patterns = [
        (r' - ', ' — '),  # Дефис с пробелами → длинное тире с пробелами
        (r'^- ', '— '),   # Дефис в начале строки
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    return text
```

**Add special characters:**

```python
def add_special_chars(text: str) -> str:
    """
    Добавляет русские специальные символы.

    Args:
        text: Исходный текст

    Returns:
        Текст со специальными символами
    """
    # Заменяем # на № где уместно
    text = re.sub(r'#(\d+)', r'№\1', text)

    # Добавляем неразрывные пробелы перед единицами измерения
    units = ['Кб', 'МБ', 'ГБ', 'ТБ', 'мс', 'сек', 'мин', 'ч', '%']
    for unit in units:
        text = re.sub(rf'(\d+)\s+{unit}', rf'\1\u00A0{unit}', text)

    return text
```

### Step 8: Validate Technical Terminology

Check that technical terms follow conventions:

```python
def validate_terminology(text: str) -> List[str]:
    """
    Проверяет правильность использования технических терминов.

    Returns:
        Список найденных проблем
    """
    issues = []

    # Проверяем транслитерацию (должны использоваться английские термины)
    transliterations = [
        'дата сайнс', 'дата бэйс', 'нетворк', 'секьюрити',
        'дев опс', 'фронт энд', 'бэк энд'
    ]

    for term in transliterations:
        if term in text.lower():
            issues.append(f"Найдена транслитерация: '{term}'. Используйте английский термин.")

    # Проверяем смешанные конструкции
    mixed_patterns = [
        r'\w+\s+(continuous|integration|deployment|delivery)',
        r'(мы|наш|наша)\s+[a-z]+',
    ]

    for pattern in mixed_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            issues.append(f"Найдена смешанная конструкция: {matches}")

    return issues
```

### Step 9: Check Grammar and Style

Run style checks:

```python
def check_style(text: str, platform: str) -> Dict[str, List[str]]:
    """
    Проверяет стиль написания для конкретной платформы.

    Args:
        text: Текст статьи
        platform: Платформа публикации (habr, vc-ru, rbc, vedomosti)

    Returns:
        Словарь с найденными проблемами по категориям
    """
    issues = {
        'tone': [],
        'structure': [],
        'terminology': [],
        'formatting': []
    }

    # Проверка тона для Habr (должно быть «ты»)
    if platform == 'habr':
        if re.search(r'\bвы\b|\bвас\b|\bвам\b', text, re.IGNORECASE):
            issues['tone'].append("Habr: используйте неформальное «ты» вместо «вы»")

    # Проверка тона для VC.ru/RBC/Vedomosti (не должно быть «ты»)
    if platform in ['vc-ru', 'rbc', 'vedomosti']:
        if re.search(r'\bты\b|\bтебя\b|\bтебе\b', text, re.IGNORECASE):
            issues['tone'].append(f"{platform}: используйте «вы» или третье лицо вместо «ты»")

    # Проверка структуры
    if platform == 'habr' and '<cut />' not in text:
        issues['structure'].append("Habr: добавьте тег <cut /> для разделения превью")

    if platform == 'vc-ru' and 'TL;DR' not in text:
        issues['structure'].append("VC.ru: добавьте TL;DR в начало статьи")

    # Проверка форматирования
    if '"' in text or '"' in text:
        issues['formatting'].append("Используйте русские кавычки « » вместо английских")

    return issues
```

---

## Auto-Save Process

### Step 10: Generate Filename

Create SEO-friendly filename:

```python
from datetime import datetime
from slugify import slugify
import os


def generate_filename(title: str, language: str = 'ru') -> str:
    """
    Генерирует имя файла для статьи.

    Args:
        title: Заголовок статьи
        language: Язык статьи

    Returns:
        Имя файла в формате YYYY-MM-DD-slug-LANG.md

    Example:
        >>> generate_filename("Как мы ускорили API в 10 раз", "ru")
        '2025-11-20-kak-my-uskorili-api-v-10-raz-ru.md'
    """
    # Получаем текущую дату
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Создаем slug из заголовка
    # Транслитерация или перевод заголовка на английский для slug
    slug = slugify(title, max_length=60, word_boundary=True)

    # Формируем имя файла
    filename = f"{date_str}-{slug}-{language}.md"

    return filename


# Примеры использования
print(generate_filename("Как мы ускорили API в 10 раз"))
# 2025-11-20-kak-my-uskorili-api-v-10-raz-ru.md

print(generate_filename("Микросервисная архитектура: полное руководство"))
# 2025-11-20-mikroservisnaya-arkhitektura-polnoe-rukovodstvo-ru.md
```

### Step 11: Validate Content Structure

Check completeness before saving:

```python
def validate_article_structure(content: str) -> Dict[str, bool]:
    """
    Проверяет наличие всех необходимых элементов статьи.

    Args:
        content: Полное содержимое статьи с frontmatter

    Returns:
        Словарь с результатами проверки
    """
    validations = {
        'has_frontmatter': False,
        'has_title': False,
        'has_date': False,
        'has_tags': False,
        'has_seo_description': False,
        'has_h1_heading': False,
        'has_sections': False,
        'has_conclusion': False,
    }

    # Проверка frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        validations['has_frontmatter'] = True
        frontmatter = frontmatter_match.group(1)

        # Проверка полей frontmatter
        validations['has_title'] = 'title:' in frontmatter
        validations['has_date'] = 'date:' in frontmatter
        validations['has_tags'] = 'tags:' in frontmatter
        validations['has_seo_description'] = 'description:' in frontmatter

    # Проверка структуры контента
    validations['has_h1_heading'] = '\n# ' in content
    validations['has_sections'] = '\n## ' in content
    validations['has_conclusion'] = 'заключение' in content.lower() or 'выводы' in content.lower()

    return validations
```

### Step 12: Auto-Save to File

Save content to designated location:

```python
import os
from pathlib import Path
from typing import Optional


def save_article(
    content: str,
    title: str,
    draft: bool = False,
    output_dir: str = "/home/user/agents/outputs/articles"
) -> str:
    """
    Сохраняет статью в файловую систему.

    Args:
        content: Полное содержимое статьи с frontmatter
        title: Заголовок статьи для генерации имени файла
        draft: Если True, сохраняет в папку drafts
        output_dir: Базовая директория для сохранения

    Returns:
        Абсолютный путь к сохраненному файлу

    Raises:
        IOError: Если не удалось создать директорию или записать файл
        ValueError: Если контент пустой или невалидный
    """
    # Валидация входных данных
    if not content or not content.strip():
        raise ValueError("Контент статьи не может быть пустым")

    if not title or not title.strip():
        raise ValueError("Заголовок статьи не может быть пустым")

    # Генерируем имя файла
    filename = generate_filename(title, language='ru')

    # Определяем директорию сохранения
    if draft:
        save_dir = os.path.join(output_dir, "drafts")
    else:
        save_dir = output_dir

    # Создаем директорию если не существует
    try:
        os.makedirs(save_dir, exist_ok=True)
    except OSError as e:
        raise IOError(f"Не удалось создать директорию {save_dir}: {e}")

    # Полный путь к файлу
    filepath = os.path.join(save_dir, filename)

    # Сохраняем файл
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Не удалось записать файл {filepath}: {e}")

    print(f"✅ Статья успешно сохранена: {filepath}")
    print(f"   Размер: {len(content)} символов")
    print(f"   Имя файла: {filename}")

    return filepath


# Пример использования
article_content = """---
title: "Как мы ускорили API в 10 раз"
date: "2025-11-20"
publication: "habr"
tags: ["python", "performance", "api"]
---

# Как мы ускорили API в 10 раз

Контент статьи...
"""

# Сохранение готовой статьи
filepath = save_article(
    content=article_content,
    title="Как мы ускорили API в 10 раз",
    draft=False
)

# Сохранение черновика
draft_filepath = save_article(
    content=article_content,
    title="Как мы ускорили API в 10 раз",
    draft=True
)
```

### Step 13: Confirm Save and Return Path

After saving, confirm success:

```python
def confirm_save(filepath: str) -> Dict[str, any]:
    """
    Проверяет успешность сохранения и возвращает информацию о файле.

    Args:
        filepath: Путь к сохраненному файлу

    Returns:
        Словарь с информацией о файле
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    # Получаем информацию о файле
    file_stats = os.stat(filepath)
    file_info = {
        'path': filepath,
        'filename': os.path.basename(filepath),
        'size_bytes': file_stats.st_size,
        'size_kb': round(file_stats.st_size / 1024, 2),
        'created': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
    }

    # Считаем количество слов
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        word_count = len(content.split())
        char_count = len(content)

    file_info['word_count'] = word_count
    file_info['char_count'] = char_count
    file_info['estimated_reading_time'] = f"{round(word_count / 200)} мин"

    return file_info
```

---

## Quality Assurance

### Step 14: Run Full Quality Check

Comprehensive validation before publishing:

```python
def full_quality_check(filepath: str, platform: str) -> Dict[str, any]:
    """
    Проводит полную проверку качества статьи.

    Args:
        filepath: Путь к файлу статьи
        platform: Целевая платформа (habr, vc-ru, rbc, vedomosti)

    Returns:
        Отчет о проверке качества
    """
    # Читаем содержимое
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    report = {
        'file': filepath,
        'platform': platform,
        'passed': True,
        'checks': {},
        'issues': [],
        'warnings': [],
        'suggestions': []
    }

    # 1. Проверка структуры
    structure = validate_article_structure(content)
    report['checks']['structure'] = structure

    if not all(structure.values()):
        report['passed'] = False
        for check, result in structure.items():
            if not result:
                report['issues'].append(f"Отсутствует: {check}")

    # 2. Проверка типографики
    typography_issues = []

    if '"' in content or '"' in content:
        typography_issues.append("Найдены английские кавычки, должны быть « »")

    if re.search(r'\s-\s', content):
        typography_issues.append("Найдены дефисы с пробелами, возможно нужно длинное тире —")

    if re.search(r'#\d', content):
        typography_issues.append("Найдены # перед цифрами, возможно нужно №")

    if typography_issues:
        report['issues'].extend(typography_issues)
        report['passed'] = False

    report['checks']['typography'] = len(typography_issues) == 0

    # 3. Проверка стиля для платформы
    style_issues = check_style(content, platform)
    if any(style_issues.values()):
        report['issues'].extend([
            issue for issues in style_issues.values() for issue in issues
        ])
        report['passed'] = False

    report['checks']['platform_style'] = not any(style_issues.values())

    # 4. Проверка терминологии
    terminology_issues = validate_terminology(content)
    if terminology_issues:
        report['warnings'].extend(terminology_issues)

    report['checks']['terminology'] = len(terminology_issues) == 0

    # 5. Проверка кода (если есть)
    code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)

    if code_blocks:
        code_issues = []
        for lang, code in code_blocks:
            if not lang:
                code_issues.append("Найден блок кода без указания языка")

        if code_issues:
            report['warnings'].extend(code_issues)

    report['checks']['code_blocks'] = len(code_issues) == 0 if code_blocks else True

    # 6. SEO проверка
    seo_suggestions = []

    # Проверка длины заголовка
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        if len(title) < 30:
            seo_suggestions.append("Заголовок короткий (<30 символов), SEO можно улучшить")
        if len(title) > 70:
            seo_suggestions.append("Заголовок длинный (>70 символов), может обрезаться в поиске")

    if seo_suggestions:
        report['suggestions'].extend(seo_suggestions)

    # Итоговый статус
    report['summary'] = {
        'total_checks': len(report['checks']),
        'passed_checks': sum(1 for v in report['checks'].values() if v),
        'issues_count': len(report['issues']),
        'warnings_count': len(report['warnings']),
        'suggestions_count': len(report['suggestions'])
    }

    return report


def print_quality_report(report: Dict[str, any]):
    """Выводит отчет о проверке качества в читаемом формате."""

    print("\n" + "="*70)
    print("ОТЧЕТ О ПРОВЕРКЕ КАЧЕСТВА")
    print("="*70)

    print(f"\nФайл: {report['file']}")
    print(f"Платформа: {report['platform']}")
    print(f"Статус: {'✅ PASSED' if report['passed'] else '❌ FAILED'}")

    print("\n--- Проверки ---")
    for check, passed in report['checks'].items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")

    if report['issues']:
        print("\n--- Критические проблемы ---")
        for issue in report['issues']:
            print(f"❌ {issue}")

    if report['warnings']:
        print("\n--- Предупреждения ---")
        for warning in report['warnings']:
            print(f"⚠️  {warning}")

    if report['suggestions']:
        print("\n--- Рекомендации ---")
        for suggestion in report['suggestions']:
            print(f"💡 {suggestion}")

    print("\n--- Итого ---")
    summary = report['summary']
    print(f"Проверок пройдено: {summary['passed_checks']}/{summary['total_checks']}")
    print(f"Критических проблем: {summary['issues_count']}")
    print(f"Предупреждений: {summary['warnings_count']}")
    print(f"Рекомендаций: {summary['suggestions_count']}")

    print("="*70 + "\n")
```

### Step 15: Fix Issues

Apply automatic fixes where possible:

```python
def auto_fix_common_issues(content: str) -> tuple[str, List[str]]:
    """
    Автоматически исправляет распространенные проблемы.

    Args:
        content: Исходный контент

    Returns:
        Tuple (исправленный контент, список примененных исправлений)
    """
    fixes_applied = []
    original_content = content

    # 1. Заменяем английские кавычки на русские
    if '"' in content or '"' in content:
        content = fix_quotes(content)
        fixes_applied.append("Заменены английские кавычки на русские « »")

    # 2. Заменяем дефисы на длинные тире где нужно
    if re.search(r'\s-\s', content):
        content = fix_dashes(content)
        fixes_applied.append("Заменены дефисы на длинные тире —")

    # 3. Добавляем специальные символы
    content = add_special_chars(content)
    if content != original_content and not fixes_applied:
        fixes_applied.append("Добавлены специальные символы (№, неразрывные пробелы)")

    # 4. Удаляем множественные пробелы
    if re.search(r'\s{2,}', content):
        content = re.sub(r'\s{2,}', ' ', content)
        fixes_applied.append("Удалены множественные пробелы")

    # 5. Исправляем пробелы вокруг пунктуации
    # Удаляем пробел перед пунктуацией
    content = re.sub(r'\s+([,.:;!?])', r'\1', content)
    # Добавляем пробел после пунктуации если его нет
    content = re.sub(r'([,.:;!?])([^\s\n])', r'\1 \2', content)

    if fixes_applied:
        print(f"\n✅ Применено {len(fixes_applied)} автоматических исправлений:")
        for fix in fixes_applied:
            print(f"   - {fix}")

    return content, fixes_applied
```

---

## Publishing Preparation

### Step 16: Generate Publishing Package

Create complete package for publishing:

```python
def create_publishing_package(filepath: str, platform: str) -> Dict[str, str]:
    """
    Создает пакет для публикации на конкретной платформе.

    Args:
        filepath: Путь к статье
        platform: Целевая платформа

    Returns:
        Словарь с путями к сгенерированным файлам
    """
    package = {
        'original': filepath,
        'platform_optimized': None,
        'metadata': None,
        'checklist': None
    }

    base_dir = os.path.dirname(filepath)
    base_name = os.path.splitext(os.path.basename(filepath))[0]

    # Читаем контент
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Оптимизированная версия для платформы
    optimized_content = optimize_for_platform(content, platform)
    optimized_path = os.path.join(base_dir, f"{base_name}-{platform}.md")

    with open(optimized_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)

    package['platform_optimized'] = optimized_path

    # 2. Метаданные для публикации
    metadata = extract_metadata(content)
    metadata_path = os.path.join(base_dir, f"{base_name}-metadata.json")

    import json
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    package['metadata'] = metadata_path

    # 3. Чеклист для публикации
    checklist = generate_publishing_checklist(platform)
    checklist_path = os.path.join(base_dir, f"{base_name}-checklist.md")

    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(checklist)

    package['checklist'] = checklist_path

    print(f"\n📦 Пакет для публикации создан:")
    print(f"   Оптимизированная версия: {optimized_path}")
    print(f"   Метаданные: {metadata_path}")
    print(f"   Чеклист: {checklist_path}")

    return package


def generate_publishing_checklist(platform: str) -> str:
    """Генерирует чеклист для публикации на конкретной платформе."""

    checklists = {
        'habr': """
# Чеклист публикации на Habr

## Перед публикацией
- [ ] Тег <cut /> размещен после 150-300 слов
- [ ] Все блоки кода имеют указание языка
- [ ] Использован неформальный тон («ты»)
- [ ] Выбраны 2-5 релевантных хабов
- [ ] Все кавычки заменены на « »
- [ ] Код протестирован и работает
- [ ] Добавлены комментарии к коду на русском

## Форматирование
- [ ] Большие блоки кода в <spoiler>
- [ ] Изображения оптимизированы и имеют alt
- [ ] Таблицы корректно отображаются
- [ ] Ссылки рабочие

## Контент
- [ ] Заголовок конкретный и информативный
- [ ] Есть введение с описанием что будет в статье
- [ ] Практические примеры и код
- [ ] Заключение с выводами
- [ ] Ссылки на ресурсы

## После публикации
- [ ] Проверить отображение
- [ ] Отвечать на комментарии
- [ ] Поделиться в соцсетях
""",
        'vc-ru': """
# Чеклист публикации на VC.ru

## Перед публикацией
- [ ] TL;DR в начале с ключевыми метриками
- [ ] Формальный тон («вы» или третье лицо)
- [ ] Все утверждения подкреплены цифрами
- [ ] Таблицы до/после с метриками
- [ ] Выбрана правильная категория
- [ ] Ключевые моменты выделены **жирным**

## Визуальные элементы
- [ ] Графики и чарты добавлены
- [ ] Скриншоты dashboard'ов или метрик
- [ ] Обложка загружена

## Контент
- [ ] Заголовок с конкретным результатом/цифрой
- [ ] Бизнес-фокус (не слишком технично)
- [ ] Actionable выводы и рекомендации
- [ ] Раздел "Что можно сделать прямо сейчас"

## SEO
- [ ] Мета-описание заполнено (150-160 символов)
- [ ] Релевантные теги выбраны
- [ ] Alt text для изображений

## После публикации
- [ ] Поделиться в Telegram-каналах
- [ ] Отвечать на комментарии
- [ ] Отслеживать метрики (views, engagement)
""",
        'rbc': """
# Чеклист публикации на RBC

## Перед публикацией
- [ ] Третье лицо throughout (никакого «я», «мы», «вы»)
- [ ] Все факты проверены и имеют источники
- [ ] Минимум 2-3 экспертные цитаты
- [ ] Дата и место в лиде
- [ ] Формальный журналистский стиль
- [ ] Нейтральный, объективный тон

## Структура
- [ ] Inverted pyramid (важное в начале)
- [ ] Короткие параграфы (2-3 предложения)
- [ ] Четкие topic sentences

## Факты и источники
- [ ] Все статистика имеет источник
- [ ] Прямые цитаты правильно атрибутированы
- [ ] Ссылки на исследования и отчеты
- [ ] Полные имена, должности, компании

## После написания
- [ ] Fact-checking всех утверждений
- [ ] Проверка баланса (разные точки зрения)
- [ ] Вычитка на ошибки
- [ ] Compliance с редакционной политикой
"""
    }

    return checklists.get(platform, "Чеклист для этой платформы не найден")
```

---

## Complete Workflow Example

### Full End-to-End Process

```python
#!/usr/bin/env python3
"""
Полный workflow создания и сохранения русской технической статьи.
"""

from datetime import datetime
from typing import Dict, List
import os


class RussianContentWorkflow:
    """Класс для управления полным workflow создания контента."""

    def __init__(self, output_dir: str = "/home/user/agents/outputs/articles"):
        """
        Инициализирует workflow.

        Args:
            output_dir: Директория для сохранения статей
        """
        self.output_dir = output_dir
        self.current_article = None
        self.current_filepath = None

    def create_article(
        self,
        topic: str,
        platform: str,
        content_type: str,
        author: str = "Имя Фамилия"
    ) -> str:
        """
        Создает новую статью с полным workflow.

        Args:
            topic: Тема статьи
            platform: Целевая платформа
            content_type: Тип контента
            author: Имя автора

        Returns:
            Путь к сохраненному файлу
        """
        print(f"\n{'='*70}")
        print(f"СОЗДАНИЕ СТАТЬИ: {topic}")
        print(f"Платформа: {platform} | Тип: {content_type}")
        print(f"{'='*70}\n")

        # Шаг 1: Генерация контента
        print("📝 Шаг 1: Генерация контента...")
        content = self._generate_content(topic, platform, content_type, author)

        # Шаг 2: Применение русских правил
        print("🔤 Шаг 2: Применение русской типографики...")
        content, fixes = auto_fix_common_issues(content)

        # Шаг 3: Валидация
        print("✓ Шаг 3: Валидация контента...")
        structure_valid = validate_article_structure(content)
        if not all(structure_valid.values()):
            print("⚠️  Предупреждение: некоторые элементы структуры отсутствуют")

        # Шаг 4: Сохранение
        print("💾 Шаг 4: Сохранение файла...")
        filepath = save_article(content, topic, draft=False, output_dir=self.output_dir)

        # Шаг 5: Проверка качества
        print("🔍 Шаг 5: Проверка качества...")
        quality_report = full_quality_check(filepath, platform)
        print_quality_report(quality_report)

        # Шаг 6: Создание пакета для публикации
        if quality_report['passed']:
            print("📦 Шаг 6: Создание пакета для публикации...")
            package = create_publishing_package(filepath, platform)

            print(f"\n{'='*70}")
            print("✅ СТАТЬЯ УСПЕШНО СОЗДАНА И ГОТОВА К ПУБЛИКАЦИИ")
            print(f"{'='*70}")
            print(f"\nОсновной файл: {filepath}")
            print(f"Версия для {platform}: {package['platform_optimized']}")
            print(f"Чеклист: {package['checklist']}")

        else:
            print(f"\n{'='*70}")
            print("⚠️  СТАТЬЯ СОЗДАНА, НО ТРЕБУЕТ ДОРАБОТКИ")
            print(f"{'='*70}")
            print(f"\nФайл сохранен: {filepath}")
            print("Исправьте найденные проблемы перед публикацией.")

        self.current_filepath = filepath
        return filepath

    def _generate_content(
        self,
        topic: str,
        platform: str,
        content_type: str,
        author: str
    ) -> str:
        """
        Генерирует контент статьи.

        В реальном использовании здесь будет AI-генерация или шаблонизация.
        """
        # Здесь placeholder - в реальности это AI-генерация
        template = self._get_template(platform, content_type)

        content = template.format(
            title=topic,
            author=author,
            date=datetime.now().strftime("%Y-%m-%d"),
            platform=platform
        )

        return content

    def _get_template(self, platform: str, content_type: str) -> str:
        """Возвращает шаблон для указанной платформы и типа контента."""

        # Базовый шаблон (можно расширить)
        return """---
title: "{title}"
author: "{author}"
date: "{date}"
publication: "{platform}"
category: "Technology"
tags: ["tech", "development"]
language: "ru"
seo:
  description: "Описание статьи"
  keywords: ["keyword1", "keyword2"]
reading_time: "10 мин"
difficulty: "intermediate"
---

# {title}

Введение в тему...

## Основная часть

Контент статьи...

## Заключение

Выводы и рекомендации...
"""


# Пример использования
if __name__ == "__main__":
    # Создаем workflow
    workflow = RussianContentWorkflow()

    # Создаем статью
    article_path = workflow.create_article(
        topic="Как мы ускорили Python API в 10 раз",
        platform="habr",
        content_type="article",
        author="Иван Петров"
    )

    print(f"\n✅ Workflow завершен!")
    print(f"Файл доступен по адресу: {article_path}")
```

---

## Summary

This workflow ensures:

1. **Structured Process:** Clear steps from ideation to publishing
2. **Quality Control:** Automated validation and error checking
3. **Russian Standards:** Proper typography, terminology, and style
4. **Auto-Save:** Automatic file naming and saving to designated location
5. **Platform Optimization:** Content adapted for specific publication requirements
6. **Publication Ready:** Complete package with checklists and metadata

**Key Output:**
- Markdown file saved to `/home/user/agents/outputs/articles/YYYY-MM-DD-slug-ru.md`
- Platform-optimized version
- Publishing checklist
- Quality assurance report

---

**Last updated:** 2025-11-20
