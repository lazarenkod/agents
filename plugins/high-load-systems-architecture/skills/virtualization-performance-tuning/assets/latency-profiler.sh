#!/usr/bin/env bash
# latency-profiler.sh - сбор p99 по сети/диску и стекам для VM/host

set -euo pipefail

DURATION="${DURATION:-120}"
OUT="${OUT:-latency-profile}"

echo "[1/3] Сбор сетевых метрик"
ss -ti > "${OUT}-ss.txt"
ethtool -S "${IFACE:-eth0}" > "${OUT}-ethtool.txt"

echo "[2/3] perf sched / block latency"
perf sched record -- sleep "$DURATION"
perf sched latency > "${OUT}-sched.txt"
perf record -e 'block:block_rq_issue,block:block_rq_complete' -a -- sleep "$DURATION"
perf report --stdio --sort comm,dso,symbol > "${OUT}-block.txt"

echo "[3/3] Сводка"
echo "Артефакты: ${OUT}-ss.txt, ${OUT}-ethtool.txt, ${OUT}-sched.txt, ${OUT}-block.txt, perf.data"
