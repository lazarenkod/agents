---
name: monitoring-alerting-systems
description: Системы мониторинга и алертинга для серверной инфраструктуры. Использовать когда требуется настройка мониторинга, определение метрик и порогов или troubleshooting систем мониторинга.
---

# Системы мониторинга и алертинга

## Когда использовать этот навык

- Проектирование архитектуры мониторинга
- Настройка алертов и определение порогов
- Выбор инструментов мониторинга
- Troubleshooting gaps в visibility
- Оптимизация алертов (reducing noise, avoiding alert fatigue)

## Принципы эффективного мониторинга

### Four Golden Signals (Google SRE)

**1. Latency**
```
Определение:
- Время обработки request (response time)
- Важно различать successful vs failed requests
- Failed requests могут быть fast (immediate rejection)

Метрики:
- Average latency: Грубая оценка, скрывает outliers
- Percentiles: p50, p95, p99, p99.9
  * p50 (median): 50% requests faster
  * p99: 99% requests faster (1 из 100 slower)
  * p99.9: 999 из 1000 faster (tail latency)

Thresholds (web application example):
p50 latency:  <100ms   Excellent
p95 latency:  <500ms   Good
p99 latency:  <1s      Acceptable
p99.9 latency: <5s     Critical threshold

Why percentiles > average:
- Average hides outliers (bad user experience)
- 1% slow requests = poor UX для 1% users
```

**2. Traffic**
```
Определение:
- Demand на service (requests per second)
- Different metrics для different services:
  * Web: HTTP requests/sec
  * Database: Queries/sec, connections
  * Storage: IOPS, throughput (MB/s)
  * Network: Packets/sec, bandwidth

Мониторинг:
- Baseline: Normal traffic patterns (daily/weekly cycles)
- Growth trends: Month-over-month capacity planning
- Anomalies: Sudden spikes (DDoS?) или drops (outage?)

Capacity planning:
- Current peak: 10,000 req/s
- Growth rate: +20% per quarter
- Plan capacity: 15,000 req/s (50% headroom)
- Timeline: Upgrade when approaching 13,000 req/s (alert threshold)
```

**3. Errors**
```
Определение:
- Rate of failed requests (explicit или implicit)
- Explicit: HTTP 5xx, database errors, exceptions
- Implicit: HTTP 200 но wrong content, timeouts

Метрики:
- Error rate: Errors/sec
- Error ratio: (Errors / Total requests) × 100%

Thresholds:
Error ratio <0.1%: Good (typical для healthy service)
Error ratio 0.1-1%: Warning (investigate)
Error ratio >1%: Critical (user impact significant)

Error types:
- Transient: Retry успешен (network blips)
- Permanent: Retry fails (application bugs, data corruption)
- Cascading: Upstream failure propagates

Correlation:
- Traffic spike + error spike = capacity limit
- No traffic change + error spike = application issue
```

**4. Saturation**
```
Определение:
- How "full" the service is (resource utilization)
- Leading indicator of performance degradation

Resources to monitor:
- CPU utilization: >80% sustained = saturation risk
- Memory utilization: >90% = risk of OOM
- Disk space: >85% = critical (filesystem behavior changes)
- Network bandwidth: >80% = packet loss risk
- Queue depths: Storage queues, network buffers

Proactive thresholds:
Warning (80%): Plan capacity addition
Critical (90%): Immediate action needed
Emergency (95%): Add capacity NOW

Why 80% not 100%:
- Headroom для burst traffic
- Performance degradation начинается before 100%
- Time для capacity planning и procurement
```

## Мониторинг hardware health

### Server Component Monitoring

