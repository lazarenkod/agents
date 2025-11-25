# CAP/PACELC Guide
- CAP: Consistency vs Availability under Partition.
- PACELC: If Partition then A/C, Else Latency vs Consistency.
- Используй: OLTP (C предпочтительно), аналитика/кеши (A/L), multi-region (A/L с локальными writes или C с leader/follower).
- Документируй: выбранная модель, SLA/latency требования, последствия для UX/данных, fallback/compensations.
