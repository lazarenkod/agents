---
name: architecture-decision-records
description: Architecture Decision Records (ADR) framework for documenting significant technical decisions, alternatives considered, and rationale. Use when making architecture decisions, evaluating technology choices, or maintaining technical decision history.
---

# Architecture Decision Records (ADR)

Systematic approach to documenting architectural decisions for maintainability, knowledge transfer, and informed decision-making.

## When to Use This Skill

- Making significant architecture decisions
- Evaluating multiple technical alternatives
- Documenting technology selection rationale
- Onboarding new engineers to system design
- Reviewing past decisions and trade-offs
- Planning architecture evolution

## Core Concepts

### What is an ADR?

**Architecture Decision Record** - короткий текстовый документ, описывающий:
- Архитектурное решение
- Контекст, в котором оно принято
- Рассмотренные альтернативы
- Последствия решения

**Ключевые принципы:**
- **Immutable**: ADRs never deleted, only superseded
- **Numbered**: Sequential numbering (ADR-001, ADR-002...)
- **Short**: 1-2 pages maximum
- **Template-based**: Consistent structure
- **Version-controlled**: Stored in git with code

### When to Write an ADR

**Triggers:**
✅ Выбор database (SQL vs NoSQL, Postgres vs MySQL)
✅ Архитектурный паттерн (Monolith vs Microservices)
✅ Technology stack (React vs Vue, Python vs Go)
✅ Cloud provider selection (AWS vs Azure vs GCP)
✅ API design approach (REST vs GraphQL vs gRPC)
✅ Authentication/authorization strategy
✅ Deployment strategy (Kubernetes vs serverless)
✅ Data storage architecture
✅ Messaging system (Kafka vs SQS vs Pub/Sub)

**Not ADR-worthy:**
❌ Coding style preferences (use linter)
❌ Tactical implementation details
❌ Temporary workarounds
❌ Reversible decisions без impact

## ADR Template

```markdown
# ADR-[NUMBER]: [TITLE]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Date**: [YYYY-MM-DD]
**Decision Makers**: [Names/Roles]
**Tags**: [relevant, tags, here]

---

## Context

[Описание проблемы или вопроса, требующего решения]

**Current Situation:**
[Что происходит сейчас? В чем проблема?]

**Business Drivers:**
[Почему это важно для бизнеса?]

**Technical Constraints:**
[Какие технические ограничения существуют?]

**Quality Attributes:**
[Какие качественные атрибуты критичны? Performance, scalability, security, etc.]

---

## Decision

[Четкое утверждение принятого решения]

**We will [ACTION]**

[Подробное описание того, что именно будем делать]

---

## Alternatives Considered

### Alternative 1: [Name]

**Description**: [Краткое описание]

**Pros**:
- [Pro 1]
- [Pro 2]
- [Pro 3]

**Cons**:
- [Con 1]
- [Con 2]
- [Con 3]

**Why Rejected**: [Причина отказа]

### Alternative 2: [Name]

[Повторить структуру]

### Alternative 3: [Name]

[Повторить структуру]

---

## Consequences

### Positive

- [Положительное последствие 1]
- [Положительное последствие 2]
- [Положительное последствие 3]

### Negative

- [Негативное последствие 1]
- [Негативное последствие 2]
- [Негативное последствие 3]

### Neutral

- [Нейтральное последствие 1]
- [Нейтральное последствие 2]

---

## Implementation

**Timeline**: [Estimated time]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Migration Path**: [If applicable]

**Rollback Plan**: [How to reverse if needed]

---

## References

- [Link to design doc]
- [Link to spike/PoC]
- [Link to research]
- [Related ADRs]

---

## Notes

[Any additional context, updates, or lessons learned]

**Last Updated**: [YYYY-MM-DD]
**Updated By**: [Name]
```

## Real-World Examples

### Example 1: Database Selection

См. `assets/adr-example-database.md` для полного примера

**Key Points:**
- Context: Новый микросервис для user preferences
- Decision: PostgreSQL вместо DynamoDB
- Rationale: Complex queries, ACID requirements
- Trade-off: Scaling complexity vs query flexibility

### Example 2: Microservices Pattern

См. `assets/adr-example-microservices.md`

**Key Points:**
- Context: Monolith becoming unmaintainable
- Decision: Migrate to microservices с domain-driven design
- Rationale: Team autonomy, independent deployment
- Trade-off: Operational complexity vs development velocity

### Example 3: API Design

См. `assets/adr-example-api.md`

**Key Points:**
- Context: New public API for partners
- Decision: RESTful API с OpenAPI spec
- Alternatives: GraphQL, gRPC
- Rationale: Ecosystem maturity, client compatibility

## Decision Framework

### Evaluation Criteria Matrix

| Criterion | Weight | Alt 1 | Alt 2 | Alt 3 | Chosen |
|-----------|--------|-------|-------|-------|--------|
| **Performance** | 20% | 8/10 | 6/10 | 9/10 | Alt 3 |
| **Scalability** | 20% | 7/10 | 9/10 | 8/10 | |
| **Cost** | 15% | 9/10 | 5/10 | 7/10 | |
| **Developer Experience** | 15% | 8/10 | 7/10 | 6/10 | |
| **Operational Complexity** | 10% | 9/10 | 4/10 | 6/10 | |
| **Ecosystem Maturity** | 10% | 8/10 | 9/10 | 5/10 | |
| **Security** | 10% | 8/10 | 8/10 | 7/10 | |
| **Weighted Score** | | **8.15** | **7.05** | **7.55** | **Alt 1** |

### Trade-off Analysis Template

