---
name: fstec-container-requirements
description: Детальная база знаний по требованиям ФСТЭК России к безопасности информации в средствах контейнеризации (Приказ № 118 от 04.07.2022). Use when analyzing FSTEC compliance, evaluating container security requirements, or preparing compliance documentation.
---

# Требования ФСТЭК к средствам контейнеризации

## Обязательные правила вывода
- Всегда отвечай **на русском**.
- Сохраняй артефакты в `outputs/fstec-security-analysis/skills/fstec-container-requirements/{timestamp}_{кратко}.md` через Write tool; обновляй один файл по итерациям.
- Формат: цель/контекст → требования 118/угрозы → контролы/статус → меры/алерты → TODO → изменения vs прошлой версии.

## 3-итерационный контур
1) **Диагностика (1–2 ч):** категория/класс (УЗ, КИИ/ПДн), модель угроз, компоненты (control/worker/registry/CI-CD), текущие контроли/политики, регуляторика (118/17/21). Черновой бриф + risk log.
2) **Дизайн (2–3 ч):** маппинг требований 118 на компоненты, меры (IAM/Network/Data/CI-CD/Monitoring), автоматизация (policy-as-code), артефакты/доказательства, метрики/алерты. Таблица контролей/владельцев/сроков.
3) **Верификация (1–2 ч):** аудит/тесты, контрольные точки, обновление логов/TODO/изменений.

## Когда использовать этот skill

- При проведении анализа соответствия системы контейнеризации требованиям ФСТЭК
- При проектировании защищенной архитектуры контейнерной инфраструктуры
- При подготовке к сертификации системы
- При разработке политик безопасности для контейнерных платформ
- При оценке рисков и аудите безопасности

## Входы (собери до старта)
- Категория КИИ/ПДн/УЗ, модель угроз, архитектура контейнерной платформы и CI/CD, текущие СЗИ/контроли.
- Перечень активов/данных (PII/гостайна), контуры/окружения, регистры/поставки.

## Выходы (обязательно зафиксировать)
- Матрица требований 118 → контролы/доказательства, план устранения несоответствий.
- Политики/процедуры (RBAC/NP/шифрование/логирование/CI-CD/registry), алерты/пороги, RACI.
- TODO/владельцы/сроки, decision/risk log, изменения vs прошлой версии.

## Метрики/алерты
- % выполненных контролей, время устранения, критичные несоответствия, повторные нарушения.
- Алерты: публичные ресурсы, отсутствие шифрования/логирования/MFA, просроченные меры/сканы, дрейф конфигов.

## Качество ответа (checklist)
- Привязка к 118 и модели угроз, покрыты control/worker/registry/CI-CD.
- Доказательства и меры перечислены; план remediation с владельцами/сроками.
- Алерты/пороги и логи/TODO обновлены; изменения зафиксированы.

## Red Flags
- Нет модели угроз/категории; нет маппинга на 118; нет доказательств.
- Нет плана устранения/владельцев; алерты/пороги отсутствуют.

## Детализация контролей (ориентиры)
- **RBAC/идентификация:** роли/группы/сервис-аккаунты, MFA, ротация ключей, аудит доступа, break-glass.
- **Сеть:** обязательные NP, firewall, ingress/egress ограничения, mTLS/TLS, DNS/DNSSEC, time sync.
- **Хранение/данные:** шифрование at rest/in transit, бэкапы, контроль снапшотов, PII/гостайна защита.
- **Образы/registry:** подпись/скан, политика допуска (block list/allow list), приватность, ретеншн, мониторинг push/pull.
- **CI/CD:** секреты/хранилища, изоляция пайплайнов, SBOM, политика зависимостей, MFA/аудиты, блок критичных CVE.
- **Логирование/мониторинг:** централизованный сбор, защита логов, ретеншн, синхронизация времени, SIEM.
- **Обновления/патчи:** частота сканов, SLA фиксов, контроль дрейфа IaC/конфигов.
- **IR/BCP:** планы реагирования, обучение, тесты, эскалации, постмортемы.
- **RedOS 7/8:** использование сертифицированных репозиториев/СКЗИ, SELinux enforcing, auditd, sysctl hardening, контроль версий ядра/модулей для совместимости с контейнерным стеком, подписанные пакеты.
- **Облако (аттестация ФСТЭК):** изоляция тенантов/виртуализаций, доверенный гипервизор, шифрование каналов/хранилищ, журналирование админов, перечень сертифицированных СЗИ и актуальных сертификатов, процедуры аттестации/контроля изменений.
- **Среда виртуализации:** защита гипервизора и управляющих узлов, сегментация mgmt/tenant/storage, защищённые миграции, контроль side-channel/SMT, шифрование VM/backup, подпись образов, аудит админских действий, соответствие 17/21/118.

