# 5 Whys Analysis Examples

## Example 1: Database Outage

**Problem**: Production database unavailable

**Why #1**: Почему database unavailable?
→ All connection attempts timing out

**Why #2**: Почему connection attempts timeout?
→ Database connection pool exhausted (100/100 connections)

**Why #3**: Почему connection pool exhausted?
→ Traffic spike 3x normal load

**Why #4**: Почему traffic spike вызвал exhaustion?
→ Connection pool не масштабируется автоматически

**Why #5**: Почему нет автоматического масштабирования?
→ Not implemented in initial architecture; load testing didn't cover 3x scenarios

**Root Cause**: Insufficient capacity planning и отсутствие auto-scaling

**Preventive Actions**:
1. Implement auto-scaling connection pool (P0)
2. Add connection pool monitoring (P0)
3. Expand load testing scenarios to 5x traffic (P1)
4. Review all resource pools for similar gaps (P1)

---

## Example 2: API Latency Spike

**Problem**: API response time increased from 200ms to 5s

**Why #1**: Почему API slow?
→ Database queries taking 4.5s average

**Why #2**: Почему database queries slow?
→ Missing index on frequently queried table

**Why #3**: Почему index missing?
→ Schema change last week removed index accidentally

**Why #4**: Почему accidental removal?
→ Database migration script не reviewed properly

**Why #5**: Почему migration not reviewed?
→ No mandatory review process для database changes

**Root Cause**: Lack of database migration review process

**Preventive Actions**:
1. Re-add missing index immediately (P0)
2. Implement mandatory DBA review для migrations (P0)
3. Add database migration testing in CI/CD (P1)
4. Create index monitoring alerts (P2)
