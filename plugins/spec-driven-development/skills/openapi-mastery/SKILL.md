---
name: openapi-mastery
description: Мастерство OpenAPI 3.1 спецификаций — полное руководство по проектированию, валидации, кодогенерации и документации REST API. Use when creating OpenAPI specs, validating API contracts, generating code from specs, or establishing API-first workflows.
---

# OpenAPI Mastery

Полное руководство по проектированию REST API с OpenAPI 3.1 — от базовых концепций до продвинутых паттернов, используемых в AWS, Google Cloud, Stripe и Twilio.

## Поддержка языков

- **Русский ввод** → Объяснения и примеры на **русском**
- **English input** → Explanations and examples in **English**
- Код и технические термины сохраняются в оригинале

**ВСЕ РЕЗУЛЬТАТЫ СОХРАНЯЮТСЯ В MARKDOWN НА РУССКОМ ЯЗЫКЕ**

## Когда использовать этот скилл

- Создание новых OpenAPI спецификаций
- Валидация и линтинг существующих спецификаций
- Генерация кода (клиенты, серверы, модели)
- Настройка API-first workflow
- Документирование REST API
- Миграция с OpenAPI 2.0 (Swagger) на 3.1
- Проектирование API для публичного использования

## Основные концепции

### OpenAPI 3.1 Structure

```yaml
# Полная структура OpenAPI 3.1 документа
openapi: 3.1.0  # Версия спецификации

# Метаинформация об API
info:
  title: "Название API"
  version: "1.0.0"
  description: "Описание API"
  termsOfService: "https://example.com/terms"
  contact:
    name: "API Support"
    email: "api@example.com"
    url: "https://example.com/support"
  license:
    name: "MIT"
    identifier: "MIT"  # SPDX identifier (новое в 3.1)

# JSON Schema dialect (новое в 3.1)
jsonSchemaDialect: "https://json-schema.org/draft/2020-12/schema"

# Серверы
servers:
  - url: "https://api.example.com/v1"
    description: "Production"
  - url: "https://staging-api.example.com/v1"
    description: "Staging"

# Пути (endpoints)
paths:
  /resources:
    get: ...
    post: ...

# Webhooks (новое в 3.1)
webhooks:
  orderCreated:
    post: ...

# Переиспользуемые компоненты
components:
  schemas: ...
  parameters: ...
  responses: ...
  requestBodies: ...
  headers: ...
  securitySchemes: ...
  links: ...
  callbacks: ...
  pathItems: ...  # новое в 3.1

# Безопасность
security:
  - bearerAuth: []

# Теги для группировки
tags:
  - name: "Resources"
    description: "Resource management"

# Внешняя документация
externalDocs:
  description: "Full documentation"
  url: "https://docs.example.com"
```

### Schema Design с JSON Schema 2020-12

```yaml
components:
  schemas:
    # Базовый объект
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
          description: "Уникальный идентификатор пользователя"
        email:
          type: string
          format: email
          description: "Email адрес"
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: "Полное имя"
        age:
          type: integer
          minimum: 0
          maximum: 150
          description: "Возраст"
        status:
          $ref: '#/components/schemas/UserStatus'
        roles:
          type: array
          items:
            $ref: '#/components/schemas/Role'
          minItems: 1
          uniqueItems: true
        metadata:
          type: object
          additionalProperties:
            type: string
          description: "Произвольные метаданные"
        preferences:
          $ref: '#/components/schemas/UserPreferences'
        createdAt:
          type: string
          format: date-time
          readOnly: true
      additionalProperties: false  # Строгая схема

    # Enum
    UserStatus:
      type: string
      enum:
        - ACTIVE
        - INACTIVE
        - SUSPENDED
        - DELETED
      default: ACTIVE
      description: "Статус аккаунта пользователя"

    # Nullable (новый синтаксис в 3.1)
    NullableString:
      type:
        - string
        - "null"

    # Composition: allOf (наследование)
    AdminUser:
      allOf:
        - $ref: '#/components/schemas/User'
        - type: object
          properties:
            permissions:
              type: array
              items:
                type: string

    # Composition: oneOf (один из вариантов)
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Dog'
        - $ref: '#/components/schemas/Cat'
      discriminator:
        propertyName: petType
        mapping:
          dog: '#/components/schemas/Dog'
          cat: '#/components/schemas/Cat'

    # Composition: anyOf (любой из вариантов)
    PaymentMethod:
      anyOf:
        - $ref: '#/components/schemas/CreditCard'
        - $ref: '#/components/schemas/BankTransfer'
        - $ref: '#/components/schemas/Crypto'

    # Pattern Properties (JSON Schema)
    DynamicObject:
      type: object
      patternProperties:
        "^x-":
          type: string
      additionalProperties: false

    # Константа (новое в 3.1)
    ApiVersion:
      const: "1.0.0"

    # If/Then/Else (JSON Schema)
    ConditionalSchema:
      type: object
      properties:
        type:
          type: string
        value:
          type: string
      if:
        properties:
          type:
            const: "percentage"
      then:
        properties:
          value:
            type: number
            minimum: 0
            maximum: 100
```

