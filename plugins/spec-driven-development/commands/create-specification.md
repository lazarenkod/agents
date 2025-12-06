---
name: create-specification
description: Создание новой спецификации API, ADR или дизайн-документа с использованием best practices и шаблонов уровня AWS, Google, Stripe
---

# Создание спецификации

Интерактивный workflow для создания спецификаций: OpenAPI, AsyncAPI, ADR, RFC, Design Documents.

## Поддержка языков

**ВСЕ РЕЗУЛЬТАТЫ СОХРАНЯЮТСЯ В MARKDOWN НА РУССКОМ ЯЗЫКЕ**

## Процесс

### Шаг 1: Определение типа спецификации

Выберите тип спецификации:

1. **OpenAPI** — REST API спецификация
2. **AsyncAPI** — Event-driven API спецификация
3. **GraphQL** — GraphQL schema
4. **gRPC** — Protocol Buffers определение
5. **ADR** — Architecture Decision Record
6. **RFC** — Request for Comments
7. **Design Doc** — Technical Design Document

### Шаг 2: Сбор информации

Для каждого типа соберите необходимую информацию:

#### OpenAPI
- Название API и версия
- Описание и назначение
- Base URL и environments
- Authentication method (Bearer, API Key, OAuth2)
- Основные endpoints
- Схемы данных (entities)

#### ADR
- Название решения
- Контекст и проблема
- Рассмотренные альтернативы
- Принятое решение
- Последствия

#### RFC/Design Doc
- Название проекта
- Мотивация и проблема
- Предлагаемое решение
- Альтернативы
- План реализации

### Шаг 3: Генерация спецификации

Создайте файл согласно выбранному типу с полным содержимым.

### Шаг 4: Валидация

Проверьте созданную спецификацию:

```bash
# OpenAPI
npx @stoplight/spectral-cli lint specs/openapi.yaml

# AsyncAPI
npx @stoplight/spectral-cli lint specs/asyncapi.yaml

# ADR
# Проверка структуры markdown
```

### Шаг 5: Интеграция

Добавьте спецификацию в систему:

1. Создайте файл в правильном месте
2. Обновите index/README
3. Настройте CI/CD валидацию
4. Создайте PR для review

## Шаблоны

### OpenAPI Template

```yaml
openapi: 3.1.0
info:
  title: "[API_NAME]"
  version: "1.0.0"
  description: |
    [ОПИСАНИЕ API НА РУССКОМ]
  contact:
    name: API Team
    email: api@company.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

security:
  - bearerAuth: []

tags:
  - name: "[RESOURCE]"
    description: "[ОПИСАНИЕ]"

paths:
  /[resources]:
    get:
      operationId: list[Resources]
      summary: "Получить список [ресурсов]"
      description: |
        Возвращает paginated список [ресурсов].
      tags:
        - "[RESOURCE]"
      parameters:
        - $ref: '#/components/parameters/PageSize'
        - $ref: '#/components/parameters/PageToken'
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]List'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: create[Resource]
      summary: "Создать [ресурс]"
      tags:
        - "[RESOURCE]"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]Request'
      responses:
        '201':
          description: "[Ресурс] создан"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'

  /[resources]/{id}:
    parameters:
      - $ref: '#/components/parameters/[Resource]Id'

    get:
      operationId: get[Resource]
      summary: "Получить [ресурс]"
      tags:
        - "[RESOURCE]"
      responses:
        '200':
          description: Успешный ответ
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      operationId: update[Resource]
      summary: "Обновить [ресурс]"
      tags:
        - "[RESOURCE]"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Update[Resource]Request'
      responses:
        '200':
          description: "[Ресурс] обновлён"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]'

    delete:
      operationId: delete[Resource]
      summary: "Удалить [ресурс]"
      tags:
        - "[RESOURCE]"
      responses:
        '204':
          description: "[Ресурс] удалён"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    [Resource]:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
          description: "Уникальный идентификатор"
        name:
          type: string
          minLength: 1
          maxLength: 255
          description: "Название"
        createdAt:
          type: string
          format: date-time
          readOnly: true
          description: "Время создания"
        updatedAt:
          type: string
          format: date-time
          readOnly: true
          description: "Время обновления"

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        requestId:
          type: string
          format: uuid

  parameters:
    PageSize:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    PageToken:
      name: cursor
      in: query
      schema:
        type: string

    [Resource]Id:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid

  responses:
    Unauthorized:
      description: Требуется аутентификация
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Ресурс не найден
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### ADR Template

```markdown
# ADR-[NNNN]: [Название решения]

## Статус

Proposed

## Контекст

[Описание ситуации, проблемы и факторов, которые привели к необходимости принятия решения]

### Текущая ситуация
- [Факт 1]
- [Факт 2]

### Требования
- [Требование 1]
- [Требование 2]

### Ограничения
- [Ограничение 1]
- [Ограничение 2]

## Решение

[Чёткая формулировка принятого решения]

### Детали реализации

[Описание ключевых аспектов реализации]

## Последствия

### Положительные
- [Преимущество 1]
- [Преимущество 2]

### Отрицательные
- [Недостаток 1]
- [Недостаток 2]

## Альтернативы рассмотренные

### Альтернатива 1: [Название]

**Описание:** [Краткое описание]

**Причина отклонения:** [Обоснование]

### Альтернатива 2: [Название]

**Описание:** [Краткое описание]

**Причина отклонения:** [Обоснование]

## Связанные документы

- [Документ 1](ссылка)
- [Документ 2](ссылка)

## Дата

[YYYY-MM-DD]

## Авторы

- [Автор 1]
```

## Выходные файлы

После выполнения команды будут созданы:

1. **Спецификация** — основной файл (YAML/MD)
2. **README** — обновлённый index
3. **Валидация** — результаты проверки
4. **Чеклист** — что нужно сделать дальше

## Примеры использования

```
/create-specification openapi "User Management API"
/create-specification adr "Выбор PostgreSQL для хранения"
/create-specification rfc "Новая система авторизации"
```
