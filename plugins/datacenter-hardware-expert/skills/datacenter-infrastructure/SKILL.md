---
name: datacenter-infrastructure
description: Проектирование и эксплуатация инфраструктуры ЦОД (электропитание, охлаждение, безопасность). Использовать когда требуется планирование ЦОД, оптимизация энергоэффективности или troubleshooting систем facilities.
---

# Инфраструктура центра обработки данных

## Когда использовать этот навык

- Проектирование новых ЦОД или модернизация существующих
- Анализ энергоэффективности и оптимизация PUE
- Troubleshooting систем электропитания и охлаждения
- Capacity planning для power и cooling
- Compliance аудиты (Tier certification, ISO standards)

## Ключевые концепции

### Tier Classification System

**Tier I - Basic**
```
Availability: 99.671% (28.8 ч downtime/год)

Требования:
✓ Single path для power и cooling
✓ Non-redundant capacity components
✓ Planned maintenance requires downtime
- No concurrent maintainability
- No fault tolerance

Use Case:
- Small business datacenter
- Non-critical applications
- Budget-constrained projects
```

**Tier II - Redundant Components**
```
Availability: 99.741% (22 ч downtime/год)

Требования:
✓ Single path с redundant components (N+1)
✓ Maintenance на компонентах без downtime
✓ Planned infrastructure maintenance requires downtime
- No concurrent maintainability
- No fault tolerance

Improvements over Tier I:
+ N+1 UPS modules
+ N+1 Cooling units
+ N+1 Generators
+ Redundant PSUs в критическом equipment
```

**Tier III - Concurrently Maintainable**
```
Availability: 99.982% (1.6 ч downtime/год)

Требования:
✓ Multiple active paths (single active at a time)
✓ N+1 redundancy на каждом path
✓ Concurrent maintenance без downtime
✓ Planned maintenance без impact
- Fault tolerance (ограниченная)

Key Features:
+ Dual power feeds (A+B buses)
+ Multiple distribution paths
+ Dual-corded equipment или STS
+ Compartmentalization для isolation
+ Redundant network paths

Use Case:
- Enterprise datacenters
- Financial services
- E-commerce platforms
- SLA 99.9%+
```

**Tier IV - Fault Tolerant**
```
Availability: 99.995% (26 мин downtime/год)

Требования:
✓ Multiple active paths (2N)
✓ Withstand любой single worst-case failure
✓ Continuous cooling (2 independent systems)
✓ Full compartmentalization
✓ Automated response для failures

Key Features:
+ 2N или 2(N+1) для всех critical systems
+ Active-Active power paths
+ Active cooling на обоих paths
+ Continuous operation через any failure
+ Sophisticated monitoring & control

Use Case:
- Mission-critical applications
- Healthcare systems
- Government/Defense
- Major cloud providers (portions of facility)
- Financial trading platforms

Cost: ~2.5-3× Tier III
```

### Power Distribution Architectures

**Single Path (Tier I-II)**
```
Utility → Main Switch → UPS → Distribution → PDU → IT
                        ↓
                    Generator

Characteristics:
- Single point of failure
- Maintenance requires downtime
- Simplest design
- Lowest cost

Failure Modes:
✗ UPS failure → full outage
✗ PDU failure → downstream equipment down
✗ Distribution panel issue → zone outage
```

**Dual Path with STS (Tier III)**
```
                  ┌─ UPS-A → Dist-A → PDU-A ─┐
Utility-A → MSB-A ┤                          ├→ STS → IT
                  └─ Gen-A                   │
                                             │
                  ┌─ UPS-B → Dist-B → PDU-B ─┘
Utility-B → MSB-B ┤
                  └─ Gen-B

STS (Static Transfer Switch):
- Monitors both A & B feeds
- <4ms transfer time
- Automatic failover при loss of preferred source
- Single-corded equipment protected

Failure Modes:
✓ UPS-A fails → STS transfers to B (no outage)
✓ Maintenance на A path → operate on B
✗ STS failure → potential outage (SPOF)
```