### Paths и Operations

```yaml
paths:
  /users:
    # Операция GET - список пользователей
    get:
      operationId: listUsers
      summary: "Получить список пользователей"
      description: |
        Возвращает paginated список пользователей.
        Поддерживает фильтрацию по статусу и поиск по имени.
      tags:
        - Users
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/PageSize'
        - $ref: '#/components/parameters/PageToken'
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/UserStatus'
          description: "Фильтр по статусу"
        - name: search
          in: query
          schema:
            type: string
            minLength: 2
          description: "Поиск по имени или email"
      responses:
        '200':
          description: "Успешный ответ"
          headers:
            X-Total-Count:
              schema:
                type: integer
              description: "Общее количество пользователей"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
              examples:
                default:
                  $ref: '#/components/examples/UserListExample'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    # Операция POST - создание пользователя
    post:
      operationId: createUser
      summary: "Создать пользователя"
      description: "Создаёт нового пользователя в системе"
      tags:
        - Users
      security:
        - bearerAuth:
            - users:write
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              minimal:
                summary: "Минимальный запрос"
                value:
                  email: "user@example.com"
                  name: "Иван Петров"
              full:
                summary: "Полный запрос"
                value:
                  email: "user@example.com"
                  name: "Иван Петров"
                  roles: ["user", "editor"]
                  metadata:
                    department: "Engineering"
      responses:
        '201':
          description: "Пользователь создан"
          headers:
            Location:
              schema:
                type: string
                format: uri
              description: "URL созданного ресурса"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: "Email уже существует"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                code: "EMAIL_EXISTS"
                message: "Пользователь с таким email уже существует"

  /users/{userId}:
    parameters:
      - $ref: '#/components/parameters/UserId'

    get:
      operationId: getUser
      summary: "Получить пользователя"
      tags:
        - Users
      responses:
        '200':
          description: "Успешный ответ"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      operationId: updateUser
      summary: "Обновить пользователя"
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
          application/merge-patch+json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: "Пользователь обновлён"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      operationId: deleteUser
      summary: "Удалить пользователя"
      tags:
        - Users
      responses:
        '204':
          description: "Пользователь удалён"
        '404':
          $ref: '#/components/responses/NotFound'
```

### Security Schemes

```yaml
components:
  securitySchemes:
    # JWT Bearer Token
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT токен аутентификации.

        **Получение токена:**
        ```bash
        curl -X POST https://api.example.com/auth/token \
          -d 'grant_type=client_credentials' \
          -d 'client_id=YOUR_CLIENT_ID' \
          -d 'client_secret=YOUR_CLIENT_SECRET'
        ```

        **Использование:**
        ```bash
        curl -H "Authorization: Bearer YOUR_TOKEN" \
          https://api.example.com/v1/users
        ```

    # API Key
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: |
        API ключ для машинной интеграции.
        Получить можно в Developer Portal.

    # OAuth 2.0
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          refreshUrl: https://auth.example.com/oauth/refresh
          scopes:
            users:read: "Чтение пользователей"
            users:write: "Создание и обновление пользователей"
            users:delete: "Удаление пользователей"
            admin: "Полный доступ"
        clientCredentials:
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            users:read: "Чтение пользователей"
            users:write: "Создание и обновление пользователей"

    # OpenID Connect
    openIdConnect:
      type: openIdConnect
      openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration

    # Mutual TLS
    mutualTLS:
      type: mutualTLS
      description: "mTLS для service-to-service"

# Применение безопасности
security:
  - bearerAuth: []
  - apiKey: []

# Или на уровне операции
paths:
  /public/health:
    get:
      security: []  # Публичный endpoint
  /admin/users:
    get:
      security:
        - oauth2:
            - admin
```

### Webhooks (OpenAPI 3.1)

