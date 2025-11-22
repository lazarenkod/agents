---
name: executive-communication
description: Effective communication с executive stakeholders, board presentations, strategic reporting, crisis communication для leadership. Use when communicating with C-level, board reporting, или executive decision support.
---

# Коммуникация с Руководством

## Принципы Executive Communication

### The Pyramid Principle
```markdown
1. **Start with conclusion** (executive summary)
2. **Support with key points** (3-5 bullets)
3. **Provide details** (only if asked)

❌ Avoid: Long build-up to conclusion
✅ Do: Answer first, justify after
```

### BLUF (Bottom Line Up Front)

```markdown
## BLUF Format

**Bottom Line**: [One-sentence answer/recommendation]

**Supporting Facts**:
- Fact 1
- Fact 2
- Fact 3

**Recommendation**: [Clear action request]

**Details**: [Available in appendix]
```

## Executive Briefing Templates

### Incident Executive Brief (During Crisis)

```markdown
# EXECUTIVE BRIEF: Production Outage

**Status**: MITIGATING (as of 15:30 UTC)
**Severity**: P1 Critical
**Duration**: 2 hours 15 minutes

## Bottom Line
Production API is down affecting 10K users. Root cause identified (database failure). Fix being deployed. ETA: 30 minutes.

## Business Impact
- Revenue loss: ~$50K (estimated)
- Customers affected: 15 enterprise, 200 SMB
- SLA breach: Yes (service credits ~$12K)
- PR risk: Medium (social media mentions increasing)

## What We're Doing
- Root cause: Primary DB hardware failure
- Fix: Failing over to standby database
- ETA: 15:45 UTC (15 minutes)
- Communication: Status page updated, customers emailed

## What We Need from You
- ❌ Nothing - we have this handled
- ℹ️ FYI: May need PR statement if media inquires

## Next Update
16:00 UTC (30 minutes) or sooner if resolved
```

### Monthly Executive Dashboard

```markdown
# Support Performance Dashboard - January 2024

## ✅ Key Wins
- **CSAT**: 92.5% (+1.5% MoM) 🎯 Target: 90%
- **Deflection Rate**: 43% (+5% MoM) 🎯 Target: 40%
- **P1 Response Time**: 12min 🎯 Target: <15min

## ⚠️ Attention Needed
- **P2 Resolution Time**: 7.8hrs (Target: <8hrs, trending ↑)
  - Root cause: Network issue complexity increased
  - Action: Network training scheduled for team

## 📊 Business Impact
- **Tickets Deflected**: 1,850 (est. $46K savings)
- **Service Credits**: $87K (within 2% revenue budget)
- **Churn Prevention**: 2 at-risk accounts recovered

## 💡 Strategic Initiatives
- AI chatbot pilot: 22% deflection in beta
- Knowledge base refresh: 50 articles updated
- Vendor support optimization: Saved $15K annual

## Ask
- ✅ Approve AI chatbot expansion ($50K investment)
```

### Board Presentation (Quarterly)

```markdown
# Board Report: Q1 2024 Support Performance

## Slide 1: Executive Summary
- Support satisfaction: 92% (↑3% YoY)
- Efficiency gains: 18% more tickets with same team
- Strategic initiative: AI deflection pilot (22% success)

## Slide 2: Customer Satisfaction Trends
[Chart: CSAT & NPS trending up over 12 months]

## Slide 3: Operational Efficiency
- Cost per ticket: $24 (↓15% YoY through automation)
- Deflection rate: 43% (↑12% YoY)
- Team productivity: 10.5 tickets/day (↑8% YoY)

## Slide 4: Strategic Investments
- AI chatbot: $150K investment, 18-month payback
- Team expansion: +15 FTE for new product launch
- Training program: Tier 1→2 promotion pipeline

## Slide 5: Risks & Mitigations
- Risk: Increasing complexity (cloud multi-vendor)
  - Mitigation: Specialized training, vendor partnerships
- Risk: Competition for talent
  - Mitigation: Career pathing, competitive comp

## Slide 6: Asks
1. Approve AI chatbot expansion ($250K)
2. Approve headcount for new product (+20 FTE)
```

## Crisis Communication (CEO/Board)

### Major Outage Brief

```markdown
Subject: URGENT: Production Outage - Action May Be Needed

[CEO Name],

**Critical Update** - We have a production outage requiring your awareness.

**Situation**:
- Complete service outage started 14:30 UTC (45 min ago)
- ALL customers affected (~50K users)
- Root cause: AWS region-wide issue (confirmed with AWS)
- ETA from AWS: 2-4 hours

**Business Impact**:
- Revenue loss: ~$150K/hour
- SLA breaches: Significant (credits TBD)
- Reputation risk: HIGH (social media activity)
- Legal/PR: No immediate concerns

**Our Actions**:
- War room activated (CTO leading)
- Escalated to AWS VP level (Enterprise support)
- Customer communication: Email sent, status page updated
- PR team briefed and monitoring

**What We Need from You**:
🔴 **Decision Needed**: Should we issue public statement?
   - Pros: Transparency, proactive
   - Cons: Amplifies issue visibility
   - Recommendation: Wait 1 hour, then decide

ℹ️ **FYI**: Board notification sent
ℹ️ **FYI**: Customer success calling top 20 accounts

**Next Update**: Every hour or significant change

Available anytime: [Your Phone]

[Your Name]
```

## Executive Writing Style

### Do's ✅
- **Be concise**: 1 page maximum for briefs
- **Use visuals**: Charts better than tables
- **Quantify impact**: Numbers speak louder
- **Provide options**: Not just problems
- **Action-oriented**: Clear next steps
- **Confident tone**: "We will" not "We might try"

### Don'ts ❌
- Jargon without explanation
- Long email threads (summarize instead)
- Surprises (bad news early)
- Excuses without solutions
- Ambiguous asks ("let me know what you think")

## Asking for Resources

### Business Case Template

```markdown
# Business Case: AI Chatbot Investment

## Executive Summary
Invest $250K in AI chatbot to deflect 25% of tier 1 tickets, saving $450K annually (18-month ROI).

## Problem
- Tier 1 tickets: 70% are repetitive, simple
- Cost: $25/ticket × 40K tickets/year = $1M
- Customer wait: Avg 2 hours for simple questions

## Proposed Solution
AI chatbot handling FAQs, password resets, status checks

## Financial Impact
- Investment: $250K (Year 1), $80K/year maintenance
- Savings: $450K annually (18K tickets × $25)
- ROI: 18 months
- 3-year NPV: $980K

## Non-Financial Benefits
- Instant 24/7 support
- Frees humans for complex issues
- Improves CSAT (instant vs 2hr wait)

## Risks & Mitigations
- Risk: Low accuracy → Mitigation: 90% threshold before launch
- Risk: Customer pushback → Mitigation: Always offer human escalation

## Ask
Approve $250K investment for Q2 implementation
```

## References
- `templates/executive-briefs/` - Situation-specific templates
- `examples/board-decks/` - Quarterly presentation examples
