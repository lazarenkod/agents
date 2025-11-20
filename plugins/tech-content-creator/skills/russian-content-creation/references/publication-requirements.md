# Publication Requirements for Russian Platforms

## Overview

This guide provides detailed requirements, style guidelines, and best practices for publishing technical content on Russia's leading platforms: Habr.com, VC.ru, RBC, and Vedomosti.

---

## Habr.com

### Platform Overview

**URL:** https://habr.com
**Audience:** Software developers, IT professionals, tech enthusiasts
**Monthly readers:** 15+ million
**Focus:** Technical articles, tutorials, case studies, open-source projects

### Content Style

**Tone:** Informal, peer-to-peer, conversational
**Address:** «Ты» (informal you) is standard and expected
**Voice:** First-person narratives encouraged («я», «мы»)
**Language:** Technical depth with accessibility

### Audience Expectations

- **Technical accuracy** above all
- **Working code examples** that readers can copy and run
- **Practical application** - not just theory
- **Personal experience** - real projects and challenges
- **Open discussion** - readers will comment and critique

### Content Types

1. **Статья (Article)** - 2,000-5,000 words
   - Deep dive into technical topic
   - Code examples with explanations
   - Best practices and patterns

2. **Туториал (Tutorial)** - 1,500-3,500 words
   - Step-by-step instructions
   - Screenshots and code
   - Troubleshooting section

3. **Кейс (Case Study)** - 1,500-3,000 words
   - Real project implementation
   - Problems and solutions
   - Metrics and results

4. **Новость (News)** - 500-1,500 words
   - Tech news and announcements
   - New tools and releases
   - Brief analysis

### Markdown Extensions

Habr supports custom markdown:

**Cut Tag (Preview Separator):**
```markdown
Вступительный текст, который виден на главной странице.

<cut />

Основной контент, видимый после клика "Читать дальше".
```

**Spoiler (Collapsible Section):**
```markdown
<spoiler title="Название спойлера">
Скрытый контент
</spoiler>
```

**Source Code with Title:**
```markdown
<source lang="python">
def hello():
    print("Привет, Habr!")
</source>
```

**Images:**
```markdown
![Alt text](https://example.com/image.png)
```

### Formatting Guidelines

**Headers:**
```markdown
# H1 - Заголовок статьи (используется один раз)
## H2 - Основные разделы
### H3 - Подразделы
#### H4 - Редко используется
```

