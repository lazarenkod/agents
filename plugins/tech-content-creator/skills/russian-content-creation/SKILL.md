---
name: russian-content-creation
description: Comprehensive skill for creating publication-ready Russian technical content for Habr, VC.ru, RBC, and Vedomosti. Use when creating Russian technical articles, case studies, tutorials, or research content that needs to meet professional editorial standards.
---

# Russian Content Creation

## Purpose

This skill enables the creation of senior-level, publication-ready Russian technical content that meets the editorial standards of leading Russian platforms: Habr.com, VC.ru, RBC, and Vedomosti. The skill covers Russian writing conventions, technical terminology, typographic rules, platform-specific formatting, and automated content saving workflows.

## When to Use This Skill

- Creating Russian technical articles, blog posts, or tutorials
- Writing case studies or research reports for Russian audience
- Preparing content for specific Russian publications (Habr, VC.ru, RBC, Vedomosti)
- Translating and adapting technical content from English to Russian
- Optimizing content for Russian search engines (Yandex, Google RU)
- Ensuring proper Russian typography and linguistic conventions

## Core Russian Writing Standards

### Typography Rules

**Quotation Marks:**
- Use « » (French guillemets) for primary quotes: «кавычки»
- Use „ " for nested quotes: «внешние „внутренние" кавычки»
- NEVER use English quotes " " in Russian text

**Dashes and Hyphens:**
- Em dash (—) with spaces for sentence breaks: «Технология — это инструмент»
- Hyphen (-) without spaces in compound words: «full-stack-разработчик»
- En dash (–) for ranges: «2020–2025»

**Special Characters:**
- Use № for numbers: «версия №5», «пункт №3»
- Use proper spacing: no space before № but space after
- Use точка (.) for decimals in numbers: «3.14» or «3,14» (both acceptable)

**Spacing and Punctuation:**
- No space before punctuation: «текст,» «текст.» «текст;»
- Space after punctuation: «Текст. Еще текст.»
- Non-breaking space before units: «100 Кб», «5 мс», «30 %»

### Tone and Voice

**For Technical Articles (Habr):**
- Professional but conversational
- Direct address to reader using «вы» (formal) or «ты» (informal, Habr-style)
- Balance between accessibility and technical depth
- Use real-world examples and practical applications

**For Business Content (VC.ru, RBC, Vedomosti):**
- Formal, journalistic style
- Third-person perspective
- Focus on business impact and ROI
- Include expert quotes and statistics
- More conservative, less colloquial

### Technical Terminology

**Translation Approach:**
1. Use established Russian terms when they exist
2. Keep English terms in Latin script for widely adopted concepts
3. Provide Russian translation in parentheses on first use
4. Maintain consistency throughout the article

