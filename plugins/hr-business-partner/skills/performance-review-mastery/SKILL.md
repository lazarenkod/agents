---
name: performance-review-mastery
description: Мастерство проведения performance review на уровне AWS, Google, Microsoft, Netflix, NVIDIA. Continuous feedback, OKR-based reviews, calibration, 360-degree feedback, performance improvement plans. Use when conducting performance reviews, calibrating ratings, managing underperformance, or designing performance management systems.
---

# Performance Review Mastery

Мастерство проведения performance review и управления performance на основе лучших практик AWS, Google, Microsoft, Netflix, NVIDIA, OpenAI, Stripe.

## Формат работы и сохранение результатов

- Все решения формулируй на русском языке и фиксируй в markdown через Write tool.
- Сохраняй материалы по пути `outputs/hr-business-partner/skills/performance-review-mastery/{timestamp}_{case}.md`.
- Каждую задачу прорабатывай в трех циклах: Диагностика контекста → Проектирование механики review/калибровок → Валидация, план внедрения и метрики.
- В отчетах отражай входные данные, выбранные фреймворки, планы коммуникаций, KPI (rating distribution, pay outcomes, talent risk) и ссылки на assets.

## Asset & Reference Toolkit

- **Assets**: `assets/annual-performance-review-template.md`, `assets/okr-review-template.md`, `assets/calibration-meeting-deck.md`, `assets/performance-improvement-plan-template.md`, `assets/feedback-synthesis-template.md`, `assets/promotion-case-template.md`.
- **References**: `references/ratings-distribution-benchmarks.md`, `references/continuous-feedback-rituals.md`, `references/google-performance-system-case.md`, `references/netflix-talent-density-notes.md`.
- Все использованные артефакты прикладывай к markdown с пометкой итерации.

## Когда использовать этот скилл

- Проведение annual/semi-annual performance reviews
- Continuous performance management и feedback
- Calibration процессы для обеспечения справедливости
- Управление underperformance и Performance Improvement Plans (PIPs)
- Разработка системы performance management
- 360-degree feedback процессы
- Промоционные решения и talent reviews
- Связь performance с compensation

## Базовые концепции

### 1. Эволюция Performance Management

**Traditional Model (устаревший)**
```
✗ Annual performance review (раз в год)
✗ Forced ranking (stack ranking)
✗ Past-focused (что было сделано)
✗ Manager-driven (односторонняя оценка)
✗ Tied directly to compensation (creates gaming)
```

**Modern Model (best practices)**
```
✓ Continuous feedback (регулярные check-ins)
✓ Growth-focused (развитие, а не punishment)
✓ Forward-looking (что можно улучшить)
✓ 360-degree input (multiple perspectives)
✓ Separated from compensation conversations
```

**Why Companies Moved Away from Traditional Reviews:**

**Microsoft (2013) - Abandoned Stack Ranking**
```
Problem:
- Stack ranking forced managers to rate team members against each other
- Created competition instead of collaboration
- High performers avoided joining strong teams
- Demotivated employees ("my team is too strong, I'll always be middle-ranked")

Solution (Growth Mindset Culture):
- Focus on individual growth, not relative ranking
- Peer collaboration rewarded
- Multiple career paths (IC and management)
- Continuous feedback, not annual reviews
```

**Adobe (2012) - Eliminated Annual Reviews**
```
Problem:
- Managers spent 80,000 hours annually on performance reviews
- Employees disliked the process
- No correlation between ratings and actual performance

Solution (Check-in Model):
- Quarterly "check-ins" (informal feedback conversations)
- Ongoing feedback throughout year
- Real-time course corrections
- Result: 30% reduction in voluntary attrition
```

### 2. Continuous Performance Management

**Weekly 1-on-1 Framework**

