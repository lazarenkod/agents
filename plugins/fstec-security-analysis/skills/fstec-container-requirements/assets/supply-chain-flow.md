# Supply Chain Flow (контейнеризация)

1) Source → SCM (policy для PR, MFA, reviewers)  
2) CI: сборка в изолированных runners, SBOM, скан зависимостей, секреты в vault  
3) Образы: подпись, скан, политика допуска (block/allow), тегирование, ретеншн  
4) Registry: приватный, RBAC, аудит push/pull, репликации, WORM/immutable tags (если доступно)  
5) Deploy: проверка подписи, политика по версиям, NP/RBAC, secrets, конфиг drift check  
6) Monitoring: алерты на новые образы без подписи, unusual traffic, CVE, drift  
7) Incident: revoke, блок push/pull, откат, уведомления, RCA