**Dual Path with Dual-Corded (Tier III-IV)**
```
Utility-A → UPS-A → Dist-A → PDU-A → Server PSU-A ─┐
                                                    ├→ Server
Utility-B → UPS-B → Dist-B → PDU-B → Server PSU-B ─┘

Dual-Corded Equipment:
- Two power supplies (PSU-A, PSU-B)
- Load sharing or active-backup
- True redundancy (no STS needed)

Failure Modes:
✓ Entire A path fails → runs on B (no outage)
✓ PSU-A fails → runs on PSU-B
✓ Concurrent maintenance: A path offline, B active
✓ Tier IV: Withstand worst-case failure (utility + gen on same path)
```

### Cooling Architectures

**Computer Room Air Conditioning (CRAC)**
```
Типы:
1. Air-Cooled CRAC:
   Datacenter → CRAC (DX cycle) → Condenser outside

   Pros:
   + Independent operation
   + No chilled water dependency
   + Good для small/medium facilities

   Cons:
   - Lower efficiency (COP ~2.5-3.0)
   - Refrigerant management
   - Limited scalability

2. Water-Cooled CRAC:
   Datacenter → CRAC (DX cycle) → Cooling tower/chiller

   Pros:
   + Higher efficiency (COP ~3.0-3.5)
   + Better scalability
   + Lower exterior noise

   Cons:
   - Chilled water dependency
   - More complex infrastructure
   - Water management required

Sizing:
- Rule of thumb: 1 Ton per 1 kW IT load (при PUE 1.4)
- Add 20-30% margin для growth и transients
- N+1 redundancy minimum
```

**Computer Room Air Handler (CRAH)**
```
Architecture:
Datacenter → CRAH (fan coils) → Chilled water from central plant

Central Chiller Plant:
Chillers → Cooling towers → Distribution pumps → CRAHs

Pros:
+ Higher system efficiency (COP 4.0-6.0 with economizer)
+ Easier to scale (add coils)
+ Less equipment в computer room (no compressors)
+ Better для large datacenters

Cons:
- Higher capital cost (chiller plant)
- Complex infrastructure
- Chilled water leak risk
- Centralized dependency

Optimization:
- Variable speed drives (fans, pumps, chillers)
- Water-side economizer (free cooling)
- Raised chilled water temp (18-20°C supply)
- Delta T management (minimize bypass)
```

**Advanced Cooling Strategies**

*Containment*
```
Cold Aisle Containment (CAC):
[Cold aisle enclosed] → [Hot aisles open]

Pros:
+ Lower pressure differential (легче на doors)
+ Easier fire suppression
+ Simpler implementation

Cons:
- Hot ambient (uncomfortable for humans)
- Less efficient (cooling entire room)

Hot Aisle Containment (HAC):
[Hot aisle enclosed] → [Cold environment]

Pros:
+ Higher return temps → better chiller efficiency
+ More free cooling hours
+ Comfortable ambient для персонала
+ Less hot air recirculation

Cons:
- Higher pressure в containment
- Fire suppression complexity
- Structural loading (chimney panels)

Recommendation: HAC для modern high-density deployments
```

*In-Row Cooling*
```
Deployment:
[Rack] - [InRow Unit] - [Rack] - [InRow Unit] - [Rack]

Characteristics:
- Close-coupled cooling
- Short air path (lower fan power)
- Modular scaling (add units с racks)
- Higher air temperature delta (ΔT 15-20°C)

Pros:
+ Highly efficient (minimal bypass air)
+ Excellent для high-density (>10kW/rack)
+ Precise temperature control
+ Pay-as-you-grow model

Cons:
- Higher unit count (more maintenance points)
- More floor space consumption
- Chilled water/coolant distribution needed

Use Case: High-performance computing, AI/ML clusters
```

*Rear Door Heat Exchangers (RDHx)*
```
Types:
1. Passive RDHx:
   - Chilled water coils на rear door
   - No fans (server exhaust provides airflow)
   - 30-50% heat removal

2. Active RDHx:
   - Coils + fans
   - 90-100% heat removal
   - Can operate standalone (no CRAC needed)

Pros:
+ Captures heat at source
+ No room cooling needed (с active)
+ Eliminates hot spots
+ Retrofit friendly (existing racks)

Cons:
- Weight (100+ kg per door)
- Water leak risk (at rack level)
- Cost ($5k-10k per rack)
- Maintenance (many units)

Use Case: Blade systems, high-density compute
```