**Структура эффективного 1-on-1 (30-60 минут):**
```
10 мин: Personal check-in
- "How are you doing?" (not just work, но life)
- Energy levels, stress, work-life balance
- Personal wins and challenges

20 мин: Performance & Growth
- Progress on key projects/OKRs
- Wins этой недели (celebrate!)
- Blockers and support needed
- Skill development discussion

15 мин: Coaching & Feedback
- Specific feedback (SBI model - Situation-Behavior-Impact)
- Career development discussion
- Stretch opportunities
- Manager shares context on team/company strategy

5 мин: Action Items & Next Steps
- Clear action items with owners
- Timeline for deliverables
- Next 1-on-1 agenda items
```

**Google - Feedback Best Practices:**
```
"Give feedback early and often, don't save it for performance reviews"

FAST Feedback:
- Frequent: Weekly in 1-on-1s, real-time when possible
- Accurate: Specific examples, not generalities
- Specific: SBI model (Situation-Behavior-Impact)
- Timely: Within 24-48 hours of observed behavior
```

**Netflix - Continuous Feedback Culture:**
```
360-Degree Feedback (continuous, not annual):
- Anyone can give feedback to anyone, anytime
- Use "Start, Stop, Continue" framework
  - Start: What should the person start doing?
  - Stop: What should they stop doing?
  - Continue: What are they doing well?

Radical Candor:
- Care personally + Challenge directly
- Avoid "Ruinous Empathy" (nice but not helpful)
- Avoid "Obnoxious Aggression" (brutal without care)
- Seek "Radical Candor" (honest feedback with empathy)
```

### 3. OKR-Based Performance Reviews

**Google/Intel OKR Methodology**

**OKR Structure:**
```
Objective: Качественная цель (inspirational, ambitious)
Key Results: 3-5 измеримых результатов (quantifiable, time-bound)

Example:
Objective: "Become the go-to platform for AI developers"

Key Results:
1. Increase API calls from 10M to 50M per month
2. Achieve 95%+ uptime SLA across all services
3. Ship 5 major developer-requested features
4. Grow developer community from 5K to 25K members
5. Achieve NPS > 60 from developer survey
```

**Performance Review based on OKRs:**

**Quarterly Review Template:**
```markdown
# Q1 2024 Performance Review: {Employee Name}

## OKR Achievement

### Objective 1: {Objective}
**Achievement: 85%** (Target: 70% is success)

Key Results:
1. [KR1]: Actual: 45M, Target: 50M → 90% ✓
2. [KR2]: Actual: 97%, Target: 95% → 100% ✓✓
3. [KR3]: Actual: 4, Target: 5 → 80% ✓
4. [KR4]: Actual: 22K, Target: 25K → 88% ✓
5. [KR5]: Actual: 65, Target: 60 → 100% ✓✓

**Impact**: Significantly grew platform adoption and developer satisfaction.
Platform is now #2 in market share (up from #4).

## What Went Well
- Exceeded uptime SLA through proactive monitoring improvements
- Developer community engagement increased dramatically
- Strong collaboration with product and marketing teams

## Growth Areas
- Could improve feature prioritization (shipped 4/5, missed social auth)
- Needs to delegate more (took on too much solo work)
- Should present work more visibly to leadership

## Career Development
- Ready for promotion to Senior Engineer (meets 90% of criteria)
- Focus areas for next level: Technical leadership, mentoring junior engineers
- Stretch goal: Tech lead role on new AI platform project
```

**Google OKR Grading:**
- **0.0-0.3**: We failed to make real progress (red flag)
- **0.4-0.6**: Made progress but fell short (needs investigation)
- **0.7-0.9**: We delivered! (success, this is the target)
- **1.0**: Sandbagging (OKRs were not ambitious enough)

**Key Insight**: 70% achievement is SUCCESS because OKRs should be stretch goals.

### 4. Rating Scales & Calibration

**Amazon Performance Ratings (pre-2023):**
```
Top Tier (TT) - 20% of team
- Exceptional performance, exceeds expectations significantly
- Demonstrates all leadership principles consistently
- Ready for next level or high-impact projects

Highly Valued (HV) - 70% of team
- Strong performance, meets expectations
- Demonstrates most leadership principles
- Solid contributor, growth potential

Least Effective (LE) - 10% of team
- Does not meet expectations
- Performance Improvement Plan or exit
- Not demonstrating leadership principles

Note: Amazon moved away from labels in 2023, but calibration concept remains
```

