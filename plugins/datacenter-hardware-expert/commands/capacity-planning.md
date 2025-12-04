---
name: capacity-planning
description: Анализ текущей емкости и прогнозирование потребностей в ресурсах (CPU, память, storage, power, cooling).
---

# Capacity Planning для Инфраструктуры ЦОД

Эта команда анализирует текущее использование ресурсов, строит тренды роста и предоставляет рекомендации по планированию емкости.

## Использование

```bash
/capacity-planning [scope: cluster/datacenter/zone] [timeframe: 3m/6m/12m]
```

**Примеры:**
```bash
/capacity-planning cluster-prod-01 12m
/capacity-planning datacenter-moscow 6m
/capacity-planning zone-compute-a 3m
```

## Процесс анализа

### Шаг 1: Сбор текущих метрик

Соберу данные о текущем состоянии:

**Compute Resources:**
- Total physical cores
- Total allocated vCPUs (в виртуализированных средах)
- CPU utilization (average, peak, p95)
- Overcommit ratio (vCPU:pCore)

**Memory Resources:**
- Total physical RAM
- Total allocated memory (VMs/containers)
- Memory utilization (active, не allocated)
- Overcommit ratio

**Storage Resources:**
- Total capacity (по типам: SSD, HDD, NVMe)
- Used capacity
- IOPS capacity vs utilization
- Latency metrics

**Network Resources:**
- Link capacities (1G/10G/25G/100G)
- Bandwidth utilization
- Packet rates
- Trunk/uplink usage

**Facilities (ЦОД уровень):**
- Power: Total capacity, current draw, PUE
- Cooling: Total tons, temperature metrics
- Space: Rack count, U space available

### Шаг 2: Исторический анализ

Проанализирую trends (последние 6-12 месяцев):

**Growth Rate Calculation:**
```
Linear regression для каждого resource:
- CPU: vCPU allocation growth per month
- Memory: GB allocation growth per month
- Storage: TB growth per month
- Power: kW growth per month
```

**Seasonal Patterns:**
- Weekly cycles (business hours vs weekend)
- Monthly patterns (end-of-month processing)
- Annual patterns (holiday seasons, tax periods)

**Events Correlation:**
- Projects launched (workload additions)
- Migrations (inbound/outbound)
- Hardware refreshes (efficiency changes)

### Шаг 3: Прогнозирование

Построю forecast на requested timeframe:

**Methods:**
1. **Linear projection** (baseline)
2. **Business-driven forecast** (известные projects)
3. **Conservative scenario** (+20% contingency)
4. **Aggressive scenario** (+40% contingency)

### Шаг 4: Capacity Runway

Вычислю "runway" - время до исчерпания емкости:

```
Runway = (Available Capacity - Current Usage) / Growth Rate
```

## Формат отчета

```markdown
# Capacity Planning Report

**Scope:** [Production Cluster prod-cluster-01]
**Analysis Period:** 2024-06-01 to 2024-12-01 (6 months historical)
**Forecast Period:** 2024-12-01 to 2025-12-01 (12 months)
**Generated:** 2024-12-04
**Analyst:** datacenter-hardware-architect

## Executive Summary

### Current Status

| Resource | Total Capacity | Used | Available | Utilization | Status |
|----------|----------------|------|-----------|-------------|--------|
| CPU (cores) | 2,240 | 1,568 | 672 | 70% | ✓ Healthy |
| Memory (GB) | 17,920 | 14,336 | 3,584 | 80% | ⚠ Warning |
| Storage (TB) | 450 | 315 | 135 | 70% | ✓ Healthy |
| Power (kW) | 800 | 520 | 280 | 65% | ✓ Healthy |
| Cooling (Tons) | 230 | 155 | 75 | 67% | ✓ Healthy |

### Capacity Runway

| Resource | Growth Rate | Runway | Exhaustion Date | Action Required |
|----------|-------------|--------|-----------------|-----------------|
| CPU | +45 cores/month | 15 months | 2026-03-01 | Plan expansion Q4 2025 |
| Memory | +650 GB/month | **5.5 months** | **2025-05-15** | **Immediate action** |
| Storage | +12 TB/month | 11 months | 2025-11-01 | Plan expansion Q3 2025 |
| Power | +18 kW/month | 15.5 months | 2026-03-15 | Monitor quarterly |
| Cooling | +10 Tons/month | 7.5 months | 2025-07-15 | Plan expansion Q2 2025 |

### Critical Alerts

🔴 **CRITICAL: Memory Capacity**
- **Current:** 80% utilized
- **Runway:** 5.5 months
- **Action:** Plan memory expansion immediately
- **Recommendation:** Add 8TB память (500GB per host × 16 hosts) к Q1 2025

⚠ **WARNING: Cooling Capacity**
- **Current:** 67% utilized
- **Runway:** 7.5 months
- **Action:** Plan cooling expansion Q2 2025
- **Recommendation:** Add 2 CRAH units (30-ton each) или upgrade existing

✓ **HEALTHY: All other resources**
- Adequate runway (>12 months)
- Continue monitoring

## Detailed Analysis

### Compute (CPU)

#### Current State
```
Total Hosts: 40
Total Physical Cores: 2,240 (56 cores per host average)
Allocated vCPUs: 6,272
Overcommit Ratio: 2.8:1 (within recommended 2-4:1)