*Liquid Cooling*
```
Direct-to-Chip:
- Cold plates на CPU/GPU
- Closed-loop liquid circulation
- 60-80% heat removal

Immersion Cooling:
- Servers погружены в dielectric fluid
- Single-phase или two-phase (boiling)
- 95%+ heat removal

Pros:
+ Extreme density support (50+ kW/rack)
+ Higher CPU/GPU frequencies (better cooling)
+ Reduced datacenter cooling infrastructure
+ Lower PUE (<1.10 achievable)

Cons:
- High initial cost
- Specialized hardware required
- Maintenance complexity
- Limited vendor ecosystem (пока)

Adoption: HPC, AI training clusters, crypto mining
```

### Free Cooling / Economization

**Air-Side Economizer**
```
Direct Air-Side:
Outside air → Filters → Datacenter (когда T_outside < T_setpoint)

Pros:
+ Максимальная эффективность (chiller off)
+ Simple implementation

Cons:
- Particulate contamination risk
- Humidity control challenges
- Security concerns (outside air intake)

Indirect Air-Side:
Outside air → Heat exchanger ← Datacenter air

Pros:
+ Separation (cleaner datacenter air)
+ Better humidity control
+ Security maintained

Cons:
- Efficiency loss (heat exchanger)
- Higher capital cost

Hours of Free Cooling (примеры):
Location          Dry-bulb <15°C    Wet-bulb <10°C
Helsinki, FI      5,500 hrs         4,800 hrs
Seattle, WA       4,200 hrs         3,600 hrs
Dublin, IE        5,800 hrs         5,200 hrs
Singapore, SG     0 hrs             200 hrs
Phoenix, AZ       1,800 hrs         500 hrs
```

**Water-Side Economizer**
```
Architecture:
Cooling tower → Heat exchanger → Chilled water loop → CRAHs
                      ↕
                   Chiller (bypass when free cooling)

Operation Modes:
1. Full free cooling: Chiller off, tower direct cooling
   (когда T_wetbulb < T_chilled_water - 3°C)

2. Partial free cooling: Chiller + tower blended
   (transition periods)

3. Mechanical cooling: Chiller only
   (high ambient temperature)

Pros:
+ Works в более широком temperature range (wet-bulb based)
+ No contamination concerns
+ Better humidity control
+ Higher availability hours vs air-side

Efficiency Example (Dublin climate):
- Full free cooling: 4,500 hrs/year (51%)
- Partial free cooling: 2,200 hrs/year (25%)
- Mechanical only: 2,100 hrs/year (24%)
- Annual PUE: ~1.15-1.20

Cloud Provider Adoption:
- AWS: Water-side economizer в Oregon, Dublin
- Google: Evaporative cooling в Netherlands, Belgium
- Microsoft: Adiabatic cooling в Ireland, Netherlands
```

### PUE Optimization

**PUE (Power Usage Effectiveness)**
```
Formula:
PUE = Total Facility Power / IT Equipment Power

Categories:
PUE     Rating              Examples
1.0     Theoretical ideal   (impossible - always losses)
<1.2    Excellent           Google avg (~1.10), hyperscale leaders
1.2-1.5 Good                Well-designed modern facilities
1.5-2.0 Average             Typical enterprise datacenter
>2.0    Poor                Legacy facilities, poor efficiency

Inverse: DCiE (Data Center infrastructure Efficiency)
DCiE = IT Power / Total Power = 1 / PUE (expressed as %)
```

**PUE Breakdown**
```
Total Power (100%):
├─ IT Equipment (50-70%):     Target high %
│  ├─ Servers (70%)
│  ├─ Storage (20%)
│  └─ Network (10%)
├─ Cooling (20-40%):          Major optimization target
│  ├─ CRAC/CRAH (60%)
│  ├─ Chillers (25%)
│  └─ Cooling towers/pumps (15%)
├─ Power Distribution (5-10%): Minimize losses
│  ├─ UPS losses (60%)
│  ├─ PDU/transformers (30%)
│  └─ Cables (10%)
└─ Lighting, security, other (2-5%): Minor contributor

Optimization Focus Priority:
1. Cooling (biggest impact)
2. Power distribution efficiency
3. IT equipment utilization
```

