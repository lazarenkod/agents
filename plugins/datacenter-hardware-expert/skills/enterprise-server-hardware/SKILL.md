---
name: enterprise-server-hardware
description: Знания о корпоративном серверном оборудовании и компонентах. Использовать когда требуется выбор оборудования, сравнение платформ или понимание характеристик enterprise hardware.
---

# Корпоративное серверное оборудование

## Когда использовать этот навык

- Выбор серверного оборудования для проектов
- Сравнение платформ и vendors
- Понимание спецификаций и характеристик
- Capacity planning и sizing
- RFP/RFQ подготовка для закупок

## Процессорные платформы

### Intel Xeon Scalable

**Поколения и кодовые имена**
```
Generation    Codename        Year    Process    Cores (max)
1st Gen       Skylake-SP      2017    14nm       28
2nd Gen       Cascade Lake    2019    14nm       28
3rd Gen       Ice Lake        2021    10nm       40
4th Gen       Sapphire Rapids 2023    Intel 7    60
5th Gen       Emerald Rapids  2024    Intel 7    64

Model naming:
Intel Xeon Platinum 8380
       │      │       │
       │      │       └─ SKU number (higher = more features)
       │      └───────── Tier (Bronze/Silver/Gold/Platinum)
       └──────────────── Brand

Tiers:
- Bronze: Entry-level (1-2 sockets, basic features)
- Silver: Mid-range (2-socket, moderate features)
- Gold: High-performance (2-4 sockets, advanced RAS features)
- Platinum: Premium (4-8 sockets, maximum features, highest core count)
```

**Key Features by Generation**
```
3rd Gen (Ice Lake):
+ PCIe Gen 4.0 (doubled bandwidth vs Gen 3)
+ Up to 6-channel DDR4-3200 memory
+ Intel SGX (Software Guard Extensions)
+ AVX-512 instructions
+ Up to 40 cores

Use cases:
- General enterprise compute
- Database servers (high memory bandwidth)
- Virtualization hosts
- AI inference (AVX-512 acceleration)

4th Gen (Sapphire Rapids):
+ PCIe Gen 5.0 (doubled bandwidth vs Gen 4)
+ DDR5 memory support (higher bandwidth, lower power)
+ Up to 60 cores (56 typical для general sku)
+ CXL (Compute Express Link) support
+ AMX (Advanced Matrix Extensions) для AI
+ Built-in accelerators: DSA, IAA, QAT

Use cases:
- AI training workloads (AMX)
- High-performance databases (DDR5 bandwidth)
- Network-intensive applications (DSA, IAA offload)
- Security-critical workloads (QAT для crypto)
```

**Model Selection Guide**
```
Workload Type          Recommended SKU    Rationale
─────────────────────────────────────────────────────────────
General purpose        Silver 4314        Good price/performance
Web servers           Silver 4316         Higher frequency
Database (OLTP)       Gold 6348           High frequency, large L3 cache
Database (OLAP)       Platinum 8360Y      Maximum cores for parallel queries
Virtualization        Gold 6338           Balanced cores/frequency, good TCO
HPC/Scientific        Platinum 8380       Maximum cores + AVX-512
AI Inference          Gold 6338N          AVX-512 + good freq
AI Training (4th Gen) Platinum 8480+      AMX accelerators
Storage controller    Silver 4309Y        Lower TDP, sufficient performance

Considerations:
- Frequency vs cores: OLTP = frequency, OLAP = cores
- Memory bandwidth: Channels × speed (6-channel DDR4-3200 = 192 GB/s)
- TDP: Higher TDP = more cooling required
- Licensing: Per-core software (Oracle) = prefer higher freq, fewer cores
```

### AMD EPYC