**Через IPMI/Redfish**
```
Key sensors:
1. Temperature sensors:
   - CPU temperature (per socket)
   - Memory temperature (per channel)
   - Disk temperatures
   - Ambient (inlet air)
   - Exhaust (outlet air)

   Thresholds:
   Component    Warning   Critical   Shutdown
   CPU          75°C      85°C       95°C
   Memory       75°C      85°C       90°C
   HDD          40°C      50°C       60°C
   SSD          60°C      70°C       80°C
   Ambient      27°C      32°C       35°C

2. Fan speeds:
   - RPM reading (each fan)
   - % of maximum speed
   - Status (OK/Warning/Failed)

   Alerts:
   - Any fan <50% max speed: Warning (bearing wear)
   - Any fan failed: Critical (redundancy lost)

3. Voltage rails:
   - 12V, 5V, 3.3V, 1.8V, 1.2V, etc.
   - Tolerance: Typically ±5-10%

   Example 12V rail:
   Normal range: 11.4V - 12.6V
   Warning: <11.4V или >12.6V
   Critical: <11.0V или >13.0V

4. Power consumption:
   - Watts consumed (per PSU или total)
   - Amperage draw
   - PSU efficiency (output/input)

   Metrics:
   - Current draw vs rated capacity
   - Trend analysis (increasing = hardware degradation?)
   - Efficiency (should be 90-95% для 80 Plus Platinum/Titanium)

5. Intrusion detection:
   - Chassis intrusion sensor
   - Physical tampering detection
   - Log all events для security audit
```

**SMART Monitoring (Storage)**
```
Critical attributes to monitor:

ID   Attribute                 Type      Threshold   Action
─────────────────────────────────────────────────────────────
5    Reallocated_Sector_Ct    Raw value >0          Warning, >10 replace
10   Spin_Retry_Count         Raw value >0          Critical, replace
184  End-to-End_Error         Raw value >0          Critical, replace
187  Reported_Uncorrect       Raw value >0          Critical, replace
188  Command_Timeout          Raw value >100        Check cables/controller
196  Reallocated_Event_Count  Raw value >0          Warning, >5 replace
197  Current_Pending_Sector   Raw value >0          Critical if persistent
198  Offline_Uncorrectable    Raw value >0          Critical, replace
199  UDMA_CRC_Error_Count     Raw value >50         Cable/connector issue

HDD specific:
C5   Current_Pending_Sector   Raw value >5          Replace (sectors failing)
C6   Uncorrectable_Sector_Ct  Raw value >0          Critical

SSD specific (NVMe):
- Media Errors: >0 = concerning
- Percentage Used: >80% = plan replacement
- Available Spare: <10% = critical
- Critical Warning bits: Any set = investigate

Polling frequency:
- Production systems: Every hour (automated)
- Critical systems: Every 15 minutes
- Pre-failure detection: Daily trend analysis
```

**ECC Memory Monitoring**
```
Tools:
- Linux: edac-util, rasdaemon
- Windows: Event Viewer (System log), WMI queries
- IPMI: SEL (System Event Log)

Correctable Errors (CE):
Thresholds:
<1 per hour per DIMM:    Normal (single-bit errors, ECC correcting)
1-10 per hour:           Warning (DIMM degrading, monitor closely)
>10 per hour:            Critical (replace within 1 week)
>100 per hour:           Emergency (replace immediately, risk UE)

Uncorrectable Errors (UE):
ANY UE = Critical:
- Immediate impact: Kernel panic, application crash, data corruption
- Action: Replace DIMM immediately (identify via MCE logs)
- RCA: Why did DIMM reach UE state? (missed CE trend?)

Logging:
```bash
# Linux - Check EDAC errors
edac-util -v

# View error history
edac-util -rfull

# Continuous monitoring
watch -n 60 'edac-util -v'

# Detailed MCE logs
mcelog --client

# Decode MCE для DIMM location
mcelog --dmi --decode-dimms
```

Prevention:
- Trend analysis: Graph CE count per DIMM weekly
- Proactive replacement: Rising CE trend (even if below threshold)
- Environmental check: Multiple DIMMs elevated CE = thermal issue?
```

## Метрики производительности

### System-level Metrics