**Code Blocks:**
- Always specify language: ```python, ```javascript, ```bash
- Add comments in Russian for clarity
- Keep examples concise and runnable
- Show expected output

**Lists:**
- Use `-` for bullets
- Use `1.` for numbered lists
- Indent nested lists with 2 spaces

**Emphasis:**
- `**bold**` for **important terms**
- `*italic*` for *emphasis*
- `` `code` `` for inline code

**Links:**
```markdown
[Текст ссылки](https://example.com)
```

**Quotes:**
```markdown
> Цитата или важная мысль
```

**Tables:**
```markdown
| Заголовок 1 | Заголовок 2 |
|-------------|-------------|
| Ячейка 1    | Ячейка 2    |
```

### Content Structure (Recommended)

```markdown
# Заголовок статьи: конкретный и информативный

Лид-абзац: о чем статья, почему это важно, что читатель узнает.

**Что будет в статье:**
- Пункт 1
- Пункт 2
- Пункт 3

<cut />

## Введение

Контекст и постановка проблемы.

## Основная часть

### Раздел 1

Текст с примерами кода.

```python
# Код с комментариями
```

### Раздел 2

Продолжение с диаграммами или скриншотами.

## Заключение

Выводы и рекомендации.

## Полезные ссылки

- [Документация](https://example.com)
- [GitHub репозиторий](https://github.com/...)
```

### Best Practices

**Do:**
- ✅ Share real experience and code
- ✅ Test all code examples before publishing
- ✅ Include complete setup instructions
- ✅ Add troubleshooting section
- ✅ Link to source code repositories
- ✅ Engage with comments
- ✅ Use informal «ты» tone
- ✅ Add relevant tags (up to 5)

**Don't:**
- ❌ Publish marketing content disguised as articles
- ❌ Use clickbait headlines
- ❌ Include untested code
- ❌ Write overly formal or academic language
- ❌ Copy-paste without attribution
- ❌ Ignore community feedback
- ❌ Write without code examples

### Tags (Хабы)

Choose 2-5 relevant tags from Habr's hub list:

- **Languages:** Python, JavaScript, Go, Rust, Java
- **Technologies:** Docker, Kubernetes, React, Vue, Django
- **Topics:** Machine Learning, DevOps, Backend, Frontend
- **Concepts:** Microservices, Architecture, Security, Performance

### Typical Article Length

- **Short article:** 1,500-2,500 words (~8 min read)
- **Medium article:** 2,500-4,000 words (~12 min read)
- **Long article:** 4,000-7,000 words (~20 min read)

### Publication Process

1. **Draft** in Habr editor or external markdown
2. **Preview** to check formatting
3. **Add tags** (2-5 hubs)
4. **Choose publication** (personal blog or corporate blog)
5. **Submit for moderation** (optional for rating boost)
6. **Publish** and engage with comments

---

## VC.ru

### Platform Overview

**URL:** https://vc.ru
**Audience:** Entrepreneurs, business executives, investors, startup founders
**Monthly readers:** 10+ million
**Focus:** Business, startups, technology, marketing, investments

### Content Style

**Tone:** Professional, business-focused, semi-formal
**Address:** «Вы» (formal you) preferred, or third person
**Voice:** First-person for founders' stories, third-person for analysis
**Language:** Less technical, more strategic and business-oriented

### Audience Expectations

- **Business value** and ROI focus
- **Metrics and numbers** - revenue, growth, conversions
- **Practical insights** for business decisions
- **Market analysis** and trends
- **Real stories** from founders and executives
- **Concrete takeaways** for business application

### Content Types

1. **Кейс (Case Study)** - 1,500-3,000 words
   - Company growth story
   - Problem → Solution → Results
   - Business metrics and impact

2. **Анализ (Analysis)** - 2,000-4,000 words
   - Market trends
   - Technology impact on business
   - Investment opportunities

3. **Мнение (Opinion)** - 1,000-2,000 words
   - Expert perspective
   - Industry commentary
   - Predictions and forecasts

4. **Гайд (Guide)** - 1,500-3,000 words
   - How to achieve business goal
   - Step-by-step business process
   - Best practices

### Formatting Guidelines

**Headers:**
```markdown
# Заголовок статьи
## Подзаголовок (опционально)

## Основной раздел
### Подраздел
```

**Text Formatting:**
- Use **bold** for key metrics and important points
- Use *italic* sparingly for emphasis
- Break text into short paragraphs (3-4 sentences)
- Use bullet points generously

**Visual Elements:**
- Charts and graphs highly valued
- Screenshots of dashboards, analytics
- Infographics for data visualization
- Company logos and product screenshots

**Quotes:**
```markdown
> «Прямая речь от эксперта или основателя», — имя, должность, компания.
```

**Links:**
- Link to sources and data
- Link to mentioned companies/products
- Use descriptive link text (not "here" or "link")

### Content Structure (Recommended)

```markdown
# Цепляющий заголовок с конкретной цифрой или результатом

**TL;DR:** Краткое резюме статьи в 2-3 предложениях с ключевыми метриками.

---

## Контекст

Кто вы/компания, какая проблема стояла.

## Проблема

Детальное описание вызова с цифрами.

## Решение

Что и как делали, какие инструменты использовали.

### Этап 1
### Этап 2
### Этап 3

## Результаты

Конкретные метрики: рост выручки, снижение затрат, увеличение конверсии.

**До и после:**
- Метрика 1: было X → стало Y
- Метрика 2: было X → стало Y

## Выводы

Основные insights и рекомендации для читателей.

## Что можно сделать прямо сейчас

3-5 actionable шагов.
```

### Best Practices

**Do:**
- ✅ Lead with strong metrics and results
- ✅ Include TL;DR at the beginning
- ✅ Use data to support claims
- ✅ Quote founders and executives
- ✅ Show before/after comparisons
- ✅ Focus on business impact
- ✅ Make it skimmable (bullets, numbers, bold)
- ✅ Include call-to-action at the end

**Don't:**
- ❌ Get too technical (keep it business-focused)
- ❌ Write without numbers/metrics
- ❌ Use informal slang or jargon
- ❌ Make unsubstantiated claims
- ❌ Bury the lead (put results up front)
- ❌ Write walls of text without breaks
- ❌ Ignore SEO (titles, headings, keywords)

### Key Metrics to Include

When applicable, include:
- Revenue/profit numbers
- Growth percentages
- User/customer numbers
- Conversion rates
- Cost savings
- Time savings
- Market share
- Investment amounts
- ROI figures

### Tags (Разделы)

Choose relevant sections:

- **Категории:** Стартапы, Маркетинг, Продукты, Технологии
- **Темы:** SaaS, E-commerce, Fintech, EdTech
- **Форматы:** Кейс, Гайд, Разбор, Мнение

### Typical Article Length

- **Short post:** 800-1,500 words (~4-6 min read)
- **Medium article:** 1,500-2,500 words (~8 min read)
- **Long-form:** 2,500-4,000 words (~12 min read)

### Headline Formulas

Effective VC.ru headlines:

- **Result-driven:** «Как мы увеличили выручку на 300% за 6 месяцев»
- **Number-focused:** «5 ошибок, которые убивают конверсию вашего SaaS»
- **Question:** «Почему 80% стартапов умирают в первый год?»
- **How-to:** «Как найти первых 100 клиентов для B2B-продукта»
- **Controversial:** «Почему Agile не работает в крупных компаниях»

---

## RBC (РБК)

### Platform Overview

**URL:** https://rbc.ru
**Audience:** Business professionals, executives, investors, general public
**Monthly readers:** 30+ million
**Focus:** Business news, economics, finance, technology, politics

### Content Style

**Tone:** Formal, journalistic, objective
**Address:** Third person (no direct address to reader)
**Voice:** Neutral, factual reporting
**Language:** Professional business language, minimal jargon

### Audience Expectations

- **Journalistic standards** - fact-checked, sourced
- **Objectivity** - multiple perspectives
- **Credibility** - expert quotes, official data
- **News value** - timely, relevant, impactful
- **Clear structure** - inverted pyramid (most important first)

### Content Types

1. **Новость (News)** - 500-1,500 words
   - Current events
   - Company announcements
   - Market updates

2. **Аналитика (Analysis)** - 1,500-3,000 words
   - Industry trends
   - Market research
   - Economic impact

3. **Интервью (Interview)** - 1,500-2,500 words
   - Executive interviews
   - Expert opinions
   - Industry leaders

4. **Исследование (Research)** - 2,000-4,000 words
   - Data-driven reports
   - Market studies
   - Trend analysis

### Formatting Guidelines

**Structure:**
- **Lead (Лид):** First paragraph with key facts (who, what, when, where, why)
- **Context:** Background information
- **Details:** Additional facts and quotes
- **Conclusion:** Implications and outlook

**Paragraphs:**
- Short paragraphs (2-3 sentences)
- One idea per paragraph
- Clear topic sentences

**Quotes:**
- Always attribute: full name, title, company
- Use Russian quotation marks « »
- Follow with attribution tag

```markdown
«Рынок облачных технологий продолжает расти», — заявил Иван Петров, генеральный директор CloudTech.
```

**Numbers:**
- Spell out one through nine
- Use digits for 10 and above
- Use proper formatting: «100 млн рублей», «$50 млрд»

### Content Structure (News Article)

```markdown
# Информативный заголовок с ключевым фактом

**[ГОРОД], [ДАТА].** Лид-абзац с ответами на вопросы: кто, что, когда, где, почему.

Второй абзац с контекстом и дополнительными деталями.

«Прямая цитата от первого эксперта», — комментирует Имя Фамилия, должность, компания.

Дополнительные факты и данные. Ссылки на источники исследований или официальные документы.

«Цитата от второго эксперта с другой перспективой», — отмечает Имя Фамилия, должность, компания.

Заключительный абзац с выводами и прогнозами.
```

### Best Practices

**Do:**
- ✅ Verify all facts and figures
- ✅ Cite sources for all data
- ✅ Include multiple expert perspectives
- ✅ Use official titles and full names
- ✅ Provide context and background
- ✅ Write in inverted pyramid structure
- ✅ Use precise, formal language
- ✅ Include publication date and location

**Don't:**
- ❌ Express personal opinions
- ❌ Use informal language or slang
- ❌ Make unsubstantiated claims
- ❌ Use first or second person
- ❌ Include marketing or promotional content
- ❌ Use clickbait headlines
- ❌ Write without fact-checking

### Sourcing Requirements

- Attribute all statistics and data
- Link to original sources when possible
- Use credible sources (research firms, government agencies, public companies)
- Quote named sources (avoid anonymous quotes)
- Include methodology for research/surveys

### Typical Article Length

- **News brief:** 300-800 words
- **Standard news:** 800-1,500 words
- **Feature article:** 1,500-2,500 words
- **In-depth analysis:** 2,500-4,000 words

### Headline Guidelines

- State the news clearly and factually
- Include key information (company, event, impact)
- Avoid sensationalism
- Keep under 80 characters

**Examples:**
- ✅ «Yandex увеличил выручку на 45% в третьем квартале 2024 года»
- ✅ «Российский рынок облачных сервисов достиг 180 млрд рублей»
- ❌ «Вы не поверите, насколько вырос Yandex!»
- ❌ «Облака захватывают Россию»

---

## Vedomosti (Ведомости)

### Platform Overview

**URL:** https://vedomosti.ru
**Audience:** Business elite, top executives, government officials, investors
**Monthly readers:** 5+ million (highest quality audience)
**Focus:** Business, finance, economy, politics, premium content

### Content Style

**Tone:** Highly formal, authoritative, analytical
**Address:** Third person exclusively
**Voice:** Objective, professional journalism
**Language:** Sophisticated business vocabulary, minimal simplification

### Audience Expectations

- **Premium quality** - in-depth analysis
- **Authoritative sources** - C-level executives, government officials
- **Complex analysis** - not simplified for general audience
- **Strategic insights** - implications for business decisions
- **Conservative presentation** - no flashy formatting

### Content Types

1. **Аналитическая статья (Analytical Article)** - 2,000-4,000 words
   - Deep market analysis
   - Strategic implications
   - Expert commentary

2. **Экспертное мнение (Expert Opinion)** - 1,500-2,500 words
   - Industry leader perspective
   - Policy analysis
   - Economic forecasts

3. **Исследование (Research Report)** - 3,000-5,000 words
   - Comprehensive market studies
   - Data-driven insights
   - Long-term trends

4. **Интервью (Executive Interview)** - 1,500-3,000 words
   - CEO/founder interviews
   - Government officials
   - Industry experts

### Formatting Guidelines

**Structure:**
- Traditional inverted pyramid
- Dense paragraphs with substantial content
- Minimal use of bullets or visual breaks
- Formal section headings

**Language:**
- Formal business Russian
- Complete sentences, complex syntax
- Technical terms without excessive explanation
- Assumed educated audience

**Citations:**
- Full credentials for all sources
- Reference to research methodology
- Links to official documents/reports
- Academic or professional sources preferred

### Content Structure

```markdown
# Формальный заголовок: конкретный и информативный

**Подзаголовок:** Краткое раскрытие темы.

**Лид:** Полный вводный абзац с ключевыми фактами, цифрами и контекстом.

Второй абзац развивает тему, предоставляя исторический контекст или отраслевую перспективу.

«Развернутая цитата от высокопоставленного эксперта, раскрывающая стратегический контекст», — комментирует Имя Отчество Фамилия, должность, компания или организация.

## Анализ ситуации

Детальный анализ с использованием данных, статистики и экспертных оценок. Рассмотрение нескольких перспектив и факторов.

Параграфы содержат развернутые аргументы, поддержанные фактами и цифрами. Ссылки на исследования, официальные документы, заявления компаний.

## Последствия для бизнеса

Анализ влияния на различные сегменты рынка, компании, экономику в целом.

«Экспертная оценка последствий и прогнозы», — отмечает другой эксперт с полными регалиями.

## Перспективы и прогнозы

Взвешенный анализ возможных сценариев развития ситуации. Мнения нескольких экспертов.

Заключительные параграфы с выводами и стратегическими импликациями.
```

### Best Practices

**Do:**
- ✅ Provide deep, sophisticated analysis
- ✅ Quote C-level executives and officials
- ✅ Include comprehensive data and research
- ✅ Write in formal, professional style
- ✅ Consider multiple perspectives
- ✅ Provide strategic business context
- ✅ Use precise, technical terminology
- ✅ Reference credible sources

**Don't:**
- ❌ Oversimplify complex topics
- ❌ Use casual or informal language
- ❌ Include promotional content
- ❌ Rely on single sources
- ❌ Use flashy formatting or clickbait
- ❌ Express personal bias
- ❌ Write for general audience
- ❌ Use informal quotes or anonymous sources

### Source Requirements

**Preferred sources:**
- CEOs and C-suite executives of major companies
- Government ministers and officials
- Leading academic researchers
- Recognized industry analysts
- Official statistics and reports

**Quote format:**
```markdown
«Детальная экспертная оценка ситуации с анализом факторов и прогнозом», — заявил Сергей Иванович Петров, председатель совета директоров компании «Технологии Будущего», бывший заместитель министра цифрового развития.
```

### Typical Article Length

- **Short analysis:** 1,500-2,000 words
- **Standard article:** 2,000-3,000 words
- **Long-form analysis:** 3,000-5,000 words
- **Special report:** 5,000-10,000 words

### Headline Guidelines

- Formal, informative, specific
- Avoid colloquialisms
- State business significance
- Include key entities/numbers

**Examples:**
- ✅ «Российские банки увеличили инвестиции в цифровизацию на 60 млрд рублей»
- ✅ «Трансформация нефтегазового сектора: вызовы и возможности»
- ❌ «Банки тратят миллиарды на digital»
- ❌ «Нефтянка переходит на цифру»

---

## Comparison Matrix

| Aspect | Habr | VC.ru | RBC | Vedomosti |
|--------|------|-------|-----|-----------|
| **Tone** | Informal | Semi-formal | Formal | Very formal |
| **Address** | Ты (informal you) | Вы or 3rd person | 3rd person | 3rd person only |
| **Audience** | Developers | Entrepreneurs | Business professionals | Business elite |
| **Technical depth** | High | Medium | Medium | Medium-High |
| **Business focus** | Low | High | High | Very high |
| **Length** | 2K-5K words | 1.5K-3K words | 1K-2.5K words | 2K-4K words |
| **Code examples** | Essential | Rare | Very rare | Never |
| **Metrics focus** | Optional | Essential | Important | Essential |
| **Expert quotes** | Optional | Recommended | Required | Required (high-level) |
| **Visual elements** | Code, diagrams | Charts, screenshots | Minimal | Very minimal |
| **SEO importance** | High | High | Medium | Low |

---

## Content Adaptation Strategy

### From Technical to Business

When adapting Habr content for VC.ru:

1. **Reduce technical details** - focus on "what" not "how"
2. **Add business context** - why it matters for business
3. **Include ROI/metrics** - quantify business impact
4. **Change examples** - from technical to business scenarios
5. **Adjust tone** - from informal to professional
6. **Shorten code** - show results, not implementation

### From Business to Journalistic

When adapting VC.ru content for RBC:

1. **Objectify tone** - remove first person
2. **Add multiple perspectives** - quote various experts
3. **Fact-check rigorously** - verify all claims
4. **Add context** - industry and market background
5. **Formalize language** - professional journalism style
6. **Structure properly** - inverted pyramid

### From General to Premium

When adapting RBC content for Vedomosti:

1. **Deepen analysis** - more sophisticated insights
2. **Elevate sources** - higher-level executives
3. **Increase complexity** - don't oversimplify
4. **Add strategic layer** - implications for decision-makers
5. **Formalize further** - most conservative language
6. **Extend length** - comprehensive coverage

---

## Quick Reference Guide

### Choosing the Right Platform

**Choose Habr when:**
- Content is highly technical
- Target audience is developers/engineers
- Focus is on implementation and code
- Tone is peer-to-peer
- Goal is community engagement

**Choose VC.ru when:**
- Content focuses on business impact
- Target audience is founders/executives
- Emphasis on metrics and growth
- Sharing startup/business stories
- Goal is business leads or investors

**Choose RBC when:**
- Content is newsworthy
- Target audience is broad business community
- Objective reporting required
- Industry analysis or trends
- Goal is credibility and reach

**Choose Vedomosti when:**
- Content is premium analytical
- Target audience is C-suite/elite
- Deep strategic insights
- High-profile sources available
- Goal is thought leadership

---

## Checklist by Platform

### Habr Checklist
- [ ] Informal «ты» tone used throughout
- [ ] Working code examples included
- [ ] Technical terms explained with examples
- [ ] `<cut />` tag used for preview
- [ ] 2-5 relevant tags selected
- [ ] Personal experience shared
- [ ] Troubleshooting section included
- [ ] Links to GitHub/repositories added

### VC.ru Checklist
- [ ] TL;DR included at top
- [ ] Key metrics highlighted (bold)
- [ ] Before/after comparison shown
- [ ] Business impact quantified
- [ ] Expert/founder quotes included
- [ ] Call-to-action at end
- [ ] Charts or graphs included
- [ ] Skimmable format (bullets, numbers)

### RBC Checklist
- [ ] Third-person perspective throughout
- [ ] All facts verified and sourced
- [ ] Multiple expert perspectives included
- [ ] Inverted pyramid structure
- [ ] Full names and titles for all sources
- [ ] Date and location in lead
- [ ] Formal business language
- [ ] No promotional content

### Vedomosti Checklist
- [ ] Highly formal tone maintained
- [ ] C-level or official sources quoted
- [ ] Deep analytical content
- [ ] Comprehensive research included
- [ ] Strategic implications discussed
- [ ] Multiple scenarios considered
- [ ] Conservative formatting
- [ ] Premium quality throughout

---

**Last updated:** 2025-11-20
