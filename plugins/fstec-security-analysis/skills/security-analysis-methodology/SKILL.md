---
name: security-analysis-methodology
description: Методология проведения анализа безопасности средств контейнеризации с пошаговыми инструкциями и best practices. Use when planning security analysis, conducting audits, or establishing security assessment processes.
---

# Методология анализа безопасности контейнеров

## Когда использовать этот skill

- При планировании аудита безопасности системы контейнеризации
- При разработке процессов анализа соответствия требованиям
- При обучении команды методам анализа безопасности
- При стандартизации процессов оценки безопасности
- При проведении самооценки (self-assessment)

## Обзор методологии

Методология представляет собой систематический подход к анализу безопасности средств контейнеризации, состоящий из 7 основных фаз:

```
1. ПОДГОТОВКА
   ↓
2. СБОР ИНФОРМАЦИИ
   ↓
3. ТЕХНИЧЕСКИЙ АНАЛИЗ
   ↓
4. ОЦЕНКА СООТВЕТСТВИЯ
   ↓
5. ОЦЕНКА РИСКОВ
   ↓
6. ДОКУМЕНТИРОВАНИЕ
   ↓
7. ВЕРИФИКАЦИЯ И FOLLOW-UP
```

---

## ФАЗА 1: Подготовка

### 1.1. Определение scope

**Что включить в анализ:**

```markdown
# Scope Definition Checklist

## Целевая система
- [ ] Платформа: Kubernetes / Docker / Podman / другое
- [ ] Версия платформы: _______
- [ ] Количество узлов/хостов: _______
- [ ] Окружения: Production / Staging / Development
- [ ] Namespaces/проекты для анализа: _______

## Компоненты для проверки
- [ ] Control plane компоненты
- [ ] Worker nodes
- [ ] Образы контейнеров
- [ ] RBAC конфигурации
- [ ] Network policies
- [ ] Storage configurations
- [ ] Secrets management
- [ ] Monitoring и logging
- [ ] CI/CD pipeline

## Исключения из scope
- Компоненты, которые НЕ будут проверяться: _______
- Обоснование исключений: _______

## Уровень защищенности
- [ ] УЗ-1
- [ ] УЗ-2
- [ ] УЗ-3
- [ ] УЗ-4
```

### 1.2. Формирование команды

**Роли в команде анализа:**

| Роль | Ответственность | Навыки |
|------|----------------|--------|
| Руководитель аудита | Общее руководство, координация, принятие решений | Управление проектами, знание ФСТЭК |
| Технический аналитик | Технический анализ конфигураций и кода | Kubernetes/Docker, безопасность |
| Аналитик рисков | Оценка рисков и угроз | Анализ рисков, threat modeling |
| Документалист | Подготовка отчетов и документации | Техническое письмо, русский язык |
| Эксперт по ФСТЭК | Консультации по требованиям | Нормативная база ФСТЭК |

### 1.3. Планирование timeline

**Типовые сроки для различных масштабов:**

```markdown
# Малая система (1-5 nodes, до 50 контейнеров)
- Подготовка: 1 день
- Сбор информации: 1 день
- Технический анализ: 2-3 дня
- Оценка соответствия: 2 дня
- Оценка рисков: 1 день
- Документирование: 2 дня
- **Итого: 9-10 рабочих дней**

# Средняя система (5-20 nodes, 50-200 контейнеров)
- Подготовка: 2 дня
- Сбор информации: 2 дня
- Технический анализ: 5 дней
- Оценка соответствия: 3 дня
- Оценка рисков: 2 дня
- Документирование: 3 дня
- **Итого: 17 рабочих дней**

# Крупная система (20+ nodes, 200+ контейнеров)
- Подготовка: 3 дня
- Сбор информации: 3 дня
- Технический анализ: 10 дней
- Оценка соответствия: 5 дней
- Оценка рисков: 3 дня
- Документирование: 5 дней
- **Итого: 29 рабочих дней**
```

### 1.4. Подготовка инструментов

**Необходимый инструментарий:**

