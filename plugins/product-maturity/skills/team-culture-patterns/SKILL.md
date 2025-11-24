---
name: team-culture-patterns
description: High-performance team culture patterns from AWS, Google, Amazon, Netflix, Meta, and Microsoft. Use when building team culture, improving collaboration, establishing values, creating psychological safety, or scaling organizational effectiveness.
---

# Team Culture Patterns

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/product-maturity/skills/team-culture-patterns/{timestamp}_{кратко}.md` через Write tool (обновляй один файл по итерациям).
- Формат: цель/контекст → диагностика культуры → паттерны/решения → метрики/алерты → план/ритм → TODO → изменения vs прошлой версии.

## When to Use This Skill

- Building high-performance team culture
- Improving collaboration and communication
- Establishing team values and principles
- Creating psychological safety
- Designing team structures and topologies
- Scaling engineering organizations
- Improving hiring and onboarding
- Building learning organizations
- Addressing cultural challenges

## Overview

Proven cultural patterns from the world's most successful product companies. These patterns create environments where talented people thrive, innovate, and deliver exceptional results consistently.

## 3-итерационный контур
1) **Диагностика (2–4 ч):** оценка культуры (безопасность, доверие, ответственность, темп), eNPS/attrition, сигналы конфликтов/согласованности. Черновой бриф + risk/decision log.
2) **Дизайн (4–6 ч):** выбор 3–5 паттернов/интервенций (принципы, ритуалы, структуры, найм/онбординг), метрики/ритмы (WBR/MBR/QBR/ретро), алерты. План коммуникаций/обучения.
3) **Верификация (1–2 ч):** критерии успеха, чек-ин cadence, корректировки, фиксация изменений и TODO с владельцами/датами.

## Входы (собери до старта)
- Метрики: eNPS, attrition/retention, найм/онбординг скорость, участие в RCA/ретро, cycle time/hand-offs.
- Опросы/фидбек, конфликты, результаты перформанс-ревью, карьерные пути/роль ясность.
- Текущие ритуалы/принципы/LP, оргструктура/топологии команд, поддержка/обучение.

## Выходы (обязательно зафиксировать)
- Культурный бриф: состояние, проблемы, цели, выбранные паттерны/интервенции.
- План ритуалов/ритма, принципы/LP, коммуникации/обучение; метрики/алерты.
- TODO/владельцы/сроки, decision/risk log, изменения vs прошлой версии.

## Метрики и алерты
- eNPS/engagement, attrition/retention, скорость найма/онбординга.
- Участие в RCA/ретро, завершённость action items, конфликт/эскалации частота.
- Доля зрелых ритуалов (1:1, ретро, WBR/MBR), ясность ролей/DRI.
- Алерты: рост attrition/конфликтов, низкий eNPS, срыв ритуалов/решений, незакрытые RCA действия.

## Качество ответа (checklist)
- Проблемы и цели культуры описаны; выбранные паттерны/интервенции с метриками/алертами.
- Ритм/ритуалы и владельцы определены; план коммуникаций/обучения задан.
- Decision/risk logs обновлены; TODO/сроки/ответственные есть; изменения зафиксированы.

## Red Flags
- Нет метрик/опросов, решения принимаются по ощущениям.
- Нет ритуалов/ритма или они не связаны с метриками/проблемами.
- Отсутствуют владельцы/сроки, нет плана коммуникаций/обучения.
- Игнорируется психологическая безопасность; конфликты подавляются или не адресуются.

## Паттерны (применяй осознанно)
- **Amazon LP:** Customer Obsession, Ownership, Dive Deep, Disagree & Commit — прошивай в решения/ревью/найм.
- **Netflix Freedom & Responsibility:** контекст вместо контроля, talent density, keeper test.
- **Google Psychological Safety:** turn-taking, social sensitivity, blameless postmortems, право на ошибку.
- **Team Topologies:** stream-aligned/platform/enabling/complicated-subsystem; ясные взаимодействия (collab/assist/ сервис).
- **Rituals:** 1:1, ретро, WBR/MBR, design/tech reviews, open Q&A, office hours.

## Шаблон артефакта
```markdown
# Культурный бриф
**Дата:** {timestamp} | **Этап:** Диагностика/Дизайн/Верификация

