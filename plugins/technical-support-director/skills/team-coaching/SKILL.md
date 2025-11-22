---
name: team-coaching
description: Coaching и development методологии для support teams. Включает performance coaching, skill development, career pathing, 1-on-1 frameworks. Use when coaching team members, developing skills, or managing performance.
---

# Коучинг Команды

## 1-on-1 Framework

### Регулярность
- IC (Individual Contributors): Bi-weekly 30min
- Team Leads: Weekly 30min
- Direct Reports: Weekly 45min

### Agenda Template

```markdown
# 1-on-1: [Name] - [Date]

## Personal/Wellbeing (5 min)
- How are you doing?
- Any personal updates?
- Work-life balance check

## Wins & Challenges (10 min)
- What went well this week?
- What was challenging?
- Any blockers?

## Development (10 min)
- Progress on goals
- Skill development opportunities
- Training needs

## Feedback (5 min)
- Manager → IC feedback
- IC → Manager feedback
- Process improvements

## Action Items
- [ ] [Item 1]
- [ ] [Item 2]

## Next Meeting Topics
- [Topic to cover next time]
```

## Performance Coaching

### Coaching Model: GROW

```markdown
# GROW Framework

**Goal**: What do you want to achieve?
**Reality**: Where are you now?
**Options**: What could you do?
**Will**: What will you do?

## Example: Low CSAT Engineer

**Goal**: Improve CSAT from 82% to 90%+
**Reality**:
- Current: 82% (below team avg 92%)
- Customer feedback: "Technically correct but rushed"
- Pattern: Short responses, minimal explanation

**Options**:
1. Slow down, spend more time on communication
2. Use templates for thorough responses
3. Shadow high-CSAT teammates
4. Communication skills training

**Will**:
- This week: Shadow Alice (95% CSAT) for 2 days
- Implement "3-sentence minimum" rule for responses
- Manager reviews 5 tickets/week for feedback
- Check-in in 2 weeks
```

## Skill Matrix & Development

```python
SKILL_LEVELS = {
    "1_novice": "Learning basics, needs guidance",
    "2_competent": "Handles routine independently",
    "3_proficient": "Handles complex, mentors others",
    "4_expert": "Subject matter expert, creates training"
}

SKILL_CATEGORIES = {
    "technical": [
        "Compute (VMs, containers)",
        "Networking (LB, VPN, CDN)",
        "Databases (SQL, NoSQL)",
        "Security (IAM, encryption)",
        "Monitoring (logs, metrics)"
    ],
    "soft_skills": [
        "Communication (written/verbal)",
        "Customer empathy",
        "Problem-solving",
        "Time management",
        "Collaboration"
    ],
    "tools": [
        "Ticketing system",
        "Cloud consoles (AWS/Azure/GCP)",
        "Monitoring tools",
        "Documentation"
    ]
}
```

### Development Plan Template

```markdown
# 90-Day Development Plan: [Name]

## Current Level: Tier 1 Support
## Target Level: Tier 2 Support

### Skills to Develop
1. **Networking** (Current: Competent → Target: Proficient)
   - Complete network troubleshooting course
   - Shadow Tier 2 on 5 network issues
   - Handle 10 network tickets independently

2. **Database** (Current: Novice → Target: Competent)
   - Complete SQL fundamentals course
   - Pair with DB specialist on 3 complex cases
   - Create KB article on common DB issues

3. **Communication** (Current: Proficient → Target: Proficient)
   - Maintain current high CSAT
   - Mentor 1 new hire

### Timeline
- **Month 1**: Focus on Networking
- **Month 2**: Focus on Database
- **Month 3**: Integration & Assessment

### Success Criteria
- [ ] All training completed
- [ ] 15 Tier 2-level tickets resolved independently
- [ ] CSAT maintained ≥90%
- [ ] Peer feedback positive
- [ ] Manager assessment: Ready for promotion
```

## Quality Assurance Coaching

### Ticket Review Process

```markdown
# Ticket Quality Review

## Weekly Sample
- Random selection: 3 tickets per engineer
- Focused review: All P1/P2 tickets
- Customer complaint triggers: Immediate review

## Review Criteria (1-5 scale)
1. **Technical Accuracy** (30%)
2. **Communication Quality** (25%)
3. **Process Adherence** (20%)
4. **Customer Experience** (25%)

## Coaching Approach

**Score 4-5**: Positive reinforcement
- "Excellent work on [specific aspect]"
- "Can you share this approach in team meeting?"

**Score 3**: Constructive feedback
- "Good job. One improvement: [specific]"
- "Next time, consider [alternative approach]"

**Score 1-2**: Development plan
- Private 1-on-1 discussion
- Root cause: Knowledge gap? Process unclear? Burnout?
- Create action plan with support
```

## Career Pathing

```markdown
# Support Career Ladder

## Individual Contributor Track
1. **Support Engineer I** (Entry-level)
   - Handles P3/P4
   - Learning platform
   - 0-1 years experience

2. **Support Engineer II**
   - Handles all priorities
   - Mentors new hires
   - 1-3 years experience

3. **Senior Support Engineer**
   - Complex troubleshooting
   - Leads projects
   - 3-5 years experience

4. **Staff Support Engineer**
   - Subject matter expert
   - Strategic initiatives
   - 5+ years experience

## Management Track
1. **Team Lead** (Player-coach)
2. **Support Manager** (People manager)
3. **Senior Manager / Director**
4. **VP of Support**

## Specialist Track
1. **Technical Account Manager**
2. **Solutions Architect**
3. **DevOps / SRE (transition)**
```

## References
- `coaching-templates/` - 1-on-1 и review templates
- `training-plans/` - Role-specific development plans