## Нормативная база

**Основной документ:** Приказ ФСТЭК России от 4 июля 2022 г. № 118 "Требования по безопасности информации к средствам контейнеризации"

**Назначение:** Установление обязательных требований по безопасности информации, которым должны удовлетворять средства контейнеризации, используемые для обработки информации, содержащей сведения, составляющие государственную тайну, и иной информации ограниченного доступа.

## Уровни защищенности

Средства контейнеризации классифицируются по 4 уровням защищенности (от высшего к низшему):

### УЗ-1 (Уровень защищенности 1)
**Применение:** Обработка информации, составляющей государственную тайну особой важности

**Характеристики:**
- Максимальные требования ко всем категориям защиты
- Обязательная мандатная модель управления доступом
- Усиленная криптографическая защита
- Полный аудит всех событий безопасности
- Обязательная сертификация всех компонентов

### УЗ-2 (Уровень защищенности 2)
**Применение:** Информация, составляющая государственную тайну совершенно секретного характера

**Характеристики:**
- Строгие требования к большинству категорий
- Мандатная или дискреционная модель управления доступом
- Криптографическая защита критичных данных
- Расширенный аудит событий безопасности

### УЗ-3 (Уровень защищенности 3)
**Применение:** Информация, составляющая государственную тайну секретного характера

**Характеристики:**
- Базовые требования к основным категориям защиты
- Дискреционная модель управления доступом
- Избирательная криптографическая защита
- Аудит ключевых событий безопасности

### УЗ-4 (Уровень защищенности 4)
**Применение:** Конфиденциальная информация, служебная тайна, персональные данные

**Характеристики:**
- Минимально необходимые требования
- Базовая модель управления доступом
- Защита критичных данных
- Регистрация основных событий

## Категории требований по безопасности

## 1. ИДЕНТИФИКАЦИЯ И АУТЕНТИФИКАЦИЯ (ИА)

### ИА.1 Идентификация субъектов доступа

**Требование:** Средство контейнеризации должно обеспечивать уникальную идентификацию субъектов доступа (пользователей, процессов, контейнеров).

**Применимость по уровням:**
- УЗ-1: ✅ Обязательно
- УЗ-2: ✅ Обязательно
- УЗ-3: ✅ Обязательно
- УЗ-4: ✅ Обязательно

**Техническая реализация:**

**Kubernetes:**
```yaml
# ServiceAccount для каждого приложения
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: production
---
# Pod с явным ServiceAccount
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  serviceAccountName: app-service-account
  automountServiceAccountToken: false  # Отключить если токен не нужен
```

**Docker:**
```yaml
# docker-compose.yml
services:
  app:
    image: app:latest
    user: "1000:1000"  # Явный non-root пользователь
    labels:
      - "security.owner=app-team"
      - "security.appid=app-001"
```

**Критерии соответствия:**
- ✅ Каждый контейнер имеет уникальный идентификатор
- ✅ Процессы внутри контейнера идентифицируемы
- ✅ Пользователи системы контейнеризации уникально идентифицированы
- ✅ Отключена возможность анонимного доступа

### ИА.2 Аутентификация субъектов доступа

**Требование:** Средство контейнеризации должно обеспечивать аутентификацию субъектов доступа перед предоставлением доступа к ресурсам.

**Применимость по уровням:**
- УЗ-1: ✅ Усиленная (многофакторная)
- УЗ-2: ✅ Усиленная
- УЗ-3: ✅ Обязательно
- УЗ-4: ✅ Обязательно

**Техническая реализация:**

**Kubernetes:**
```yaml
# Интеграция с OIDC провайдером
apiVersion: v1
kind: Config
users:
- name: admin-user
  user:
    auth-provider:
      name: oidc
      config:
        client-id: kubernetes
        client-secret: secret
        id-token: <токен>
        idp-issuer-url: https://keycloak.example.ru/auth/realms/k8s
```