```bash
# Инструменты сканирования
- Trivy (сканирование образов)
- Grype (альтернативный сканер)
- Kube-bench (CIS benchmarks для K8s)
- Kubescape (комплексное сканирование K8s)

# Инструменты анализа конфигураций
- kubectl (Kubernetes CLI)
- docker CLI
- yq/jq (парсинг YAML/JSON)

# Инструменты мониторинга
- Falco (runtime security)
- Prometheus + Grafana (метрики)

# Инструменты для документирования
- Pandoc (конвертация Markdown → PDF)
- Git (версионирование отчетов)

# Установка
./install-security-tools.sh
```

---

## ФАЗА 2: Сбор информации

### 2.1. Сбор метаданных системы

**Скрипт для сбора общей информации (Kubernetes):**

```bash
#!/bin/bash
# collect-k8s-metadata.sh

OUTPUT_DIR="./collected-data/metadata"
mkdir -p "$OUTPUT_DIR"

echo "Сбор версий компонентов..."
kubectl version --output=yaml > "$OUTPUT_DIR/versions.yaml"

echo "Сбор информации о нодах..."
kubectl get nodes -o yaml > "$OUTPUT_DIR/nodes.yaml"

echo "Сбор namespaces..."
kubectl get namespaces -o yaml > "$OUTPUT_DIR/namespaces.yaml"

echo "Сбор информации о подах..."
kubectl get pods --all-namespaces -o yaml > "$OUTPUT_DIR/all-pods.yaml"

echo "Сбор deployments..."
kubectl get deployments --all-namespaces -o yaml > "$OUTPUT_DIR/deployments.yaml"

echo "Сбор statefulsets..."
kubectl get statefulsets --all-namespaces -o yaml > "$OUTPUT_DIR/statefulsets.yaml"

echo "Сбор daemonsets..."
kubectl get daemonsets --all-namespaces -o yaml > "$OUTPUT_DIR/daemonsets.yaml"

echo "Сбор информации о сервисах..."
kubectl get services --all-namespaces -o yaml > "$OUTPUT_DIR/services.yaml"

echo "Сбор завершен: $OUTPUT_DIR"
```

### 2.2. Сбор конфигураций безопасности

**Скрипт для сбора security конфигураций:**

```bash
#!/bin/bash
# collect-security-configs.sh

OUTPUT_DIR="./collected-data/security"
mkdir -p "$OUTPUT_DIR"

echo "Сбор ServiceAccounts..."
kubectl get serviceaccounts --all-namespaces -o yaml > "$OUTPUT_DIR/serviceaccounts.yaml"

echo "Сбор RBAC ролей..."
kubectl get roles --all-namespaces -o yaml > "$OUTPUT_DIR/roles.yaml"
kubectl get clusterroles -o yaml > "$OUTPUT_DIR/clusterroles.yaml"

echo "Сбор RoleBindings..."
kubectl get rolebindings --all-namespaces -o yaml > "$OUTPUT_DIR/rolebindings.yaml"
kubectl get clusterrolebindings -o yaml > "$OUTPUT_DIR/clusterrolebindings.yaml"

echo "Сбор NetworkPolicies..."
kubectl get networkpolicies --all-namespaces -o yaml > "$OUTPUT_DIR/networkpolicies.yaml"

echo "Сбор PodSecurityPolicies (если есть)..."
kubectl get psp -o yaml > "$OUTPUT_DIR/podsecuritypolicies.yaml" 2>/dev/null || echo "PSP не найдены"

echo "Сбор Secrets (только metadata)..."
kubectl get secrets --all-namespaces -o yaml | \
  yq eval 'del(.items[].data)' - > "$OUTPUT_DIR/secrets-metadata.yaml"

echo "Сбор ConfigMaps..."
kubectl get configmaps --all-namespaces -o yaml > "$OUTPUT_DIR/configmaps.yaml"

echo "Сбор завершен: $OUTPUT_DIR"
```

### 2.3. Сбор образов для анализа

**Скрипт для извлечения списка образов:**

```bash
#!/bin/bash
# collect-images.sh

OUTPUT_FILE="./collected-data/images-list.txt"

echo "Сбор уникальных образов из всех подов..."

kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | \
  sort -u > "$OUTPUT_FILE"

echo "Найдено $(wc -l < $OUTPUT_FILE) уникальных образов"
echo "Список сохранен: $OUTPUT_FILE"
```

### 2.4. Документирование архитектуры

**Создание диаграмм:**