**Generations**
```
Generation    Codename    Year    Process    Cores (max)
1st Gen       Naples      2017    14nm       32
2nd Gen       Rome        2019    7nm        64
3rd Gen       Milan       2021    7nm        64
4th Gen       Genoa       2022    5nm        96
               Bergamo     2023    5nm        128 (cloud-optimized)

Model naming:
AMD EPYC 7763
      │   │││
      │   │└┴─ Generation (7=3rd Gen, 9=4th Gen)
      │   └─── Segment (4=value, 6=standard, 7=performance, 9=flagship)
      └─────── Socket (1=SP3/SP5 single socket, 7=dual socket)

Examples:
- EPYC 7443: 3rd Gen, dual-socket, standard segment, 24 cores
- EPYC 9654: 4th Gen, dual-socket, flagship, 96 cores
- EPYC 9754: 4th Gen, dual-socket (Bergamo), 128 cores
```

**EPYC Advantages**
```
1. Core count leadership:
   - Genoa: Up to 96 cores vs Sapphire Rapids 60 cores
   - Bergamo: 128 cores (cloud-optimized, lower freq)

2. Memory bandwidth:
   - 12-channel DDR5 (Genoa) vs 8-channel (Sapphire Rapids)
   - 460 GB/s vs 320 GB/s

3. PCIe lanes:
   - 128 lanes (Genoa) vs 80 lanes (Sapphire Rapids)
   - Critical для NVMe, GPU, high-speed networking

4. Cost-effectiveness:
   - Generally lower price per core
   - Better TCO для scale-out workloads

Disadvantages:
- Software ecosystem: Some ISV certifications slower than Intel
- Single-thread performance: Typically slightly lower frequency
- Enterprise features: Intel AMT, vPro (management) more mature
```

**When to Choose EPYC**
```
Ideal scenarios:
✓ Highly parallel workloads (many independent threads)
✓ Memory bandwidth critical (HPC, in-memory databases)
✓ Many PCIe devices (NVMe arrays, GPU clusters)
✓ Cloud/virtualization (high VM density)
✓ Cost-sensitive projects (better price/performance)

Consider Intel when:
- Maximum single-thread performance needed
- ISV certification requirements (Oracle, SAP, etc.)
- Advanced management features required (AMT, vPro)
- AI workloads (AMX на Sapphire Rapids)
```

### ARM Servers

**Ampere Altra / Altra Max**
```
Specs:
- Up to 128 cores (Altra Max)
- ARMv8.2+ architecture
- PCIe Gen 4.0
- 8-channel DDR4-3200

Characteristics:
+ Excellent power efficiency (~5W per core TDP)
+ Predictable performance (no SMT, 1 thread per core)
+ Good cost per core
+ Cloud-native workloads optimized
- Software ecosystem smaller (но growing)
- x86 compatibility через emulation only

Use cases:
- Cloud-native applications (containers, microservices)
- Web servers, CDN edge nodes
- CI/CD build farms
- Development environments
- Workloads где power efficiency critical
```

**AWS Graviton (ARM-based)**
```
Graviton3:
- 64 cores (ARMv8.4)
- DDR5 memory
- 25% better performance vs Graviton2
- 60% better energy efficiency

AWS instances:
- m7g: General purpose
- c7g: Compute optimized
- r7g: Memory optimized

Cost: 20% less expensive чем x86 equivalents

When to use:
✓ AWS-native deployments
✓ Containerized workloads
✓ Open-source software (Linux, Kubernetes, Docker)
✗ Legacy x86 binaries (need recompilation)
✗ Windows workloads (ARM64 Windows limited)
```

## Memory Technologies

### DDR4 vs DDR5

**DDR4 (Current mainstream)**
```
Specs:
- Speed: 2133-3200 MT/s (typical enterprise)
- Voltage: 1.2V
- Module capacity: Up to 256GB LRDIMM
- ECC: Standard на enterprise platforms

Configurations:
Intel Xeon 3rd Gen:
- 6 channels per socket
- Up to 3200 MT/s
- Max 6TB per socket (12 DIMMs × 512GB)

AMD EPYC 3rd Gen:
- 8 channels per socket
- Up to 3200 MT/s
- Max 4TB per socket (8 DIMMs × 512GB)

Memory Bandwidth Calculation:
Bandwidth = Channels × Speed × 8 bytes/transfer
6 channels × 3200 MT/s × 8 = 153.6 GB/s
```