**X.509 сертификаты для аутентификации:**
```bash
# Создание клиентского сертификата
openssl req -new -key user.key -out user.csr -subj "/CN=username/O=developers"

# Подписание сертификата CA кластера
openssl x509 -req -in user.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out user.crt -days 365
```

**Docker:**
```bash
# Настройка TLS аутентификации для Docker daemon
dockerd --tlsverify \
  --tlscacert=/etc/docker/ca.pem \
  --tlscert=/etc/docker/server-cert.pem \
  --tlskey=/etc/docker/server-key.pem \
  -H=0.0.0.0:2376
```

**Критерии соответствия:**
- ✅ Обязательная аутентификация перед доступом к API
- ✅ Использование сильных методов аутентификации (сертификаты, OAuth2/OIDC)
- ✅ Для УЗ-1, УЗ-2: многофакторная аутентификация
- ✅ Невозможность обхода аутентификации

### ИА.3 Управление учетными записями

**Требование:** Обеспечение создания, модификации, блокировки и удаления учетных записей.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Автоматическое управление ServiceAccounts:**
```yaml
# Автоматическое создание с аннотациями
apiVersion: v1
kind: ServiceAccount
metadata:
  name: temp-job-sa
  namespace: jobs
  annotations:
    security.fstec/expires: "2025-12-31"
    security.fstec/owner: "devops-team"
    security.fstec/purpose: "batch-processing"
```

**Критерии соответствия:**
- ✅ Процедура создания учетных записей
- ✅ Регулярный пересмотр активных учетных записей
- ✅ Автоматическая блокировка неиспользуемых учетных записей
- ✅ Журналирование операций с учетными записями

---

## 2. УПРАВЛЕНИЕ ДОСТУПОМ (УД)

### УД.1 Дискреционное управление доступом

**Требование:** Контроль доступа субъектов к объектам на основе списков управления доступом.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Kubernetes RBAC:**
```yaml
# Role для чтения подов в namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding для назначения роли
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: ServiceAccount
  name: monitoring-sa
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Критерии соответствия:**
- ✅ RBAC включен и настроен
- ✅ Принцип наименьших привилегий (least privilege)
- ✅ Отсутствие избыточных прав
- ✅ Запрет wildcard permissions для продакшена

### УД.2 Мандатное управление доступом

**Требование:** Контроль доступа на основе меток конфиденциальности (для УЗ-1, УЗ-2).

**Применимость:**
- УЗ-1: ✅ Обязательно
- УЗ-2: ✅ Обязательно
- УЗ-3: ➖ Опционально
- УЗ-4: ➖ Не требуется

**Техническая реализация:**

**Использование Pod Security Standards:**
```yaml
# Namespace с enforced уровнем безопасности
apiVersion: v1
kind: Namespace
metadata:
  name: classified-zone
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    security.fstec/classification: secret  # Метка конфиденциальности
```

**SELinux/AppArmor для мандатного контроля:**
```yaml
# Pod с SELinux контекстом
apiVersion: v1
kind: Pod
metadata:
  name: classified-app
spec:
  securityContext:
    seLinuxOptions:
      level: "s0:c123,c456"  # MLS уровень конфиденциальности
  containers:
  - name: app
    image: classified-app:latest
```

**Критерии соответствия:**
- ✅ Реализован механизм меток конфиденциальности
- ✅ Невозможность доступа с низшего уровня к высшему
- ✅ Контроль передачи информации между уровнями
- ✅ Аудит попыток нарушения мандатной политики

### УД.3 Изоляция процессов и контейнеров

**Требование:** Обеспечение изоляции процессов контейнеров друг от друга и от хост-системы.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**SecurityContext с полной изоляцией:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: isolated-app
spec:
  hostNetwork: false  # Запрет использования host network
  hostPID: false      # Запрет видимости host PID namespace
  hostIPC: false      # Запрет использования host IPC
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
      privileged: false
```

**Namespace изоляция:**
```yaml
# Использование User Namespaces (Docker)
{
  "userns-remap": "default"
}
```

