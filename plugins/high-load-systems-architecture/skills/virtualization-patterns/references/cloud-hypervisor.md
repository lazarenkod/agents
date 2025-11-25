# Cloud Hypervisor
- Rust-базированный гипервизор, ориентирован на cloud-native нагрузки, минимальный TCB.
- Поддержка: KVM, virtio, vIOMMU, vPMEM, seccomp.
- Преимущества: быстрый старт, низкий overhead; ограничения: меньшая экосистема vs QEMU.
- Конфигурация: TOML/CLI, похожие параметры CPU/мем/диск/сеть.
- Use-cases: безопасные multi-tenant среды, огрубленные образы, CNF/VNF.