**Cooling Optimization для PUE**
```
Strategy 1: Raise temperatures
- Traditional: 20°C supply, 25°C ambient
- Modern: 18°C supply, 27°C ambient
- Impact: +1°C return temp → ~2-4% chiller efficiency gain

Strategy 2: Airflow management
- Seal bypass air (blanking panels, brush strips)
- Containment (CAC или HAC)
- Impact: Reduce CRAC/CRAH airflow 20-30% → fan power savings

Strategy 3: Free cooling
- Water-side economizer
- Impact: 40-60% reduction cooling energy (в suitable climates)

Strategy 4: Variable speed drives
- Fans, pumps, chillers
- Impact: 20-40% reduction energy при partial loads

Strategy 5: Hot water cooling
- Raise chilled water temp: 7°C → 18°C
- More economizer hours, better chiller efficiency
- Impact: 15-25% cooling energy reduction

Combined Impact Example:
Baseline PUE: 1.8
+ Raise temps: 1.8 → 1.7 (-6%)
+ Containment: 1.7 → 1.55 (-9%)
+ Free cooling: 1.55 → 1.35 (-13%)
+ VFDs: 1.35 → 1.25 (-7%)
Target PUE: 1.25 (30% improvement overall)
```

## Capacity Planning

### Power Capacity

**Calculation Method**
```
Step 1: Current IT Load
- Measure: PDU/UPS readings
- Or nameplate: Sum server PSU ratings × 60-70% (realistic load)

Step 2: Overhead (Infrastructure Loss)
- UPS efficiency: 92-96% (4-8% loss)
- Transformer/PDU: 2-3% loss
- Cabling: 1-2% loss
- Total power loss: ~8-12%

Step 3: Cooling Load
- Depends на PUE target
- PUE 1.5: Cooling = IT Load × 0.5
- PUE 1.3: Cooling = IT Load × 0.3

Step 4: Total Facility Load
Total = IT Load / DCiE
Or: Total = IT Load × PUE

Example:
- IT Load: 1,000 kW (measured)
- Target PUE: 1.4
- Total Facility: 1,000 × 1.4 = 1,400 kW
- UPS sizing: 1,400 kW (utility input side)
- Generator sizing: 1,400 kW × 1.25 = 1,750 kW (transient loads)
```

**Growth Planning**
```
Method 1: Historical Trend
- Collect 12-24 months data
- Linear regression для load growth
- Example: +50 kW/quarter → 200 kW/year growth

Method 2: Business-Driven
- Project launches: +X servers = +Y kW
- Migrations: Inbound +Z kW, outbound -W kW
- Refresh cycles: New gen = -10-20% power (efficiency)

Method 3: Headroom Target
- Maintain 20-30% available capacity
- Triggers for expansion:
  * <30% available → plan expansion
  * <20% available → freeze new deployments
  * <10% available → emergency capacity measures

Capacity Runway Calculation:
Available Capacity: 500 kW
Current Growth Rate: 50 kW/quarter
Runway: 500 / 50 = 10 quarters = 2.5 years

Expansion Timeline:
- 2.5 years remaining
- 18 months planning/design/procurement
- Start expansion now (в 6 months remaining)
```

### Cooling Capacity

**Heat Load Calculation**
```
IT Heat Generation:
- 1 kW electrical = 3,412 BTU/hr heat
- 1 Ton cooling = 12,000 BTU/hr = 3.517 kW cooling

Example:
- IT Load: 600 kW
- Heat: 600 × 3,412 = 2,047,200 BTU/hr
- Cooling needed: 2,047,200 / 12,000 = 171 Tons

Infrastructure Heat:
- UPS heat: IT × (1 - UPS_efficiency) = 600 × 0.08 = 48 kW
- Lighting: 5 W/m² × 2,000 m² = 10 kW
- People: 20 people × 0.1 kW = 2 kW
- Total infra heat: 60 kW = 20 Tons

Total Cooling: 171 + 20 = 191 Tons

Safety Factor: +20% → 229 Tons

Redundancy: N+1 с 30-Ton units → 8 units (240 Tons total, 210 available при 1 failed)
```

