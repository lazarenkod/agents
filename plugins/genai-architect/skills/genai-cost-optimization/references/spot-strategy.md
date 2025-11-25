# Стратегии spot/прерываемых ресурсов
- Use-case: batch/offline, low-priority inference; избегать для P0 SLA.
- Политики: mix on-demand + spot, max % spot, приоритетные очереди.
- Контроль: PDB/eviction handling, checkpointing, warm pool на on-demand.
- Мониторинг: interruption notice, failover время, потери задач.
- Экономия: измерять $/час vs on-demand, оценивать риск прерываний.
