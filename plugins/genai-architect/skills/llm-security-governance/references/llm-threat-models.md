# Threat models для LLM
- Источники угроз: prompt injection, data poisoning, model hijack, supply chain (weights, deps), infra (keys, IAM).
- Активы: модели, промпты, данные, логи, ключи, клиенты/тенанты.
- Сценарии: jailbreak → policy bypass, exfil через контекст, SQL/SSRFi через плагины/инструменты, RCE в коннекторах.
- Контроли: isolation, allow/deny lists, sandbox tool use, strict outputs, E2E audit, минимизация контекста.
- Обновление: при смене моделей/фич, ежеквартально; включать abuse кейсы.
