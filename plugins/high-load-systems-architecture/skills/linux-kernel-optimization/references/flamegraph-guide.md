# Flamegraph: кратко
- Сбор: `perf record -F 99 -ag -- sleep 30` → `perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg`.
- Интерпретация: ширина = время CPU; ищите широкие блоки (горячие функции), частые VM-exit/syscall.
- Удобные флаги: `--color=io`/`java` для подсветки, `--title`.
- Публикация: сохраняйте svg в артефакт с метаданными (ядро, нагрузка, commit).
- Антипаттерны: разные среды в одном графе, sampling rate слишком низкий (пропуски tail).
