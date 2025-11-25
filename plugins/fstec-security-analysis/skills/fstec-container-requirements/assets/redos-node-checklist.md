# RedOS 7/8 baseline для узлов контейнеризации
- Репозитории: только сертифицированные RedOS, проверки подписей, запрет сторонних rpm.
- Ядро/модули: версия из сертификата, отключить ненужные (usb, firewire при отсутствии), kexec off.
- SELinux: enforcing, policy для kubelet/containerd/docker, запрет semodule -i без change control.
- Auditd: включен, правила на auth, sudo, изменения конфигов, docker/containerd/kubelet действия.
- Sysctl: net.ipv4.conf.*.rp_filter=1, disable ip forwarding если не требуется, dmesg_restrict=1, kernel.kptr_restrict=2, fs.protected_*=1.
- Сеть: firewalld/nftables правила, time sync с доверным NTP, логирование drop.
- Крипто/СКЗИ: использование сертифицированных библиотек, TLS профили, управление ключами.
- Обновления: регламентированные окна, тестовый стенд, rollback plan, журнал изменений.
