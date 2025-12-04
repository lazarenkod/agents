---
name: virtualization-troubleshooting
description: Устранение проблем виртуализационных платформ и гипервизоров. Использовать когда требуется troubleshooting VM performance, анализ проблем гипервизора или оптимизация виртуальной инфраструктуры.
---

# Troubleshooting виртуализации

## Когда использовать этот навык

- Диагностика проблем производительности VM
- Расследование критических ошибок гипервизора (PSOD, kernel panic)
- Оптимизация ресурсов виртуализации
- Troubleshooting storage latency и network issues в виртуальной инфраструктуре
- Анализ проблем live migration и HA

## Ключевые метрики производительности

### CPU Metrics

**CPU Ready Time**
```
Определение:
- Время ожидания VM для получения CPU ресурсов
- VM готова работать, но hypervisor не может предоставить физические cores

Измерение:
- vSphere: esxtop, vCenter performance charts
- Значение: ms per 20-second sampling interval
- Percentage: (Ready Time / 20000ms) × 100%

Thresholds:
Good:      <5% (<1000ms per 20s)      Excellent performance
Warning:   5-10% (1000-2000ms)       Starting to impact
Critical:  >10% (>2000ms)             Significant degradation
Severe:    >20% (>4000ms)             Major performance issue

Causes:
1. CPU overcommitment:
   - Too many vCPUs allocated vs physical cores
   - Ratio >4:1 (vCPU:pCore) risky для latency-sensitive

2. Multi-vCPU co-scheduling:
   - VM с 8 vCPUs needs 8 physical cores simultaneously
   - Harder to schedule than smaller VMs
   - Unnecessary vCPUs exacerbate problem

3. CPU limits/reservations:
   - Artificial constraints causing ready time
   - Resource pool misconfiguration

4. Host CPU saturation:
   - Overall host CPU >80% sustained
   - DRS не балансирует (disabled или misconfigured)

Resolution:
✓ Rightsize VMs (reduce unnecessary vCPUs)
  - Most apps don't scale beyond 4-8 vCPUs
  - Test performance с fewer vCPUs

✓ Load balancing:
  - Enable DRS (Distributed Resource Scheduler)
  - Set агрессивный threshold (если conservative)
  - Manual vMotion overloaded hosts

✓ NUMA optimization:
  - VM vCPU count <= NUMA node size
  - Avoid wide VMs (many sockets)

✓ CPU reservations:
  - Reserve CPU для critical VMs only
  - Remove unnecessary limits
```

**CPU Co-Stop**
```
Определение:
- Multi-vCPU VM: время waiting для co-scheduling всех vCPUs
- Specific problem для VMs >4 vCPUs

Impact:
- Даже low % Co-Stop = significant performance hit
- >3% Co-Stop: Consider reducing vCPUs

Resolution:
- Primary fix: Reduce vCPU count
- vSphere 6.5+: Relaxed co-scheduling (automatic)
- CPU affinity (extreme cases, limits vMotion)
```

**CPU Wait**
```
Types:
- CPU Wait-IO: Waiting для I/O completion
- CPU Wait-Network: Waiting для network operations

High Wait-IO:
→ Indicates storage bottleneck, not CPU issue
→ Investigate storage latency (see Storage section)

High Wait-Network:
→ Network saturation или configuration problem
→ Check network throughput, drops, errors
```

### Memory Metrics

**Memory Ballooning**
```
VMware Balloon Driver (vmmemctl):

States:
0%      Ideal        No memory pressure
<30%    Good         Slight pressure, normal
30-65%  Warning      Increasing pressure, monitor
>65%    Critical     Significant pressure, performance impact

How it works:
1. ESXi host под memory pressure
2. Balloon driver inflates в guest OS
3. Guest OS thinks память используется app
4. Guest OS pages out to swap (inside guest)
5. ESXi reclaims "ballooned" pages

Когда происходит:
- Host memory >94% used (soft threshold)
- No free memory для allocations
- Before swapping (better than hypervisor swap)

Resolution:
Immediate:
- Add host memory (hardware upgrade)
- vMotion VMs to less loaded hosts
- Reduce VM memory allocations (если overprovisioned)

Long-term:
- Memory reservations для critical VMs
- DRS memory load balancing
- Capacity planning (add hosts)

Check ballooning:
```bash
# vSphere
esxtop -> 'm' (memory view)
Look for: MCTLSZ (balloon size), SWCUR (swap size)

