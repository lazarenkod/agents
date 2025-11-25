# План capacity для GPU/инференса
- Профиль нагрузки: rps/конкаренси, токены in/out, модель mix.
- Требования: target latency, рост трафика (%/мес), пики.
- Расчёт: batch size, max seq len, tokens/s per GPU, instance types, headroom 20–30%.
- Политики: autoscale (HPA/Karpenter), приоритет очереди, fallback модель.
- Риски: холодные старты, очередь > бюджет, spot прерывания; меры: warm pools, pod disruption budgets.