**Google Performance Ratings:**
```
5-Point Scale (normalized across company):

1. Needs Improvement (5%)
- Does not meet expectations
- Performance plan required
- May not be a fit for role

2. Consistently Meets Expectations (25%)
- Solid performer
- Delivers on commitments
- Meets role expectations

3. Exceeds Expectations (50%)
- Strong performer (this is the target)
- Goes beyond role requirements
- Role model for others

4. Strongly Exceeds Expectations (15%)
- Top performer
- Significant impact beyond role
- Promotion candidate

5. Superb (5%)
- Exceptional, transformational impact
- Sets new standards
- Consistently exceeds highest expectations

Distribution is a guide, not forced ranking.
```

**Microsoft - No More Ratings:**
```
After 2013, Microsoft eliminated numerical ratings:
- Focus on Growth Mindset development
- Qualitative feedback instead of numbers
- Compensation decisions separate from performance discussions

Review Structure:
1. Impact: What did you accomplish?
2. Learning: How did you grow?
3. Collaboration: How did you help others succeed?
```

**Calibration Process**

**Purpose**: Ensure consistency and fairness across teams and managers.

**Calibration Session Structure (2-3 hours, 20-30 employees):**
```
Pre-Calibration (Week before):
- Managers draft performance assessments
- Rate employees on scale
- Prepare evidence (examples, data, feedback)

Calibration Session:
1. Overview (10 min): Review process, rating distribution, criteria

2. Discuss High Ratings (30 min):
   - Managers present "Exceeds" and "Superb" ratings
   - Share specific examples and impact
   - Group discusses: Is this rating appropriate?
   - Ensure high bar for top ratings

3. Discuss Low Ratings (30 min):
   - Managers present "Needs Improvement" ratings
   - Share evidence and context
   - Discussion: PIP, coaching, or exit?
   - Ensure fairness and due process

4. Normalize Middle (60 min):
   - Discuss "Meets/Exceeds" ratings
   - Compare similar roles across teams
   - Identify outliers (too harsh or too lenient)
   - Adjust ratings for consistency

5. Final Review (15 min):
   - Review final distribution
   - Identify promotions and PIPs
   - Plan for compensation and development
```

**Calibration Principles:**
- **Consistency**: Similar performance = similar rating across teams
- **Fairness**: No bias based on team, manager, tenure, demographics
- **Evidence-based**: Ratings supported by data and examples
- **Transparency**: Clear criteria and process
- **Development**: Focus on growth, not punishment

### 5. 360-Degree Feedback

**Netflix 360-Degree Feedback Process**

**Annual 360 Survey Structure:**
```
Participants:
- Self-assessment
- Manager assessment
- 3-5 peer assessments (chosen by employee)
- 2-3 cross-functional partner assessments
- Direct reports (if manager)

Questions (6-8 open-ended):
1. What should [Name] START doing?
2. What should [Name] STOP doing?
3. What should [Name] CONTINUE doing?
4. Describe [Name]'s biggest strength.
5. Describe one area for growth/development.
6. How well does [Name] embody our values? (specific examples)
7. Additional comments (optional)
```

**Google 360-Degree Peer Feedback:**
```
Peer Feedback Input (for performance review):
- Manager selects 4-6 peers (with employee input)
- Peers complete short survey (15 min)
- Feedback aggregated into themes
- Manager incorporates into performance review

Questions:
1. What are [Name]'s key strengths? (2-3 examples)
2. What could [Name] do to be even more effective? (1-2 areas)
3. Rate [Name] on:
   - Technical expertise (1-5)
   - Collaboration (1-5)
   - Communication (1-5)
   - Impact (1-5)
```

**Best Practices for 360 Feedback:**
```
✓ Anonymous peer feedback (encourages honesty)
✓ Multiple perspectives (avoid bias)
✓ Specific examples (not vague generalizations)
✓ Focus on behaviors, not personality
✓ Balanced (strengths + growth areas)
✗ Avoid: Forced ratings, comparison to others
✗ Avoid: Used punitively (should be developmental)
```