Utilization:
- Average: 45% (healthy)
- Peak: 72% (manageable)
- p95: 65%
```

#### Historical Trend
```
Month       Allocated vCPUs    Growth    Physical Cores Used
2024-06     5,100             -          1,290 (58%)
2024-07     5,200             +100       1,320 (59%)
2024-08     5,450             +250       1,390 (62%)
2024-09     5,680             +230       1,445 (65%)
2024-10     5,950             +270       1,515 (68%)
2024-11     6,200             +250       1,580 (71%)
2024-12     6,272             +72        1,568 (70%)

Average Growth: +195 vCPUs/month (~45 physical cores/month at 2.8:1 ratio)
```

#### Forecast (12 months)
```
Linear Projection:
2025-03: 6,857 vCPUs (1,745 cores, 78% util)
2025-06: 7,442 vCPUs (1,890 cores, 84% util)
2025-09: 8,027 vCPUs (2,039 cores, 91% util) ← Warning threshold
2025-12: 8,612 vCPUs (2,190 cores, 98% util) ← Critical

Conservative (+20%):
2025-12: 9,149 vCPUs (2,326 cores) ← **Exceeds capacity**
```

#### Capacity Runway
```
Available cores: 672 (2,240 - 1,568)
Growth rate: 45 cores/month
Runway: 672 / 45 = **15 months** (March 2026)

Recommended Action Threshold: 80% utilization
Threshold: 1,792 cores (80% of 2,240)
Time to 80%: (1,792 - 1,568) / 45 = **5 months** (May 2025)
```

#### Recommendations

**Short-term (0-6 months):**
✓ Current capacity sufficient
- Continue monitoring monthly
- Optimize workloads (rightsize VMs)
- DRS load balancing tuning

**Long-term (6-18 months):**
- **Action trigger:** May 2025 (80% utilization)
- **Procurement lead time:** 3-4 months
- **Decision point:** February 2025

**Expansion Options:**

**Option 1: Add Hosts (Scale Out)**
```
Add: 8 new hosts (448 cores total)
- Model: Dell PowerEdge R750 или equivalent
- Config: 2× Intel Xeon Gold 6348 (28 cores each = 56 cores per host)
- New total: 2,688 cores
- New utilization: 1,568 / 2,688 = 58%
- Extended runway: ~24 months

Cost estimate: $15k per host × 8 = $120k (hardware only)
+ Licensing: vSphere, storage, network ($40k estimated)
Total: ~$160k

Pros:
+ More fault domains (better HA)
+ Network/storage bandwidth scales
+ Easier incremental expansion

