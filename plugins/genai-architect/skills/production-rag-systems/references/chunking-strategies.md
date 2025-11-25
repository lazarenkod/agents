# Chunking стратегии
- По структуре: markdown headers/sections для сохранения иерархии.
- Семантическое: breakpoint percentile, embeddings для разбиения по смыслу.
- Код: токен-бейз сплиттер + сохранение сигнатур функций/классов.
- Гибрид: большие чанки для recall + маленькие для точности, multi-vector (parent/child).
- Метрики: overlap %, avg tokens, coverage, leakage/дубли.