### 6. Performance Improvement Plans (PIPs)

**Purpose of PIPs**: Give underperforming employees clear expectations and support to improve OR document performance issues before termination.

**PIP Success Rate**: ~15-20% successfully complete PIP and return to good standing. Most PIPs result in exit (mutual or involuntary).

**When to use PIP:**
- Consistent underperformance despite coaching
- Quality issues (bugs, mistakes, missed deadlines)
- Behavioral issues (attitude, collaboration, communication)
- Not meeting role expectations (skill gaps)

**When NOT to use PIP:**
- Serious misconduct (immediate termination)
- Layoff/restructuring (not a performance issue)
- Culture fit issues (address differently)
- New hire in first 90 days (extend onboarding or exit)

**PIP Structure (60-90 days):**

```markdown
# Performance Improvement Plan
**Employee**: {Name}
**Role**: {Title}
**Manager**: {Manager Name}
**Start Date**: {Date}
**End Date**: {Date + 60-90 days}
**HR Partner**: {Name}

## Current Performance Issues
Specific, documented examples of underperformance:

1. **Issue**: Code quality below standards
   - **Example**: Last 5 PRs had 15+ bugs found in QA (team average: 3)
   - **Impact**: Delays in releases, QA team overload
   - **Expected**: Max 5 bugs per PR, first-pass QA success rate 80%+

2. **Issue**: Missed project deadlines
   - **Example**: Missed Q1 API project deadline by 4 weeks (committed to March 31)
   - **Impact**: Partner team blocked, roadmap slipped
   - **Expected**: Meet committed deadlines or communicate risks 2+ weeks in advance

3. **Issue**: Communication gaps
   - **Example**: Did not update team on blockers in 3 standups, causing last-minute scrambles
   - **Impact**: Team had to re-plan sprints, missed dependencies
   - **Expected**: Proactive communication of blockers, daily standup updates

## Expectations & Goals
Clear, measurable goals for improvement:

### Goal 1: Code Quality
- **Target**: 80%+ first-pass QA success rate
- **Measurement**: QA bug counts, PR review feedback
- **Support**: Pair programming with Senior Engineer 3hrs/week
- **Check-in**: Weekly code review with Tech Lead

### Goal 2: Project Delivery
- **Target**: Deliver Sprint commitments 100% (next 6 sprints)
- **Measurement**: Sprint board, JIRA tickets completed on time
- **Support**: Manager helps with scope/prioritization, daily check-ins
- **Check-in**: End of each 2-week sprint retrospective

### Goal 3: Communication
- **Target**: Proactive updates in standups, flag blockers within 24hrs
- **Measurement**: Manager observation, peer feedback
- **Support**: 1-on-1 communication coaching with manager
- **Check-in**: Weekly feedback from manager and peers

## Support & Resources
- **Manager 1-on-1s**: 2x per week (Monday, Thursday)
- **Mentorship**: Assigned senior engineer mentor (3 hrs/week pairing)
- **Training**: Udemy course on code quality & testing (complete by Week 3)
- **Tools**: Access to better testing tools (approved budget)

## Timeline & Milestones

**Week 2 (Check-in 1)**:
- Review progress on Goals 1-3
- Adjust support if needed
- Continue or escalate

**Week 4 (Mid-Point Review)**:
- Assess 50% progress toward goals
- Decision: On track, needs adjustment, or exit conversation

**Week 8 (Final Review)**:
- Evaluate goal achievement
- Decision: Return to good standing, extend PIP 30 days, or exit

## Consequences
If goals are not met by end date:
- Employment may be terminated
- OR extension of PIP for additional 30 days (rare)

## Acknowledgment
I understand the expectations outlined in this PIP. I commit to working toward these goals with the support provided.

**Employee Signature**: _________________ Date: _______
**Manager Signature**: _________________ Date: _______
**HR Partner Signature**: _______________ Date: _______
```

