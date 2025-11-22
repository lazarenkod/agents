---
name: vendor-escalation
description: Procedures и best practices для escalation к облачным вендорам (AWS, Azure, Google Cloud, Oracle). Включает support тарифы, эскалацию, TAM engagement, SLA management. Use when escalating to cloud providers, coordinating vendor support, or optimizing vendor relationships.
---

# Эскалация к Вендорам (Vendor Escalation)

## Когда Использовать

- Проблемы на уровне cloud provider platform
- Требуется vendor engineering expertise
- Подтвержденный platform bug
- Service limit increases urgent
- Performance issues на vendor стороне

## AWS Support

### Support Plans

| Plan | P1 Response | P2 Response | Cost |
|------|------------|-------------|------|
| Basic | N/A | N/A | Free |
| Developer | N/A | 12 hours | $29/mo или 3% |
| Business | <1 hour | <4 hours | $100/mo или 10% |
| Enterprise | <15 min | <1 hour | $15K/mo или 10% |

### Escalation Process

**1. Create Support Case**
```bash
# Via AWS CLI
aws support create-case \
    --subject "Production RDS instance unresponsive" \
    --service-code "amazon-rds" \
    --severity-code "urgent" \
    --category-code "performance" \
    --communication-body "RDS instance db-prod-01 not responding to connections since 14:30 UTC.
    All application servers unable to connect. Critical production impact - 10K users affected."
```

**2. Severity Selection**
- **Critical**: Production system down, data loss
- **Urgent**: Production system impaired, business impact
- **High**: Important functions impaired
- **Normal**: General questions, feature requests
- **Low**: General info

**3. TAM Engagement (Enterprise)**
```markdown
## When to Contact TAM

**Immediately**:
- P1 incidents requiring urgent attention
- Need architecture guidance during incident
- Coordination of multiple AWS services

**Within 24 hours**:
- P2 incidents for priority handling
- Service limit increases (urgent)
- Account reviews needed

**Regular cadence**:
- Weekly/bi-weekly check-ins
- Quarterly business reviews
- Architecture planning sessions
```

**4. Escalation Template**
```markdown
Subject: ESCALATION REQUEST - Production Outage

AWS Support Case: 1234567890
Severity: Critical (P1)
Service: Amazon RDS
Region: us-east-1

Business Impact:
- Production environment completely down
- 10,000 active users unable to access application
- Estimated revenue loss: $50,000/hour
- SLA with our customers being breached

Technical Summary:
- RDS instance: db-prod-01
- Issue: All connection attempts timing out
- Started: 2024-01-20 14:30 UTC
- Duration: 2 hours 15 minutes
- Instance metrics show CPU 0%, no queries processing

Actions Taken:
1. [14:35] Verified network security groups - correct
2. [14:40] Attempted reboot via console - no effect
3. [14:50] Created Support Case #1234567890
4. [15:00] Reviewed CloudWatch logs - no errors

Requesting:
- Immediate AWS engineering engagement
- Investigation of RDS instance health
- ETA for resolution
- Regular updates every 30 minutes

Our TAM: Jane Smith (jsmith@aws.amazon.com)
Emergency Contact: John Doe +1-555-0100
```

### AWS Premium Support Features

**Infrastructure Event Management (IEM)**:
- AWS engineer присутствует during major events
- Pre-event planning и architecture review
- Real-time support during event
- Post-event analysis

**Well-Architected Review**:
- Quarterly architecture reviews
- Best practices assessment
- Security и cost optimization
- Performance improvement recommendations

## Azure Support

### Support Plans

| Plan | Sev A Response | Cost |
|------|---------------|------|
| Basic | N/A | Free |
| Developer | <8 bus hrs | $29/mo |
| Standard | <1 hour | $100/mo или 10% |
| Professional Direct | <1 hour | $1K/mo |
| Premier | <15 min | Custom |

### Escalation Process

**1. Create Support Request**
```powershell
# Via Azure CLI
az support tickets create \
    --ticket-name "prod-sql-db-down" \
    --title "Production SQL Database Unavailable" \
    --description "Azure SQL Database prod-db-01 not responding. Connection timeout errors. 5000 users impacted." \
    --severity "critical" \
    --problem-classification "/providers/Microsoft.Support/services/sql_database_service_guid/problemClassifications/connectivity_problemClassification_guid" \
    --contact-first-name "John" \
    --contact-last-name "Smith" \
    --contact-email "john.smith@company.com" \
    --contact-phone "+1-555-0100" \
    --contact-timezone "Pacific Standard Time" \
    --contact-country "USA"
```

**2. Engage Microsoft DSE (Premier/Unified)**
- Designated Support Engineer - ваш primary contact
- Direct phone/email for escalations
- Can coordinate cross-team resources

**3. Service Health Incidents**
```markdown
## If Azure Service Health shows incident:

1. Navigate to Azure Service Health
2. Check if your subscription affected
3. Create support ticket linked to incident
4. Reference Service Health incident number
5. Request proactive updates
6. Ask for customer-specific impact assessment
```

