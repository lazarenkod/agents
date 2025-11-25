# Kata Containers
- Лёгкие VM для контейнеров: безопасность VM + UX контейнеров.
- Требования: поддержка KVM, CRI интеграция, initrd образ Kata.
- Настройка: `containerd`/`CRI-O` runtimeClass, TOML конфиг (vCPUs, memory, entropy).
- Use-case: multi-tenant, изоляция для чувствительных ворклоадов, сочетание с SR-IOV/vDPA.
- Метрики: cold/warm start, pod density, p99 latency сети/диска.
