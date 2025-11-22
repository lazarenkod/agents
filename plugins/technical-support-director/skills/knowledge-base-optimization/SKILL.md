---
name: knowledge-base-optimization
description: Оптимизация базы знаний для максимального deflection rate и customer self-service. Включает content strategy, search optimization, analytics, AI integration. Use when improving KB performance, increasing deflection rate, or optimizing self-service.
---

# Оптимизация Базы Знаний

## Метрики Эффективности

### Deflection Rate
```python
deflection_rate = (self_service_resolutions / (self_service_attempts + tickets_created)) * 100
# Target: ≥40%
```

### Search Success Rate
```python
search_success = (searches_with_article_click / total_searches) * 100
# Target: ≥70%
```

### Content Quality
- Article helpfulness: ≥85% positive
- Zero-result searches: ≤5%
- Article freshness: 90% updated <6 months

## Оптимизация Поиска

### SEO для KB

```markdown
## Title Optimization
- Start with action verb: "How to...", "Fix...", "Troubleshoot..."
- Include primary keyword
- Keep under 60 characters
- Be specific

❌ Bad: "VM Problems"
✅ Good: "How to Fix VM Connectivity Issues in 5 Steps"

## Content Structure
- H1: One per article (title)
- H2: Main sections (with keywords)
- H3: Subsections
- Short paragraphs (3-4 sentences)
- Bullet points для lists
- Code blocks для commands
```

### Semantic Search

```python
# AI-Powered Search Enhancement
search_improvements = {
    "intent_understanding": "Understand user intent, not just keywords",
    "synonym_expansion": "Map 'broken' to 'not working', 'down', 'unavailable'",
    "context_aware": "Consider user's product, tier, recent activity",
    "personalization": "Rank results по user's role, history"
}
```

## Content Gap Analysis

```markdown
# Monthly Gap Analysis

## Top Zero-Result Queries
1. "kubernetes pod restart loop" - 145 searches ❌ Create article (P0)
2. "cdn cache purge api" - 98 searches ❌ Create article (P0)
3. "ssl certificate renewal" - 87 searches ❌ Create article (P1)

## Ticket → KB Conversion
- Analyze resolved tickets
- Identify repeating issues without KB articles
- Prioritize by frequency × impact
- Create articles for top 10 monthly
```

## Content Lifecycle

```markdown
## Article Workflow

Draft → SME Review → Edit → Approval → Publish → Monitor → Update/Archive

## Review Triggers
- Age > 6 months
- Helpfulness < 70%
- Views declining
- Product updates
- Customer feedback
```

## AI Integration

```markdown
# AI-Powered Features

## Chatbot
- Instant answers from KB
- Conversational troubleshooting
- Escalation to human when needed
- Additional deflection: 15-25%

## Auto-Tagging
- ML model suggests tags
- Reduces manual effort
- Improves discoverability

## Content Suggestions
- "Related articles" recommendations
- Collaborative filtering
- Increases KB engagement
```

## References
- `seo-guide.md` - Comprehensive SEO best practices
- `analytics-dashboard.json` - KB performance dashboard configs