**CPU Metrics**
```
1. CPU Utilization (%):
   - User: Application code execution
   - System: Kernel/OS overhead
   - IOWait: Waiting для I/O completion (not CPU bound!)
   - Idle: Unused capacity

   Thresholds:
   <70%: Healthy (headroom для spikes)
   70-85%: Warning (plan capacity)
   >85%: Critical (performance impact, user-visible latency)

   Important:
   - High IOWait = storage bottleneck (not CPU issue)
   - System% high = kernel bottleneck (networking, context switches)

2. Load Average:
   - 1-minute: Immediate load
   - 5-minute: Short-term trend
   - 15-minute: Long-term trend

   Interpretation:
   Load avg / # cores:
   <0.7: Healthy (CPUs keeping up)
   0.7-1.0: Busy но managing
   >1.0: Saturation (tasks queuing)
   >1.5: Overloaded (significant delays)

   Example: 16-core system
   Load avg 8.0: 8/16 = 0.5 (OK)
   Load avg 20.0: 20/16 = 1.25 (overloaded)

3. Context Switches:
   - Voluntary: Process yields CPU (waiting I/O)
   - Involuntary: Scheduler preempts (time slice expired)

   High involuntary CS/s = CPU contention (more processes than cores)

4. Run Queue Length:
   - Number of processes ready to run, waiting для CPU
   - Should be near 0 (all processes getting CPU quickly)
   - Persistent >0 = CPU saturation
```

**Memory Metrics**
```
1. Memory Utilization (%):
   Total = Used + Buffers/Cache + Free

   Linux memory reality:
   - "Used" memory includes buffers/cache (reclaimable)
   - Actual free = Free + Buffers/Cache
   - Threshold на actual free, not "used"

   Thresholds:
   Free memory <10%: Warning (risk of swapping)
   Free memory <5%: Critical (swapping likely)

2. Swap Usage:
   - Swap used: Amount of swap space active
   - Swap in/out rate: Pages swapped per second

   Thresholds:
   Swap used >0: Warning (memory pressure occurred)
   Swap in/out >10 pages/s: Critical (active swapping, performance impact)

   Best practice: Minimal swap (1-2GB) для emergency, avoid usage

3. Page Faults:
   - Minor: Page в memory, no disk access
   - Major: Page must be read from disk (slow!)

   High major page fault rate = swapping активен = add memory

4. OOM (Out of Memory) Events:
   - Kernel kills processes to reclaim memory
   - ANY OOM event = Critical (data loss, application failure)
   - Prevent via proper sizing и monitoring
```

**Storage Metrics**
```
1. IOPS (I/O Operations Per Second):
   - Read IOPS, Write IOPS
   - Total IOPS = Reads + Writes

   Capacity (examples):
   7200 RPM HDD: ~100 IOPS
   15K RPM HDD: ~200 IOPS
   SATA SSD: ~50,000 IOPS
   NVMe SSD: ~500,000 IOPS

   Monitoring: Current IOPS vs drive capability
   Alert: >80% capacity (plan upgrade)

2. Throughput (MB/s):
   - Sequential read/write performance
   - Different from IOPS (large block vs small block)

   Capacity:
   SATA 6Gbps: ~550 MB/s
   SAS 12Gbps: ~1,200 MB/s
   NVMe PCIe Gen3 x4: ~3,500 MB/s
   NVMe PCIe Gen4 x4: ~7,000 MB/s

3. Latency (ms):
   - Time from request to completion
   - Most critical for user-facing applications

   Thresholds:
   <5ms: Excellent (NVMe/all-flash)
   5-10ms: Good (fast SSD/hybrid)
   10-20ms: Acceptable (general workloads)
   >20ms: Warning (investigate)
   >50ms: Critical (user-visible impact)

4. Queue Depth:
   - Outstanding I/O requests
   - Sustained high queue = saturation

   Ideal: Queue depth 1-4 (requests processed quickly)
   Warning: Queue depth >32 sustained (backlog forming)

5. Disk Busy %:
   - % of time disk servicing requests
   - >80% sustained = approaching saturation
   - >95% = saturated (latency increasing)
```

