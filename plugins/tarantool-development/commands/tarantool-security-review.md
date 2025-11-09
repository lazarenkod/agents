---
name: tarantool-security-review
description: Comprehensive security audit for Tarantool covering authentication, authorization, encryption, and compliance
---

# Tarantool Security Review & Hardening

Comprehensive security audit covering authentication, authorization, encryption, network security, and compliance for Tarantool deployments:

[Extended thinking: This command performs thorough security assessment of Tarantool installations including authentication mechanisms, role-based access control, data encryption at rest and in transit, network security, audit logging, vulnerability scanning, and compliance verification. It provides actionable security hardening recommendations with implementation guidance.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Review Scope
- **basic**: Essential security checks (1-2 hours)
- **standard**: Comprehensive security audit (4-6 hours)
- **comprehensive**: Deep security assessment with penetration testing (2-3 days)
- **compliance**: Compliance-focused review (custom scope)

### Security Domain
- **authentication**: Authentication mechanisms and password policies
- **authorization**: Role-based access control (RBAC)
- **encryption**: Data encryption at rest and in transit
- **network**: Network security and firewall rules
- **audit**: Audit logging and monitoring
- **compliance**: Regulatory compliance (GDPR, PCI-DSS, etc.)
- **all**: All security domains

### Compliance Framework
- **gdpr**: GDPR compliance requirements
- **pci-dss**: PCI-DSS compliance for payment data
- **hipaa**: HIPAA compliance for healthcare data
- **sox**: SOX compliance for financial data
- **custom**: Custom compliance requirements

## Phase 1: Security Discovery & Assessment

1. **Security Posture Assessment**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Assess security posture for: $ARGUMENTS. Review current security controls. Identify security gaps and vulnerabilities. Assess authentication and authorization mechanisms. Review encryption implementation. Identify security risks and threats. Create security baseline."
   - Expected output: Security posture assessment report

2. **Access Control Review**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Review access controls for: $ARGUMENTS. Audit user accounts and roles. Review privilege assignments. Check for excessive permissions. Identify inactive accounts. Review service accounts. Analyze access patterns. Check for privilege escalation risks."
   - Expected output: Access control audit report with findings

3. **Authentication Analysis**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Analyze authentication mechanisms for: $ARGUMENTS. Review Tarantool authentication configuration. Check password policies and strength. Analyze authentication methods (chap-sha1). Review session management. Check for default credentials. Assess multi-factor authentication needs."
   - Expected output: Authentication security analysis with recommendations

4. **Network Security Review**
   - Use Task tool with subagent_type="cloud-infrastructure::network-engineer"
   - Prompt: "Review network security for: $ARGUMENTS. Analyze network topology and segmentation. Review firewall rules and restrictions. Check for exposed ports and services. Analyze TLS/SSL configuration. Review replication channel security. Assess network access controls."
   - Expected output: Network security assessment with hardening recommendations

## Phase 2: Authorization & Access Control

5. **Role-Based Access Control Audit**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Audit RBAC implementation for: $ARGUMENTS. Review user and role definitions. Analyze privilege assignments. Check for role separation. Identify over-privileged accounts. Review function and space permissions. Validate least privilege principle. Document role hierarchy."
   - Expected output: RBAC audit report with privilege analysis

6. **Permission Matrix Analysis**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Analyze permission matrix for: $ARGUMENTS. Map users to roles to permissions. Identify permission overlaps and conflicts. Check for unauthorized access paths. Review grant/revoke history. Analyze space and function access. Create permission visualization."
   - Expected output: Permission matrix with access analysis

7. **Privilege Escalation Testing**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Test for privilege escalation for: $ARGUMENTS. Review scope: $REVIEW_SCOPE. Test vertical privilege escalation. Test horizontal privilege escalation. Check for function injection vulnerabilities. Test stored procedure security. Analyze Lua code security. Identify escalation vectors."
   - Expected output: Privilege escalation test results with vulnerabilities

8. **Service Account Security**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Review service account security for: $ARGUMENTS. Audit application service accounts. Review service account permissions. Check for shared credentials. Analyze service account usage patterns. Review credential rotation policies. Identify service account risks."
   - Expected output: Service account security report

## Phase 3: Encryption & Data Protection

9. **Encryption at Rest Analysis**
   - Use Task tool with subagent_type="security-scanning::security-auditor"
   - Prompt: "Analyze encryption at rest for: $ARGUMENTS. Review snapshot and WAL encryption. Check encryption algorithms and key strength. Analyze key management practices. Review encrypted storage configuration. Identify unencrypted sensitive data. Assess encryption performance impact."
   - Expected output: Encryption at rest analysis with implementation recommendations

10. **Encryption in Transit Review**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Review encryption in transit for: $ARGUMENTS. Analyze TLS/SSL configuration for client connections. Review replication channel encryption. Check certificate management and validation. Analyze cipher suites and protocols. Test for SSL/TLS vulnerabilities. Review encryption between cluster nodes."
    - Expected output: Transport encryption analysis with configuration recommendations

11. **Key Management Assessment**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Assess key management for: $ARGUMENTS. Review encryption key storage and protection. Analyze key rotation policies. Check key access controls. Review key backup and recovery. Assess key management service integration. Identify key management risks."
    - Expected output: Key management assessment with best practices

12. **Data Masking & Redaction**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Review data masking for: $ARGUMENTS. Identify sensitive data (PII, PCI, PHI). Assess masking requirements. Review current masking implementation. Design data redaction strategies. Plan for column-level encryption. Create data classification schema."
    - Expected output: Data masking strategy with implementation plan

## Phase 4: Vulnerability Assessment

13. **Vulnerability Scanning**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Perform vulnerability scan for: $ARGUMENTS. Scan for known Tarantool vulnerabilities. Check Tarantool version for security patches. Scan Lua modules for vulnerabilities. Review dependency vulnerabilities. Check for CVEs and security advisories. Identify zero-day exposure."
    - Expected output: Vulnerability scan report with remediation priorities

14. **Configuration Security Review**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Review security configuration for: $ARGUMENTS. Audit tarantool.cfg() security settings. Review admin socket security. Check memtx and vinyl configuration. Review WAL and snapshot settings. Analyze network binding configuration. Identify insecure configurations."
    - Expected output: Configuration security audit with hardening recommendations

15. **Code Security Analysis**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Analyze code security for: $ARGUMENTS. Review Lua code for security issues. Check for SQL injection vulnerabilities. Analyze input validation and sanitization. Review error handling and information disclosure. Check for race conditions. Identify insecure coding patterns."
    - Expected output: Code security analysis with vulnerability details

16. **Penetration Testing**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Perform penetration testing for: $ARGUMENTS. Scope: $REVIEW_SCOPE. Test authentication bypass. Test authorization bypass. Test injection vulnerabilities. Test network-based attacks. Test denial of service resilience. Document exploitation paths and proof of concepts."
    - Expected output: Penetration test report with findings and remediation

## Phase 5: Audit & Compliance

17. **Audit Logging Review**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Review audit logging for: $ARGUMENTS. Assess audit log coverage and completeness. Review logged security events. Check log retention policies. Analyze log protection and integrity. Review log monitoring and alerting. Assess log analysis capabilities."
    - Expected output: Audit logging assessment with recommendations

18. **Compliance Gap Analysis**
    - Use Task tool with subagent_type="security-compliance::security-auditor"
    - Prompt: "Perform compliance gap analysis for: $ARGUMENTS. Framework: $COMPLIANCE_FRAMEWORK. Map requirements to controls. Identify compliance gaps. Assess control effectiveness. Review documentation and evidence. Create compliance roadmap. Document remediation priorities."
    - Expected output: Compliance gap analysis with remediation plan

19. **Data Privacy Assessment**
    - Use Task tool with subagent_type="security-compliance::security-auditor"
    - Prompt: "Assess data privacy for: $ARGUMENTS. Identify personal data and PII. Review data retention policies. Assess data deletion capabilities. Review consent management. Check for data minimization. Assess privacy by design. Review data subject rights implementation."
    - Expected output: Data privacy assessment with GDPR compliance

20. **Security Monitoring Review**
    - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
    - Prompt: "Review security monitoring for: $ARGUMENTS. Assess security event monitoring. Review intrusion detection capabilities. Check anomaly detection. Review security alerting rules. Assess incident response procedures. Review SIEM integration."
    - Expected output: Security monitoring assessment with improvements

## Phase 6: Hardening & Remediation

21. **Security Hardening Plan**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Create security hardening plan for: $ARGUMENTS. Prioritize security findings by risk. Design hardening implementation roadmap. Plan authentication and authorization improvements. Design encryption implementation. Plan network security hardening. Create implementation timeline."
    - Expected output: Security hardening roadmap with priorities

22. **Authentication Hardening**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Implement authentication hardening for: $ARGUMENTS. Strengthen password policies. Implement strong authentication mechanisms. Configure session timeouts. Implement account lockout policies. Setup password rotation. Configure secure defaults."
    - Expected output: Authentication hardening configuration

23. **Authorization Hardening**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Implement authorization hardening for: $ARGUMENTS. Implement least privilege principle. Refine role definitions. Remove excessive permissions. Implement function-level security. Configure space-level permissions. Setup regular access reviews."
    - Expected output: Authorization hardening implementation

24. **Network Security Hardening**
    - Use Task tool with subagent_type="cloud-infrastructure::network-engineer"
    - Prompt: "Implement network hardening for: $ARGUMENTS. Configure firewall rules. Implement network segmentation. Enable TLS for all connections. Configure secure replication. Disable unnecessary services. Setup intrusion prevention."
    - Expected output: Network security hardening configuration

## Phase 7: Documentation & Training

25. **Security Documentation**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Create security documentation for: $ARGUMENTS. Document security architecture. Create security policies and procedures. Document authentication and authorization. Create incident response playbook. Document security monitoring. Create security best practices guide."
    - Expected output: Comprehensive security documentation

26. **Security Runbooks**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Create security runbooks for: $ARGUMENTS. Create incident response procedures. Document security event handling. Create vulnerability remediation procedures. Document access review procedures. Create disaster recovery procedures. Document security change management."
    - Expected output: Security operations runbooks

27. **Team Security Training**
    - Use Task tool with subagent_type="security-scanning::security-auditor"
    - Prompt: "Design security training for: $ARGUMENTS. Create security awareness training. Document secure coding practices. Create access control training. Document security procedures. Create security testing guide. Plan ongoing security education."
    - Expected output: Security training materials and schedule

## Execution Parameters

### Required
- **--target**: Target Tarantool instance or cluster for security review
- **--review-scope**: Scope of review (basic|standard|comprehensive|compliance)

### Optional
- **--security-domain**: Specific domains (authentication|authorization|encryption|network|audit|compliance|all) - default: all
- **--compliance-framework**: Compliance requirements (gdpr|pci-dss|hipaa|sox|custom) - default: none
- **--include-pentest**: Include penetration testing (true|false) - default: false
- **--vulnerability-scan**: Enable automated vulnerability scanning (true|false) - default: true
- **--code-analysis**: Include code security analysis (true|false) - default: true
- **--remediation-plan**: Generate remediation plan (true|false) - default: true
- **--generate-report**: Generate executive summary report (true|false) - default: true

## Success Criteria

- Complete security assessment performed
- All vulnerabilities identified and documented
- Risk ratings assigned to findings
- Actionable remediation plan created
- Compliance gaps documented
- Security hardening implemented
- Security monitoring configured
- Audit logging operational
- Team trained on security procedures
- Complete documentation delivered

## Example Security Reviews

1. **Basic Security Audit**
   - Essential security checks
   - Authentication and authorization review
   - Configuration security
   - Quick remediation plan

2. **Standard Production Audit**
   - Comprehensive multi-domain review
   - Vulnerability scanning
   - Code security analysis
   - Full hardening plan

3. **Compliance Audit (PCI-DSS)**
   - PCI-DSS gap analysis
   - Encryption assessment
   - Access control audit
   - Compliance documentation

4. **Comprehensive Security Assessment**
   - Deep security analysis
   - Penetration testing
   - Compliance review
   - Full remediation and monitoring

Tarantool security review for: $ARGUMENTS
