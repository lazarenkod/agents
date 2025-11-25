# Runbook: автоскейлинг и деградации
- Триггеры: latency p99 > бюджет, queue depth > X, GPU util > 85%, error rate.
- Действия: проверить лимиты/квоты, warm pool размер, включить aggressive batching, временно route на более дешёвые модели.
- Проверки: capacity planner, HPA/Cluster Autoscaler события, spot interruptions.
- Rollback: фиксированные реплики, отключение agressive batching при росте ошибок, route freeze.
- Коммуникация: алерты → on-call, статус страница, ETA восстановления.