**Network Metrics**
```
1. Throughput (Mbps/Gbps):
   - Inbound (RX) и outbound (TX) bandwidth
   - Peak и average utilization

   Capacity:
   1GbE: ~950 Mbps actual (after overhead)
   10GbE: ~9.5 Gbps actual
   25GbE: ~24 Gbps actual

   Thresholds:
   <70% utilization: Healthy
   70-85%: Warning (plan upgrade)
   >85%: Critical (packet loss risk)

2. Packets Per Second (pps):
   - Critical для firewall, router, load balancer
   - Small packet workloads (IoT, VoIP) = high pps, low bandwidth

   Example:
   64-byte packets at 1Gbps ≈ 1.48M pps
   1500-byte packets at 1Gbps ≈ 81K pps

3. Errors и Drops:
   - RX errors: Incoming packet errors (CRC, frame errors)
   - TX errors: Outgoing packet errors
   - Drops: Buffer overflow (too much traffic)

   Thresholds:
   Error rate <0.01%: Normal
   Error rate >0.1%: Investigate (cable, transceiver, switch port)
   Any drops: Indicates saturation или misconfiguration

4. Retransmits (TCP):
   - Retransmitted segments / Total segments
   - >1% retransmit rate = network quality issue

5. Connection Tracking:
   - Active connections
   - Connection rate (new connections/sec)

   Monitor limits:
   Linux conntrack table: Default 65,536 entries
   Firewall connection table: Varies (check device specs)
```

## Мониторинг виртуализации

### vSphere-Specific Metrics

**Host Metrics**
```
1. CPU:
   - Usage (%): Overall host CPU utilization
   - Ready Time (ms): VMs waiting для CPU (see virtualization-troubleshooting skill)
   - Co-Stop (ms): Multi-vCPU co-scheduling delays

   Thresholds:
   Usage <80%, Ready <5%: Healthy
   Usage >80% или Ready >5%: Warning (load balance needed)
   Usage >90% или Ready >10%: Critical (performance impact)

2. Memory:
   - Usage (%): Active memory used by VMs
   - Ballooning (MB): Memory reclaimed via balloon driver
   - Swapping (MB): Hypervisor swapping (worst case)
   - Compressed (MB): Memory compression active

   Thresholds:
   Usage <90%, no swapping: Healthy
   Ballooning active: Warning (memory pressure)
   Any swapping: Critical (major performance impact)

3. Storage:
   - Latency per datastore (GAVG, KAVG, DAVG)
   - IOPS per datastore
   - Outstanding I/O (queue depth)

   See virtualization-troubleshooting skill для detailed analysis

4. Network:
   - Throughput per vSwitch/dvSwitch
   - Dropped packets (%DRPTX, %DRPRX)
   - Network utilization per uplink
```

**VM Metrics**
```
1. CPU:
   - Usage (%): CPU consumed by VM
   - Ready Time (%): Time waiting для CPU scheduling
   - vCPU count: Number of virtual CPUs

   Rightsizing:
   - CPU usage <50% sustained AND ready <1%: Consider reducing vCPUs
   - CPU usage >80% sustained OR ready >5%: Consider adding vCPUs или DRS

2. Memory:
   - Active: Memory actively used by guest OS
   - Consumed: Total memory allocated to VM
   - Granted: Host memory allocated to VM
   - Ballooned: Memory reclaimed by balloon driver

   Rightsizing:
   - Active << Consumed (e.g., 4GB active, 32GB consumed): Overallocated, reduce
   - Active ≈ Consumed: Well-sized
   - Ballooning >0: Host memory pressure (add host memory или migrate VM)

3. Storage:
   - Latency: VM-experienced storage latency
   - IOPS: VM-generated I/O operations
   - Throughput: VM-generated MB/s

4. Network:
   - Throughput: VM network bandwidth usage
   - Drops: Packet drops (guest unable to keep up)
```

### Kubernetes Metrics

**Node Metrics**
```
1. Resource Allocatable:
   - CPU: Total - (System reserved + Kubelet reserved)
   - Memory: Total - (System + Kubelet + Eviction threshold)

   Example:
   16-core node, 2 cores system/kubelet = 14 allocatable cores

2. Resource Utilization:
   - % of allocatable capacity used by pods
   - % of actual resource consumption (vs requests)

   Thresholds:
   Allocated <80%: Healthy (headroom для scheduling)
   Allocated >80%: Warning (limited scheduling capacity)
   Allocated >90%: Critical (risk of pod evictions)

3. Pressure Indicators:
   - MemoryPressure: Node running low на memory
   - DiskPressure: Disk space или inodes exhausted
   - PIDPressure: Too many processes

   Any pressure = Critical (pods may be evicted)
```

