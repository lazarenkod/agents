---
name: hardware-diagnostics
description: Комплексная диагностика серверного оборудования с автоматическим сбором метрик и генерацией отчета.
---

# Диагностика серверного оборудования

Эта команда выполняет полную диагностику серверного оборудования, собирая данные со всех доступных источников и генерируя подробный отчет на русском языке.

## Использование

```bash
/hardware-diagnostics [hostname или IP]
```

## Процесс диагностики

### Шаг 1: Сбор информации о системе

Соберу следующую информацию:

1. **Базовая информация**
   - Vendor и модель сервера
   - Serial number
   - BIOS/UEFI версия
   - BMC/iDRAC/iLO версия

2. **Конфигурация**
   - CPU: модель, количество, частота
   - Memory: тип, объем, конфигурация
   - Storage: диски, RAID configuration
   - Network: адаптеры, конфигурация

### Шаг 2: Проверка аппаратного состояния

Проверю следующие компоненты:

1. **Процессоры**
   - Температура каждого CPU
   - Machine Check Exceptions (MCE)
   - Thermal throttling events
   - Microcode версия

2. **Память**
   - ECC errors (correctable и uncorrectable)
   - Температура модулей
   - Memory training errors
   - DIMM population (правильность конфигурации)

3. **Системы хранения**
   - SMART статус всех дисков
   - RAID controller статус
   - Predictive failures
   - Performance metrics (latency, IOPS)

4. **Сетевые адаптеры**
   - Link status
   - Errors и drops
   - Optical power levels (для SFP/QSFP)
   - Firmware версии

5. **Системы питания**
   - PSU статус и здоровье
   - Voltage rails (12V, 5V, 3.3V)
   - Power consumption и efficiency
   - Redundancy status

6. **Охлаждение**
   - Fan speeds и статус
   - Temperature sensors (CPU, ambient, exhaust)
   - Thermal management events

### Шаг 3: Анализ логов

Проанализирую system event logs:

1. **IPMI/BMC SEL (System Event Log)**
   - Critical hardware events
   - Environmental warnings
   - Power events
   - Firmware errors

2. **Operating System Logs**
   - Kernel hardware errors (dmesg)
   - EDAC errors (memory)
   - Storage errors (SCSI sense codes)
   - Network errors

3. **Firmware Logs**
   - BIOS POST errors
   - RAID controller events
   - NIC firmware events

### Шаг 4: Performance Baseline

Соберу текущие метрики производительности:

1. **CPU Metrics**
   - Utilization %
   - Load average
   - Context switches
   - Temperature under load

2. **Memory Metrics**
   - Utilization %
   - Bandwidth usage
   - Page faults
   - NUMA statistics

3. **Storage Metrics**
   - IOPS (read/write)
   - Latency (average, p95, p99)
   - Throughput (MB/s)
   - Queue depth

4. **Network Metrics**
   - Throughput (Mbps)
   - Packets per second
   - Latency
   - Errors/drops

### Шаг 5: Генерация отчета

## Формат отчета

Отчет будет сгенерирован в формате Markdown на русском языке:

```markdown
# Отчет диагностики серверного оборудования

**Сервер:** [hostname]
**Дата проверки:** [timestamp]
**Проверку выполнил:** hardware-diagnostics-specialist

## Резюме

[Краткое резюме состояния: OK / Warning / Critical]

### Критические проблемы
- [Список проблем требующих немедленного внимания]

### Предупреждения
- [Список проблем требующих мониторинга]

## Конфигурация системы

### Общая информация
- **Vendor/Модель:** [Dell PowerEdge R750]
- **Serial Number:** [SN123456]
- **BIOS версия:** [2.15.0]
- **BMC версия:** [iDRAC 6.00.00.00]

### Процессоры
| Socket | Модель | Cores | Частота | Температура | Статус |
|--------|--------|-------|---------|-------------|--------|
| 0 | Intel Xeon Gold 6348 | 28 | 2.6 GHz | 45°C | ✓ OK |
| 1 | Intel Xeon Gold 6348 | 28 | 2.6 GHz | 47°C | ✓ OK |

### Память
| Channel | DIMM | Размер | Тип | Частота | Температура | ECC Errors | Статус |
|---------|------|--------|-----|---------|-------------|------------|--------|
| A1 | DIMM_A1 | 32GB | DDR4 RDIMM | 3200 MT/s | 42°C | 0 CE, 0 UE | ✓ OK |
[...]

### Хранилище
#### RAID Controller: PERC H755
- **Firmware:** 52.24.0-4296
- **Статус:** Optimal
- **BBU:** Optimal, 100% charged

#### Physical Disks
| Slot | Model | Capacity | Type | SMART | Temperature | Predictive Failure | Статус |
|------|-------|----------|------|-------|-------------|--------------------|--------|
| 0:0 | Samsung PM1735 | 3.84TB | NVMe SSD | PASSED | 38°C | No | ✓ OK |
[...]

#### Virtual Disks
| VD | RAID Level | Size | Состояние | Disks |
|----|-----------|------|-----------|-------|
| 0 | RAID1 | 1.8TB | Optimal | 0:0, 0:1 |
| 1 | RAID5 | 10.8TB | Optimal | 0:2-0:7 |

### Сетевые адаптеры
| Interface | Model | Speed | Link | MAC Address | Errors | Drops | Статус |
|-----------|-------|-------|------|-------------|--------|-------|--------|
| eth0 | Intel XXV710 | 25Gbps | Up | xx:xx:xx:xx:xx:xx | 0 | 0 | ✓ OK |
[...]

### Электропитание
| PSU | Model | Capacity | Input | Output | Efficiency | Статус |
|-----|-------|----------|-------|--------|------------|--------|
| PSU1 | Dell 800W | 800W | 220V AC | 12V DC | 94% | ✓ OK |
| PSU2 | Dell 800W | 800W | 220V AC | 12V DC | 94% | ✓ OK |

**Total Power Consumption:** 450W / 1600W (28%)

### Охлаждение
| Fan | Location | RPM | Speed % | Статус |
|-----|----------|-----|---------|--------|
| FAN1 | System Board | 5400 | 60% | ✓ OK |
[...]

**Temperature Summary:**
- **CPU0:** 45°C (Max: 95°C)
- **CPU1:** 47°C (Max: 95°C)
- **Ambient:** 22°C (Max: 35°C)
- **Exhaust:** 32°C

## Анализ состояния

### Процессоры
**Статус:** ✓ Healthy

- Температуры в норме (<75°C)
- Нет MCE errors
- Нет thermal throttling events
- Microcode актуален

### Память
**Статус:** ⚠ Warning

- **Warning:** DIMM A1 показывает 3 correctable errors за последний час
- **Рекомендация:** Мониторить DIMM A1, если ошибки продолжают расти - планировать замену в течение 1-2 недель

**Все остальные модули:** Без ошибок

### Хранилище
**Статус:** ✓ Healthy

**RAID Controller:** Optimal, BBU healthy
**Physical Disks:** Все диски PASSED SMART tests
**Performance:**
- Average latency: 2.5ms (Excellent для NVMe)
- IOPS: 45,000 (под текущей нагрузкой)

### Сеть
**Статус:** ✓ Healthy

- Все links UP на ожидаемой скорости
- Нет packet errors или drops
- Firmware актуален

### Электропитание
**Статус:** ✓ Healthy

- Обе PSU operational (N+1 redundancy)
- Voltage rails stable
- Efficiency >90% (Platinum rated)
- Power consumption нормальный для конфигурации

### Охлаждение
**Статус:** ✓ Healthy

- Все fans operating нормально (50-70% speed)
- Температуры well within spec
- Airflow нормальный

## System Event Log Analysis

### Последние 30 дней

**Critical Events:** 0
**Warning Events:** 2
**Informational:** 147

### Notable Events:
```
2024-12-01 14:23:15 | Warning | Memory | Correctable ECC error, DIMM A1
2024-11-28 09:15:42 | Warning | Memory | Correctable ECC error, DIMM A1
```

**Анализ:** DIMM A1 показывает pattern повторяющихся CE ошибок. Требуется мониторинг.

## Performance Baseline

### CPU
- **Utilization:** 35% average (healthy)
- **Load Average:** 12.5 (56 cores = 0.22 load/core, excellent)
- **Temperature:** 45-47°C under load

### Memory
- **Utilization:** 75% (384GB used из 512GB)
- **Bandwidth:** ~150 GB/s (good utilization для DDR4-3200)
- **No swapping activity**

### Storage
- **IOPS:** 45,000 average, peaks 120,000
- **Latency:** Average 2.5ms, p95 4.2ms, p99 8.1ms (excellent)
- **Throughput:** 1.2 GB/s average

### Network
- **eth0:** 8 Gbps average (25G link, 32% utilization)
- **eth1:** 6 Gbps average (25G link, 24% utilization)
- **Latency:** <0.5ms local network
- **No packet loss**

## Рекомендации

### Немедленные действия (0-7 дней)
**Нет критических проблем требующих немедленного вмешательства.**

### Краткосрочные (1-4 недели)
1. **Мониторинг DIMM A1**
   - Настроить ежедневный check correctable errors
   - Если errors продолжают расти (>10/час) → Замена DIMM
   - Иметь spare DIMM в inventory

### Долгосрочные (1-6 месяцев)
1. **Firmware Updates**
   - BIOS: Текущая 2.15.0, latest 2.18.1 available (проверить release notes)
   - iDRAC: Текущая 6.00.00.00, latest 6.10.00.00 available
   - RAID Controller: Актуален

2. **Capacity Planning**
   - Memory: 75% utilization, комфортный headroom
   - Storage: 8.2TB используется из 12.6TB (65%), достаточно пространства
   - Network: Low utilization, хороший headroom

3. **Preventive Maintenance**
   - Сервер введен в эксплуатацию: 2 года назад
   - Следующий refresh cycle: Через 2-3 года
   - Все компоненты within design life

## Заключение

**Overall Health Status: ⚠ Warning (Minor Issue)**

Сервер в целом находится в хорошем состоянии. Единственная обнаруженная проблема - повторяющиеся correctable ECC errors на DIMM A1. Это типичный предвестник degradation памяти и требует проактивного мониторинга с возможной заменой модуля в краткосрочной перспективе.

Все остальные подсистемы функционируют нормально с хорошим performance profile и достаточным headroom для роста.

**Следующая проверка:** Рекомендуется через 30 дней для trending analysis.

---
**Отчет сгенерирован:** hardware-diagnostics-specialist
**Инструмент:** Claude Code datacenter-hardware-expert plugin
```

## После генерации отчета

Отчет будет сохранен в файл: `hardware-diagnostics-report-[hostname]-[timestamp].md`

Если обнаружены критические проблемы, я также создам:
1. **Incident ticket template** с деталями для tracking system
2. **Action plan** с приоритизированными шагами remediation
3. **Escalation matrix** если требуется vendor support

## Требования

Для полной диагностики необходимо:
- IPMI/Redfish доступ к BMC (iDRAC, iLO, etc.)
- SSH доступ к операционной системе
- Права на чтение hardware logs и метрик
- Доступные утилиты: `ipmitool`, `smartctl`, `dmidecode`, `ethtool`