# Inside guest
# Linux
vmware-toolbox-cmd stat balloon
# Windows
Check VMware Tools memory balloon counter
```
```

**Memory Swapping**
```
Hypervisor Swapping (worst case):

Levels:
SWR/s   Impact
<1      Minimal      Occasional swap activity
1-10    Warning      Starting to swap, slows VMs
>10     Critical     Heavy swapping, major performance loss

Why it's bad:
- Hypervisor swaps to disk (не видимо guest OS)
- VM не знает pages swapped → random access patterns
- Latency: Memory access 100ns → Disk swap 10ms (100,000× slower)

Causes:
- Severe host memory exhaustion
- Ballooning unable to reclaim enough
- Memory reservations preventing ballooning

Resolution (Emergency):
1. Identify swapping VMs:
   esxtop -> 'm' -> sort by SWCUR
2. Immediate action:
   - vMotion VMs off host (distribute load)
   - Или controlled shutdown non-critical VMs
3. Add physical memory to host
4. Review memory overcommitment ratio

Prevention:
- Memory admission control (vSphere HA)
- Limit overcommitment (<1.5:1 для production)
- Reservations для critical workloads
```

**Memory Consumed vs Active**
```
Key Metrics:
- Consumed: Total allocated to VM (from host perspective)
- Active: Actually accessed by guest OS (working set)
- Overhead: Hypervisor memory для VM (VMX, snapshots)

Sizing:
- Consumed >> Active: VM over-allocated, можно reduce
- Active ≈ Consumed: Well-sized или под pressure
- Active > Consumed - Overhead: Impossible, check metrics

Example:
VM configured: 32 GB
Consumed: 32 GB (allocated)
Active: 8 GB (actually used)
→ Can reduce to 12-16 GB (headroom для spikes)
```

### Storage Metrics

**Latency Components (vSphere)**
```
GAVG (Guest Average Latency):
= KAVG + DAVG (total latency guest experiences)

KAVG (Kernel Average Latency):
= Time in VMkernel queue (before送 to storage device)
= High KAVG → CPU/memory pressure на host, или queue depth saturation

DAVG (Device Average Latency):
= QAVG + Physical storage latency
= Time от device до completion

QAVG (Queue Average Latency):
= Time в device driver queue (HBA, iSCSI adapter)
= High QAVG → adapter saturation

Physical storage latency:
= Time на storage array (после HBA)
= Measured by array (controller processing + disk I/O)

Thresholds:
Latency    Status      Action
<10ms      Excellent   No action needed
10-15ms    Good        Monitor trends
15-20ms    Acceptable  Acceptable для general workloads
20-30ms    Warning     Investigate causes
>30ms      Critical    Immediate troubleshooting needed

Database workloads: <10ms target
VDI: <15ms for responsive experience
Batch processing: <30ms acceptable
```

**Latency Troubleshooting**
```
Scenario 1: High GAVG, Low KAVG и DAVG
→ Not possible (GAVG = KAVG + DAVG)
→ Check measurement точка или timing

Scenario 2: High KAVG, Normal DAVG
Causes:
- ESXi host CPU saturation (storage stack не получает CPU time)
- Memory pressure (paging affecting storage stack)
- Queue depth limits (Outstanding I/O limit reached)

Resolution:
- Check host CPU usage (should be <80%)
- Increase disk.schedNumReqOutstanding (if <32)
- Review storage multi-pathing (load balanced?)

Scenario 3: High DAVG, Low KAVG
Causes:
- Storage array overloaded
- Path saturation (FC/iSCSI bandwidth limit)
- Array-side queue full
- Slow disks (HDD performance limits)

Resolution:
Check array-side:
- IOPS usage vs capacity
- Cache hit ratio (low = performance problem)
- Controller CPU usage
- Disk busy percentage

Check paths:
- Bandwidth utilization per path
- Errors on paths (CRC, timeouts)
- Path count (more paths = more bandwidth)

Scenario 4: High QAVG
Causes:
- HBA/adapter saturated
- Driver queue depth low (default 32 для FC)
- Too many VMs на single datastore через single HBA

Resolution:
- Increase HBA queue depth (balance против host memory)
- Add HBA adapters (more paths, more queue depth)
- Distribute VMs across datastores/adapters
```

