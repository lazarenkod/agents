# Confidential Computing (SEV/TDX)
- SEV/SEV-ES/SEV-SNP: шифрование памяти per-VM, защита от гипервизора; требует поддерживаемых CPU/BIOS.
- TDX: Intel TEE для VM, аналогично защищает память и состояние.
- Libvirt: `<launchSecurity type='sev'>…</launchSecurity>` или `<features><tdx/></features>`.
- Ограничения: совместимость устройств, невозможность дебага, цена/производительность (5–15%).
- Use-cases: регуляторика, multi-tenant чувствительные данные; проверить поддержку гостевых ядер/дистров.
