# Firecracker (microVM)
- Лёгкие microVM для serverless/containers; минимальный девайс-модель, быстрый старт (<150мс).
- Запуск: `firecracker --api-sock /tmp/fc.sock`, загрузка kernel/rootfs через API.
- Изоляция: jailer, seccomp, cgroups; нет устройства с богатым функционалом (GPU/SR-IOV).
- Use-case: многотысячные краткоживущие VM, FaaS.
- Метрики: старт/стоп время, memory footprint, cold/warm start latency.