**Density Planning**
```
Low Density (<5 kW/rack):
- Standard office servers, VDI
- Perimeter cooling (CRAC/CRAH) sufficient
- 25-30% perforated tiles

Medium Density (5-10 kW/rack):
- General enterprise compute
- Containment recommended
- May need supplemental cooling (hot spots)

High Density (10-20 kW/rack):
- Database servers, storage arrays
- In-row cooling recommended
- Hot aisle containment required

Very High Density (>20 kW/rack):
- Blade chassis, HPC, AI/ML
- Rear door heat exchangers
- или liquid cooling (direct-to-chip)

Planning:
- Zoning: Group similar densities
- Cooling strategy per zone
- Power distribution (higher voltage для high density)
```

## Мониторинг и Alerting

### Critical Metrics

**Power Monitoring**
```
Real-time (5-minute intervals):
- UPS: Load %, input/output voltage, battery status
- Generator: Running status, fuel level, load %
- PDU: Per-circuit load (A, kW), voltage
- Branch circuits: Load % (<80% threshold)

Historical (daily/weekly):
- PUE trending
- Power consumption по зонам
- Peak demand analysis
- Stranded capacity identification

Alerts:
Critical (immediate):
- UPS на battery (utility failure)
- Generator failed start
- Circuit >90% load
- UPS bypass mode (no battery backup!)

Warning (30 min response):
- UPS battery <30 min runtime
- Circuit >80% load
- Generator fuel <24 hours
- Voltage out of range (±10%)
```

**Cooling Monitoring**
```
Real-time (1-5 minute intervals):
- Rack inlet temperature (top/middle/bottom)
- Supply air temperature (CRAC/CRAH output)
- Return air temperature
- Differential pressure (raised floor, containment)
- Humidity (RH %, dew point)

Historical:
- Temperature trending
- Hot spot identification
- Cooling unit efficiency (kW/Ton)
- Free cooling hours

Alerts:
Critical:
- Rack inlet >27°C (ASHRAE recommended limit)
- Supply air >20°C (CRAC/CRAH issue)
- Dew point >17°C (condensation risk)
- Cooling unit failure

Warning:
- Rack inlet >25°C
- Temperature trending up (>1°C increase/hour)
- Humidity <20% или >80% RH
- Differential pressure low (<10 Pa)
```

**Environmental**
```
Continuous:
- Water leak detection (под raised floor, CRAC units)
- Smoke detection (VESDA air sampling)
- Fire alarm status

Periodic (hourly/daily):
- Outdoor temperature (для economizer control)
- Generator auto-start test (weekly)
- UPS battery test (monthly)
- Transfer switch test (quarterly)

Alerts:
- Water leak: Immediate response (potential equipment damage)
- Smoke: Emergency response (fire risk)
- Generator test failure: Investigate within 24h
- UPS battery degradation: Plan replacement <6 months
```

## Troubleshooting Scenarios

### Scenario 1: Overheating Zone

**Symptoms**
- Multiple racks в одной зоне >27°C inlet temp
- Servers throttling или thermal shutdown
- Алерты от hardware monitoring

**Systematic Diagnosis**
```
1. Isolate Problem Scope:
   ☐ Single rack или multiple?
   ☐ Specific row или entire zone?
   ☐ Recent changes (new equipment, load increase)?

2. Cooling Supply Check:
   ☐ CRAC/CRAH units: Operating status, alarms?
   ☐ Supply air temp: Should be 15-18°C
   ☐ Airflow rate: Fan speed, VFD status
   ☐ Chilled water (если CRAH): Valve position, flow rate

3. Airflow Path Analysis:
   ☐ Raised floor pressure: 10-25 Pa normal
   ☐ Perforated tiles: Blocked? Correct placement?
   ☐ Under-floor obstructions: Cables blocking plenum?
   ☐ Containment integrity: Gaps? Missing panels?

4. Heat Load Verification:
   ☐ PDU readings: Recent load increase?
   ☐ New equipment: High-density servers added?
   ☐ Rack density: Exceeding design (>10 kW/rack)?

5. Local Issues:
   ☐ Blanking panels: Missing? (bypass air)
   ☐ Cable management: Poor (blocking airflow)?
   ☐ Server fans: Operating normally?
```

