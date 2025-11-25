# Azure: dedicated hosts и изолированные SKU
- Варианты: Dedicated Host группы (`az vm host create`), Isolated VM SKU (Esv3/Eisv3).
- Включайте `host group` + `--host` при создании VM для пиннинга на конкретный хост.
- Hyper-V изоляция: убедитесь, что соседние noisy workloads отсутствуют; используйте политику размещения.
- Метрики: Azure Monitor — CPU credits (B-series), CPU ready/steal недоступен напрямую → прокси через latency/host events.
- Стоимость/ограничения: предоплата за host, лимиты регионов, квоты.