### Network Metrics

**Throughput и Drops**
```
Key metrics:
- Throughput (Mbps): Actual data transfer rate
- Packets/s: Packet rate (важно для small packet workloads)
- Drops TX/RX: Dropped packets (lost data)

Drops TX (Transmit):
Causes:
1. vNIC → vSwitch:
   - VM sending faster than vSwitch can handle
   - Buffer overflow в vSwitch

2. vSwitch → pNIC:
   - Physical uplink saturation (1Gbps vSwitch, 1Gbps uplink)
   - Uplink oversubscription (many VMs → single uplink)

Resolution:
- Load balancing (multiple uplinks, proper teaming policy)
- Network I/O Control (NIOC) для prioritization
- vMotion VMs для reduce load
- Upgrade uplinks (10Gbps+)

Drops RX (Receive):
Causes:
1. pNIC → vSwitch:
   - Physical NIC buffer overflow
   - Driver ring buffer too small

2. vSwitch → vNIC:
   - VM cannot process fast enough (CPU bound guest)
   - Small RX buffer в guest OS

Resolution:
- Check guest OS CPU (если 100%, scale up)
- Increase driver ring buffer (ethtool в Linux, registry в Windows)
- Adjust vSwitch buffer sizes (advanced settings)

Checking:
```bash
# vSphere
esxtop -> 'n' (network view)
Look for: %DRPTX, %DRPRX

# Linux guest
ethtool -S eth0 | grep -i drop
ifconfig eth0 | grep -i drop

# Windows guest
Get-NetAdapterStatistics | Select Name, *Discard*, *Error*
```
```

**Latency (Network)**
```
Types:
- Inter-VM (same host): <0.1ms typical
- Inter-VM (different host, same switch): <1ms
- VM to external: Depends на network path

High latency troubleshooting:
1. Same host, high latency:
   - vSwitch misconfiguration
   - Security features overhead (promiscuous mode?)
   - Host CPU saturation

2. Different hosts, high latency:
   - Physical switch congestion
   - Routing issues (unnecessary hops)
   - MTU mismatch (fragmentation)

3. VM to external:
   - Same as #2 + external network factors
   - Firewall processing delay
   - WAN latency

Tools:
- vmkping (ESXi to ESXi)
- iperf3 (bandwidth и latency testing)
- MTR/traceroute (path analysis)
```

## Common Issues и Resolution

### Issue 1: Purple Screen of Death (PSOD) - vSphere

**Symptoms**
```
- ESXi host crashes с purple diagnostic screen
- All VMs на host abruptly stop
- Host requires reboot to recover
```

**Common Causes**
```
1. Hardware issues:
   - Memory errors (ECC uncorrectable)
   - CPU MCE (Machine Check Exception)
   - Storage controller firmware bugs
   - NIC driver issues

2. Software bugs:
   - VMkernel bugs (rare but possible)
   - Third-party driver incompatibilities (backup agents, monitoring)
   - CIM provider crashes (hardware monitoring agents)

3. Configuration errors:
   - BIOS settings incompatible (NUMA, C-states, Turbo)
   - Overcommitment of resources
   - Unsupported hardware (not на HCL)
```

**Diagnosis Process**
```
1. Collect core dump:
   Location: /var/core/
   Files: vmkernel-zdump-*, vmkernel-log.*

2. Analyze PSOD screen:
   Key info:
   - Exception type (e.g., #PF Page Fault, #GP General Protection)
   - Backtrace (function call stack)
   - Registers (RIP register = instruction pointer)

3. Review logs before crash:
   /var/log/vmkernel.log
   /var/log/vmkwarning.log
   /var/log/hostd.log

   Look for:
   - Hardware errors (NMI, MCE, PCIe errors)
   - Storage timeouts (SCSI sense codes, APD/PDL)
   - Memory errors (EDAC messages)

4. Check hardware:
   - IPMI SEL (System Event Log):
     ipmitool sel list

   - Hardware health:
     esxcli hardware pci list
     esxcli storage core adapter list

   - Firmware versions:
     esxcfg-info -a (all hardware info)

5. VMware KB lookup:
   - Search PSOD backtrace
   - Check known issues для ESXi version
   - HCL verification (hardware + firmware compatibility)
```

