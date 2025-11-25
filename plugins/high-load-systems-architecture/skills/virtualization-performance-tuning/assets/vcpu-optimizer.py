#!/usr/bin/env python3
"""
vcpu-optimizer.py - черновой расчёт пиннинга/NUMA для VM.
Ввод: lscpu --extended, количество vCPU, NUMA политика.
Вывод: рекомендация pinning + SMT избегание для latency-critical.
"""
import json
import sys

def parse_lscpu(lines):
    cpus = []
    for line in lines:
        if line.startswith("CPU"):
            continue
        parts = line.split()
        if len(parts) >= 5:
            cpus.append({"cpu": int(parts[0]), "node": parts[1], "core": parts[3]})
    return cpus

def suggest_pinning(cpus, vcpus):
    cpus_sorted = sorted(cpus, key=lambda x: (x["node"], x["core"], x["cpu"]))
    return [c["cpu"] for c in cpus_sorted[:vcpus]]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: lscpu.txt vcpus")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        cpus = parse_lscpu(f.readlines())
    pins = suggest_pinning(cpus, int(sys.argv[2]))
    print(json.dumps({"pinning": pins, "hint": "Проверьте SMT siblings и NUMA локальность"}, ensure_ascii=False))
