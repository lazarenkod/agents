# Тюнинг памяти
- Hugepages: 2M/1G для предсказуемости; pinning памяти через numatune.
- Ballooning: используйте для уплотнения, отключайте для latency-критичных; контролируйте guest agent.
- Swap: disable для RT, limit/alert для общих; `vm.swappiness=0-10`.
- THP: `always` для throughput, `never` для latency; `madvise` для выборочного.
- Метрики: RSS, cache, swap in/out, balloon stats, THP faults/hits, NUMA misses.
