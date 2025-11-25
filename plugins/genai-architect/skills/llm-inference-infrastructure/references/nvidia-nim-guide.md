# NVIDIA NIM guide
- Контейнеры NIM (Triton/NeMo): оптимизированные сервинг-образы, поддержка Llama/Mistral/GPT4All и кастом.
- Архитектура: Kubernetes + GPU nodes, MIG/мульти-GPU, HF TGI совместимость, vLLM интеграция.
- Производительность: paged attention, kv-cache reuse, tensor parallel, fp8/bf16 настройки.
- Ops: мониторинг tokens/s, latency p95, GPU util/mem, autoscale (HPA/Karpenter), spot fallback.
- Безопасность: image signing, частные реестры, IAM RBAC, сеть (CNI policies), supply chain сканирование.
