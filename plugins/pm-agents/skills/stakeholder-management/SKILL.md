---
name: stakeholder-management
description: Advanced stakeholder management for senior PMs including power mapping, influence strategies, conflict resolution, and executive communication. Use when managing complex stakeholder dynamics, executive alignment, or cross-functional coordination.
---

# Stakeholder Management

Комплексное управление стейкхолдерами для сложных технических проектов с множеством заинтересованных сторон.

## When to Use This Skill

- Projects с 10+ stakeholders различных уровней
- Executive alignment и communication
- Cross-functional coordination (5+ teams)
- Conflicting priorities и interests
- Organizational change management
- High-visibility, high-risk initiatives

## Core Concepts

### Stakeholder Analysis Framework

**Power/Interest Matrix:**

```
         INTEREST →
         Low    High
      ┌──────┬──────┐
High  │ Keep │Manage│ POWER
      │Satis-│Close-│  ↓
      │ fied │  ly  │
      ├──────┼──────┤
Low   │Moni- │ Keep │
      │ tor  │Infor-│
      │      │ med  │
      └──────┴──────┘

Квадранты:
1. Manage Closely (High Power, High Interest)
   - Executive sponsors, key decision makers
   - Требуют regular engagement, detailed updates

2. Keep Satisfied (High Power, Low Interest)
   - Senior executives не прямо involved
   - High-level updates, ensure satisfaction

3. Keep Informed (Low Power, High Interest)
   - Team members, contributors
   - Regular communication, involvement

4. Monitor (Low Power, Low Interest)
   - Peripheral stakeholders
   - Minimal communication
```

### Stakeholder Categories

**By Role:**
- **Sponsors**: Funding, executive support
- **Decision Makers**: Approve key decisions
- **Contributors**: Do the work
- **Beneficiaries**: Use deliverables
- **Influencers**: Shape opinions
- **Gatekeepers**: Control resources/access

**By Attitude:**
- **Champions**: Actively support project
- **Supporters**: Positive but passive
- **Neutral**: No strong opinion
- **Skeptics**: Concerns but persuadable
- **Blockers**: Actively oppose

## Stakeholder Mapping

### Detailed Stakeholder Profile

```markdown
## Stakeholder: [Name]

**Role**: [Title/Position]
**Category**: [Sponsor/Decision Maker/Contributor/etc.]
**Department**: [Org unit]

### Influence Assessment

**Power**: ⬛⬛⬛⬛⬜ (4/5) - High
**Interest**: ⬛⬛⬛⬜⬜ (3/5) - Medium
**Attitude**: 😊 Supporter
**Influence Type**: [Formal authority/Expert power/Relationship network]

### Interests & Motivations

**What they care about**:
- [Interest 1]: Revenue growth
- [Interest 2]: Team development
- [Interest 3]: Technical excellence

**Success criteria for them**:
- [Criterion 1]
- [Criterion 2]

**Concerns/Risks they worry about**:
- [Concern 1]: Budget overruns
- [Concern 2]: Timeline slips

### Communication Strategy

**Preferred Channel**: [Email/Slack/Meetings/1-on-1]
**Frequency**: [Weekly/Bi-weekly/Monthly]
**Format**: [Detailed/Executive summary/Data-driven]
**Best Time**: [Morning/Afternoon/specific days]

**Communication Plan**:
- **Weekly**: Slack updates on progress
- **Bi-weekly**: 30min sync on blockers
- **Monthly**: Detailed metrics review

### Engagement Strategy

**How to engage**:
- [Tactic 1]: Involve in key decisions
- [Tactic 2]: Seek input on strategy
- [Tactic 3]: Recognize contributions publicly

**What to avoid**:
- [Anti-pattern 1]: Surprise escalations
- [Anti-pattern 2]: Technical jargon without context

### Relationship Building

**Current Relationship**: Strong / Developing / Weak
**Last 1-on-1**: [Date]
**Next Touch-point**: [Date and purpose]
**Trust Level**: High / Medium / Low

**Relationship building actions**:
- [Action 1]: Coffee chat on career goals
- [Action 2]: Involve in architecture review
```

### Stakeholder Map Template

```markdown
# Stakeholder Map - [Project]

## Manage Closely (High Power, High Interest)

| Stakeholder | Role | Attitude | Strategy | Owner |
|------------|------|----------|----------|-------|
| [Name] | CTO | 😊 Champion | Weekly updates, involve in decisions | PM |
| [Name] | VP Product | 😐 Neutral → 😊 | Build trust, align on vision | PM |

## Keep Satisfied (High Power, Low Interest)

| Stakeholder | Role | Attitude | Strategy | Owner |
|------------|------|----------|----------|-------|
| [Name] | CFO | 😐 Neutral | Monthly budget reports | PM |

## Keep Informed (Low Power, High Interest)

| Stakeholder | Role | Attitude | Strategy | Owner |
|------------|------|----------|----------|-------|
| [Name] | Tech Lead | 😊 Champion | Include in standups | Eng Lead |
| [Name] | Designer | 😊 Supporter | Design reviews | Product |

## Monitor

| Stakeholder | Role | Attitude | Strategy | Owner |
|------------|------|----------|----------|-------|
| [Name] | Legal | 😐 Neutral | Quarterly updates | PM |
```

## Influence Strategies

### For Different Stakeholder Types

**Champions (активные сторонники):**
✅ Leverage их influence для gaining support
✅ Involve в advocacy и communication
✅ Recognize и reward их support
✅ Keep them well-informed (first to know)