Cons:
- More rack space (8U)
- More power/cooling (4.8kW per host × 8 = 38kW)
- More management overhead
```

**Option 2: Upgrade Existing Hosts (Scale Up)**
```
Upgrade: 20 hosts to higher core count CPUs
- Current: 2× 28-core (56 cores)
- Upgrade to: 2× 40-core (80 cores)
- Net gain: +24 cores × 20 hosts = +480 cores
- New total: 2,720 cores
- New utilization: 1,568 / 2,720 = 58%
- Extended runway: ~25 months

Cost estimate: ~$4k per socket × 2 × 20 hosts = $160k

Pros:
+ No additional rack space
+ No additional power/cooling infrastructure
+ Less management overhead

Cons:
- Requires maintenance windows (downtime per host)
- Old CPUs waste (resale value low)
- No additional fault domains
- Memory capacity not increased (separate concern)
```

**Recommendation: Hybrid Approach**
```
Phase 1 (Q2 2025): Add 4 new hosts
- Cost: $80k
- Adds 224 cores
- Immediate relief (68% → 62% utilization)
- Addresses memory capacity simultaneously (add memory to new hosts)

Phase 2 (Q4 2025): Add 4 more hosts
- Cost: $80k
- Adds 224 cores
- Target utilization: ~55%
- Total expansion: 448 cores over 2 quarters

Total investment: $160k over 2 quarters (spread capex)
Runway extended: ~30 months
Addresses multiple constraints (CPU + memory + power/cooling planning)
```

### Memory

#### Current State
```
Total Physical Memory: 17,920 GB (448 GB per host average)
Allocated to VMs: 21,504 GB (overcommit 1.2:1)
Active Memory Usage: 14,336 GB (67% of allocated, 80% of physical)

Utilization:
- Physical: 80% (warning threshold)
- Ballooning: Minimal (<5% VMs affected)
- Swapping: None (healthy)
```

#### Historical Trend
```
Month       Physical Used (GB)    Growth    Utilization
2024-06     9,920                 -         55%
2024-07     10,560                +640      59%
2024-08     11,360                +800      63%
2024-09     12,160                +800      68%
2024-10     13,120                +960      73%
2024-11     13,760                +640      77%
2024-12     14,336                +576      80%

Average Growth: +736 GB/month
Recent trend (3 months): +725 GB/month (slowing slightly)
Conservative: +650 GB/month (use для planning)
```

#### Forecast (12 months)
```
Linear Projection:
2025-03: 16,286 GB (91% util) ← Warning
2025-04: 16,936 GB (95% util) ← Critical
2025-05: 17,586 GB (98% util) ← **Nearly full**
2025-06: 18,236 GB ← **EXCEEDS CAPACITY**

Conservative (+20%):
2025-04: **EXCEEDS CAPACITY**
```

#### Capacity Runway
```
Available memory: 3,584 GB (17,920 - 14,336)
Growth rate: 650 GB/month
Runway: 3,584 / 650 = **5.5 months** (May 2025)

**CRITICAL: Memory exhaustion в Q2 2025**
```

#### Recommendations

**IMMEDIATE ACTION REQUIRED:**

**Phase 1: Emergency Capacity (Q1 2025 - January)**
```
Quick wins (no hardware):
1. VM rightsizing audit
   - Tool: vRealize Operations или RVTools
   - Target: Identify over-allocated VMs (memory >> active)
   - Potential reclaim: 10-15% (1,500-2,000 GB)
   - Timeline: 2 weeks

2. Memory deduplication/compression
   - Enable TPS (Transparent Page Sharing) if disabled (security trade-off)
   - Potential savings: 5-10% (700-1,400 GB)
   - Timeline: 1 week

3. Workload migration
   - Move non-production VMs to separate cluster (if available)
   - Potential relief: Variable

Estimated runway extension: +2-3 months (to July-August 2025)
```

**Phase 2: Hardware Expansion (Q1 2025 - February/March)**
```
Add memory to existing hosts:

Option A: Increase all hosts to 768GB
- Current: 448 GB per host (14 DIMMs × 32GB)
- Target: 768 GB per host (24 DIMMs × 32GB)
- Add: 10 DIMMs × 32GB per host × 40 hosts = 12,800 GB total
- New capacity: 30,720 GB
- New utilization: 14,336 / 30,720 = 47%
- Extended runway: ~24 months