## Контекст и цели
- Проблемы/сигналы, целевые метрики (eNPS/attrition/ритуалы/конфликты)

## Диагностика
- Таблица: сфера (безопасность/коммуникации/ответственность/найм/обучение/ритмы) → факты/метрики → риски

## Паттерны и план
- Выбранные паттерны (Amazon/Netflix/Google/Topologies), что меняем, владельцы/сроки
- Метрики/алерты, коммуникации/обучение, ритм чек-инов

## Риски и допущения
- Потенциальные сопротивления, зависимые функции

## TODO и изменения
- Список действий, статусы, изменения vs предыдущей версии
```

## Cultural Philosophies

### Amazon: Leadership Principles

**14 Leadership Principles** that guide every decision:

1. **Customer Obsession**: Start with customer, work backwards
2. **Ownership**: Act on behalf of entire company, long-term thinking
3. **Invent and Simplify**: Seek new ideas, simplify complex
4. **Are Right, A Lot**: Good judgment, strong instincts, seek diverse perspectives
5. **Learn and Be Curious**: Never done learning, always improving
6. **Hire and Develop the Best**: Raise performance bar with every hire
7. **Insist on the Highest Standards**: Relentlessly high standards
8. **Think Big**: Bold direction inspires results
9. **Bias for Action**: Speed matters, calculated risk-taking
10. **Frugality**: Do more with less, resourcefulness
11. **Earn Trust**: Listen, speak candidly, treat others respectfully
12. **Dive Deep**: Stay connected to details, audit frequently
13. **Have Backbone; Disagree and Commit**: Challenge decisions, commit once decided
14. **Deliver Results**: Focus on key inputs, deliver with right quality

**Application:**
- Every interview question maps to principles
- Performance reviews evaluated against principles
- Decision-making guided by principles
- Cultural consistency across organization

**Example in Practice:**
```markdown
# Decision: Should we delay feature to improve quality?

## Leadership Principles Analysis

**Customer Obsession** ✅
- Customers prefer reliable features over rushed ones

**Ownership** ✅
- Long-term reputation more important than short-term deadline

**Insist on the Highest Standards** ✅
- Our quality bar requires more testing

**Deliver Results** ⚠️
- Missing deadline impacts business goals

**Bias for Action** ⚠️
- Delay means lost opportunity

## Decision: Delay by 1 week, add testing, launch with quality
Rationale: Customer trust is long-term asset, one week delay is acceptable
```

### Netflix: Freedom and Responsibility

**Core Philosophy:** Responsible people thrive on freedom; become more innovative and effective.

**Cultural Pillars:**

**1. Context, Not Control**
- Leaders provide context (strategy, goals, priorities)
- Teams have freedom to execute
- Trust over micromanagement

**2. Highly Aligned, Loosely Coupled**
- Clear goals and strategy (alignment)
- Teams decide how to achieve (loose coupling)
- Collaboration without coordination overhead

**3. No Rules Rules**
- Minimize policies and procedures
- Hire adults who don't need babysitting
- Context enables good decisions

**4. Keeper Test**
- "If person resigned, would you fight to keep them?"
- If no, help them find better fit elsewhere
- High performance over tenure

**Implementation:**
```markdown
## Netflix Culture Practices

### Unlimited Vacation
- No tracking, no approval process
- Responsible adults take what they need
- Managers model good behavior

### No Expense Policy
- Guideline: "Act in Netflix's best interest"
- Employees use judgment
- Rare abuse handled individually

### Context Documents
- Strategy memos shared widely
- Quarterly business reviews transparent
- Information flows freely

