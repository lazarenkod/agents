# Playbook резервирования capacity
- Критерии: стабильный трафик, SLA высокие, частые throttling.
- Шаги: расчёт потребления (tokens/s), выбор провайдера (PTU/Provisioned throughput), контракт/квоты.
- Экономика: сравнение on-demand vs reserved, срок окупаемости, штрафы за недоиспользование.
- Операции: мониторинг использования, перераспределение, renew/modify, fallback на on-demand при пиках.
- Риски: lock-in, изменения цен, рост/падение трафика; mitigations: короткие сроки, mix reserved/on-demand.