**DDR5 (Next generation)**
```
Improvements:
+ Higher speeds: 4800-6400 MT/s (initial), scalable to 8000+
+ Lower voltage: 1.1V (vs 1.2V) = power savings
+ On-die ECC: Every module has basic ECC (still need registered ECC для enterprise)
+ Higher density: Up to 512GB DIMMs initially (roadmap to 2TB)
+ Dual 32-bit channels per DIMM (vs single 64-bit на DDR4)

Intel Sapphire Rapids:
- 8 channels per socket
- Up to 4800 MT/s
- Max 4TB per socket

AMD Genoa:
- 12 channels per socket
- Up to 4800 MT/s
- Max 6TB per socket (12 DIMMs × 512GB)

Memory Bandwidth:
12 channels × 4800 MT/s × 8 = 460 GB/s (AMD Genoa)
50% more bandwidth vs DDR4

Cost: ~20-30% premium vs DDR4 (decreasing)
```

**DIMM Types**
```
UDIMM (Unbuffered):
- Direct connection memory controller → DRAM chips
- Lower latency
- Limited capacity per channel
- Consumer/workstation use
- Not typical для enterprise servers

RDIMM (Registered):
- Register buffer between controller и DRAM
- Reduces electrical load на controller
- Enables more DIMMs per channel
- Slightly higher latency (+1-2ns)
- Most common enterprise DIMM
- Up to 64GB per DIMM (DDR4), 128GB (DDR5)

LRDIMM (Load Reduced):
- Memory buffer isolates DRAM chips
- Enables highest capacity (256GB DDR4, 512GB DDR5)
- Higher latency (+2-3ns vs RDIMM)
- Use для maximum memory capacity configs

NVDIMM (Non-Volatile):
- Battery-backed DRAM или persistent memory
- Data survives power loss
- Use cases: Database log buffers, caching tier
- Types: NVDIMM-N (DRAM + flash), NVDIMM-P (persistent memory)

Intel Optane PMem (Persistent Memory):
- Larger capacity than DRAM (128GB-512GB per module)
- Non-volatile (data persists)
- Lower cost per GB vs DRAM
- Higher latency vs DRAM (~300ns vs ~80ns)
- Use cases: Large in-memory databases, analytics
- Note: Discontinued (2022), existing deployments supported
```

**Memory Configuration Best Practices**
```
1. Populate all channels equally:
   ✓ Good: 6 DIMMs (1 per channel) или 12 DIMMs (2 per channel)
   ✗ Bad: 3 DIMMs (only half channels populated)
   Impact: Unbalanced = reduced bandwidth

2. Match DIMM sizes:
   ✓ Good: All 32GB DIMMs
   ✗ Bad: Mix 16GB и 32GB
   Impact: May limit interleaving

3. DIMM ranks:
   - Single rank (SR): 1 set of DRAM chips
   - Dual rank (DR): 2 sets
   - Quad rank (QR): 4 sets (LRDIMM)

   Higher rank = more capacity но lower max speed
   1DPC (DIMM per channel): Max speed (3200 MT/s)
   2DPC: Reduced speed (2933 MT/s typical)

4. Memory population order:
   Follow server manual (typically furthest slots first)
   Ensures optimal signal integrity

5. Monitor ECC errors:
   Correctable errors: >1 per hour = warning (replace soon)
   Uncorrectable errors: Any = critical (immediate replacement)
```

## Storage Technologies

### NVMe vs SATA/SAS

**Protocol Comparison**
```
                SATA            SAS             NVMe
────────────────────────────────────────────────────────────
Interface       SATA 3.0        SAS-3/4         PCIe 3.0/4.0/5.0
Max Speed       6 Gbps          12/24 Gbps      32/64/128 Gbps (x4 lanes)
Queue Depth     32              254             65,536
Queues          1               1               65,536
Latency         ~100μs          ~50μs           ~10μs
CPU Overhead    High            Medium          Low
Use Case        Low-perf        Enterprise      High-performance
```