### Talent Density
- Pay top of market
- Adequate performance → generous severance
- Keep performance bar rising
```

### Google: Psychological Safety

**Project Aristotle Research:** Studied 180+ teams to find what makes teams effective.

**Key Finding:** Psychological safety is most important factor.

**Psychological Safety:** Team members feel safe to take risks, be vulnerable, speak up without fear of embarrassment or punishment.

**Five Key Dynamics:**
1. **Psychological Safety**: Can take risks without feeling insecure
2. **Dependability**: Count on each other for quality work
3. **Structure & Clarity**: Clear roles, plans, goals
4. **Meaning**: Work is personally important
5. **Impact**: Work matters and creates change

**Building Psychological Safety:**

**Leadership Behaviors:**
- Admit mistakes openly
- Ask for feedback genuinely
- Welcome questions and challenges
- Respond positively to bad news
- Share credit, take blame

**Team Practices:**
- **Turn-taking**: Everyone speaks roughly equally
- **Social sensitivity**: Reading others' emotions
- **No interruptions**: Everyone heard
- **Disagree without judgment**: Ideas challenged, not people
- **Blameless post-mortems**: Learn from failures

**Conversation Framework:**
```markdown
## Blameless Post-Mortem Template

### What Happened?
[Timeline of events, factual]

### What Was the Impact?
[Users affected, duration, business impact]

### What Went Well?
[Effective responses, what limited damage]

### What Went Wrong?
[System failures, not people failures]
- Configuration X was set to Y
- Monitoring didn't alert on Z
- Process didn't catch A

### What Did We Learn?
[Insights about systems, processes]

### What Will We Change?
[Actionable improvements with owners]
- [ ] Action item 1 (Owner: @person, Due: date)
- [ ] Action item 2 (Owner: @person, Due: date)

### Thank Yous
[Recognize people who helped]
```

### Meta: Move Fast Together

**Cultural Values:**

**1. Move Fast**
- Bias toward action and impact
- Don't wait for perfect
- Learn by doing

**2. Be Bold**
- Take risks, big thinking
- Challenge conventional
- Ambitious goals

**3. Focus on Impact**
- Prioritize high-impact work
- Ruthless prioritization
- Say no to low-impact

**4. Be Open**
- Radical transparency
- Information flows freely
- Direct communication

**5. Build Social Value**
- Connect the world
- Technology serves people
- Responsibility to society

**Practices:**

**Bootcamp (Onboarding):**
```markdown
## 6-Week Bootcamp Program

### Week 1-2: Foundations
- Codebase orientation
- Ship first diff (code change)
- Meet cross-functional partners
- Shadow on-call rotation

### Week 3-4: Exploration
- Rotate through 3-4 teams
- Work on small tasks for each
- Understand different product areas
- Identify interests

### Week 5-6: Team Selection
- Choose team based on interest + need
- Start ramping on team
- Complete bootcamp project
- Ramp to full productivity

Benefits:
- Engineers understand broader product
- Teams compete for talent (quality bar)
- Engineers find best fit
- Faster productivity
```

**Hack-a-thons:**
- Regular (quarterly) hack events
- Work on anything for 24-48 hours
- Demo to company
- Best ideas get resourced
- Innovation pipeline

### Microsoft: Growth Mindset

**Cultural Transformation (Satya Nadella era):**

**From:**
- Know-it-all culture
- Internal competition
- Not invented here syndrome
- Arrogance

**To:**
- Learn-it-all culture
- Collaboration
- Partner with anyone
- Customer empathy

**Growth Mindset Principles:**

**1. Customer Obsession**
- Understand customer needs deeply
- Empathy over ego
- Success measured by customer success

**2. Diversity and Inclusion**
- Diverse perspectives drive innovation
- Inclusion creates belonging
- Everyone can contribute

**3. One Microsoft**
- Break down silos
- Collaborate across boundaries
- Company success over team success

**4. Growth Mindset**
- Challenges are opportunities
- Failure is learning
- Continuous improvement

**Implementation:**
```markdown
## Growth Mindset in Action

### Performance Reviews
**Old:** Individual achievements, competitive ranking
**New:** Learning, collaboration, customer impact

### Team Meetings
**Old:** Status updates, top-down
**New:** Learning shares, bottom-up ideas

### Innovation
**Old:** Compete with external products
**New:** Partner and integrate (e.g., Linux on Azure)

### Hiring
**Old:** Hire for what they know
**New:** Hire for learning potential

