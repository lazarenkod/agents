# RBAC Hardening Checklist (контейнеризация)

- Роли: principle of least privilege, service accounts per workload, no wildcard admin.
- AuthN/AuthZ: MFA для админов, короткие токены, ротация ключей/сертификатов.
- Policies: ограничить create/patch/delete в кластере, ограничения на privileged/hostPath.
- Audit: включен audit log, мониторинг админ операций, alert на новые cluster-admin.
- Break-glass: документирован, логируется, ограничен по времени.
