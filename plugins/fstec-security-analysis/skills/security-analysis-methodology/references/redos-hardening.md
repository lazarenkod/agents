# Hardening RedOS 7/8
- Базовые настройки: SELinux Enforcing, auditd, sudo логирование, faillock, парольные политики.
- Kernel/sysctl: disable unused FS/modules, restrict ptrace, dmesg_restrict, kernel.kexec_disabled, network stack hardening.
- Сеть: firewall/nftables, ограничить слушающие сервисы, syslog защищён, время через доверный NTP.
- Контейнеризация на RedOS: контейнер runtime под ограниченным юзером, seccomp/AppArmor (если доступно), cgroup изоляция.
- Обновления: только сертифицированные репо RedOS 7/8, тестирование патчей, журнал изменений, контроль хэшей.
- СКЗИ: интеграция с сертифицированными библиотеками/крипто, TLS профили, управление ключами, проверка сертификатов.
