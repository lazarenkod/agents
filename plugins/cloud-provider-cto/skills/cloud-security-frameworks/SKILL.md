---
name: cloud-security-frameworks
description: Фреймворки безопасности для облачных платформ (NIST, ISO 27001, CIS, CSA). Use when implementing security controls, preparing for audits, establishing security baseline, or designing security architecture.
---

# Фреймворки безопасности облачных платформ

## Когда использовать

- Внедрение security controls
- Подготовка к audit/certification
- Разработка security baseline
- Compliance mapping
- Security architecture design

## NIST Cybersecurity Framework

### 5 Functions

**1. IDENTIFY** - Asset Management, Risk Assessment
```yaml
ID.AM-1: Physical devices and systems inventoried
ID.AM-2: Software platforms and applications inventoried
ID.RA-1: Asset vulnerabilities identified
ID.RA-5: Threats, vulnerabilities, impacts understood
```

**Implementation**:
- CMDB (Configuration Management Database)
- Asset tagging (mandatory)
- Vulnerability scanning (weekly)
- Threat modeling

**2. PROTECT** - Access Control, Data Security
```yaml
PR.AC-1: Identities and credentials managed
PR.AC-3: Remote access managed
PR.DS-1: Data-at-rest protected
PR.DS-2: Data-in-transit protected
PR.PT-1: Audit/log records determined
```

**3. DETECT** - Anomalies and Events, Monitoring
**4. RESPOND** - Response Planning, Communications
**5. RECOVER** - Recovery Planning, Improvements

## CIS Benchmarks для Cloud

### AWS CIS Benchmark (избранное)

```markdown
### 1. Identity and Access Management
1.1 Avoid root account use (CRITICAL)
1.5 MFA enabled для console access (CRITICAL)
1.12 Credentials unused for 90 days removed
1.14 Access keys rotated every 90 days

### 2. Storage
2.1.1 S3 buckets not public (CRITICAL)
2.1.5 S3 bucket logging enabled
2.2.1 EBS encryption enabled

### 3. Logging
3.1 CloudTrail enabled in all regions (CRITICAL)
3.4 CloudTrail log file validation enabled
3.6 S3 bucket access logging enabled

### 4. Monitoring
4.1-4.15 CloudWatch alarms для security events:
- Unauthorized API calls
- Console sign-in without MFA
- Root account usage
- IAM policy changes
- CloudTrail configuration changes
- Failed console authentications
- S3 bucket policy changes
```

**Automated Compliance Checking**:
```python
# AWS Config Rules
rules = [
    'root-account-mfa-enabled',
    'iam-password-policy',
    's3-bucket-public-read-prohibited',
    's3-bucket-public-write-prohibited',
    'cloudtrail-enabled',
    'ebs-encrypted-volumes',
    'rds-encryption-enabled',
    'vpc-flow-logs-enabled'
]
```

## CSA Cloud Controls Matrix (CCM)

### 16 Domains

**AIS - Application & Interface Security**
```
AIS-01: Application Security
- Secure SDLC implementation
- Code review и testing
- Vulnerability management
```

**IAM - Identity & Access Management**
```
IAM-01: Audit Tools Access
IAM-02: User Access Policies
IAM-08: Encryption & Key Management
```

**DSI - Data Security & Information Lifecycle**
```
DSI-02: Data Inventory / Flows
DSI-05: Data Loss Prevention
DSI-07: Secure Disposal
```

## Compliance Automation

```python
# Compliance-as-Code (OPA Policy)
package cloud.compliance.s3

deny[msg] {
    bucket := input.resource_changes[_]
    bucket.type == "aws_s3_bucket"

    not bucket.change.after.server_side_encryption_configuration

    msg := sprintf("S3 bucket %v must have encryption enabled", [bucket.address])
}

deny[msg] {
    bucket := input.resource_changes[_]
    bucket.type == "aws_s3_bucket"

    bucket.change.after.acl == "public-read"

    msg := sprintf("S3 bucket %v cannot be public", [bucket.address])
}
```

---

**Все security frameworks документируются в Markdown на русском языке.**