**Критерии соответствия:**
- ✅ Отсутствие привилегированных контейнеров
- ✅ Запрет hostNetwork, hostPID, hostIPC
- ✅ Использование namespace изоляции
- ✅ Применение seccomp и AppArmor/SELinux профилей

### УД.4 Управление доступом к ресурсам контейнеров

**Требование:** Контроль доступа к CPU, памяти, хранилищу контейнеров.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Resource Limits и Quotas:**
```yaml
# Pod с ограничениями ресурсов
apiVersion: v1
kind: Pod
metadata:
  name: resource-limited
spec:
  containers:
  - name: app
    image: app:latest
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
---
# ResourceQuota для namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
```

**Критерии соответствия:**
- ✅ Все контейнеры имеют resource limits
- ✅ Настроены ResourceQuotas для namespaces
- ✅ Невозможность DoS через потребление ресурсов
- ✅ Мониторинг использования ресурсов

### УД.5 Контроль сетевого взаимодействия

**Требование:** Ограничение сетевого взаимодействия между контейнерами.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Network Policies:**
```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
# Разрешение только необходимого трафика
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

**Критерии соответствия:**
- ✅ Включены Network Policies
- ✅ Default deny политика
- ✅ Явное разрешение только необходимого трафика
- ✅ Микросегментация на уровне приложений

---

## 3. РЕГИСТРАЦИЯ И УЧЕТ (РУ)

### РУ.1 Регистрация событий безопасности

**Требование:** Регистрация событий, связанных с безопасностью информации.

**Применимость:** Все уровни ✅

**События, подлежащие регистрации:**
- Попытки доступа (успешные и неуспешные)
- Изменения конфигурации
- Создание/удаление контейнеров и подов
- Изменения в RBAC
- Аномальная активность
- Изменения в образах

**Техническая реализация:**

**Kubernetes Audit Logging:**
```yaml
# kube-apiserver audit policy
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
# Логировать все запросы на metadata уровне
- level: Metadata
  omitStages:
  - RequestReceived
# Детальное логирование для секретов
- level: RequestResponse
  resources:
  - group: ""
    resources: ["secrets"]
# Детальное логирование для RBAC
- level: RequestResponse
  verbs: ["create", "update", "patch", "delete"]
  resources:
  - group: "rbac.authorization.k8s.io"
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
```

**Централизованное логирование:**
```yaml
# FluentBit для сбора логов
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush        5
        Daemon       Off
        Log_Level    info

    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*

    [OUTPUT]
        Name              forward
        Match             *
        Host              elasticsearch.logging.svc
        Port              24224
```

**Критерии соответствия:**
- ✅ Включен audit logging
- ✅ Логируются все критичные события
- ✅ Логи отправляются в централизованное хранилище
- ✅ Логи защищены от модификации и удаления

### РУ.2 Хранение и защита журналов

**Требование:** Обеспечение целостности и защиты журналов регистрации.

**Применимость:** Все уровни ✅

**Требования к хранению:**
- УЗ-1: минимум 12 месяцев
- УЗ-2: минимум 12 месяцев
- УЗ-3: минимум 6 месяцев
- УЗ-4: минимум 3 месяца

**Техническая реализация:**

**Защищенное хранилище логов:**
```yaml
# PersistentVolume с WORM (Write Once Read Many)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: audit-logs-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: audit-storage
  mountOptions:
    - ro  # Read-only после записи
```

**Критерии соответствия:**
- ✅ Логи хранятся требуемый период
- ✅ Защита от несанкционированного удаления
- ✅ Контроль целостности логов (хеши, подписи)
- ✅ Резервное копирование логов

### РУ.3 Анализ событий безопасности

**Требование:** Анализ зарегистрированных событий для выявления инцидентов.

**Применимость:**
- УЗ-1: ✅ Автоматический + ручной
- УЗ-2: ✅ Автоматический + ручной
- УЗ-3: ✅ Автоматический
- УЗ-4: ✅ Базовый

**Техническая реализация:**

**Falco для runtime security:**
```yaml
# Falco rules для обнаружения аномалий
- rule: Container with Sensitive Mount
  desc: Detect container mounting sensitive host paths
  condition: >
    container and
    (fd.name startswith /etc or
     fd.name startswith /root or
     fd.name startswith /var/run/docker.sock)
  output: >
    Container mounting sensitive path
    (user=%user.name container=%container.name path=%fd.name)
  priority: WARNING