```markdown
# Архитектурная документация

## Сетевая топология
[Диаграмма: namespaces, pods, services, network policies]

## Потоки данных
[Диаграмма: как данные перемещаются между компонентами]

## Права доступа
[Диаграмма: RBAC matrix - кто к чему имеет доступ]

## Хранение данных
[Диаграмма: PersistentVolumes, StorageClasses, бэкапы]
```

---

## ФАЗА 3: Технический анализ

### 3.1. Сканирование образов

**Процесс сканирования:**

```bash
#!/bin/bash
# scan-images.sh

IMAGES_FILE="./collected-data/images-list.txt"
OUTPUT_DIR="./scan-results/images"
mkdir -p "$OUTPUT_DIR"

while IFS= read -r image; do
    echo "Сканирование: $image"

    # Trivy сканирование
    trivy image \
      --format json \
      --output "$OUTPUT_DIR/$(echo $image | tr '/:' '_').json" \
      "$image"

    # Grype сканирование (для сравнения)
    grype "$image" \
      --output json \
      --file "$OUTPUT_DIR/$(echo $image | tr '/:' '_')_grype.json"
done < "$IMAGES_FILE"

echo "Сканирование завершено: $OUTPUT_DIR"
```

**Анализ результатов сканирования:**

```python
#!/usr/bin/env python3
# analyze-scan-results.py

import json
import glob
from collections import defaultdict

def analyze_scan_results(scan_dir):
    results = {
        'CRITICAL': defaultdict(list),
        'HIGH': defaultdict(list),
        'MEDIUM': defaultdict(list),
        'LOW': defaultdict(list)
    }

    for scan_file in glob.glob(f"{scan_dir}/*.json"):
        with open(scan_file) as f:
            data = json.load(f)

        image_name = scan_file.split('/')[-1].replace('.json', '')

        for vuln in data.get('Results', [{}])[0].get('Vulnerabilities', []):
            severity = vuln.get('Severity', 'UNKNOWN')
            if severity in results:
                results[severity][image_name].append({
                    'CVE': vuln.get('VulnerabilityID'),
                    'Package': vuln.get('PkgName'),
                    'Version': vuln.get('InstalledVersion'),
                    'FixVersion': vuln.get('FixedVersion', 'N/A')
                })

    # Генерация отчета
    print("# Результаты сканирования образов\n")

    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = sum(len(vulns) for vulns in results[severity].values())
        print(f"## {severity}: {count} уязвимостей\n")

        for image, vulns in results[severity].items():
            if vulns:
                print(f"### Образ: {image}")
                print(f"Уязвимостей: {len(vulns)}\n")

                for vuln in vulns[:5]:  # Топ-5 для каждого образа
                    print(f"- **{vuln['CVE']}**: {vuln['Package']} "
                          f"({vuln['Version']} → {vuln['FixVersion']})")
                print()

if __name__ == '__main__':
    analyze_scan_results('./scan-results/images')
```

### 3.2. Анализ SecurityContext

**Скрипт проверки SecurityContext:**

```bash
#!/bin/bash
# analyze-security-context.sh

echo "# Анализ SecurityContext"
echo

echo "## Проблема 1: Привилегированные контейнеры"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] |
    select(.spec.containers[]?.securityContext.privileged==true) |
    "\(.metadata.namespace)/\(.metadata.name)"' | \
  while read pod; do
    echo "❌ $pod"
  done

echo
echo "## Проблема 2: Контейнеры без runAsNonRoot"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] |
    select(.spec.securityContext.runAsNonRoot!=true and
           .spec.containers[].securityContext.runAsNonRoot!=true) |
    "\(.metadata.namespace)/\(.metadata.name)"' | \
  while read pod; do
    echo "⚠️  $pod"
  done

echo
echo "## Проблема 3: Контейнеры с allowPrivilegeEscalation=true"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] |
    select(.spec.containers[]?.securityContext.allowPrivilegeEscalation==true) |
    "\(.metadata.namespace)/\(.metadata.name)"' | \
  while read pod; do
    echo "⚠️  $pod"
  done

echo
echo "## Проблема 4: Использование hostNetwork/hostPID/hostIPC"
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] |
    select(.spec.hostNetwork==true or .spec.hostPID==true or .spec.hostIPC==true) |
    "\(.metadata.namespace)/\(.metadata.name) - hostNetwork:\(.spec.hostNetwork // false) hostPID:\(.spec.hostPID // false) hostIPC:\(.spec.hostIPC // false)"' | \
  while read pod; do
    echo "❌ $pod"
  done
```