```yaml
webhooks:
  orderCreated:
    post:
      operationId: onOrderCreated
      summary: "Событие создания заказа"
      description: |
        Вызывается когда создаётся новый заказ.

        **Настройка webhook:**
        ```bash
        curl -X POST https://api.example.com/webhooks \
          -H "Authorization: Bearer $TOKEN" \
          -d '{
            "url": "https://your-server.com/webhooks/orders",
            "events": ["order.created"]
          }'
        ```

        **Верификация подписи:**
        ```python
        import hmac
        import hashlib

        def verify_signature(payload, signature, secret):
            expected = hmac.new(
                secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(signature, expected)
        ```
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderCreatedEvent'
      responses:
        '200':
          description: "Webhook обработан"
        '400':
          description: "Ошибка обработки"
      security:
        - webhookSignature: []

  orderStatusChanged:
    post:
      operationId: onOrderStatusChanged
      summary: "Событие изменения статуса заказа"
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderStatusChangedEvent'
      responses:
        '200':
          description: "OK"
```

## Паттерны и практики

### Pagination Pattern

```yaml
components:
  schemas:
    # Cursor-based pagination (рекомендуется)
    PaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items:
            type: object
        pagination:
          type: object
          required:
            - hasMore
          properties:
            nextCursor:
              type: string
              nullable: true
              description: "Курсор для следующей страницы"
            prevCursor:
              type: string
              nullable: true
              description: "Курсор для предыдущей страницы"
            hasMore:
              type: boolean
              description: "Есть ли ещё страницы"
            totalCount:
              type: integer
              description: "Общее количество (опционально)"

  parameters:
    PageSize:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
      description: "Количество элементов на странице"

    PageCursor:
      name: cursor
      in: query
      schema:
        type: string
      description: "Курсор для пагинации"
```

### Error Handling Pattern

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: "Machine-readable код ошибки"
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: "Human-readable сообщение"
          example: "Поле email обязательно"
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
        requestId:
          type: string
          format: uuid
          description: "ID запроса для отладки"
        documentationUrl:
          type: string
          format: uri
          description: "Ссылка на документацию ошибки"

    ErrorDetail:
      type: object
      properties:
        field:
          type: string
          description: "Поле с ошибкой"
        reason:
          type: string
          description: "Причина ошибки"
        value:
          description: "Некорректное значение"

  responses:
    BadRequest:
      description: "Некорректный запрос"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "VALIDATION_ERROR"
            message: "Ошибка валидации"
            details:
              - field: "email"
                reason: "Некорректный формат email"
                value: "invalid-email"

    Unauthorized:
      description: "Требуется аутентификация"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Требуется аутентификация"

    Forbidden:
      description: "Доступ запрещён"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: "Ресурс не найден"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    InternalError:
      description: "Внутренняя ошибка сервера"
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "INTERNAL_ERROR"
            message: "Внутренняя ошибка сервера"
            requestId: "550e8400-e29b-41d4-a716-446655440000"
```

## Инструменты

### Валидация и линтинг

```bash
# Spectral - линтинг OpenAPI
npm install -g @stoplight/spectral-cli
spectral lint openapi.yaml

# Redocly CLI - валидация и bundle
npm install -g @redocly/cli
redocly lint openapi.yaml
redocly bundle openapi.yaml -o bundled.yaml

# OpenAPI Generator - валидация
openapi-generator-cli validate -i openapi.yaml
```

### Генерация кода

```bash
# OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Генерация TypeScript клиента
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./generated/client

# Генерация Python сервера (FastAPI)
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./generated/server

# Генерация Go клиента
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./generated/go-client
```

### Документация

```bash
# Redoc - статическая документация
npx @redocly/cli build-docs openapi.yaml -o docs.html

# Swagger UI
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/openapi.yaml \
  -v $(pwd)/openapi.yaml:/openapi.yaml \
  swaggerapi/swagger-ui
```

## Ресурсы

- **references/openapi-3.1-changelog.md** — Изменения в OpenAPI 3.1
- **references/json-schema-patterns.md** — Паттерны JSON Schema
- **assets/openapi-template.yaml** — Шаблон OpenAPI спецификации
- **assets/spectral-config.yaml** — Конфигурация Spectral

## Частые ошибки

1. **Отсутствие examples** — Всегда добавляйте примеры
2. **Слабые descriptions** — Описывайте не что, а зачем
3. **Игнорирование error responses** — Документируйте все ошибки
4. **Неконсистентное именование** — Используйте style guide
5. **Breaking changes без версионирования** — Всегда версионируйте
