# Nested virtualization
- Требования: включить VMX/SVM на хосте (`kvm_intel nested=1`), CPU mode `host-passthrough`.
- Использование: тестовые среды, CI, lab для Kubernetes-in-Kubernetes.
- Риски: overhead 10–30%, проблемы с таймерами/TSX, ограниченная поддержка миграции.
- Советы: ограничить глубину (L2 макс), не смешивать с высокими SLA, использовать SR-IOV/vDPA для сети в L2 если возможно.
- Мониторинг: st%, runqueue, EPT/NPT faults, L1/L2 clocks.
