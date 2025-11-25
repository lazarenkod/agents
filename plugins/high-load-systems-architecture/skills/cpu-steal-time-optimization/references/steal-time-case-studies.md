# Кейсы снижения steal time

## 1) Переезд на dedicated host (AWS c5.metal)
- Было: st 12–18%, p99 API 420→900 мс.
- Действия: миграция на dedicated, pinning vCPU, irq affinity, perf audit.
- Итог: st <1%, p99 280 мс, стоимость +18%.

## 2) NUMA misplacement фикса
- Было: 8 vCPU размазаны по 2 NUMA, st 7–9%, latency джиттер.
- Действия: NUMA pinning, huge pages, irq balancer tuning.
- Итог: st 2–3%, p99 стабильность, без изменения стоимости.

## 3) Noisy neighbor в публичном облаке
- Было: bursty сосед, st скачки до 25%.
- Действия: алерты на st>8%, автоматический live-migration по тегу, квоты для тенанта.
- Итог: снижение SEV-1 на 70%, предсказуемость SLAs.