**NVMe Advantages**
```
1. Parallelism:
   - 65,536 queues × 65,536 queue depth
   - Perfect для multi-core CPUs (no contention)

2. Latency:
   - Direct PCIe connection (no controller bottleneck)
   - ~10-20μs latency vs ~100μs SATA

3. Bandwidth:
   - PCIe Gen3 x4: ~3.5 GB/s per drive
   - PCIe Gen4 x4: ~7 GB/s per drive
   - PCIe Gen5 x4: ~14 GB/s per drive

4. CPU efficiency:
   - Lower CPU usage per IOP
   - Important для high-IOPS workloads

Deployment considerations:
- PCIe lanes (16 NVMe = 64 lanes)
- Cooling (NVMe generates heat, especially Gen4+)
- Form factors: U.2 (2.5"), M.2, EDSFF (E1.S, E3.S)
```

**SAS/SATA Use Cases (still relevant)**
```
Why still use SAS/SATA:
✓ Large capacity HDDs (20TB+) for archival/sequential
✓ Cost-effective storage pools ($/TB lower)
✓ Mature ecosystem (controllers, shelves, JBODs)
✓ Hot-swap support (easier serviceability)

Typical deployment:
- Boot: Small SATA SSD (480GB) в RAID 1
- OS/Apps: NVMe для performance
- Data: SAS SSD или HDD для capacity
- Archive: SATA HDD для cold storage
```

### Enterprise SSD Characteristics

**Endurance (DWPD - Drive Writes Per Day)**
```
Definition:
DWPD = (Drive capacity × writes per day × warranty years) / TBW

Example:
3.84TB SSD, 1 DWPD, 5-year warranty:
TBW = 3.84 × 1 × 365 × 5 = 7,008 TBW

Endurance tiers:
Read-Intensive (RI): 0.3-1 DWPD
  Use: Read-mostly (databases, web content, VDI)
  Cost: $$$

Mixed-Use (MU): 1-3 DWPD
  Use: Balanced read/write (general applications, virtualization)
  Cost: $$$$

Write-Intensive (WI): 3-10+ DWPD
  Use: Write-heavy (logging, caching, analytics ingestion)
  Cost: $$$$$

Selection:
- Overbuying endurance wastes money
- Underbuying = premature failure, warranty void
- Monitor write amplification factor (WAF) in production
```

**Performance Consistency**
```
Consumer SSD:
- High peak performance (marketing numbers)
- Performance cliff при sustained writes (SLC cache exhausted)
- Garbage collection pauses (unpredictable latency)

Enterprise SSD:
- Consistent performance (99th percentile matters)
- Sustained write performance (no cliff)
- Power loss protection (capacitors ensure data integrity)
- Advanced wear leveling (even wear across cells)

Key metrics:
- Steady-state performance (after SLC cache full)
- 99.9th percentile latency (tail latency)
- Quality of Service (QoS) guarantees
```

**NVMe over Fabrics (NVMe-oF)**
```
Protocols:
- NVMe/FC: NVMe over Fibre Channel
- NVMe/TCP: NVMe over Ethernet (most accessible)
- NVMe/RoCE: NVMe over RDMA Ethernet (lowest latency)

Benefits:
+ Shared NVMe storage (vs local-only)
+ Low latency (~100-200μs network + storage)
+ High bandwidth (match storage capability)
+ Standard Ethernet infrastructure (NVMe/TCP)

Use cases:
- Shared storage для virtualization (vSAN, NVMe datastores)
- Database clusters (RAC, distributed DBs)
- Kubernetes persistent volumes (high-performance)
```

## Server Form Factors

### Rack Servers

**1U Servers**
```
Characteristics:
- Height: 1.75" (44.45mm)
- Depth: Standard 24-30" (610-762mm)
- Max power: ~500-800W (cooling limits)

Typical specs:
- 1-2 sockets
- 16-32 cores per socket
- 16-24 DIMM slots
- 4-10 × 2.5" drive bays
- 2-4 PCIe slots (low-profile)

Use cases:
- Web servers (high density, moderate compute)
- Edge computing (limited rack space)
- Caching layers (many nodes, moderate resources each)

Limitations:
- Limited expansion (PCIe slots, drives)
- Cooling constraints (high fan noise)
- Difficult serviceability (crowded)

Examples:
- Dell PowerEdge R650: 2-socket, 24 DIMM, 10 × 2.5" NVMe
- HPE ProLiant DL360 Gen11: 2-socket, 32 DIMM, 10 × 2.5"
```

