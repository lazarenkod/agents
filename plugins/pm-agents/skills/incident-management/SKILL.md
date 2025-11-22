---
name: incident-management
description: Incident management framework for production issues including response coordination, post-mortems, and process improvement. Use when coordinating incident response, conducting post-mortems, or improving incident management processes.
---

# Incident Management

Comprehensive incident management для production issues с focus на быстрое восстановление и learning.

## When to Use This Skill

- Coordinating production incident response
- Running post-mortem reviews
- Improving incident management processes
- Establishing on-call practices
- SLO/SLA management
- Crisis communication

## Incident Response Process

### Severity Levels

**P0 - Critical:**
- Complete service outage
- Data loss risk
- Security breach
- Revenue-impacting
- Response: Immediate, all hands
- Communication: Real-time executive updates

**P1 - High:**
- Major feature broken
- Significant user impact
- Performance degradation
- Response: Within 15min
- Communication: Hourly updates

**P2 - Medium:**
- Minor feature broken
- Limited user impact
- Response: Within 1 hour
- Communication: Daily updates

**P3 - Low:**
- Cosmetic issues
- No user impact
- Response: Best effort
- Communication: Weekly

### Incident Lifecycle

```
Detection → Response → Mitigation → Resolution → Post-Mortem

1. Detection (Alerting)
   - Automated monitoring
   - User reports
   - Internal discovery

2. Response (Mobilization)
   - Page on-call engineer
   - Assess severity
   - Form war room if needed

3. Mitigation (Damage Control)
   - Stop the bleeding
   - Rollback/hotfix
   - Communication starts

4. Resolution (Fix)
   - Root cause identified
   - Permanent fix deployed
   - Monitoring confirms recovery

5. Post-Mortem (Learning)
   - Blameless analysis
   - Action items
   - Process improvements
```

## Incident Response Template

```markdown
# Incident Report: [Title]

**Incident ID**: INC-[YYYYMMDD-NNN]
**Severity**: P[0-3]
**Status**: Investigating / Mitigating / Resolved / Closed
**Incident Commander**: [Name]
**Started**: [Timestamp]
**Resolved**: [Timestamp]
**Duration**: [Duration]

---

## Impact

**User Impact**: [Description]
**Affected Users**: [Number or %]
**Revenue Impact**: $[Amount] (if applicable)
**SLA Breach**: Yes/No

---

## Timeline

| Time | Event |
|------|-------|
| 10:15 | Alert fired: High error rate |
| 10:17 | On-call paged |
| 10:20 | War room established |
| 10:25 | Rollback initiated |
| 10:30 | Service restored |
| 10:45 | Incident resolved |

---

## Root Cause

[Detailed analysis of what caused incident]

**Contributing Factors**:
- [Factor 1]
- [Factor 2]

---

## Mitigation

**Immediate Actions Taken**:
- [Action 1]: Rolled back deployment
- [Action 2]: Increased capacity

**Effectiveness**: [How well mitigation worked]

---

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Preventive action 1] | [Name] | [Date] | 🟢 Done |
| [Monitoring improvement] | [Name] | [Date] | 🔵 In Progress |
| [Process update] | [Name] | [Date] | ⚪ Planned |

---

## Lessons Learned

**What Went Well**:
- [Positive 1]: Fast detection
- [Positive 2]: Effective communication

**What Went Wrong**:
- [Issue 1]: Inadequate testing
- [Issue 2]: Missing monitoring

**How to Improve**:
- [Improvement 1]
- [Improvement 2]
```

## Post-Mortem Framework

### Blameless Post-Mortem

**Principles:**
✅ Focus on systems, не people
✅ Assume good intentions
✅ Learn from failure
✅ Share widely
✅ Action-oriented

**Questions to Answer:**
1. What happened?
2. Why did it happen?
3. How did we respond?
4. What worked well?
5. What didn't work?
6. How do we prevent recurrence?
7. What did we learn?

### Post-Mortem Meeting

**Attendees:**
- Incident Commander
- On-call engineers
- Affected team leads
- Key stakeholders

**Agenda (60min):**
- 5min: Context setting
- 20min: Timeline review
- 20min: Root cause analysis
- 10min: Action items
- 5min: Lessons learned

## Incident Communication

### Communication Matrix

| Audience | P0 | P1 | P2 |
|----------|----|----|-----|
| **Users** | Status page immediately | Within 30min | As needed |
| **Executives** | Real-time | Hourly | Daily |
| **Engineering** | War room + Slack | Slack updates | Ticket updates |
| **Support** | Immediate brief | Within 15min | Email update |

### Status Page Update Template

```markdown
# [Service] Experiencing Issues

**Status**: Investigating / Identified / Monitoring / Resolved
**Last Updated**: [Timestamp]

## Current Status

[Brief description of issue and impact]

## Timeline

**[Time]**: Investigating reports of [issue]
**[Time]**: Issue identified. Working on fix.
**[Time]**: Fix deployed. Monitoring.
**[Time]**: Confirmed resolved.

## What We're Doing

[Actions being taken]

## Next Update

In [X] minutes
```

## Best Practices

✅ **Practice Drills**: Quarterly game days
✅ **Clear Runbooks**: Document common scenarios
✅ **Automated Alerting**: Don't rely on users
✅ **Blameless Culture**: Focus on learning
✅ **Action Items**: Always follow through
✅ **Share Learnings**: Public post-mortems

## Success Metrics

- **MTTR**: <1 hour (P0), <4 hours (P1)
- **Detection Time**: <5 minutes
- **Post-Mortem Completion**: Within 72 hours
- **Action Item Completion**: >90%
- **Repeat Incidents**: <5%