Cost: ~$150/GB × 12,800 GB = $1.92M (too expensive)

Option B: Selective upgrade (targeted hosts)
- Identify highest-utilized hosts (top 20)
- Upgrade to 768GB each
- Add: 10 DIMMs × 32GB × 20 hosts = 6,400 GB
- New capacity: 24,320 GB
- New utilization: 14,336 / 24,320 = 59%
- Extended runway: ~15 months

Cost: ~$150/GB × 6,400 GB = $960k

Option C: Add new high-memory hosts (recommended)
- Add: 4 new hosts с 1TB each = 4,096 GB
- New capacity: 22,016 GB
- New utilization: 14,336 / 22,016 = 65%
- Extended runway: ~12 months

Cost: ~$20k per host × 4 = $80k (hardware)
+ Memory: ~$150/GB × 4,096 GB = $615k
Total: ~$695k

Pros:
+ Adds compute capacity simultaneously (addresses both CPU and memory)
+ New hardware (warranty, latest gen)
+ Can use DDR5 (if new gen servers)
+ Better long-term investment

Cons:
- Higher upfront cost
- Rack space/power/cooling required
```

**Recommended Action Plan:**
```
January 2025:
- Execute VM rightsizing (reclaim ~1,500 GB)
- Procure 4 new hosts с 1TB memory each
- Lead time: 6-8 weeks

March 2025:
- Install и commission new hosts
- Migrate workloads для balanced utilization
- New utilization: ~60%

Q3 2025:
- Re-evaluate growth trend
- Plan next expansion if needed

Investment: ~$700k
Risk mitigation: High (prevents capacity exhaustion)
```

### Storage

[Similar detailed analysis для storage...]

### Power & Cooling

[Similar detailed analysis для datacenter facilities...]

## Financial Summary

### Capital Expenditure (CapEx)

| Item | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 | Total |
|------|---------|---------|---------|---------|-------|
| Compute hosts (8 total) | $160k | $160k | - | - | $320k |
| Memory upgrades | $700k | - | - | - | $700k |
| Storage expansion | $150k | - | $200k | - | $350k |
| Network upgrades | $50k | - | - | - | $50k |
| Cooling infrastructure | - | $120k | - | - | $120k |
| **Total** | **$1,060k** | **$280k** | **$200k** | **$0** | **$1,540k** |

### Operational Expenditure (OpEx) Impact

| Item | Annual Cost | Notes |
|------|-------------|-------|
| Power (additional 60kW × $0.10/kWh × 8760h) | $52.6k | Incremental power cost |
| Cooling (proportional) | $15k | Estimated increase |
| Maintenance (hardware) | $30k | 2% of hardware cost |
| Licensing (vSphere, etc.) | $80k | Per-host/per-core licenses |
| **Total OpEx Increase** | **$177.6k/year** | - |

### Return on Investment (ROI)

```
Cost of capacity expansion: $1,540k (CapEx) + $177k (first year OpEx) = $1,717k

Cost of NOT expanding (business impact):
- Revenue at risk (service outages): ~$500k/month
- Inability to launch new projects: ~$300k/month opportunity cost
- Emergency procurement premium: +30% hardware cost (~$460k)