### Failure Response
**Old:** "Who messed up?"
**New:** "What did we learn?"
```

## Team Topologies

### Two-Pizza Teams (Amazon/AWS)

**Principle:** Team should be small enough to feed with two pizzas (8-10 people).

**Characteristics:**
- Full-stack capability
- End-to-end ownership
- Minimal dependencies
- Clear APIs between teams

**Structure:**
```
Two-Pizza Team (8-10 people)
├── Product Manager (1)
├── Engineering Manager (1)
├── Software Engineers (4-6)
├── Designer (0.5-1)
└── QA/Data (0.5-1)

Owns:
- Product roadmap
- Codebase
- Services
- Infrastructure
- Operations
- Metrics
```

**Benefits:**
- Fast decision-making
- High autonomy
- Clear accountability
- Low coordination overhead

**Challenges:**
- Finding right boundaries
- Shared infrastructure
- Cross-cutting concerns
- Technical standards consistency

### Platform Teams (Google)

**Structure:**
```
Product Development
├── Platform Teams (provide infrastructure)
│   ├── Core Infrastructure
│   ├── Developer Tools
│   ├── Data Platform
│   └── ML Platform
└── Product Teams (build features)
    ├── Product Team 1
    ├── Product Team 2
    └── Product Team N
```

**Platform Team Mission:**
- Build self-service tools
- Reduce cognitive load
- Increase productivity
- Maintain consistency

**Example:**
```markdown
## ML Platform Team

### Services Provided:
- Model training infrastructure
- Feature store
- Model deployment
- A/B testing framework
- Model monitoring

### Customers:
- All product teams that use ML

### Success Metrics:
- Time to deploy model: < 1 day
- Platform adoption: 90%+ of ML models
- Customer satisfaction: NPS > 40
- Incidents caused by platform: < 1/month
```

### Squad Model (Spotify)

**Structure:**
```
Tribe (40-150 people)
├── Squad 1 (6-12 people)
├── Squad 2 (6-12 people)
└── Squad 3 (6-12 people)

Chapter (functional group across squads)
├── Backend Chapter
├── Frontend Chapter
└── QA Chapter

Guild (community of practice)
├── Web Guild
├── Data Guild
└── Testing Guild
```

**Squads:**
- Cross-functional
- Long-lived
- Mission-focused
- Autonomous

**Chapters:**
- Functional expertise
- Career development
- Best practices
- Skill building

**Guilds:**
- Interest-based communities
- Knowledge sharing
- Cross-pollination
- Optional participation

## Communication Patterns

### Amazon: Writing Culture

**6-Pager Narrative:**
- No PowerPoint presentations
- Write full prose documents
- First 20 minutes of meeting: silent reading
- Forces clear thinking

**Why Writing?**
- Complete thoughts, not bullet points
- Everyone starts with same context
- Encourages depth over superficiality
- Archived for future reference

**Email Culture:**
- Detailed, thoughtful
- CC minimal (ownership clear)
- Subject lines specific
- Action items explicit

### Asynchronous First (Remote-Friendly)

**Principles:**
1. **Document by default**: Write it down
2. **Async-first communication**: Don't assume synchronous
3. **Transparent context**: Share widely
4. **Minimize meetings**: Respect time zones
5. **Over-communicate**: Clarity over brevity

**Tools and Practices:**
```markdown
## Async Communication Guidelines

### Documentation
- Decision records (ADRs)
- Meeting notes (public by default)
- Design docs
- Status updates

### Communication Channels
- **Chat**: Urgent, quick questions
- **Email**: Important, needs response
- **Docs**: Collaboration, feedback
- **Meetings**: Decision-making only

### Response Time Expectations
- **Urgent (P0)**: < 1 hour
- **Important (P1)**: < 4 hours
- **Normal (P2)**: < 24 hours
- **Low (P3)**: < 3 days

### Meeting Hygiene
- Agenda required
- Pre-reads shared 24h before
- Record for those who can't attend
- Notes and decisions documented
```

### Standups (Synchronous)

**Format:**
```markdown
## Daily Standup (15 min max)

### Round Robin (2 min each):
**Yesterday:** Shipped mobile checkout UI
**Today:** Integrating payment API
**Blockers:** Need design approval on error states

