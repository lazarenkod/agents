# Сетевой чек-лист (контейнеры)

- Сегментация: namespaces/tenants, NP default deny ingress/egress.
- Ingress: TLS/mTLS, WAF/IDS (при необходимости), ограничение публичных LB.
- Egress: egress policies, ограничения внешних адресов, прокси/egress gateway.
- Firewall/ACL: уровни (cloud/VPC + cluster), контроль открытых портов.
- DNS/time: защищённый DNS, DNSSEC (если доступно), time sync (NTP).
- Monitoring/alerts: открытые сервисы, новые публичные endpoints, spikes traffic.
