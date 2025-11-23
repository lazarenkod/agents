---
name: compliance-automation
description: Автоматизация compliance процессов для облачных платформ. Use when automating compliance checks, implementing policy-as-code, preparing for audits, or establishing continuous compliance.
---

# Автоматизация Compliance

## Когда использовать

- Автоматизация compliance проверок
- Policy-as-Code implementation
- Continuous compliance monitoring
- Audit preparation
- Evidence collection automation

## Policy-as-Code Frameworks

### Open Policy Agent (OPA)

```rego
package terraform.aws.s3

# Правило: Все S3 buckets должны иметь encryption
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"

    not has_encryption(resource)

    msg := sprintf(
        "S3 bucket '%v' должен иметь server-side encryption",
        [resource.name]
    )
}

has_encryption(resource) {
    resource.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default
}

# Правило: Запрет public buckets
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"

    resource.change.after.acl == "public-read"

    msg := sprintf("S3 bucket '%v' не может быть public", [resource.name])
}

# Правило: Versioning enabled
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"

    not resource.change.after.versioning[_].enabled

    msg := sprintf("S3 bucket '%v' должен иметь versioning", [resource.name])
}
```

**Integration с Terraform**:
```bash
# Pre-deploy check
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa exec --decision terraform/aws/s3/deny --bundle policy/ tfplan.json

# Если violations:
exit 1  # Block deployment
```

### Sentinel (HashiCorp)

```hcl
import "tfplan/v2" as tfplan

# Require encryption для все EBS volumes
require_ebs_encryption = rule {
    all tfplan.resource_changes as _, rc {
        rc.type is "aws_ebs_volume" implies
            rc.change.after.encrypted is true
    }
}

# Enforce tagging
required_tags = ["Environment", "Owner", "CostCenter"]

require_tags = rule {
    all tfplan.resource_changes as _, rc {
        rc.type in ["aws_instance", "aws_ebs_volume"] implies
            all required_tags as tag {
                rc.change.after.tags contains tag
            }
    }
}

main = rule {
    require_ebs_encryption and require_tags
}
```

## Continuous Compliance Monitoring

### AWS Config Rules

```python
# Custom Config Rule: Check для secure HTTPS listeners
def evaluate_compliance(config_item):
    """Check ALB has only HTTPS listeners"""

    if config_item['resourceType'] != 'AWS::ElasticLoadBalancingV2::LoadBalancer':
        return 'NOT_APPLICABLE'

    alb_arn = config_item['configuration']['loadBalancerArn']

    # Get listeners
    listeners = elbv2.describe_listeners(LoadBalancerArn=alb_arn)

    # Check all use HTTPS
    for listener in listeners['Listeners']:
        if listener['Protocol'] != 'HTTPS':
            return {
                'ComplianceType': 'NON_COMPLIANT',
                'Annotation': f"Listener {listener['ListenerArn']} uses {listener['Protocol']}"
            }

    return 'COMPLIANT'
```

### Cloud Custodian

```yaml
policies:
  - name: s3-encryption-required
    resource: s3
    filters:
      - type: bucket-encryption
        state: false
    actions:
      - type: notify
        to: [security@company.com]
        subject: "S3 Bucket without encryption"
      - type: auto-tag-user
        tag: non-compliant

  - name: unused-ebs-volumes
    resource: ebs
    filters:
      - State: available
      - type: value
        key: CreateTime
        value_type: age
        value: 30
        op: greater-than
    actions:
      - snapshot
      - delete

  - name: public-rds-prohibited
    resource: rds
    filters:
      - PubliclyAccessible: true
    actions:
      - type: modify-db-instance
        PubliclyAccessible: false
      - type: notify
```

## Audit Evidence Collection

### Automated Evidence Gathering

```python
class EvidenceCollector:
    """Collect compliance evidence"""

    def collect_monthly_evidence(self, month, year):
        evidence = {
            'period': f"{year}-{month:02d}",
            'collected_at': datetime.now(),
            'artifacts': []
        }

        # 1. CloudTrail logs
        evidence['artifacts'].append({
            'type': 'cloudtrail_logs',
            'description': 'All API calls для audit period',
            's3_location': self.export_cloudtrail_logs(month, year),
            'hash': self.calculate_hash()
        })

        # 2. Config snapshots
        evidence['artifacts'].append({
            'type': 'config_snapshots',
            'description': 'Resource configuration snapshots',
            'data': self.get_config_snapshots(month, year)
        })

        # 3. Compliance scan results
        evidence['artifacts'].append({
            'type': 'compliance_scans',
            'description': 'CIS benchmark scan results',
            'results': self.run_compliance_scans()
        })

        # 4. Access reviews
        evidence['artifacts'].append({
            'type': 'access_reviews',
            'description': 'User access review logs',
            'reviews': self.get_access_reviews(month, year)
        })

        # 5. Incident reports
        evidence['artifacts'].append({
            'type': 'security_incidents',
            'description': 'Security incident reports',
            'incidents': self.get_incident_reports(month, year)
        })

        # Store в tamper-proof storage
        self.store_evidence(evidence)

        return evidence
```

---

**Все compliance материалы сохраняются в Markdown на русском языке.**