### Parking Lot:
- Detailed discussions after standup
- Only relevant people stay
```

**Anti-patterns:**
- Status reports to manager
- Detailed problem-solving
- Over 15 minutes
- Not discussing blockers

## Hiring and Onboarding

### Bar Raiser Program (Amazon)

**Concept:** Designated interviewers who ensure every hire raises the bar.

**Bar Raiser Role:**
- Trained interviewer
- Not on hiring team (objective)
- Veto power over hire
- Guards long-term culture

**Process:**
```markdown
## Interview Loop

1. Phone Screen (45 min)
   - Recruiter or engineer
   - Basic technical assessment

2. On-site (4-5 hours)
   - Coding (2 rounds)
   - System design (1 round)
   - Behavioral (2 rounds)
   - Bar raiser (1 round, overlaps with others)

3. Debrief
   - Each interviewer shares feedback
   - Bar raiser facilitates
   - Unanimous decision required
   - "Would this person raise our bar?"
```

**Benefits:**
- Consistent quality
- Long-term thinking
- Cultural consistency
- Reduced bias

### Google: Structured Interviewing

**Principles:**
- Same questions for all candidates
- Rubrics for evaluation
- Independent assessors
- Committee decision (not manager alone)

**Interview Types:**
1. **Coding**: Algorithm and data structures
2. **System Design**: Architecture and scalability
3. **Behavioral**: Past behavior predicts future
4. **Googleyness**: Collaboration, culture fit

**Hiring Committee:**
- 4-5 senior engineers
- Review interview feedback
- Independent of hiring team
- Consistent standards

### Onboarding Excellence

**First Day:**
```markdown
## New Engineer - Day 1

### Before Arrival:
- [ ] Laptop configured and shipped
- [ ] Accounts created (email, GitHub, Slack)
- [ ] Welcome email sent
- [ ] Buddy assigned
- [ ] Manager 1:1 scheduled

### Day 1 Schedule:
- 9:00: Welcome by manager
- 9:30: IT setup help
- 10:00: Buddy introduction
- 10:30: Codebase walkthrough
- 12:00: Team lunch
- 1:00: Security and compliance training
- 2:00: Development environment setup
- 3:00: First commit (typo fix, documentation)
- 4:00: Team standup
- 4:30: Day 1 retro with buddy

### Day 1 Goals:
- [ ] Laptop working
- [ ] Can build and run tests locally
- [ ] First commit merged
- [ ] Met team
- [ ] Feel welcome
```

**First Week:**
```markdown
## New Engineer - Week 1

### Learning:
- Product walkthrough
- Architecture overview
- Development workflow
- Testing strategy
- Deployment process

### Doing:
- Fix 2-3 beginner-friendly bugs
- Add tests to existing code
- Improve documentation
- Shadow on-call

### Connecting:
- 1:1 with manager
- Coffee chats with team members
- Attend team meetings
- Join relevant Slack channels
```

**First Month:**
```markdown
## New Engineer - Month 1

### Milestones:
- [ ] Shipped meaningful feature
- [ ] Understand team's product area
- [ ] Participated in on-call rotation
- [ ] Contributed to design discussions

### Feedback:
- 30-day check-in with manager
- Buddy feedback
- Self-assessment
- Adjustments for month 2
```

## Learning and Development

### 20% Time (Google)

**Concept:** Spend 20% of time on projects outside core work.

**Examples:**
- Gmail started as 20% project
- Google News started as 20% project
- AdSense started as 20% project

**Implementation:**
```markdown
## 20% Time Guidelines

### Eligible Projects:
- Aligned with company goals
- Learning new skills
- Exploring new technologies
- Improving internal tools

### Process:
1. Propose project to manager
2. Get approval (usually yes)
3. Work 1 day per week (or block time)
4. Demo results to team
5. Option to make it full-time if successful

### Success Criteria:
- Learning occurred
- Prototype created
- Insights shared
- Or: Product launched!
```

### Tech Talks and Knowledge Sharing

**Regular Cadences:**
```markdown
## Knowledge Sharing Schedule

### Weekly (Team Level):
- **Lunch & Learn**: 30 min, anyone can present
- **Code Review Discussion**: Interesting PRs
- **Incident Review**: Learn from outages

### Monthly (Organization Level):
- **Tech Talk**: 1 hour, deep dive on technology
- **Engineering All-Hands**: Company updates
- **Demo Day**: Teams show what they shipped