### 3.3. Анализ RBAC

**Скрипт поиска избыточных привилегий:**

```bash
#!/bin/bash
# analyze-rbac.sh

echo "# Анализ RBAC"
echo

echo "## Проблема 1: ClusterRoles с wildcard permissions"
kubectl get clusterroles -o json | \
  jq -r '.items[] |
    select(.rules[]?.verbs[]? == "*" or
           .rules[]?.resources[]? == "*" or
           .rules[]?.apiGroups[]? == "*") |
    .metadata.name' | \
  while read role; do
    echo "⚠️  ClusterRole: $role (использует wildcards)"
  done

echo
echo "## Проблема 2: ServiceAccounts с cluster-admin"
kubectl get clusterrolebindings -o json | \
  jq -r '.items[] |
    select(.roleRef.name == "cluster-admin") |
    "\(.metadata.name): \(.subjects[].name) (\(.subjects[].namespace // "cluster-wide"))"' | \
  while read binding; do
    echo "❌ $binding"
  done

echo
echo "## Проблема 3: Опасные permissions"
DANGEROUS_VERBS=("create" "delete" "deletecollection")
DANGEROUS_RESOURCES=("pods/exec" "pods/attach" "secrets" "clusterroles" "clusterrolebindings")

for resource in "${DANGEROUS_RESOURCES[@]}"; do
    echo "### Доступ к $resource:"
    kubectl get clusterroles -o json | \
      jq -r --arg res "$resource" '.items[] |
        select(.rules[]? |
          (.resources[]? == $res and
           (.verbs[]? == "*" or .verbs[]? == "create" or .verbs[]? == "get"))) |
        .metadata.name'
done
```

### 3.4. Анализ Network Policies

**Проверка наличия и корректности Network Policies:**

```bash
#!/bin/bash
# analyze-network-policies.sh

echo "# Анализ Network Policies"
echo

echo "## Namespaces без Network Policies"
for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
    np_count=$(kubectl get networkpolicies -n $ns --no-headers 2>/dev/null | wc -l)
    if [ "$np_count" -eq 0 ]; then
        pod_count=$(kubectl get pods -n $ns --no-headers 2>/dev/null | wc -l)
        if [ "$pod_count" -gt 0 ]; then
            echo "❌ $ns (подов: $pod_count, NetworkPolicies: 0)"
        fi
    fi
done

echo
echo "## Namespaces с default-deny политикой"
for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
    has_default_deny=$(kubectl get networkpolicies -n $ns -o json | \
      jq -r '.items[] |
        select(.spec.podSelector.matchLabels == null or .spec.podSelector.matchLabels == {}) |
        select(.spec.policyTypes[]? == "Ingress" or .spec.policyTypes[]? == "Egress") |
        select(.spec.ingress == null or .spec.egress == null) |
        .metadata.name' 2>/dev/null)

    if [ -n "$has_default_deny" ]; then
        echo "✅ $ns (default-deny: $has_default_deny)"
    fi
done
```

---

## ФАЗА 4: Оценка соответствия

### 4.1. Создание чек-листа

**Шаблон чек-листа соответствия:**

```markdown
# Чек-лист соответствия требованиям ФСТЭК (УЗ-3)

## Идентификация и аутентификация (ИА)

### ИА.1: Идентификация субъектов доступа
- [ ] Каждый под имеет явный ServiceAccount
- [ ] ServiceAccounts уникальны для каждого приложения
- [ ] Отключен automountServiceAccountToken где не нужен
- **Статус:** ✅ / ⚠️ / ❌
- **Доказательства:** [ссылка на файл]
- **Комментарий:** _______

### ИА.2: Аутентификация субъектов доступа
- [ ] API сервер требует аутентификацию
- [ ] Используется сильная аутентификация (cert/OIDC)
- [ ] Нет анонимного доступа
- **Статус:** ✅ / ⚠️ / ❌
- **Доказательства:** [ссылка]
- **Комментарий:** _______

[... продолжение для всех требований ...]
```

### 4.2. Процесс оценки

**Для каждого требования:**

1. **Определить применимость**
   - Применимо ли это требование к данной системе?
   - Для данного уровня защищенности?

2. **Собрать доказательства**
   - Конфигурационные файлы
   - Результаты сканирований
   - Screenshots
   - Логи