**PIP Best Practices:**
```
✓ Specific examples and expectations (not vague)
✓ Measurable goals (quantitative targets)
✓ Sufficient support (mentoring, training, tools)
✓ Regular check-ins (don't wait until end)
✓ Documented (written PIP document, signed)
✓ HR involvement (ensure legal compliance)
✓ Respectful (focus on improvement, not punishment)

✗ Avoid: Vague expectations ("be better")
✗ Avoid: Unrealistic goals (impossible to achieve)
✗ Avoid: Surprise PIPs (should have prior coaching)
✗ Avoid: Using PIP as termination paperwork (unethical)
```

### 7. Promotion Processes

**Levels & Career Ladders**

**Example: Engineering Career Ladder (common across big tech)**
```
IC Track:
- L3: Junior Engineer (0-2 years)
- L4: Software Engineer (2-4 years)
- L5: Senior Engineer (4-7 years) ← ~40% of engineers
- L6: Staff Engineer (8+ years, ~10% of engineers)
- L7: Senior Staff Engineer (10+ years, ~3%)
- L8: Principal Engineer (12+ years, <1%)
- L9: Distinguished Engineer (15+ years, <<1%)

Management Track:
- L5: Engineering Manager (5-8 direct reports)
- L6: Senior Engineering Manager (2-3 teams, 12-20 people)
- L7: Director of Engineering (4-6 managers, 40-80 people)
- L8: Senior Director (multiple directors, 100-200 people)
- L9: VP of Engineering (org of 300-1000 people)
- L10: SVP / CTO (company-wide)
```

**Promotion Criteria (Google L4 → L5 Example):**
```
Technical Ability:
- Demonstrates senior-level expertise in 1-2 technical areas
- Designs systems that scale and are maintainable
- Mentors junior engineers effectively

Impact:
- Delivers projects with team/org-level impact
- Takes ownership of ambiguous problems
- Delivers consistently high-quality work

Leadership:
- Influences team technical decisions
- Drives projects from design to deployment
- Improves team processes and standards

Communication:
- Writes clear technical docs
- Presents technical topics to diverse audiences
- Gives constructive feedback to peers

Scope:
- Operates at team level (multiple projects)
- Collaborates cross-functionally (PM, Design, QA)
- Thinks beyond immediate tasks (strategic)
```

**Promotion Process:**
```
1. Employee Readiness:
   - Manager and employee discuss promotion readiness
   - Review promotion criteria (typically 70-80% ready before nominating)
   - Begin "promotion packet" preparation (3-6 months)

2. Promotion Packet:
   - Self-summary (1-2 pages, address each criterion)
   - Manager recommendation (1-2 pages, specific examples)
   - Peer endorsements (4-6 peers, cross-functional)
   - Work artifacts (design docs, code reviews, project impact)

3. Promotion Committee Review:
   - Cross-functional committee (engineers, managers, HR)
   - Reviews packets against criteria
   - Votes: Promote, Not Yet, or Need More Information
   - Typical approval rate: 60-70% of submissions

4. Promotion Approval:
   - VP/Director approves (budget, headcount, calibration)
   - Effective date (next quarter or review cycle)
   - Compensation adjustment (title, salary, equity)

5. Communication:
   - Manager delivers news in 1-on-1
   - Public announcement (team, company)
   - Updated career ladder and expectations
```

**Amazon Promotion Process (Unique - Promotion Doc):**
```
Amazon uses narrative-driven promotions:
- Employee writes 2-page "Promotion Document"
- Structured like 6-pager: Context, Problem, Solution, Impact, Leadership Principles
- Manager adds endorsement
- Reviewed by "Promotion Panel" (senior leaders)
- Decision based on storytelling + data

Key Amazon concept: "You're promoted when you're already operating at next level for 6-12 months"
```

### 8. Performance Review Templates

**Template 1: Annual Performance Review**