**Resolution Steps**
```
Immediate (Tier 1):
1. Add/adjust perforated tiles (более airflow под hot racks)
2. Install missing blanking panels
3. Lower CRAC/CRAH setpoint (temporary, -2°C)
4. Check/clear under-floor obstructions

Short-term (Tier 2):
1. Rebalance IT load:
   - vMotion VMs от hot hosts
   - Power down non-critical workloads
2. Add supplemental cooling:
   - Portable spot coolers (temporary)
   - Adjust adjacent CRAC units для more airflow
3. Containment improvements:
   - Seal gaps с brush strips
   - Add/fix containment panels

Long-term (Tier 3):
1. Thermal audit:
   - CFD modeling для airflow optimization
   - Thermal camera survey (identify bypass air)
2. Cooling infrastructure:
   - Add in-row cooling (для high density zones)
   - Deploy hot aisle containment
   - Upgrade CRAC/CRAH capacity
3. Design review:
   - Rack layout optimization
   - Power density limits per zone
   - Cooling strategy update
```

### Scenario 2: PUE Deterioration

**Symptoms**
- PUE increasing over months (e.g., 1.3 → 1.5)
- Cooling costs rising
- No significant IT load increase

**Investigation**
```
1. Data Collection (3-6 months trend):
   ☐ Total facility power (UPS input)
   ☐ IT power (PDU measurements)
   ☐ Cooling power (CRAC/CRAH, chiller, pumps)
   ☐ Outdoor temperature (weather correlation)
   ☐ IT utilization (server CPU, storage I/O)

2. Cooling System Analysis:
   ☐ Chiller efficiency degradation?
     - Refrigerant charge low (leaks)
     - Condenser fouling (cooling tower)
     - Compressor wear
   ☐ Economizer usage:
     - Operating properly?
     - Lockout set points correct?
     - Stuck в mechanical mode?
   ☐ Airflow management:
     - New hot spots (thermal mapping)
     - Containment breaches (missing panels)
     - Bypass air increase (wear на seals)

3. Power Distribution Losses:
   ☐ UPS efficiency:
     - Operating в efficient load range (40-80%)?
     - Battery age (older = lower efficiency)
     - Bypass mode usage (check logs)
   ☐ Transformer/PDU:
     - Loading balanced?
     - Harmonic distortion (poor power quality)

4. IT Efficiency:
   ☐ Server utilization:
     - Zombie servers (powered но underutilized)?
     - Idle VMs (consuming power for no work)
     - Old equipment (less efficient)
   ☐ Storage:
     - Disk spinning vs SSD (power difference)
     - Underutilized arrays
```

**Remediation Plan**
```
Cooling Optimization:
1. Chiller maintenance:
   - Refrigerant check/recharge
   - Condenser tube cleaning
   - Compressor health check
   → Expected: 5-15% efficiency improvement

2. Economizer optimization:
   - Verify set points (enable more hours)
   - Sensor calibration
   - Control logic review
   → Expected: 10-20% cooling energy reduction

3. Airflow management:
   - Blanking panel audit (install missing)
   - Re-seal containment (brush strips, gaskets)
   - Perforated tile optimization (CFD analysis)
   → Expected: 10-15% airflow improvement = fan energy reduction

Power Distribution:
1. UPS optimization:
   - Load balancing между modules
   - Battery health check (replace aging)
   - Eco-mode enable (если available, risk assessment)
   → Expected: 2-5% efficiency gain

IT Optimization:
1. Server consolidation:
   - Identify zombies (monitoring + decom)
   - VM rightsizing (reduce overprovisioning)
   - Old server retirement (refresh program)
   → Expected: 10-20% IT load reduction

Expected Total Impact:
- Current PUE: 1.50
- Post-optimization target: 1.30
- Cooling improvements: -10% total energy
- IT efficiency: -15% IT load
- Result: ~13% total energy reduction
- ROI: Payback typically 12-24 months
```

## Референсы

Detailed guides в `references/`:
- `tier-certification-requirements.md` - Uptime Institute Tier criteria
- `cooling-design-guide.md` - ASHRAE thermal guidelines и best practices
- `pue-measurement-standard.md` - Green Grid PUE measurement protocol
- `free-cooling-analysis.md` - Climate analysis для economizer planning

Templates и tools в `assets/`:
- `capacity-planning-calculator.xlsx` - Power/cooling capacity calculator
- `pue-tracking-dashboard.md` - PUE monitoring dashboard template
- `cooling-troubleshooting-flowchart.pdf` - Decision tree для thermal issues
- `preventive-maintenance-schedules.md` - PM schedules для facilities equipment
