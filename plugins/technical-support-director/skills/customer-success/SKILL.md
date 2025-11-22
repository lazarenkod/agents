---
name: customer-success
description: Customer Success methodologies для технической поддержки облачного провайдера. Включает CSAT/NPS management, customer health scoring, relationship building, proactive support. Use when improving customer satisfaction, managing strategic accounts, or building customer success programs.
---

# Успех Клиентов (Customer Success)

## Когда Использовать

- Improving CSAT/NPS scores
- Managing enterprise customer relationships
- Building proactive support programs
- Customer health monitoring
- Churn prevention
- Expansion opportunities identification

## Ключевые Метрики

### Customer Satisfaction (CSAT)

**Survey Design:**
```markdown
После закрытия тикета:

"How satisfied were you with the support you received?"
⭐⭐⭐⭐⭐ (1-5 scale)

1 - Very Dissatisfied
2 - Dissatisfied
3 - Neutral
4 - Satisfied
5 - Very Satisfied

[Optional] What could we improve?
[Text field]
```

**Target: ≥90% (4-5 ratings)**

### Net Promoter Score (NPS)

**Survey Question:**
```markdown
"On a scale of 0-10, how likely are you to recommend our service to a colleague?"

0-6: Detractors
7-8: Passives
9-10: Promoters

NPS = % Promoters - % Detractors
Target: ≥50
```

### Customer Effort Score (CES)

```markdown
"How easy was it to get your issue resolved?"

1 - Very Easy
2 - Easy
3 - Neutral
4 - Difficult
5 - Very Difficult

Target: ≤2.0 (low effort)
```

## Customer Health Scoring

```python
HEALTH_SCORE_COMPONENTS = {
    "support_satisfaction": {
        "weight": 0.25,
        "metrics": ["CSAT", "NPS", "CES"],
        "thresholds": {
            "excellent": "CSAT≥95%, NPS≥70",
            "good": "CSAT≥90%, NPS≥50",
            "at_risk": "CSAT<85% OR NPS<30"
        }
    },
    "engagement": {
        "weight": 0.30,
        "metrics": ["QBR_attendance", "product_adoption", "training_completion"],
        "signals": {
            "positive": "High engagement, feature adoption growing",
            "negative": "Low engagement, declining usage"
        }
    },
    "support_usage": {
        "weight": 0.25,
        "metrics": ["ticket_volume_trend", "escalation_rate", "p1_p2_frequency"],
        "red_flags": {
            "volume_spike": "Tickets up 50%+ month-over-month",
            "quality_issues": "High reopen rate, repeated issues"
        }
    },
    "relationship": {
        "weight": 0.20,
        "metrics": ["executive_engagement", "reference_willingness", "feedback_participation"],
        "indicators": {
            "strong": "Active in advisory board, willing reference",
            "weak": "Minimal executive engagement"
        }
    }
}
```

## Proactive Support Programs

### Health Checks (Enterprise Customers)

**Quarterly Review Agenda:**
```markdown
# Quarterly Business Review (QBR)

## Pre-Meeting Preparation
- Review customer's support metrics
- Identify trends и concerns
- Prepare recommendations

## Agenda (60 minutes)

### 1. Support Performance Review (15 min)
- CSAT/NPS trends
- Ticket volume analysis
- SLA performance
- Notable incidents и resolution

### 2. Product Usage Review (15 min)
- Feature adoption
- Underutilized capabilities
- Optimization opportunities
- Cost optimization recommendations

### 3. Roadmap Discussion (15 min)
- Upcoming features relevant to customer
- Customer feedback incorporation
- Beta program opportunities

### 4. Action Items и Next Steps (15 min)
- Address any concerns
- Commit to improvements
- Schedule next QBR
```

### Success Planning

**90-Day Success Plan (New Enterprise Customer):**
```markdown
## Days 1-30: Onboarding
- [ ] Welcome call with TAM
- [ ] Technical architecture review
- [ ] Support процедуры training
- [ ] Escalation paths established
- [ ] Monitoring setup guidance

## Days 31-60: Adoption
- [ ] First QBR scheduled
- [ ] Feature adoption review
- [ ] Best practices session
- [ ] Performance optimization review
- [ ] Feedback collection

## Days 61-90: Optimization
- [ ] Cost optimization review
- [ ] Advanced features training
- [ ] Case study discussion
- [ ] Reference program invitation
- [ ] Expansion opportunities discussion
```

## Customer Journey Mapping

```markdown
# Support Journey Touchpoints

## Discovery → Purchase
- Pre-sales technical consultation
- POC support

## Onboarding (0-90 days)
- Welcome package
- Dedicated onboarding specialist
- Training sessions
- Architecture review

## Adoption (3-12 months)
- Regular check-ins
- QBRs
- Feature spotlights
- Optimization recommendations

## Renewal (Annual)
- Renewal conversation (90 days before)
- Year in review
- Success metrics presentation
- Contract negotiation support

## Expansion
- New use case discovery
- Additional services introduction
- Co-selling opportunities
```

## Churn Prevention

### Early Warning Signs

```python
CHURN_RISK_INDICATORS = {
    "high_risk": [
        "NPS score <20 (Detractors)",
        "Multiple executive escalations",
        "Decreasing product usage (-30% MoM)",
        "Incomplete contract renewals",
        "Exploring competitors (signals)",
        "Key champion left company"
    ],
    "medium_risk": [
        "CSAT declining 3 months",
        "Escalation rate increasing",
        "Low engagement (missed QBRs)",
        "Support volume spike (frustration)",
        "Budget cuts communicated"
    ]
}
```

### Intervention Playbook

```markdown
## High-Risk Customer Intervention

### Immediate (Week 1)
1. Executive engagement (Director/VP call)
2. Understand root issues deeply
3. Develop action plan
4. Assign dedicated recovery team

### Short-term (Weeks 2-4)
1. Address critical pain points
2. Weekly check-ins
3. Quick wins delivered
4. Enhanced support (temporary)

### Medium-term (Months 2-3)
1. Comprehensive solution implementation
2. Relationship rebuilding
3. Value demonstration
4. Future roadmap alignment
```

## VOC (Voice of Customer) Program

```markdown
# Feedback Collection Channels

## Transactional
- Post-ticket CSAT surveys
- Post-escalation feedback
- Incident post-mortems

## Relationship
- Quarterly NPS surveys
- QBR discussions
- Executive sponsor conversations

## Product
- Feature requests tracking
- Beta program feedback
- User group sessions
- Customer advisory board
```

## References
- `qbr-templates/` - QBR slide decks и agendas
- `playbooks/churn-prevention.md` - Детальные intervention playbooks
- `metrics/health-scoring.py` - Health score calculation scripts