```

**Критерии соответствия:**
- ✅ Автоматический анализ событий
- ✅ Алерты на критичные события
- ✅ Регулярный ручной анализ (для УЗ-1, УЗ-2)
- ✅ Реагирование на инциденты

---

## 4. АНТИВИРУСНАЯ ЗАЩИТА (АВ)

### АВ.1 Обнаружение вредоносного кода

**Требование:** Обнаружение вредоносного кода в образах и файловой системе контейнеров.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Сканирование образов:**
```bash
# Trivy сканирование перед deploy
trivy image --severity HIGH,CRITICAL registry.example.ru/app:v1.0

# Автоматическое сканирование в CI/CD
# .gitlab-ci.yml
container_scanning:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

**Admission Controller для проверки образов:**
```yaml
# OPA policy для блокировки непроверенных образов
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    image := input.request.object.spec.containers[_].image
    not image_scanned(image)
    msg := sprintf("Image %v must be scanned before deployment", [image])
}

image_scanned(image) {
    # Проверка наличия метки о сканировании
    scan_result := data.scans[image]
    scan_result.clean == true
}
```

**Критерии соответствия:**
- ✅ Все образы сканируются перед развертыванием
- ✅ Блокировка образов с критичными уязвимостями
- ✅ Регулярное обновление антивирусных баз
- ✅ Периодическое сканирование running контейнеров

### АВ.2 Обновление антивирусных баз

**Требование:** Регулярное обновление сигнатур и баз данных уязвимостей.

**Применимость:** Все уровни ✅

**Критерии соответствия:**
- ✅ Автоматическое обновление баз CVE
- ✅ Периодичность: ежедневно или чаще
- ✅ Мониторинг статуса обновлений

---

## 5. ОБНАРУЖЕНИЕ ВТОРЖЕНИЙ (ОВ)

### ОВ.1 Обнаружение аномальной активности

**Требование:** Мониторинг и обнаружение аномального поведения контейнеров.

**Применимость:**
- УЗ-1: ✅ Обязательно (runtime + network)
- УЗ-2: ✅ Обязательно
- УЗ-3: ✅ Рекомендуется
- УЗ-4: ⚠️ Базовый уровень

**Техническая реализация:**

**Falco для runtime anomaly detection:**
```yaml
# Falco правила
customRules:
  rules-suspicious-activity.yaml: |-
    - rule: Terminal shell in container
      desc: A shell was spawned in a container
      condition: >
        container and
        proc.name in (shell_binaries) and
        not proc.pname in (shell_binaries)
      output: >
        Shell spawned in container
        (user=%user.name container=%container.name shell=%proc.name)
      priority: WARNING

    - rule: Unexpected network connection
      desc: Container making unexpected outbound connection
      condition: >
        outbound and
        container and
        not allowed_outbound_destinations
      output: >
        Unexpected outbound connection
        (container=%container.name dest=%fd.rip:%fd.rport)
      priority: WARNING
```

**Критерии соответствия:**
- ✅ Включен runtime security мониторинг
- ✅ Обнаружение подозрительных процессов
- ✅ Мониторинг сетевых соединений
- ✅ Алертинг при обнаружении аномалий

---

## 6. КОНТРОЛЬ ЦЕЛОСТНОСТИ (КЦ)

### КЦ.1 Контроль целостности образов

**Требование:** Проверка целостности образов контейнеров перед запуском.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Подписание образов с Cosign:**
```bash
# Подписание образа
cosign sign --key cosign.key registry.example.ru/app:v1.0

# Проверка подписи
cosign verify --key cosign.pub registry.example.ru/app:v1.0
```

**Admission Controller для проверки подписей:**
```yaml
# Kyverno policy для проверки подписей
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-signature
    match:
      resources:
        kinds:
        - Pod
    verifyImages:
    - image: "registry.example.ru/*"
      key: |-
        -----BEGIN PUBLIC KEY-----
        [публичный ключ]
        -----END PUBLIC KEY-----
```

**Pull by digest:**
```yaml
# Использование SHA256 digest вместо тегов
spec:
  containers:
  - name: app
    image: registry.example.ru/app@sha256:abc123...
    imagePullPolicy: Always
```