3. **Оценить статус**
   - ✅ Полностью соответствует
   - ⚠️ Частично соответствует
   - ❌ Не соответствует
   - ➖ Не применимо

4. **Документировать**
   - Записать обоснование оценки
   - Указать ссылки на доказательства
   - Описать выявленные проблемы

### 4.3. Расчет процента соответствия

```python
#!/usr/bin/env python3
# calculate-compliance.py

def calculate_compliance(checklist_results):
    """
    Расчет процента соответствия

    Args:
        checklist_results: dict с результатами чек-листа
        {
            'ИА.1': 'compliant',
            'ИА.2': 'partial',
            'УД.1': 'non-compliant',
            'УД.2': 'not-applicable',
            ...
        }
    """
    status_weights = {
        'compliant': 1.0,
        'partial': 0.5,
        'non-compliant': 0.0,
        'not-applicable': None  # Не учитывается
    }

    applicable_count = 0
    weighted_sum = 0

    for req, status in checklist_results.items():
        weight = status_weights.get(status)
        if weight is not None:
            applicable_count += 1
            weighted_sum += weight

    if applicable_count == 0:
        return 0

    compliance_percentage = (weighted_sum / applicable_count) * 100
    return compliance_percentage

# Пример
results = {
    'ИА.1': 'compliant',
    'ИА.2': 'compliant',
    'УД.1': 'partial',
    'УД.2': 'non-compliant',
    'УД.3': 'compliant',
}

percentage = calculate_compliance(results)
print(f"Соответствие: {percentage:.1f}%")
```

---

## ФАЗА 5: Оценка рисков

См. skill `fstec-container-requirements` раздел "Оценка рисков" и агент `risk-assessor`.

**Ключевые шаги:**

1. Идентификация активов
2. Выявление угроз и уязвимостей
3. Расчет уровня риска (Вероятность × Воздействие)
4. Приоритизация рисков
5. Разработка мер по снижению

---

## ФАЗА 6: Документирование

### 6.1. Структура итоговых документов

```
final-reports/
├── 01-audit-conclusion.md              # Аудиторское заключение
├── 02-technical-analysis.md            # Технический отчет
├── 03-compliance-matrix.md             # Матрица соответствия
├── 04-risk-assessment.md               # Оценка рисков
├── 05-remediation-plan.md              # План мероприятий
├── 06-executive-summary.md             # Сводка для руководства
└── appendices/                         # Приложения
    ├── evidence/
    │   ├── configurations/
    │   ├── scan-results/
    │   └── screenshots/
    ├── scripts/
    │   ├── collect-data.sh
    │   ├── analyze-security.sh
    │   └── check-compliance.sh
    └── references/
        ├── fstec-requirements.pdf
        └── best-practices.md
```

### 6.2. Процесс создания отчетов

1. **Сбор всех данных**
   - Результаты технического анализа
   - Заполненный чек-лист
   - Оценка рисков
   - Доказательства

2. **Генерация черновиков**
   ```bash
   /generate-compliance-report \
     --type all \
     --input ./collected-data \
     --output ./draft-reports
   ```

3. **Проверка и редактирование**
   - Проверка полноты информации
   - Корректировка формулировок
   - Проверка ссылок и форматирования

4. **Рецензирование**
   - Peer review техническим экспертом
   - Проверка экспертом по ФСТЭК
   - Юридическая проверка (если требуется)

5. **Финализация**
   - Внесение правок
   - Добавление подписей
   - Экспорт в PDF

### 6.3. Контроль качества отчетов

**Чек-лист качества отчета:**

- [ ] Все обязательные разделы присутствуют
- [ ] Все таблицы корректно отформатированы
- [ ] Все ссылки на доказательства рабочие
- [ ] Нет противоречий между разделами
- [ ] Используется единая терминология
- [ ] Нумерация требований корректна
- [ ] Расчеты проверены
- [ ] Нет грамматических ошибок
- [ ] Подписи и даты проставлены
- [ ] Приложения прикреплены

---

## ФАЗА 7: Верификация и Follow-up

### 7.1. Внутренняя верификация

**Перед предоставлением отчета:**

1. **Техническая верификация**
   - Повторное выполнение ключевых проверок
   - Валидация выводов
   - Проверка воспроизводимости результатов

