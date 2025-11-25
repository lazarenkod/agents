# XDP: основы
- Режимы: native (в драйвере, быстрее), generic (в netstack, для тестов), offload (в NIC).
- Use-cases: DDoS mitigation, load shedding, packet filtering, telemetry.
- Скрипт-шаблон (libbpf CO-RE): drop по маске, отправка в user-space.
- Инструменты: `xdp-tools` (`xdp-loader`, `xdp-filter`), bpftool для аттача.
- Проверка: `ethtool -S eth0 | grep xdp`, pcap до/после, latency/pps, CPU load.