**Критерии соответствия:**
- ✅ Все образы подписаны
- ✅ Проверка подписи перед запуском
- ✅ Использование digest вместо тегов
- ✅ Блокировка неподписанных образов

### КЦ.2 Контроль целостности исполняемых файлов

**Требование:** Мониторинг изменений исполняемых файлов в контейнерах.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Read-only файловая система:**
```yaml
spec:
  containers:
  - name: app
    image: app:latest
    securityContext:
      readOnlyRootFilesystem: true
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache
  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

**Критерии соответствия:**
- ✅ Использование readOnlyRootFilesystem
- ✅ Мониторинг изменений файлов (Falco)
- ✅ Алерты при модификации исполняемых файлов
- ✅ Immutable infrastructure подход

---

## 7. ЗАЩИТА МАШИННЫХ НОСИТЕЛЕЙ (ЗМ)

### ЗМ.1 Шифрование данных в томах

**Требование:** Защита данных в persistent volumes с помощью шифрования.

**Применимость:**
- УЗ-1: ✅ Обязательно (сертифицированные средства)
- УЗ-2: ✅ Обязательно
- УЗ-3: ✅ Для конфиденциальных данных
- УЗ-4: ⚠️ Рекомендуется

**Техническая реализация:**

**Encryption at rest:**
```yaml
# StorageClass с шифрованием
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: encrypted-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  encrypted: "true"
  kmsKeyId: arn:aws:kms:region:account:key/key-id
```

**Секреты в etcd (Kubernetes):**
```yaml
# kube-apiserver configuration
apiVersion: v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: <base64 encoded key>
    - identity: {}
```

**Критерии соответствия:**
- ✅ Шифрование PersistentVolumes
- ✅ Шифрование Secrets в etcd
- ✅ Использование сертифицированных средств (для УЗ-1)
- ✅ Управление ключами шифрования

---

## 8. ЗАЩИТА ТЕХНИЧЕСКИХ СРЕДСТВ (ЗТС)

### ЗТС.1 Защита среды выполнения контейнеров

**Требование:** Обеспечение защиты хост-системы от контейнеров.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Запрет capabilities:**
```yaml
spec:
  containers:
  - name: app
    securityContext:
      capabilities:
        drop:
          - ALL  # Удалить все capabilities
        add:
          - NET_BIND_SERVICE  # Добавить только необходимые
```

**Seccomp профиль:**
```yaml
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/audit.json
```

**Критерии соответствия:**
- ✅ Минимальный набор capabilities
- ✅ Применение seccomp профилей
- ✅ SELinux/AppArmor включены
- ✅ Запрет hostPath volumes (или строгие ограничения)

---

## 9. ЗАЩИТА ИНФОРМАЦИОННОЙ СИСТЕМЫ (ЗИС)

### ЗИС.1 Управление обновлениями

**Требование:** Регулярное обновление компонентов системы контейнеризации.

**Применимость:** Все уровни ✅

**Критерии соответствия:**
- ✅ Регулярное обновление платформы (Kubernetes, Docker)
- ✅ Автоматизированное сканирование образов на уязвимости
- ✅ Процедура экстренного применения патчей
- ✅ Тестирование обновлений перед продакшеном

### ЗИС.2 Резервное копирование

**Требование:** Резервное копирование критичных данных и конфигураций.

**Применимость:** Все уровни ✅

**Техническая реализация:**

**Velero для backup Kubernetes:**
```bash
# Создание backup
velero backup create production-backup \
  --include-namespaces production \
  --storage-location default