**4. FastTrack Program**
- Available для eligible migrations и deployments
- Direct access to Microsoft engineers
- Guidance on best practices
- Expedited support during migration

## Google Cloud Support

### Support Plans

| Plan | P1 Response | Cost |
|------|------------|------|
| Basic | N/A | Free |
| Development | <4 hours | 3% of spend |
| Production | <1 hour | 9% of spend |
| Enterprise | <15 min | Custom |
| Premium | <15 min | Custom + TAM |

### Escalation Process

**1. Create Support Case**
```bash
# Via gcloud CLI
gcloud support cases create \
    --title="Production GKE cluster nodes failing" \
    --description="GKE cluster prod-cluster-01 nodes failing to schedule pods. Critical production impact." \
    --severity=P1 \
    --component="Google Kubernetes Engine"
```

**2. Customer Engineer (CE) Engagement**
- Enterprise/Premium plans have assigned CE
- Direct Slack Connect channel
- Phone/email for emergencies

**3. Escalation to TAM (Premium)**
```markdown
## TAM Escalation Process

**When to Escalate**:
- P1 not receiving adequate attention
- Multi-service coordination needed
- Executive visibility required
- Strategic guidance during incident

**How to Escalate**:
1. Direct call/text to TAM (emergency number)
2. Email with "URGENT" subject
3. Post in dedicated Slack Connect channel
4. Reference support case number
5. Provide business impact summary
```

### GCP Support Best Practices

**Optimize Support Case Quality:**
```markdown
# High-Quality Support Case Template

**Title**: [Clear, specific problem statement]

**Severity**: P1 (Critical) - Production environment down

**Environment**:
- Project ID: my-production-project
- Region: us-central1
- Service: Google Kubernetes Engine
- Cluster: prod-cluster-01

**Problem Description**:
[Clear description of what's happening]

**Business Impact**:
- Users affected: 15,000
- Services down: [List]
- Revenue impact: $100K/hour

**When Started**: 2024-01-20 14:30 UTC

**Troubleshooting Already Done**:
1. [Action 1] - [Result]
2. [Action 2] - [Result]
3. [Action 3] - [Result]

**Logs/Screenshots**: [Attached]

**Expected Response**:
- Immediate engineering engagement
- Root cause identification
- ETA for resolution
```

## Oracle Cloud Support

### Support Plans

| Plan | P1 Response | Cost |
|------|------------|------|
| Basic | 24 hours | Included |
| Advanced | <1 hour | 10% of cloud spend |
| Premier | <15 min | Custom |

### My Oracle Support (MOS)

**Service Request (SR) Creation**:
1. Login to My Oracle Support portal
2. Create Service Request
3. Select Severity 1 for production down
4. Provide detailed problem description
5. Upload relevant logs/screenshots

**Escalation Path**:
```markdown
1. Initial Response: Standard support engineer
2. Level 1 Escalation: Senior engineer (if not progressing)
3. Level 2 Escalation: Support manager
4. Level 3 Escalation: Development team (if bug suspected)
```

## Multi-Vendor Coordination

### Scenario: Issue spans multiple platforms

```markdown
# Example: Database on AWS, App on GCP

## Coordination Strategy

**1. Parallel Support Cases**
- AWS Case: Database performance degradation
- GCP Case: Application errors connecting to external DB

**2. Cross-Reference**
- Mention other vendor case in each ticket
- Share relevant info between vendors
- Request coordination if needed

**3. Internal Coordination Lead**
- Designate one person as coordinator
- Aggregate updates from both vendors
- Maintain single source of truth timeline
- Coordinate joint troubleshooting if needed

**4. Resolution Approach**
- Determine which side owns root cause
- Coordinate fix implementation
- Joint verification of resolution
```

## Vendor SLA Management

### Tracking Vendor Response Times

```python
VENDOR_SLA_TRACKING = {
    "case_id": "AWS-12345",
    "vendor": "AWS",
    "severity": "P1",
    "sla_target": "15 minutes",
    "created_at": "2024-01-20T14:30:00Z",
    "first_response_at": "2024-01-20T14:42:00Z",
    "response_time_minutes": 12,
    "sla_met": True,
    "escalations": [
        {
            "level": "TAM",
            "time": "2024-01-20T15:00:00Z",
            "reason": "No progress in 30 minutes"
        }
    ]
}
```

### Escalation если SLA Breach

```markdown
## If Vendor Misses SLA

**Immediate Action**:
1. Update case: "SLA breach - [X minutes] since case creation, no response"
2. Call vendor emergency line
3. Engage TAM/DSE/CE if available
4. Escalate to account team

**Follow-Up**:
1. Request service credit (if contractual)
2. Document SLA breach in vendor relationship review
3. Quarterly review of vendor performance
4. Escalate patterns to vendor management
```

## References
- `vendor-contacts/` - Emergency escalation contacts
- `templates/` - Case creation templates by vendor
- `sla-tracking/` - Vendor SLA monitoring dashboards