2. **Процессная верификация**
   - Все этапы методологии пройдены
   - Документация полная
   - Требуемые подписи получены

3. **Тестирование рекомендаций**
   - Рекомендации реалистичны и выполнимы
   - Оценка трудозатрат корректна
   - Нет конфликтующих рекомендаций

### 7.2. Презентация результатов

**Структура презентации:**

```markdown
# Презентация результатов анализа

## Слайд 1: Заголовок
- Название проекта
- Дата
- Команда

## Слайд 2: Executive Summary
- Общий процент соответствия
- Топ-3 критичных проблем
- Рекомендуемые сроки

## Слайд 3-4: Детальные результаты
- Диаграмма соответствия по категориям
- Распределение по критичности

## Слайд 5: Риски
- Топ-5 рисков
- Матрица рисков

## Слайд 6: Roadmap
- План мероприятий
- Timeline

## Слайд 7: Q&A
```

### 7.3. План повторного аудита

**После устранения несоответствий:**

1. **Определить scope повторной проверки**
   - Какие несоответствия должны быть устранены
   - Какие требования проверять повторно

2. **Запланировать повторный аудит**
   - Через 1 месяц для критичных
   - Через 3 месяца для высоких
   - Через 6 месяцев для средних

3. **Провести целевую проверку**
   - Фокус только на устраненных проблемах
   - Сбор новых доказательств
   - Обновление матрицы соответствия

4. **Финальное заключение**
   - Обновленный процент соответствия
   - Статус готовности к сертификации
   - Остаточные риски

---

## Best Practices

### DO (Рекомендуется)

✅ Автоматизировать сбор данных где возможно
✅ Версионировать все отчеты и доказательства
✅ Документировать каждый шаг процесса
✅ Использовать скриншоты для визуальных доказательств
✅ Сохранять даты и версии всех проверенных компонентов
✅ Проводить peer review результатов
✅ Поддерживать объективность оценки

### DON'T (Не рекомендуется)

❌ Полагаться только на ручные проверки
❌ Пропускать документирование промежуточных результатов
❌ Делать предположения без проверки
❌ Игнорировать "мелкие" несоответствия
❌ Завышать или занижать оценки
❌ Предоставлять отчеты без проверки
❌ Забывать про follow-up после устранения

---

## Чек-лист полной методологии

### Подготовка
- [ ] Scope определен и согласован
- [ ] Команда сформирована
- [ ] Инструменты установлены и протестированы
- [ ] Timeline утвержден

### Сбор информации
- [ ] Метаданные системы собраны
- [ ] Конфигурации безопасности экспортированы
- [ ] Список образов получен
- [ ] Архитектура задокументирована

### Технический анализ
- [ ] Все образы просканированы
- [ ] SecurityContext проанализирован
- [ ] RBAC проверен
- [ ] Network Policies оценены
- [ ] Логирование проверено

### Оценка соответствия
- [ ] Чек-лист заполнен для всех требований
- [ ] Доказательства собраны
- [ ] Статусы присвоены
- [ ] Процент соответствия рассчитан

### Оценка рисков
- [ ] Активы идентифицированы
- [ ] Угрозы и уязвимости выявлены
- [ ] Риски рассчитаны
- [ ] Приоритизация выполнена

### Документирование
- [ ] Все отчеты сгенерированы
- [ ] Качество отчетов проверено
- [ ] Приложения прикреплены
- [ ] Финальные версии готовы

### Верификация
- [ ] Внутренняя проверка пройдена
- [ ] Результаты презентованы
- [ ] План повторного аудита создан
- [ ] Follow-up запланирован

---

## Справочные материалы

### Скрипты автоматизации
- [Скрипт сбора данных Kubernetes](assets/scripts/collect-k8s-data.sh)
- [Скрипт анализа безопасности](assets/scripts/analyze-security.sh)
- [Скрипт генерации отчетов](assets/scripts/generate-reports.sh)

### Шаблоны
- [Шаблон программы аудита](assets/templates/audit-program-template.md)
- [Шаблон чек-листа](assets/templates/checklist-template.md)
- [Шаблон презентации](assets/templates/presentation-template.md)

### Инструкции
- [Установка инструментов](references/tools-installation.md)
- [Настройка окружения](references/environment-setup.md)
- [Troubleshooting](references/troubleshooting.md)