# Restore из backup
velero restore create --from-backup production-backup
```

**Критерии соответствия:**
- ✅ Регулярное резервное копирование etcd
- ✅ Backup persistent volumes
- ✅ Backup конфигураций и секретов
- ✅ Тестирование восстановления

---

## Матрица применимости требований по уровням

| Требование | УЗ-1 | УЗ-2 | УЗ-3 | УЗ-4 |
|------------|------|------|------|------|
| **ИА.1** Идентификация | ✅ | ✅ | ✅ | ✅ |
| **ИА.2** Аутентификация | ✅ MFA | ✅ Усиленная | ✅ | ✅ |
| **ИА.3** Управление УЗ | ✅ | ✅ | ✅ | ✅ |
| **УД.1** Дискреционное УД | ✅ | ✅ | ✅ | ✅ |
| **УД.2** Мандатное УД | ✅ | ✅ | ⚠️ | ➖ |
| **УД.3** Изоляция | ✅ Полная | ✅ Полная | ✅ | ✅ |
| **УД.4** Управление ресурсами | ✅ | ✅ | ✅ | ✅ |
| **УД.5** Сетевой контроль | ✅ Полный | ✅ Полный | ✅ | ✅ |
| **РУ.1** Регистрация | ✅ Полная | ✅ Полная | ✅ | ✅ |
| **РУ.2** Защита логов | ✅ 12м | ✅ 12м | ✅ 6м | ✅ 3м |
| **РУ.3** Анализ событий | ✅ Авто+Ручн | ✅ Авто+Ручн | ✅ Авто | ✅ |
| **АВ.1** Антивирус | ✅ | ✅ | ✅ | ✅ |
| **АВ.2** Обновление баз | ✅ | ✅ | ✅ | ✅ |
| **ОВ.1** Обнаружение вторжений | ✅ | ✅ | ⚠️ | ⚠️ |
| **КЦ.1** Целостность образов | ✅ Подпись | ✅ Подпись | ✅ Digest | ✅ |
| **КЦ.2** Целостность файлов | ✅ | ✅ | ✅ | ✅ |
| **ЗМ.1** Шифрование | ✅ Сертиф. | ✅ | ✅ Выб. | ⚠️ |
| **ЗТС.1** Защита runtime | ✅ Полная | ✅ Полная | ✅ | ✅ |
| **ЗИС.1** Обновления | ✅ | ✅ | ✅ | ✅ |
| **ЗИС.2** Резервирование | ✅ | ✅ | ✅ | ✅ |

**Легенда:**
- ✅ Обязательно
- ⚠️ Рекомендуется / Частично
- ➖ Не требуется

## Рекомендуемые инструменты и технологии

### Безопасность образов
- **Trivy**: Сканирование образов на уязвимости
- **Grype**: Быстрое сканирование
- **Cosign**: Подписание и верификация образов
- **Notary**: Docker Content Trust

### Runtime Security
- **Falco**: Обнаружение аномального поведения
- **Sysdig**: Мониторинг и форензика
- **Tracee**: eBPF-based security

### Policy Management
- **OPA (Open Policy Agent)**: Гибкие политики безопасности
- **Kyverno**: Kubernetes-native policy engine
- **jsPolicy**: JavaScript-based policies

### Network Security
- **Calico**: Network policies и микросегментация
- **Cilium**: eBPF-based networking
- **Istio**: Service mesh с mTLS

### Secrets Management
- **HashiCorp Vault**: Централизованное управление секретами
- **Sealed Secrets**: Шифрованные secrets для Git
- **External Secrets Operator**: Интеграция с внешними системами

### Audit & Compliance
- **Kube-bench**: CIS Kubernetes Benchmark
- **Kubescape**: Комплексное сканирование безопасности
- **Polaris**: Best practices validation

## Справочные материалы

### Документы ФСТЭК
- [Требования к средствам контейнеризации](references/fstec-118-requirements.md)
- [Методические рекомендации](references/fstec-methodological-guidelines.md)

### Шаблоны документов
- [Шаблон аудиторского заключения](assets/templates/audit-conclusion-template.md)
- [Шаблон матрицы соответствия](assets/templates/compliance-matrix-template.md)
- [Шаблон плана мероприятий](assets/templates/remediation-plan-template.md)

### Примеры конфигураций
- [Безопасный SecurityContext](assets/examples/secure-security-context.yaml)
- [Network Policies примеры](assets/examples/network-policies.yaml)
- [RBAC best practices](assets/examples/rbac-examples.yaml)

### Дополнительные справочники
- [Baseline RedOS 7/8 для узлов контейнеризации](references/redos-7-8-baseline.md)
- [Требования ФСТЭК к облачным средам](references/fstec-cloud-requirements.md)
- [Чек-лист RedOS 7/8](assets/redos-node-checklist.md)
- [Чек-лист облака для аттестации](assets/cloud-attestation-checklist.md)
- [Требования к виртуализации](references/fstec-virtualization-requirements.md)
- [Чек-лист виртуализации](assets/virtualization-security-checklist.md)