**Resolution**
```
Based on cause:

Hardware failure:
→ Replace failed component (Memory, controller, NIC)
→ Update firmware to latest compatible version
→ Run hardware diagnostics (vendor tools)

Driver/firmware:
→ Update to latest VMware-certified version
→ Downgrade если regression (check release notes)
→ Engage vendor support (Dell, HPE, etc.)

VMkernel bug:
→ Apply ESXi patches
→ Upgrade to newer version/build
→ Apply workaround from VMware KB (если available)

Configuration:
→ Adjust BIOS settings (disable problematic features)
→ Remove third-party agents (CIM providers, backup agents)
→ Verify HCL compliance

Prevention:
- Regular firmware updates (planned maintenance)
- Proactive hardware monitoring (replace before failure)
- Test patches на non-production before production deployment
- Maintain N+1 host redundancy (HA tolerates host failures)
```

### Issue 2: vMotion Failures

**Common Failure Modes**
```
1. "Migration failed: Timeout waiting for page data"
   Cause: Network bandwidth insufficient для memory transfer

2. "The destination host does not support the virtual machine's network configuration"
   Cause: Distributed vSwitch version mismatch или port group missing

3. "A general system error occurred: Unable to get the MD5 digest of file"
   Cause: Storage accessibility problem (path failure)

4. "Incompatible CPU features"
   Cause: CPU compatibility issue между source и destination hosts
```

**Troubleshooting Process**
```
1. Network validation:
   Check vMotion network:
   - Dedicated vMotion VMkernel interface configured?
   - 10Gbps+ recommended для large VMs
   - Jumbo frames enabled end-to-end (MTU 9000)
   - No firewall blocking vMotion ports (TCP 8000)

   Test bandwidth:
   vmkping -I vmk1 -s 8972 -d destination-host
   (Tests jumbo frames connectivity)

2. Storage accessibility:
   Both hosts can access VM datastores:
   esxcli storage filesystem list
   esxcli storage core path list -d naa.xxx

   Check multipathing:
   - All paths active?
   - No dead paths (APD/PDL conditions)?

3. CPU compatibility:
   Check EVC (Enhanced vMotion Compatibility):
   - Cluster EVC mode set?
   - Matches oldest CPU в cluster?

   Or CPU compatibility mode:
   - VM advanced settings: cpuid.* settings

   Manual check:
   - Compare CPU features: /proc/cpuinfo (Linux)
   - Look for missing features на destination

4. Network configuration:
   Verify vSwitch/dvSwitch config matches:
   - Port group names identical
   - VLAN IDs match
   - dvSwitch versions compatible

5. VM configuration issues:
   - Snapshots: Large snapshots slow migration
   - CD-ROM/Floppy: Disconnect ISOs
   - Devices: Remove unnecessary hardware (serial ports, etc.)
   - Memory size: Very large VMs (>1TB) need special handling
```

**Resolution**
```
Network:
✓ Allocate dedicated vMotion network (separate VLAN)
✓ 10Gbps minimum (25/40/100Gbps для large VMs)
✓ Configure jumbo frames end-to-end
✓ QoS/traffic shaping для vMotion priority

Storage:
✓ Verify both hosts на same storage network
✓ Resolve path failures (re-scan, reset HBAs)
✓ Check SAN fabric (switch ports, zoning)

CPU:
✓ Enable cluster EVC mode (before migration)
✓ Or configure VM CPU compatibility manually
✓ Group same CPU generation hosts в separate clusters

VM optimization:
✓ Consolidate snapshots before migration
✓ Remove unnecessary virtual devices
✓ Consider storage vMotion separately (if storage issue)
```

### Issue 3: High Storage Latency (>30ms)

**Systematic Diagnosis**
```
Step 1: Identify scope
☐ Single VM или multiple VMs?
☐ Single datastore или multiple datastores?
☐ Single host accessing datastore или multiple hosts?
☐ All times или specific time windows?

Step 2: Latency component analysis
Use esxtop:
```bash
esxtop
Press 'u' for disk device view
Press 'd' for disk adapter view

