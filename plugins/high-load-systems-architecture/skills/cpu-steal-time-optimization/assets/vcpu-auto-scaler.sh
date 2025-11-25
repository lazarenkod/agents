#!/usr/bin/env bash
# vcpu-auto-scaler.sh - пример автоскейла vCPU по steal time
# Используйте как шаблон; требует SSH доступ к гостю и virsh на гипервизоре.

set -euo pipefail

VM_NAME="${1:?vm name required}"
THRESHOLD="${THRESHOLD:-8}"   # % steal при котором добавляем vCPU
MIN_VCPU="${MIN_VCPU:-2}"
MAX_VCPU="${MAX_VCPU:-16}"
SLEEP="${SLEEP:-60}"

while true; do
  STEAL="$(ssh "$VM_NAME" "mpstat 1 1 | awk '/Average/ {print \$NF}'")"
  CUR="$(virsh vcpucount "$VM_NAME" --live | awk '/current/ {print $2}')"

  if (( $(echo "$STEAL > $THRESHOLD" | bc -l) )) && [ "$CUR" -lt "$MAX_VCPU" ]; then
    NEXT=$((CUR + 1))
    virsh setvcpus "$VM_NAME" "$NEXT" --live
    echo "$(date -Is) scaled up to $NEXT vCPU (steal=$STEAL%)"
  fi

  if (( $(echo "$STEAL < ($THRESHOLD/2)" | bc -l) )) && [ "$CUR" -gt "$MIN_VCPU" ]; then
    NEXT=$((CUR - 1))
    virsh setvcpus "$VM_NAME" "$NEXT" --live
    echo "$(date -Is) scaled down to $NEXT vCPU (steal=$STEAL%)"
  fi

  sleep "$SLEEP"
done