### Quarterly (Company Level):
- **Conference Learnings**: Share external conferences
- **Innovation Showcase**: Hack-a-thon demos
- **Strategy Review**: Where we're heading
```

**Tech Talk Template:**
```markdown
# Tech Talk: [Topic]

## Presenter: [Name]
## Date: [Date]
## Duration: 45 min + 15 min Q&A

### Abstract:
[What will audience learn?]

### Outline:
1. Problem/Context (5 min)
2. Solution Overview (10 min)
3. Technical Deep Dive (20 min)
4. Results and Learnings (10 min)
5. Q&A (15 min)

### Target Audience:
[Who should attend?]

### Prerequisites:
[What should audience know beforehand?]

### Resources:
[Slides, code, documentation]
```

### Conferences and External Learning

**Professional Development Budget:**
```markdown
## Annual Learning Budget: $2,000/person

### Eligible Expenses:
- Conference tickets
- Travel and accommodation
- Online courses (Coursera, Udemy, etc.)
- Books
- Certifications (AWS, GCP, etc.)

### Expectations:
- Share learnings with team
- Apply knowledge to work
- Blog post or tech talk
```

## Performance and Recognition

### Continuous Feedback Culture

**Regular 1:1s:**
```markdown
## Manager-Direct Report 1:1 (Weekly, 30 min)

### Agenda:
1. **You (10 min)**: How are you? Blockers? Concerns?
2. **Work (10 min)**: Project updates, priorities
3. **Growth (10 min)**: Career development, feedback

### Manager Preparation:
- Review recent work
- Note feedback to share
- Prepare career discussion

### Direct Report Preparation:
- Agenda items to discuss
- Questions for manager
- Feedback to give upward
```

**Peer Feedback:**
```markdown
## Peer Feedback (Quarterly)

### Request Feedback From:
- Collaborators on projects
- Code reviewers
- Cross-functional partners

### Feedback Areas:
- Technical skills
- Communication
- Collaboration
- Impact
- Growth areas

### Format:
- Anonymous or attributed (recipient choice)
- Specific examples
- Actionable suggestions
```

### Recognition Programs

**Peer Recognition:**
```markdown
## Kudos Program

### How It Works:
- Anyone can give kudos to anyone
- Public in Slack channel
- Tied to company values
- Manager notified

### Example:
@jane shipped the mobile checkout ahead of schedule while maintaining high quality. Great example of "Move Fast" and "Insist on High Standards"! 🎉

### Impact:
- Builds positive culture
- Reinforces values
- Boosts morale
- Costs nothing
```

**Spot Bonuses:**
- Manager-initiated
- Immediate (not annual)
- Significant impact
- $500-$5,000 range

## Anti-Patterns to Avoid

**Toxic Patterns:**
1. **Hero Culture**: Dependence on individuals, not systems
2. **Blame Culture**: Fear-based, hiding mistakes
3. **Crunch Culture**: Unsustainable hours, burnout
4. **Brilliant Jerks**: Tolerating bad behavior for skills
5. **Information Hoarding**: Knowledge as power
6. **HiPPO Decisions**: Highest paid person's opinion
7. **Process Over People**: Bureaucracy without value
8. **Zero Feedback**: No growth, surprises in reviews

**Warning Signs:**
- High turnover (especially top performers)
- Low engagement scores
- Frequent conflicts
- Lack of innovation
- Siloed teams
- Slow decision-making
- Fear of failure
- Burnout

## Reference Materials

See `references/` directory for:
- Complete culture handbooks
- Interview templates
- Onboarding checklists
- 1:1 guides
- Recognition program examples

See `assets/` directory for:
- Team topology diagrams
- Communication flow examples
- Meeting templates
- Org chart patterns

## Success Indicators

This skill is being applied effectively when:
- High employee satisfaction (eNPS > 40)
- Low regrettable attrition (< 5%)
- Fast onboarding (productive in < 2 weeks)
- Psychological safety (team speaks up)
- High collaboration (cross-team projects)
- Innovation happening (20% time projects)
- Learning culture (regular tech talks)
- Diverse perspectives (inclusion)