**Pod Metrics**
```
1. Resource Requests vs Limits:
   - Requests: Guaranteed resources (scheduling decision)
   - Limits: Maximum allowed (throttling/OOM if exceeded)

   Best practice:
   - Requests = Realistic usage (profiled)
   - Limits = Peak + headroom (prevent noisy neighbor)

2. Resource Utilization:
   - CPU usage vs request/limit
   - Memory usage vs request/limit

   Rightsizing:
   - Usage << Request: Overprovisioned (wasteful)
   - Usage ≈ Limit frequently: Throttling risk (increase limit)
   - Memory usage > Limit: OOMKilled (increase limit)

3. Pod Status:
   - Running: Healthy
   - Pending: Cannot be scheduled (resource constraints?)
   - CrashLoopBackOff: Container repeatedly crashing
   - ImagePullBackOff: Cannot pull container image

   Alert на non-Running states (immediate investigation)
```

## Мониторинг инструменты

### Open Source Solutions

**Prometheus + Grafana**
```
Architecture:
Prometheus (metrics collection & storage):
- Pull model: Scrapes /metrics endpoints
- Time-series database
- PromQL query language
- Alerting rules

Grafana (visualization):
- Dashboards from Prometheus data
- Templates и community dashboards
- Multi-datasource support

Strengths:
+ Native Kubernetes integration (service discovery)
+ Huge community (exporters для everything)
+ Powerful query language (PromQL)
+ Free и open source

Limitations:
- Long-term storage (default 15-day retention, need Thanos/Cortex для more)
- Scalability (single Prometheus instance limits)
- No built-in log aggregation (need separate ELK/Loki)

Best for:
- Cloud-native applications (containers, Kubernetes)
- DevOps teams (infrastructure as code)
- Microservices architectures
```

**Zabbix**
```
Architecture:
- Zabbix Server (central collection & processing)
- Zabbix Agents (installed на monitored hosts)
- Zabbix Proxy (для distributed monitoring)
- Web UI (configuration & visualization)

Strengths:
+ Comprehensive monitoring (servers, network, applications)
+ Mature (20+ years development)
+ Auto-discovery (network devices, VMs)
+ Templates для 1000s of devices/applications
+ Free и open source

Limitations:
- Older UI/UX (не as modern as Grafana)
- Steeper learning curve
- Scalability requires careful tuning

Best for:
- Traditional infrastructure (servers, network gear)
- Enterprises (mature, proven)
- Heterogeneous environments (mix of vendors/tech)
```

**ELK Stack (Elasticsearch, Logstash, Kibana)**
```
Architecture:
- Logstash/Beats: Log collection
- Elasticsearch: Storage & search
- Kibana: Visualization & dashboards

Strengths:
+ Powerful log aggregation & search
+ Real-time analysis
+ Machine learning anomaly detection (X-Pack)
+ Scalable (horizontal scaling)

Limitations:
- Resource intensive (Elasticsearch RAM requirements)
- Complexity (requires tuning для production)
- Licensing (X-Pack features require license)

Best for:
- Log aggregation & analysis
- Security (SIEM use cases)
- Application troubleshooting (log correlation)
```

### Commercial Solutions

**Datadog**
```
Model:
- SaaS (hosted)
- Agent-based collection
- Per-host pricing

Strengths:
+ Unified monitoring (infrastructure, apps, logs, APM)
+ Easy setup (cloud integrations)
+ Advanced features (AI/ML anomaly detection, forecasting)
+ Excellent mobile app

Cost:
- Pro: $15/host/month (infrastructure monitoring)
- Enterprise: $23/host/month (advanced features)
- APM, logs, synthetics: Additional costs

Best for:
- Cloud-first organizations
- Rapid deployment (no infrastructure to manage)
- Comprehensive visibility (all-in-one)
```

**New Relic**
```
Model:
- SaaS (hosted)
- Agent-based collection
- Usage-based pricing (GB ingested)

Strengths:
+ APM (Application Performance Monitoring) leader
+ Full-stack observability
+ Distributed tracing
+ AI-driven insights

Cost:
- Standard: $0.30/GB ingested data
- Pro: $0.50/GB + advanced features
- Enterprise: Custom pricing

Best for:
- Application-centric monitoring
- Developer teams (code-level visibility)
- Microservices troubleshooting
```

