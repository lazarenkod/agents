# Self-hosted GenAI: гайд
- Платформы: vLLM, TGI, Triton, NIM, SageMaker/Vertex custom; выбор по latency/стоимости/управляемости.
- GPU/инфра: типы (A100/H100/L4), kv-cache/paged attention, storage для weights, CI/CD модели.
- Безопасность: приватные реестры, supply chain, сеть (mTLS), RBAC, секреты.
- Ops: autoscale, spot/on-demand микс, мониторинг tokens/s, p99, GPU util, OOM.
- Стоимость: амортизация, резервы, power/cooling (on-prem), сравнение с API.