```markdown
## Trade-offs Summary

**Decision**: [Chosen option]

| Dimension | Gain | Loss |
|-----------|------|------|
| Performance | [What we gain] | [What we lose] |
| Complexity | [What we gain] | [What we lose] |
| Cost | [What we gain] | [What we lose] |
| Flexibility | [What we gain] | [What we lose] |

**Net Assessment**: [Overall trade-off evaluation]
```

## ADR Lifecycle

### 1. Proposed
- Decision being discussed
- Gathering input from stakeholders
- Evaluating alternatives
- Status: **Proposed**

### 2. Accepted
- Decision approved and committed
- Implementation начата или запланирована
- Status: **Accepted**

### 3. Deprecated
- Decision больше не рекомендуется
- Но legacy code может использовать
- Status: **Deprecated**

### 4. Superseded
- Decision replaced by newer ADR
- Link to superseding ADR
- Status: **Superseded by ADR-XXX**

## Organization & Storage

### Directory Structure

```
docs/
├── architecture/
│   ├── adr/
│   │   ├── README.md (index of all ADRs)
│   │   ├── 0001-use-postgres-for-user-data.md
│   │   ├── 0002-adopt-microservices-architecture.md
│   │   ├── 0003-choose-rest-over-graphql.md
│   │   ├── 0004-kubernetes-for-container-orchestration.md
│   │   ├── 0005-event-sourcing-for-audit-log.md
│   │   └── template.md
│   ├── diagrams/
│   └── rfcs/
```

### Naming Convention

```
NNNN-short-title-with-dashes.md

Examples:
0001-use-mongodb-for-session-storage.md
0002-adopt-typescript-for-frontend.md
0003-implement-oauth2-authentication.md
```

### Index File (README.md)

```markdown
# Architecture Decision Records

## Active ADRs

| ADR | Title | Status | Date | Tags |
|-----|-------|--------|------|------|
| [0005](0005-event-sourcing-for-audit.md) | Event Sourcing for Audit Log | Accepted | 2024-01-15 | data, compliance |
| [0004](0004-kubernetes-deployment.md) | Kubernetes for Deployment | Accepted | 2024-01-10 | infrastructure |
| [0003](0003-rest-api-design.md) | REST API Design | Accepted | 2024-01-05 | api, integration |

## Deprecated/Superseded

| ADR | Title | Status | Superseded By |
|-----|-------|--------|---------------|
| [0002](0002-microservices.md) | Microservices Architecture | Superseded | ADR-0010 |
| [0001](0001-mongodb-sessions.md) | MongoDB for Sessions | Deprecated | - |

## By Category

**Data & Storage**:
- ADR-0001, ADR-0005

**Infrastructure**:
- ADR-0004

**API Design**:
- ADR-0003
```

## Best Practices

### Writing Effective ADRs

✅ **Be Concise**: 1-2 pages максимум
✅ **Be Specific**: Concrete decisions, не vague statements
✅ **Show Your Work**: Document why, not just what
✅ **List Alternatives**: Показывает thorough analysis
✅ **Be Honest**: Признавать trade-offs и limitations
✅ **Update Status**: Keep lifecycle status current
✅ **Link Related**: Reference related ADRs, docs, tickets

### Common Anti-Patterns

❌ **Decision After Implementation**: ADR должен предшествовать решению
✅ Write ADR во время decision process

❌ **Too Much Detail**: ADR превращается в design doc
✅ Keep it high-level, link to detailed specs

❌ **No Alternatives**: Только описание chosen solution
✅ Document все серьезно рассмотренные варианты

❌ **Emotional Arguments**: "I like X" or "Y is obviously better"
✅ Objective criteria и data-driven reasoning

❌ **Never Updated**: Stale ADRs с incorrect status
✅ Update status when superseded или deprecated

## Integration with Development Process

### When in Development Cycle

```
Feature Request
  ↓
Requirements Analysis
  ↓
Architecture Decision Needed? ──Yes──→ Write ADR (Proposed)
  ↓                                         ↓
  No                                    Review & Discussion
  ↓                                         ↓
Design & Implementation  ←────────────  Approve ADR (Accepted)
  ↓
Code Review
  ↓
Deployment
  ↓
Retrospective ──Issues?──→ Update ADR or Create New ADR
```

### Review Process

**1. Author Creates ADR**
- Status: Proposed
- Submit PR with ADR

**2. Architecture Review**
- Architecture team reviews
- Stakeholders provide feedback
- Iterate on alternatives

**3. Decision Meeting**
- Key stakeholders attend
- Present alternatives и trade-offs
- Make decision

**4. ADR Approved**
- Merge PR
- Status: Accepted
- Communicate decision

## Tools & Automation

**ADR Tools:**
- `adr-tools` (CLI для managing ADRs)
- `log4brains` (Web UI для ADRs)
- `adr-manager` (VS Code extension)

**Commands:**
```bash
# Initialize ADR structure
adr init docs/architecture/adr

# Create new ADR
adr new "Use PostgreSQL for User Data"

# Supersede existing ADR
adr new -s 2 "Use MongoDB for User Data"

# Generate ADR graph
adr-graph -o png docs/architecture/adr
```

## Templates

См. `assets/` для:
- `adr-template.md` - Базовый шаблон
- `adr-example-database.md` - Пример выбора БД
- `adr-example-microservices.md` - Пример архитектуры
- `adr-example-api.md` - Пример API design
- `evaluation-matrix.md` - Матрица оценки альтернатив

## Success Criteria

- **Comprehensive Coverage**: Все major decisions documented
- **Up-to-Date**: Status reflects current reality
- **Easy Discovery**: Well-organized, searchable index
- **Used in Onboarding**: New engineers read ADRs
- **Referenced in Design**: Design docs link to ADRs
- **Living Documentation**: Updated when superseded