### Выбор платформы

**Критерии выбора**
```
1. Environment type:
   - Cloud-native (Kubernetes): Prometheus + Grafana
   - Traditional (VMs, физические): Zabbix, PRTG
   - Hybrid: Datadog, New Relic
   - Security-focused: Splunk, ELK

2. Scale:
   - Small (<50 hosts): Zabbix, Nagios
   - Medium (50-500 hosts): Prometheus, commercial SaaS
   - Large (>500 hosts): Enterprise monitoring, federated Prometheus

3. Budget:
   - Open source: Prometheus, Zabbix, ELK
   - Commercial: Evaluate ROI (ops time saved vs cost)

4. Team expertise:
   - Strong internal skills: Open source (lower cost, more control)
   - Limited resources: SaaS (outsource infrastructure management)

5. Compliance:
   - Data residency requirements: On-premise or specific cloud regions
   - Audit logs: Enterprise features (RBAC, audit trails)
```

## Алертинг best practices

### Alert Design Principles

**Actionable Alerts**
```
Rule: Every alert must have clear action

Good alert:
Title: "Production database CPU >90% для 10 minutes"
Action: 1) Check slow queries (pt-query-digest)
        2) Scale vertically (add CPU) или horizontally (read replicas)
        3) Optimize queries или cache layer
Escalation: Page DBA если >15 minutes, database team lead если >30 minutes

Bad alert:
Title: "Server CPU high"
Action: ??? (what's high? which server? what to do?)
```

**Meaningful Thresholds**
```
Avoid:
- Arbitrary thresholds (e.g., "CPU >50%" without context)
- Static thresholds ignoring patterns (diurnal load cycles)

Use:
- Baseline + deviation (e.g., "CPU >20% above 7-day average")
- Business-impact thresholds (e.g., "Latency causing <99% SLA")
- Leading indicators (e.g., "Disk 85% full" before "Disk full" outage)
```

**Reducing Alert Fatigue**
```
Problem: Too many alerts = ignored alerts = missed critical issues

Solutions:
1. Severity levels:
   - Critical/P1: Immediate page (user-facing impact NOW)
   - Warning/P2: Ticket (investigate within business hours)
   - Info/P3: Log only (FYI, no action needed)

2. Aggregation:
   - BAD: Alert per disk (10 disks = 10 alerts)
   - GOOD: Single alert "Multiple disks >85% full" (list affected)

3. Intelligent routing:
   - Critical database alert → DBA on-call
   - Network alert → NetOps team
   - Application error → Dev team
   (Not everything to everyone)

4. Time-based:
   - Maintenance windows: Suppress alerts during planned work
   - Business hours: Different thresholds (higher tolerance off-hours)

5. Correlation:
   - Root cause: Alert на primary failure, suppress cascading alerts
   - Example: Switch down → suppress all server "network unreachable" alerts
```

**Alert Escalation**
```
Tier 1 (Immediate response):
- User-facing outage (service down)
- Data loss risk (disk full, backup failing)
- Security incident (intrusion detected)
→ Page on-call immediately (phone call)

Tier 2 (Business hours response):
- Performance degradation (latency high но not critical)
- Capacity warnings (disk 85%, memory 80%)
- Non-critical service failures (monitoring agent down)
→ Create ticket, assign to team

Tier 3 (Informational):
- Trends (gradual capacity growth)
- Resolved issues (automatic recovery)
- Maintenance events
→ Email digest, no immediate action
```

## Референсы

Best practices guides в `references/`:
- `sre-monitoring-principles.md` - Google SRE monitoring philosophy
- `alert-threshold-tuning.md` - Методология определения порогов алертинга
- `prometheus-best-practices.md` - Production-ready Prometheus setup
- `monitoring-tool-comparison.md` - Detailed comparison матрица

Dashboards и templates в `assets/`:
- `grafana-infrastructure-dashboard.json` - Comprehensive infrastructure dashboard
- `prometheus-recording-rules.yml` - Pre-aggregated metrics для performance
- `alert-runbook-template.md` - Runbook template для alert response
- `capacity-planning-report.xlsx` - Resource trend analysis и forecasting