**Supporters (пассивные сторонники):**
✅ Keep them engaged и informed
✅ Convert to champions через involvement
✅ Seek their input и feedback
✅ Make it easy для них to support

**Neutral:**
✅ Understand их motivations и concerns
✅ Build relationship через value delivery
✅ Demonstrate benefits relevant to them
✅ Avoid pushing too hard

**Skeptics:**
✅ Listen to concerns genuinely
✅ Address objections с данными
✅ Find common ground
✅ Build trust через transparency
✅ Small wins to demonstrate value

**Blockers:**
✅ Understand root causes opposition
✅ One-on-one conversations
✅ Find mutually beneficial solutions
✅ Escalate если needed
✅ Sometimes work around если unavoidable

### Communication Techniques

**Executives:**
- **Start с bottom line**: Answer first, details после
- **Focus на business impact**: Revenue, cost, risk, opportunity
- **Be concise**: Max 1-2 pages, bullet points
- **Data-driven**: Metrics, trends, benchmarks
- **Options не problems**: Present solutions, не just issues
- **Respect их time**: Agenda, pre-reads, clear asks

**Technical Stakeholders:**
- **Depth и detail**: Technical accuracy важна
- **Architecture diagrams**: Visual representations
- **Trade-off analysis**: Technical pros/cons
- **Open discussion**: Collaborative problem-solving
- **Credibility**: Know your technical stuff

**Cross-Functional Peers:**
- **Partnership mindset**: Win-win solutions
- **Mutual respect**: Acknowledge их expertise
- **Regular sync**: Consistent communication
- **Transparency**: Share early, share often
- **Support their goals**: Help them succeed

## Conflict Resolution

### Conflict Types

**1. Priority Conflicts:**
- Ситуация: Multiple teams want resources
- Approach: Data-driven prioritization (RICE, WSJF)
- Escalation path: Clear decision framework (DACI)

**2. Technical Disagreements:**
- Ситуация: Competing technical approaches
- Approach: POCs, trade-off analysis, ADRs
- Decision maker: Technical authority (CTO, Architect)

**3. Resource Contentions:**
- Ситуация: Competing для same engineers/budget
- Approach: Capacity planning, phased approach
- Escalation: Resource management committee

**4. Timeline Expectations:**
- Ситуация: Stakeholder wants faster delivery
- Approach: Scope negotiation, MVP approach
- Reality check: Show data, provide options

### Conflict Resolution Framework

**Step 1: Understand All Perspectives**
- Listen actively to каждого stakeholder
- Separate facts от opinions
- Identify underlying interests (не just positions)

**Step 2: Find Common Ground**
- Shared goals
- Mutual constraints
- Common enemies (competitors, market pressure)

**Step 3: Generate Options**
- Brainstorm solutions collaboratively
- Trade-offs и compromises
- Creative alternatives

**Step 4: Evaluate Options**
- Against shared criteria
- Data-driven comparison
- Impact analysis

**Step 5: Decide & Commit**
- Clear decision
- Document rationale
- Get buy-in
- Move forward united

**Step 6: Follow Through**
- Execute decision
- Monitor outcomes
- Revisit если needed

## Executive Communication

### Executive Update Template

```markdown
# Executive Update - [Project]

**To**: [Executives]
**From**: [PM]
**Date**: [Date]
**Status**: 🟢 On Track

---

## TL;DR

[2-3 sentences: current status, key progress, critical asks]

---

## Status Dashboard

| Metric | Status | Notes |
|--------|--------|-------|
| Schedule | 🟢 | On track for [Date] launch |
| Budget | 🟢 | 85% utilization, within forecast |
| Quality | 🟡 | Minor issues being addressed |
| Stakeholders | 🟢 | Aligned and supportive |

---

## Key Progress

- ✅ [Achievement 1 with business impact]
- ✅ [Achievement 2 with business impact]

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [$X revenue at risk] | [Mitigation plan] |

---

## Decisions Needed

**Decision 1**: [Context and options]
- **Option A**: [Pros/cons, recommendation]
- **Option B**: [Pros/cons]
- **Recommendation**: Option A
- **Deadline**: [Date]

---

## Next Milestone

[Milestone] by [Date] - [Confidence level]
```

### One-on-One Meeting Guide

**Before Meeting:**
- [ ] Clear agenda sent 24h advance
- [ ] Pre-read materials если needed
- [ ] Understand их current priorities
- [ ] Prepare data/visuals

**During Meeting:**
- Start с their agenda items
- Listen more than talk
- Take notes on feedback
- Clarify expectations
- End with clear action items

**After Meeting:**
- Send summary email same day
- Follow up on commitments
- Update stakeholder profile
- Adjust engagement strategy

## Templates

См. `assets/` для:
- `stakeholder-profile-template.md` - Детальный профиль
- `stakeholder-map-template.md` - Power/Interest map
- `executive-update-template.md` - Executive communication
- `1on1-agenda-template.md` - One-on-one guide
- `conflict-resolution-framework.md` - Conflict resolution

## Best Practices

✅ **Start Early**: Map stakeholders в project kickoff
✅ **Regular Updates**: Consistent communication rhythm
✅ **Tailor Communication**: Different formats для different audiences
✅ **Build Relationships**: Invest time in 1-on-1s
✅ **Transparent**: Share good и bad news early
✅ **Follow Through**: Deliver on commitments
✅ **Political Awareness**: Understand org dynamics

## Success Criteria

- **Alignment**: >90% key stakeholders aligned
- **Satisfaction**: High satisfaction scores
- **Engagement**: Regular participation
- **Trust**: Open, honest communication
- **Support**: Champions actively advocating
- **No Surprises**: Stakeholders informed early
