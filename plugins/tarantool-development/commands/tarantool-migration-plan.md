---
name: tarantool-migration-plan
description: Interactive command for planning and executing Tarantool database migrations with validation and rollback support
---

# Tarantool Migration Planning & Execution

Plan, execute, and validate database migrations for Tarantool with comprehensive rollback support and zero-downtime strategies:

[Extended thinking: This command handles complete migration lifecycle from schema changes to data migrations, supporting both simple DDL operations and complex data transformations. It includes migration validation, rollback planning, dependency management, and production migration strategies with minimal downtime.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Migration Type
- **schema**: Space/index structure changes (DDL)
- **data**: Data transformation and migration
- **combined**: Schema + data migration together
- **versioning**: Migration versioning system setup
- **rollback**: Rollback execution for failed migration

### Migration Strategy
- **online**: Zero-downtime online migration
- **offline**: Offline migration with downtime window
- **gradual**: Progressive migration with feature flags
- **dual-write**: Dual-write pattern for gradual transition
- **blue-green**: Blue-green deployment with migration

### Risk Level
- **low**: Simple schema changes (add nullable column)
- **medium**: Complex schema changes (modify indexes)
- **high**: Data migrations with transformations
- **critical**: Breaking changes requiring coordinated deployment

## Phase 1: Planning & Analysis

1. **Migration Requirements Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Analyze migration requirements for: $ARGUMENTS. Review current schema and target schema. Identify schema changes needed. Identify data transformations. Assess migration complexity and risks. Document dependencies and constraints."
   - Expected output: Migration requirements document with risk assessment

2. **Impact Assessment**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Assess migration impact for: $ARGUMENTS. Migration type: $MIGRATION_TYPE. Analyze data volume and processing time. Identify affected applications and services. Assess downtime requirements. Estimate rollback complexity. Identify breaking changes."
   - Expected output: Impact assessment report with downtime estimates

3. **Dependency Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Analyze migration dependencies for: $ARGUMENTS. Identify foreign key constraints. Map application dependencies. Identify migration order requirements. Document data integrity constraints. Plan migration sequencing."
   - Expected output: Dependency graph with migration ordering

4. **Rollback Strategy**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Design rollback strategy for: $ARGUMENTS. Risk level: $RISK_LEVEL. Plan reverse migration steps. Design rollback validation. Plan for partial rollback scenarios. Document rollback testing procedures. Create rollback decision criteria."
   - Expected output: Comprehensive rollback plan with procedures

## Phase 2: Migration Design

5. **Schema Migration Design**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Design schema migration for: $ARGUMENTS. Strategy: $MIGRATION_STRATEGY. Create DDL migration scripts. Design index changes with minimal locking. Plan space format changes. Handle backward compatibility. Design temporary structures if needed."
   - Expected output: Schema migration scripts with DDL statements

6. **Data Migration Design**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Design data migration for: $ARGUMENTS. Plan data transformation logic. Design batch processing strategy for large datasets. Plan for data validation during migration. Handle data type conversions. Design error handling and recovery."
   - Expected output: Data migration scripts with transformation logic

7. **Zero-Downtime Strategy**
   - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
   - Prompt: "Design zero-downtime migration for: $ARGUMENTS. Plan online schema changes using ghost migrations. Design dual-write patterns for gradual transition. Plan feature flags for controlled rollout. Design backward-compatible schema changes. Plan rolling deployment coordination."
   - Expected output: Zero-downtime migration strategy document

8. **Migration Versioning**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Setup migration versioning for: $ARGUMENTS. Design migration version tracking. Create migration registry in Tarantool. Plan migration history and auditing. Design version conflict detection. Create migration metadata structure."
   - Expected output: Migration versioning system implementation

## Phase 3: Testing & Validation

9. **Migration Validation Scripts**
   - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
   - Prompt: "Create validation scripts for: $ARGUMENTS. Design pre-migration validation (schema, data integrity). Design post-migration validation (data consistency, performance). Create automated validation tests. Design data comparison utilities. Plan validation reporting."
   - Expected output: Comprehensive validation test suite

10. **Test Environment Setup**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Setup migration testing environment for: $ARGUMENTS. Clone production data to test environment. Create test migration execution scripts. Setup monitoring for migration testing. Plan test scenarios (success, failure, partial). Document test environment procedures."
    - Expected output: Test environment configuration and procedures

11. **Migration Testing**
    - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
    - Prompt: "Execute migration testing for: $ARGUMENTS. Run migration on test data. Validate data integrity post-migration. Test rollback procedures. Measure migration performance and duration. Test partial failure scenarios. Document test results."
    - Expected output: Migration test results with performance metrics

12. **Performance Impact Testing**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Test migration performance impact for: $ARGUMENTS. Measure migration execution time. Test system performance during migration. Identify performance bottlenecks. Test index rebuild performance. Validate post-migration query performance. Plan performance optimization."
    - Expected output: Performance test results with optimization recommendations

## Phase 4: Production Execution

13. **Pre-Migration Checklist**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Create pre-migration checklist for: $ARGUMENTS. Verify backup completion and verification. Check cluster health and replication status. Validate application readiness. Verify rollback procedures tested. Check monitoring and alerting ready. Document go/no-go criteria."
    - Expected output: Pre-migration checklist and go/no-go decision framework

14. **Backup & Safety Measures**
    - Use Task tool with subagent_type="tarantool-development::tarantool-devops-engineer"
    - Prompt: "Setup migration safety measures for: $ARGUMENTS. Create full backup before migration. Setup snapshot and WAL archival. Configure migration monitoring. Setup automatic rollback triggers. Plan communication procedures. Create migration runbook."
    - Expected output: Safety measures configuration and runbook

15. **Migration Execution**
    - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
    - Prompt: "Execute production migration for: $ARGUMENTS. Execute pre-migration validation. Run migration scripts with monitoring. Execute post-migration validation. Verify data integrity. Monitor system performance. Document execution progress and issues."
    - Expected output: Migration execution report with validation results

16. **Post-Migration Validation**
    - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
    - Prompt: "Validate post-migration state for: $ARGUMENTS. Run validation test suite. Verify data consistency and integrity. Test application functionality. Monitor system performance metrics. Verify replication consistency. Check for data loss or corruption."
    - Expected output: Post-migration validation report

## Phase 5: Monitoring & Optimization

17. **Migration Monitoring**
    - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
    - Prompt: "Setup migration monitoring for: $ARGUMENTS. Configure migration progress metrics. Setup performance monitoring during migration. Create migration alerting rules. Setup data validation monitoring. Create migration dashboard. Configure audit logging."
    - Expected output: Monitoring configuration and dashboards

18. **Post-Migration Optimization**
    - Use Task tool with subagent_type="tarantool-development::tarantool-performance-optimizer"
    - Prompt: "Optimize post-migration performance for: $ARGUMENTS. Analyze query performance post-migration. Optimize new indexes if needed. Tune memory allocation for new schema. Validate space engine configuration. Run ANALYZE for statistics update. Document optimization results."
    - Expected output: Post-migration optimization recommendations

19. **Documentation & Runbooks**
    - Use Task tool with subagent_type="documentation-generation::docs-architect"
    - Prompt: "Create migration documentation for: $ARGUMENTS. Document migration procedures executed. Create rollback procedures guide. Document validation procedures. Create troubleshooting guide. Document lessons learned. Create future migration templates."
    - Expected output: Comprehensive migration documentation

20. **Knowledge Transfer**
    - Use Task tool with subagent_type="tarantool-development::tarantool-migration-specialist"
    - Prompt: "Prepare knowledge transfer for: $ARGUMENTS. Document migration decisions and rationale. Create team training materials. Document edge cases and gotchas. Share migration best practices. Create migration playbook for future use."
    - Expected output: Knowledge transfer materials and playbook

## Execution Parameters

### Required
- **--migration-name**: Descriptive migration name
- **--migration-type**: Type of migration (schema|data|combined|versioning|rollback)
- **--source-version**: Current database version/schema
- **--target-version**: Target database version/schema

### Optional
- **--migration-strategy**: Strategy (online|offline|gradual|dual-write|blue-green) - default: online
- **--risk-level**: Risk assessment (low|medium|high|critical) - default: medium
- **--batch-size**: Batch size for data migration - default: 1000
- **--downtime-window**: Acceptable downtime in minutes - default: 0
- **--enable-rollback**: Enable automatic rollback on failure (true|false) - default: true
- **--validation-mode**: Validation strictness (basic|standard|comprehensive) - default: standard
- **--dry-run**: Execute in dry-run mode (true|false) - default: false

## Success Criteria

- Migration requirements fully analyzed and documented
- Rollback strategy tested and verified
- All validation tests passing
- Zero data loss or corruption
- Application functionality verified post-migration
- Performance meets or exceeds baseline
- Rollback procedures tested and documented
- Team trained on migration procedures
- Complete documentation and runbooks created

## Example Migrations

1. **Simple Schema Change**
   - Add nullable column to existing space
   - Create non-unique index
   - Online migration with no downtime
   - Automatic validation

2. **Complex Data Migration**
   - Data transformation between spaces
   - Batch processing for large datasets
   - Dual-write pattern for gradual transition
   - Comprehensive validation and monitoring

3. **Breaking Change Migration**
   - Schema restructuring with data migration
   - Blue-green deployment pattern
   - Feature flags for controlled rollout
   - Comprehensive rollback plan

4. **Version Migration System**
   - Setup migration versioning framework
   - Create migration history tracking
   - Implement migration dependency resolution
   - Automated migration execution

Tarantool migration planning for: $ARGUMENTS