Fields:
DAVG - Device latency (where problem?)
KAVG - Kernel latency (host CPU/queue issue?)
GAVG - Guest latency (total experienced)
CMDS/s - IOPS rate
```

High DAVG → Storage array problem
High KAVG → Host-side problem (CPU, queue depth)
High GAVG но low DAVG/KAVG → Measurement issue (check timing)
```

**Array-side Investigation**
```
Check storage array:
1. IOPS utilization:
   - Current IOPS vs rated capacity
   - >80% = saturation likely

2. Cache hit ratio:
   - Should be >80% для good performance
   - Low ratio = cache undersized или working set too large

3. Controller CPU:
   - >80% = controller bottleneck

4. Disk performance:
   - HDD: ~150 IOPS per disk
   - SSD: 50K-100K IOPS per disk
   - Check busy %

5. RAID rebuild:
   - Active rebuild = degraded performance
   - Wait for completion или throttle rebuild rate

6. Snapshot overhead:
   - Too many snapshots = metadata overhead
   - Snapshot space exhausted?

7. Replication:
   - Synchronous replication adds latency (RTT)
   - Asynchronous should have minimal impact
```

**Host-side Investigation**
```
1. Queue depth saturation:
   ```bash
   # Check current queue depth
   esxcli storage core adapter list
   # Shows max queue depth per adapter

   # Check per-LUN queue depth
   esxcli storage core device list -d naa.xxx
   # Look for Queueing
   ```

   Resolution:
   - Increase disk.schedNumReqOutstanding (default 32)
   - Increase device queue depth (LUN level)
   - Add more paths (FC HBAs, iSCSI adapters)

2. Path saturation:
   - 8Gbps FC: ~800 MB/s per path
   - 10Gbps iSCSI: ~1,000 MB/s per path
   - Check utilization per path:
     esxtop -> 'u' -> check MBREAD/s, MBWRTN/s per path

   Resolution:
   - Add more FC HBAs / iSCSI NICs
   - Verify multipathing policy (Round Robin preferred)
   - IOPS=1 для Round Robin (balance per-IO)

3. Host CPU bottleneck:
   - Storage stack needs CPU time
   - If host CPU >90%, storage I/O suffers

   Check:
   esxtop -> 'c' -> CPU usage

   Resolution:
   - Reduce VM density на host
   - DRS load balancing
   - Upgrade host CPUs

4. Oversized I/O:
   - Large I/O sizes (>1MB) saturate paths faster
   - Check I/O size distribution:
     vscsiStats -p histogram -c ...

   Resolution:
   - Optimize guest OS I/O patterns (database tuning)
   - Storage tiering (large sequential I/O to HDD tier)
```

**VM-level Investigation**
```
1. Queueing в guest OS:
   # Linux
   iostat -x 1
   # Look for avgqu-sz (queue size)
   # High queue + high await = bottleneck

   # Windows
   Get-Counter "\PhysicalDisk(*)\Avg. Disk Queue Length"
   # >2 per disk = bottleneck

2. Application I/O pattern:
   - Random vs sequential
   - Read vs write ratio
   - I/O size distribution

   Optimization:
   - Database: Separate data/log to different datastores
   - Alignment: Verify partition alignment (Windows pre-2008, Linux improper fdisk)
   - Filesystem: XFS/ext4 (Linux), ReFS (Windows) optimized options

3. Snapshots (VM-level):
   - Excessive snapshots (>3-5) = delta file overhead
   - Large snapshots (>50GB) = metadata bloat

   Resolution:
   - Consolidate snapshots (VM -> Snapshot -> Delete All)
   - Avoid using snapshots для backup (use array-level или agent-based)
```

## Референсы

Detailed guides в `references/`:
- `vmware-performance-metrics.md` - Complete metric definitions & thresholds
- `hyperv-troubleshooting.md` - Hyper-V specific diagnostics
- `kvm-performance-tuning.md` - KVM/QEMU optimization guide
- `storage-multipathing.md` - FC, iSCSI, NFS multipathing best practices

Tools и scripts в `assets/`:
- `esxtop-analysis-script.sh` - Automated esxtop data collection & analysis
- `vm-rightsizing-calculator.xlsx` - VM resource sizing recommendations
- `performance-baseline-template.md` - Performance baselining methodology
- `troubleshooting-flowcharts.pdf` - Decision trees для common issues
