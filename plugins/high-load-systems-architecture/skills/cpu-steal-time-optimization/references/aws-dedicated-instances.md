# AWS: dedicated/isolated инстансы против steal time
- Используйте `--tenancy dedicated` или dedicated hosts для устранения overcommit.
- Серии: `c5/m5/r5d` (dedicated), bare metal (`*.metal`) для полного контроля.
- Для burstable (t3/t4g): включать `unlimited`, мониторить CPUCreditBalance.
- Проверки: CloudWatch `CPUCreditBalance`, `CPUUtilization`, user-data для irq/NUMA pinning.
- Стоимость: dedicated host ≈ +10–20% vs shared; оправдано для latency-critical путей.