**Examples:**
- ✅ «DevOps-практики»
- ✅ «Continuous Integration (непрерывная интеграция, CI)»
- ✅ «микросервисная архитектура»
- ❌ «дев опс» (don't transliterate)
- ❌ «continuous интеграция» (mixed language)

See [Russian Style Guide](./references/russian-style-guide.md) for comprehensive terminology glossary.

## Content Structure Requirements

### Article Frontmatter

Every article must include YAML frontmatter:

```yaml
---
title: "Название статьи"
subtitle: "Подзаголовок (опционально)"
author: "Имя автора"
date: "YYYY-MM-DD"
publication: "habr|vc-ru|rbc|vedomosti"
category: "Категория"
tags: ["тег1", "тег2", "тег3"]
language: "ru"
seo:
  description: "Мета-описание для поисковых систем (150-160 символов)"
  keywords: ["ключевое слово 1", "ключевое слово 2"]
reading_time: "X мин"
difficulty: "beginner|intermediate|advanced"
---
```

### Typical Article Structure

1. **Лид (Lead/Opening)**
   - Hook that captures attention (2-3 sentences)
   - Brief context and problem statement
   - What reader will learn

2. **Введение (Introduction)**
   - Expand on the problem
   - Why it matters
   - Brief overview of solution

3. **Основная часть (Main Content)**
   - Logical sections with clear headings
   - Code examples with explanations
   - Diagrams and illustrations
   - Step-by-step instructions where applicable

4. **Практические рекомендации (Practical Recommendations)**
   - Actionable takeaways
   - Best practices
   - Common pitfalls to avoid

5. **Заключение (Conclusion)**
   - Summary of key points
   - Next steps or further reading
   - Call to action (if appropriate)

6. **Ссылки и ресурсы (References and Resources)**
   - Links to documentation
   - Related articles
   - Tools and libraries mentioned

## Platform-Specific Formatting

### Habr.com

**Style:**
- Technical depth with accessibility
- Code-heavy with detailed explanations
- Informal «ты» form acceptable
- Use habr-specific markdown extensions

**Structure:**
- Lead paragraph under `<cut />` tag for preview
- Heavy use of code blocks with syntax highlighting
- Spoilers for large code examples
- Tables for comparisons

See [Habr Format Guide](./assets/habr-format.md) for details.

### VC.ru

**Style:**
- Business and startup focus
- Less technical, more strategic
- Formal «вы» form preferred
- Emphasis on metrics and ROI

**Structure:**
- Strong headline and subtitle
- Bullet points and numbered lists
- Quotes from experts/founders
- Charts and infographics

See [VC.ru Format Guide](./assets/vc-ru-format.md) for details.

### RBC and Vedomosti

**Style:**
- Journalistic, objective tone
- Formal business language
- Third-person narrative
- Extensive fact-checking and citations

**Structure:**
- Inverted pyramid (most important first)
- Clear attribution for all claims
- Professional headlines
- Conservative formatting

See [Publication Requirements](./references/publication-requirements.md) for all platforms.

## Code Block Formatting

### Syntax Highlighting

Always specify language for code blocks:

````markdown
```python
def fibonacci(n: int) -> int:
    """Вычисляет n-е число Фибоначчи."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```
````

### Code Comments

- Write comments in Russian for Russian articles
- Keep variable names in English (standard practice)
- Explain complex logic in surrounding text

```python
# Создаем словарь для кэширования результатов
cache = {}

def memoized_fibonacci(n: int) -> int:
    # Проверяем, есть ли результат в кэше
    if n in cache:
        return cache[n]

    # Базовые случаи
    if n <= 1:
        return n

    # Рекурсивное вычисление с кэшированием
    cache[n] = memoized_fibonacci(n-1) + memoized_fibonacci(n-2)
    return cache[n]
```

## SEO Optimization for Russian Search

### Yandex-Specific Considerations

1. **Title Optimization:**
   - Keep titles under 60 characters
   - Include main keyword at the beginning
   - Use natural language, avoid keyword stuffing

2. **Meta Description:**
   - 150-160 characters
   - Include call to action
   - Use question format when appropriate

3. **Content Structure:**
   - Clear H1, H2, H3 hierarchy
   - Use numbered and bulleted lists
   - Include relevant images with alt text in Russian
   - Internal linking to related content

4. **Keywords:**
   - Use Russian keywords naturally in text
   - Include synonyms and related terms
   - Consider regional variations (RU, UA, BY)

### Technical SEO

- Proper HTML structure in markdown
- Fast-loading images (optimized)
- Mobile-friendly formatting
- Structured data where applicable

## Auto-Save Workflow

### File Naming Convention

Save all content to `/home/user/agents/outputs/articles/` with format:

```
YYYY-MM-DD-slug-ru.md
```

**Examples:**
- `2025-11-20-kubernetes-best-practices-ru.md`
- `2025-11-20-microservices-architecture-ru.md`

### Directory Structure

```
/home/user/agents/outputs/articles/
├── 2025-11-20-kubernetes-best-practices-ru.md
├── 2025-11-20-microservices-architecture-ru.md
└── drafts/
    └── 2025-11-20-draft-article-ru.md
```

### Saving Process

1. **Generate Content:** Create complete article with frontmatter
2. **Validate Structure:** Check frontmatter, sections, formatting
3. **Apply Typography:** Ensure all Russian typography rules
4. **Generate Filename:** Create slug from title (transliterated or translated)
5. **Save File:** Write to `/home/user/agents/outputs/articles/`
6. **Confirm:** Return absolute file path to user

**Example Code for Saving:**

```python
import os
from datetime import datetime
from slugify import slugify

def save_article(title: str, content: str, draft: bool = False) -> str:
    """
    Сохраняет статью в формате markdown.

    Args:
        title: Заголовок статьи
        content: Полное содержание с frontmatter
        draft: Флаг черновика

    Returns:
        Абсолютный путь к сохраненному файлу
    """
    # Создаем slug из заголовка
    slug = slugify(title, max_length=50)

    # Формируем имя файла
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{slug}-ru.md"

    # Определяем директорию
    base_dir = "/home/user/agents/outputs/articles"
    if draft:
        base_dir = os.path.join(base_dir, "drafts")

    # Создаем директорию если не существует
    os.makedirs(base_dir, exist_ok=True)

    # Полный путь к файлу
    filepath = os.path.join(base_dir, filename)

    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath
```

## Quality Checklist for Russian Content

Before finalizing content, verify:

### Language and Style
- [ ] All typography rules followed (« », —, №)
- [ ] Consistent terminology throughout
- [ ] Appropriate tone for target publication
- [ ] No mixed-language constructions
- [ ] Proper use of formal/informal address

### Content Quality
- [ ] Clear, compelling lead paragraph
- [ ] Logical flow between sections
- [ ] Technical accuracy verified
- [ ] Code examples tested and working
- [ ] All claims supported by evidence

### Structure and Formatting
- [ ] Complete and valid YAML frontmatter
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Code blocks with language specification
- [ ] Images with descriptive alt text
- [ ] Internal links working

### SEO and Discoverability
- [ ] Optimized title with main keyword
- [ ] Meta description (150-160 chars)
- [ ] Relevant tags and categories
- [ ] Alt text for all images
- [ ] Reading time estimated

### Technical Requirements
- [ ] File saved with correct naming convention
- [ ] UTF-8 encoding
- [ ] Valid markdown syntax
- [ ] Platform-specific formatting applied

## Content Types

### Technical Articles (Статьи)

**Purpose:** Deep dive into technical topics with code examples and detailed explanations.

**Length:** 2,000-5,000 words

**Key Elements:**
- Problem statement and context
- Step-by-step technical explanation
- Working code examples
- Best practices and recommendations
- Performance considerations

**Best For:** Habr, technical sections of VC.ru

### Case Studies (Кейсы)

**Purpose:** Real-world implementation stories showing before/after and business impact.

**Length:** 1,500-3,000 words

**Key Elements:**
- Company/project background
- Challenge description
- Solution architecture and implementation
- Results with metrics
- Lessons learned

**Best For:** VC.ru, RBC, Vedomosti

### Tutorials (Туториалы)

**Purpose:** Step-by-step guides teaching specific skills or technologies.

**Length:** 1,500-3,500 words

**Key Elements:**
- Prerequisites clearly stated
- Sequential steps with explanations
- Screenshots or diagrams
- Troubleshooting section
- Links to additional resources

**Best For:** Habr, educational content

### Research Articles (Исследования)

**Purpose:** Analysis of trends, technologies, or methodologies with data and insights.

**Length:** 2,500-6,000 words

**Key Elements:**
- Research methodology
- Data collection and analysis
- Findings and insights
- Visualizations (charts, graphs)
- Implications and predictions

**Best For:** RBC, Vedomosti, analytical sections of VC.ru and Habr

## References and Resources

- [Russian Style Guide](./references/russian-style-guide.md) - Comprehensive writing standards
- [Publication Requirements](./references/publication-requirements.md) - Platform-specific guidelines
- [Article Template](./assets/article-template-ru.md) - Complete Russian article template
- [Habr Format](./assets/habr-format.md) - Habr-specific markdown and conventions
- [VC.ru Format](./assets/vc-ru-format.md) - VC.ru-specific formatting
- [Content Workflow](./assets/content-workflow.md) - Step-by-step creation process

## Quick Start Example

To create a Russian technical article:

1. **Define Parameters:**
   - Topic and target publication
   - Article type (article/case study/tutorial/research)
   - Technical depth level

2. **Generate Content:**
   - Create frontmatter with all required fields
   - Write lead paragraph with hook
   - Develop main content with proper structure
   - Add code examples with Russian comments
   - Write conclusion with takeaways

3. **Apply Russian Standards:**
   - Replace all quotes with « »
   - Use — for dashes with spaces
   - Add № where appropriate
   - Check all technical terminology
   - Verify typography throughout

4. **Optimize for SEO:**
   - Include target keywords naturally
   - Write compelling meta description
   - Add relevant tags
   - Ensure proper heading structure

5. **Save and Validate:**
   - Generate appropriate filename slug
   - Save to `/home/user/agents/outputs/articles/YYYY-MM-DD-slug-ru.md`
   - Run through quality checklist
   - Return file path to user

See [Content Workflow](./assets/content-workflow.md) for detailed step-by-step process.

## Advanced Techniques

### Adapting English Content

When translating from English:

1. **Don't Translate Literally:** Adapt idioms and expressions to Russian equivalents
2. **Adjust Examples:** Use Russian companies, services, or contexts when appropriate
3. **Cultural Context:** Consider Russian business culture and practices
4. **Technical Terms:** Follow established Russian tech terminology
5. **Tone Adjustment:** Russian tech writing tends to be slightly more formal

### Multi-Platform Publishing

When creating content for multiple platforms:

1. **Master Version:** Create full technical version first
2. **Adapt Per Platform:** Adjust tone, depth, and formatting
3. **Maintain Core Message:** Keep key insights consistent
4. **Platform-Specific SEO:** Optimize separately for each platform
5. **Cross-Reference:** Link between versions when appropriate

### Handling Complex Technical Concepts

For difficult-to-translate concepts:

1. **Provide Both:** «Machine Learning (машинное обучение, ML)»
2. **Explain in Context:** Define term when first used
3. **Use Analogies:** Russian-friendly comparisons and metaphors
4. **Visual Aids:** Diagrams with Russian labels
5. **Consistency:** Once term chosen, use consistently

## Common Mistakes to Avoid

1. **Typography Errors:**
   - ❌ Using English quotes "text"
   - ✅ Using Russian quotes «текст»

2. **Mixed Language:**
   - ❌ «Мы используем continuous integration»
   - ✅ «Мы используем Continuous Integration (непрерывную интеграцию)»

3. **Informal Tone Where Inappropriate:**
   - ❌ Using «ты» in RBC or Vedomosti
   - ✅ Using formal «вы» or third person

4. **Incorrect Technical Terms:**
   - ❌ «дата сайнс» (transliteration)
   - ✅ «Data Science» or «наука о данных»

5. **Poor Structure:**
   - ❌ Wall of text without sections
   - ✅ Clear headings and logical flow

6. **Missing Frontmatter:**
   - ❌ Article without metadata
   - ✅ Complete YAML frontmatter

7. **Inconsistent Terminology:**
   - ❌ Switching between terms for same concept
   - ✅ Define once, use consistently

## Success Metrics

Quality Russian technical content should achieve:

- **Readability:** Clear, engaging prose that flows naturally
- **Accuracy:** Technically correct with verified examples
- **Completeness:** All necessary context and details included
- **Professionalism:** Meets editorial standards of target publication
- **Engagement:** Compelling narrative that holds reader attention
- **Actionability:** Practical takeaways reader can apply
- **Discoverability:** Optimized for search and recommendations

---

**Note:** This skill is designed for senior-level technical content creation. The quality standard is equivalent to AWS, Microsoft, or Google technical blogs, adapted for Russian language and platforms.
