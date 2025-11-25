# Ballooning стратегии
- Включать для уплотнения/экономии, отключать для latency-critical.
- Контролируйте guest agent + драйвер `virtio-balloon`; лимиты через `<memtune>`.
- Алерты: частые inflate/deflate, swap in/out гостя, p99 рост.
- Политики: статический лимит для баз данных, гибкий для batch/CI.
- Тесты: нагрузка с и без balloon, проверка OOM/swap, влияние на p99.