Payback period: ~2 months of avoided outages
ROI: Immediate (risk mitigation) + strategic (growth enablement)
```

## Risk Assessment

### High Risk (Immediate Attention)

🔴 **Memory Capacity Exhaustion (5.5 months)**
- **Impact:** Cannot provision new VMs, service disruption risk
- **Probability:** 95% (если no action taken)
- **Mitigation:** Execute Phase 1 & 2 memory expansion immediately

### Medium Risk (Monitor Closely)

⚠ **Cooling Capacity (7.5 months)**
- **Impact:** Thermal throttling, potential hardware damage
- **Probability:** 70% (при continued growth)
- **Mitigation:** Plan CRAH expansion Q2 2025

### Low Risk (Routine Monitoring)

✓ **CPU Capacity (15 months)**
- **Impact:** Performance degradation, scheduling delays
- **Probability:** 50% (good runway, может optimize)
- **Mitigation:** Plan expansion Q4 2025, optimize workloads

✓ **Storage Capacity (11 months)**
- **Impact:** Cannot store new data
- **Probability:** 60% (depends на data growth patterns)
- **Mitigation:** Plan expansion Q3 2025

✓ **Power Capacity (15.5 months)**
- **Impact:** Cannot add equipment
- **Probability:** 40% (may optimize PUE)
- **Mitigation:** Monitor quarterly, plan if needed

## Recommendations Summary

### Q1 2025 (January - March)

**Priority 1: Memory Capacity (CRITICAL)**
- [ ] Execute VM rightsizing audit (Week 1-2)
- [ ] Procure 4 high-memory hosts (Week 1, delivery Week 6-8)
- [ ] Install и commission new hosts (Week 9-10)
- **Budget:** $700k

**Priority 2: Compute Expansion**
- [ ] Procure 4 standard hosts (Week 1, delivery Week 6-8)
- [ ] Plan installation Q2
- **Budget:** $160k

**Priority 3: Network Infrastructure**
- [ ] Upgrade core switches to support additional bandwidth
- **Budget:** $50k

### Q2 2025 (April - June)

**Priority 1: Cooling Infrastructure**
- [ ] Install 2 additional CRAH units (30-ton each)
- [ ] Commission и test
- **Budget:** $120k

**Priority 2: Compute Expansion Phase 2**
- [ ] Install 4 standard hosts from Q1 procurement
- [ ] Balance workloads
- **Budget:** (Already procured)

### Q3 2025 (July - September)

**Priority 1: Storage Expansion**
- [ ] Add NVMe capacity (100TB usable)
- [ ] Expand existing arrays или add new
- **Budget:** $200k

**Priority 2: Capacity Review**
- [ ] Mid-year capacity review
- [ ] Adjust forecasts based на actual growth
- [ ] Plan H2 и 2026 expansions

### Q4 2025 (October - December)

**Priority 1: 2026 Planning**
- [ ] Annual capacity planning cycle
- [ ] Budget submission для 2026
- [ ] Long-term architectural reviews

## Monitoring & Review

**Monthly Reviews:**
- Capacity utilization dashboards
- Trend analysis updates
- Runway recalculation

**Quarterly Reviews:**
- Detailed capacity report
- Forecast adjustments
- Investment recommendations

**Annual Review:**
- Comprehensive capacity plan
- Multi-year roadmap
- Technology refresh planning

## Appendix

### Assumptions
- Growth rates based на 6-month historical data
- Linear regression used для baseline forecast
- Business-driven forecast incorporates known projects
- Hardware lead times: 6-8 weeks
- Installation/commissioning: 2 weeks per batch

### Data Sources
- vCenter performance metrics (6 months)
- DCIM power/cooling data (6 months)
- Storage array capacity reports (6 months)
- Network monitoring (6 months)
- Project pipeline (IT PMO)

### Tools Used
- vRealize Operations Manager (VMware monitoring)
- Grafana (metrics visualization)
- Excel/Python (trend analysis, forecasting)
- DCIM platform (facilities data)

---

**Report prepared by:** datacenter-hardware-architect
**Review date:** Quarterly (Next: 2025-03-01)
**Distribution:** IT Leadership, Operations, Finance
```

## Deliverables

1. **Capacity Planning Report** (Markdown/PDF) - Полный отчет как выше
2. **Executive Summary** (PowerPoint) - 5-slide presentation для leadership
3. **Budget Proposal** (Excel) - Детализированный CapEx/OpEx breakdown
4. **Implementation Timeline** (Project plan) - Gantt chart с milestones
5. **Monitoring Dashboard** (Grafana) - Real-time capacity tracking

## Требования

- Historical data (minimum 3 months, recommended 6-12 months)
- Access to monitoring systems (vCenter, DCIM, storage arrays)
- Business roadmap (upcoming projects, migrations)
- Budget constraints и approval processes
- Hardware procurement lead times
