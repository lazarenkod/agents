# virtio-blk vs virtio-scsi
- virtio-blk: проще, меньше оверхеда, 1 queue (или MQ с modern драйверами), меньше фич.
- virtio-scsi: множественные очереди, SCSI фичи (hotplug, multi-LUN), выше оверхед.
- Выбор: virtio-blk для single-disk high-IOPS, virtio-scsi для множества дисков/фич.
- Важное: используйте iothreads, cache=none/writeback, io=native, multiqueue для scsi.
- Тесты: fio randread/write, p99 latency, queue depth, CPU per IO thread.