**2U Servers**
```
Characteristics:
- Height: 3.5" (88.9mm)
- More cooling airflow vs 1U
- Max power: ~1,200-1,600W

Typical specs:
- 1-2 sockets
- 24-32 DIMM slots
- 8-24 × 2.5" или 12 × 3.5" drive bays
- 4-8 PCIe slots (full-height)
- Up to 4 GPUs (low-profile или half-length)

Use cases:
- General-purpose compute (most popular form factor)
- Database servers (more memory, storage than 1U)
- Virtualization hosts (balanced resources)
- Storage servers (24-bay configurations)

Examples:
- Dell PowerEdge R750: 2-socket, 32 DIMM, 16 × 2.5" NVMe
- HPE ProLiant DL380 Gen11: 2-socket, 32 DIMM, 24 × 2.5"
```

**4U Servers**
```
Characteristics:
- Height: 7" (177.8mm)
- Maximum expansion capacity
- Max power: ~2,000-3,000W

Typical specs:
- 2-4 sockets (high-end models)
- 48+ DIMM slots
- 24-60 × 3.5" drive bays (storage configs)
- 8+ GPUs (full-height, full-length)
- 10-16 PCIe slots

Use cases:
- Storage servers (60-bay для high capacity)
- GPU compute (AI training, 8× A100/H100)
- Mission-critical applications (4-socket, maximum redundancy)
- Scale-up databases (massive memory configs)

Examples:
- Dell PowerEdge R750xa: GPU-optimized, 4 double-width GPUs
- HPE ProLiant DL580 Gen11: 4-socket, 96 DIMM, 48 cores per socket
```

### Blade Systems

**Architecture**
```
Components:
- Blade chassis (enclosure): 6U-10U rack mount
- Blade servers (half-width или full-width)
- Shared infrastructure:
  * Power supplies (N+1 redundant)
  * Network switches (fabric modules)
  * Management module
  * Cooling (shared fans)

Blade capacity:
Half-width: 16 blades per chassis
Full-width: 8 blades per chassis

Examples:
- Dell PowerEdge MX: 7U chassis, 8 full-width или 16 half-width blades
- HPE Synergy: 10U chassis, 12 compute modules
- Cisco UCS: 6U chassis, 8 blades
```

**Advantages**
```
+ High density: More compute per rack unit
+ Shared infrastructure: Fewer power supplies, fans, switches
+ Simplified cabling: Fabric connections в chassis, not per blade
+ Hot-swap blades: Replace без shutdown chassis
+ Integrated management: Single interface для all blades
+ Energy efficiency: Shared power/cooling more efficient

Challenges:
- High initial cost (chassis + blades)
- Vendor lock-in (blades proprietary to chassis)
- All eggs в one basket (chassis failure = many blades)
- Limited per-blade expansion (no PCIe slots typically)
```

**When to Use Blades**
```
Ideal for:
✓ Large deployments (>50 servers)
✓ Standardized workloads (virtualization, web farms)
✓ Data center с space constraints
✓ Simplified operations (single management plane)

Consider rack servers when:
- Small deployments (<50 servers)
- Diverse workloads (GPU, storage, compute mix)
- Vendor flexibility important
- Lower upfront cost preferred
```

## Референсы

Detailed specifications в `references/`:
- `cpu-selection-guide.md` - Comprehensive CPU comparison и selection criteria
- `memory-configuration-best-practices.md` - DIMM population rules и optimization
- `storage-technology-comparison.md` - SSD/HDD technologies и use cases
- `server-vendor-comparison.md` - Dell vs HPE vs Lenovo vs Cisco vs Supermicro

Sizing tools в `assets/`:
- `server-sizing-calculator.xlsx` - Workload-based server sizing
- `memory-bandwidth-calculator.md` - Memory bandwidth calculation
- `storage-capacity-planner.xlsx` - Storage capacity и performance planning
- `tco-analysis-template.xlsx` - 5-year TCO comparison