```markdown
# Annual Performance Review: {Name}
**Period**: {Date Range}
**Role**: {Title}
**Manager**: {Manager Name}
**Review Date**: {Date}

---

## Summary
{1-2 paragraph overall summary of performance this year}

---

## Key Achievements

### Achievement 1: {Title}
**Impact**: {Business impact, metrics, outcomes}
**Details**: {What you did, how you did it, why it mattered}
**Skills Demonstrated**: {Technical, leadership, collaboration skills}

### Achievement 2: {Title}
**Impact**: {Impact}
**Details**: {Details}
**Skills Demonstrated**: {Skills}

### Achievement 3: {Title}
**Impact**: {Impact}
**Details**: {Details}
**Skills Demonstrated**: {Skills}

---

## Core Competencies

### Technical Excellence
**Rating**: Exceeds Expectations ⭐⭐⭐⭐⭐
- {Specific examples of technical skill}
- {Innovations, improvements, mastery}

### Collaboration & Teamwork
**Rating**: Meets Expectations ⭐⭐⭐⭐
- {Cross-functional partnerships}
- {Peer feedback themes}

### Communication
**Rating**: Exceeds Expectations ⭐⭐⭐⭐⭐
- {Written, verbal, presentations}
- {Documentation, knowledge sharing}

### Leadership & Influence
**Rating**: Meets Expectations ⭐⭐⭐⭐
- {Mentoring, tech leadership, driving initiatives}
- {Influence beyond immediate team}

### Ownership & Accountability
**Rating**: Exceeds Expectations ⭐⭐⭐⭐⭐
- {Taking ownership, follow-through}
- {Handling ambiguity and challenges}

---

## 360-Degree Feedback Summary

### Strengths (themes from peer feedback):
1. {Strength 1} - "{Specific quote from peer feedback}"
2. {Strength 2} - "{Quote}"
3. {Strength 3} - "{Quote}"

### Growth Opportunities (themes from peer feedback):
1. {Area 1} - "{Quote}"
2. {Area 2} - "{Quote}"

---

## Growth & Development

### What Went Well
- {Positive behavior/outcome 1}
- {Positive behavior/outcome 2}
- {Positive behavior/outcome 3}

### Areas for Growth
1. **{Area 1}**: {Specific feedback and examples}
   - **Action**: {Concrete steps to improve}
   - **Support**: {Manager/company support}

2. **{Area 2}**: {Feedback}
   - **Action**: {Steps}
   - **Support**: {Support}

---

## Career Development

### Current Level: {Level}
### Readiness for Next Level: {%}
- **On Track For**: {Timeline, e.g., "Promotion in next cycle"}
- **Gaps to Close**: {Specific criteria not yet met}
- **Development Plan**: {Action items to reach next level}

### Career Aspirations
- **Short-term (1 year)**: {Goals}
- **Long-term (3-5 years)**: {Aspirations}

---

## Goals for Next Review Period

### Goal 1: {Title}
**Objective**: {What you want to achieve}
**Key Results**: {Measurable outcomes}
**Timeline**: {When}

### Goal 2: {Title}
**Objective**: {Objective}
**Key Results**: {KRs}
**Timeline**: {Timeline}

### Goal 3: {Title}
**Objective**: {Objective}
**Key Results**: {KRs}
**Timeline**: {Timeline}

---

## Overall Rating: {Rating}

## Manager Comments
{Additional context, perspective, and recommendations from manager}

---

**Employee Acknowledgment**:
I have reviewed this performance review with my manager and understand the feedback provided.

**Employee Signature**: _________________ Date: _______
**Manager Signature**: _________________ Date: _______
```

## Practical Frameworks

### Framework: SBI Feedback Model

**SBI = Situation - Behavior - Impact**

**Structure:**
```
Situation: Where and when did it happen?
Behavior: What specific behavior did you observe?
Impact: What was the impact of that behavior?
```

**Example (Positive Feedback):**
```
Situation: "In yesterday's design review meeting..."
Behavior: "...you asked clarifying questions that helped the team identify 3 edge cases we hadn't considered."
Impact: "This prevented potential bugs and saved us days of rework. The team felt more confident in the design."
```

**Example (Constructive Feedback):**
```
Situation: "In this morning's standup..."
Behavior: "...you mentioned you were blocked but didn't share specific details or ask for help."
Impact: "The team couldn't offer solutions, and you lost a day of productivity. Next time, please share the specific blocker so we can help unblock you quickly."
```

