# Выбор инстанса для низкого steal time
- **Bare metal**: максимум предсказуемости, нет overcommit; минус — стоимость/операции.
- **Dedicated host/sole-tenant**: изоляция tenant, контроль NUMA/IRQ; минус — квоты/цена.
- **Isolated SKU**: фиксированное размещение, хорошо для баз/RT.
- **Burstable**: избегать latency-critical путей; включать unlimited/credits мониторинг.
- Чеклист: vCPU:pCPU ≤ 1:1 для критичных задач, NUMA topology совпадает с гостем, SMT policy (off/isolated), доступность hugepages/SR-IOV.
