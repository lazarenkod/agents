---
name: escalation-workflow
description: Guide through escalation workflow for critical customer or technical issues.
---

# Escalation Workflow Guide

Interactive workflow для управления эскалациями.

## Escalation Types

### 1. Technical Escalation (Tier 1 → Tier 2 → Tier 3 → Vendor)

**When to Escalate**:
- Issue beyond current tier's expertise
- SLA at risk (>50% time consumed)
- Customer requests escalation

**Handoff Checklist**:
```markdown
- [ ] Complete troubleshooting summary
- [ ] Document steps already attempted
- [ ] Customer impact assessment
- [ ] Diagnostic data collected
- [ ] Customer expectation set
- [ ] Next tier engineer assigned
- [ ] Customer notified of escalation
```

### 2. Executive Escalation (Customer → Team Lead → Manager → Director → VP)

**Triggers**:
- Customer dissatisfaction (CSAT <3)
- Enterprise customer requests manager
- Repeated issues (3+ in 30 days)
- Revenue impact >$10K

**Response Template**:
```markdown
Subject: RE: [Customer Issue] - Escalation Acknowledged

Dear [Customer],

Thank you for escalating this to my attention. I want to assure you we're fully committed to resolving this.

**What I've Done**:
- ✅ Reviewed complete case history
- ✅ Assigned senior technical team
- ✅ Established priority tracking

**Next Steps**:
- Dedicated point of contact (me)
- Updates every [X hours]
- Next update: [Specific time]

Best regards,
[Name]
[Title]
[Direct Contact]
```

### 3. Vendor Escalation (AWS/Azure/GCP/Oracle)

**Process**:
1. Create vendor support case (severity appropriate)
2. Engage TAM/DSE/CE if Enterprise support
3. Provide detailed context и business impact
4. Request regular updates
5. Coordinate internally while vendor investigates

**Template**: See vendor-escalation skill for detailed templates

## Workflow Output

Generates escalation tracking document:
```markdown
# Escalation Tracking: [Customer/Incident]

**Type**: [Technical / Executive / Vendor]
**Level**: [Current escalation level]
**Status**: [ACTIVE / RESOLVED / ESCALATED]

## Timeline
[HH:MM] - Initial escalation received
[HH:MM] - Escalation acknowledged
[HH:MM] - [Actions taken]

## Actions & Owners
- [ ] [Action 1] - @owner
- [ ] [Action 2] - @owner

## Communication Log
[All customer/internal communications]

## Resolution Plan
[Next steps and ETA]
```

Сохраняется в: `./escalations/ESC-XXXXX-tracking.md`