### Framework: Radical Candor Matrix (Kim Scott)

```
        Care Personally
              ↑
              │
              │   Radical Candor
              │   ✓ Care + Challenge
    Ruinous   │   (IDEAL)
    Empathy   │
    (Nice but │──────────────────→ Challenge Directly
    not       │   Obnoxious
    helpful)  │   Aggression
              │   (Challenge without care)
              │
         Manipulative
         Insincerity
         (Neither care nor challenge)
```

**Goal**: Radical Candor - Care personally AND challenge directly

**Examples:**
```
Radical Candor: "I care about your growth, and I need to tell you that your code quality has dropped in the last month. Let's figure out what's going on and how I can support you."

Ruinous Empathy: "You're doing great!" (avoiding hard conversation about poor performance)

Obnoxious Aggression: "Your code is garbage, fix it!" (harsh without empathy)

Manipulative Insincerity: Saying positive things you don't mean, avoiding all feedback
```

## Advanced: Company-Specific Practices

### Amazon - Forte Review Process

**Forte Document (Self-Review):**
```markdown
# Forte: {Your Name} - {Period}

## Introduction
{Who you are, your role, your scope}

## Key Accomplishments

### Accomplishment 1: {Title}
**Customer Impact**: {How this helped customers}
**Business Impact**: {Metrics, revenue, efficiency}
**Leadership Principles**: {Which LPs you demonstrated}
**Details**: {Story of what you did and how}

### Accomplishment 2: {Title}
{Same structure}

## Leadership Principles

For each Leadership Principle:
- Customer Obsession: {Example of how you demonstrated}
- Ownership: {Example}
- Invent & Simplify: {Example}
- Are Right, A Lot: {Example}
- Learn & Be Curious: {Example}
- Hire & Develop the Best: {Example}
- (etc. for all 16 LPs)

## Development Areas
{Where you want to grow}
```

### Netflix - Keeper Test & 360 Review

**Keeper Test (Manager Self-Check):**
```
Question: "If [Name] told me they were leaving for a similar role at another company, would I fight to keep them?"

- If YES → They pass the Keeper Test → Invest in retention
- If NO → Generous severance conversation → Help them find better fit

Philosophy: Keep only the players you'd fight to retain. This creates high-performing teams.
```

**Netflix 360 Review (Start-Stop-Continue):**
```
To: {Name}
From: {Your Name}

START doing:
- {Specific behavior you'd like them to start}
- Example: "Start presenting your work at Engineering All-Hands. Your technical insights would benefit the broader team."

STOP doing:
- {Behavior you'd like them to stop}
- Example: "Stop being the last to respond in Slack. It blocks async collaboration and delays the team."

CONTINUE doing:
- {Behavior that's working well}
- Example: "Continue your detailed code reviews. They're teaching the team best practices."
```

## Metrics & Success Criteria

**Performance Management Health Metrics:**
```
Metric                                    Target        Actual   Trend
──────────────────────────────────────────────────────────────────────
1-on-1 Completion Rate                    > 95%         [  ]    [↑↓→]
Performance Review On-Time Rate           > 98%         [  ]    [↑↓→]
Calibration Attendance                    100%          [  ]    [↑↓→]
PIP Success Rate                          15-20%        [  ]    [↑↓→]
Promotion Approval Rate                   60-70%        [  ]    [↑↓→]
Manager Effectiveness (feedback quality)  > 4.0/5.0     [  ]    [↑↓→]
Employee Agreement with Review            > 80%         [  ]    [↑↓→]
```

## Дополнительные ресурсы

См. `assets/` для:
- Performance review templates (annual, quarterly, 360-degree)
- PIP templates
- OKR templates
- 1-on-1 conversation guides
- Feedback scripts (SBI, Radical Candor)
- Promotion packet templates

См. `references/` для:
- Company-specific processes (Amazon Forte, Google OKRs, Netflix 360)
- Research papers (Project Aristotle, performance management studies)
- Books (Radical Candor, Measure What Matters, Work Rules!)
