# Изменения в OpenAPI 3.1

## Основные изменения с OpenAPI 3.0

### JSON Schema 2020-12 Compatibility

OpenAPI 3.1 полностью совместим с JSON Schema Draft 2020-12.

```yaml
# Новый dialect
jsonSchemaDialect: "https://json-schema.org/draft/2020-12/schema"
```

### Nullable изменился

```yaml
# OpenAPI 3.0
type: string
nullable: true

# OpenAPI 3.1
type:
  - string
  - "null"
```

### Webhooks

Новая секция для описания webhooks:

```yaml
webhooks:
  newOrder:
    post:
      summary: New order webhook
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      responses:
        '200':
          description: OK
```

### PathItems в Components

```yaml
components:
  pathItems:
    reusableEndpoint:
      get:
        summary: Reusable GET operation
```

### License Identifier

```yaml
info:
  license:
    name: Apache 2.0
    identifier: Apache-2.0  # SPDX identifier
```

### Summary в Info

```yaml
info:
  title: My API
  summary: Short summary of the API  # Новое поле
  description: Longer description...
```

## Миграция с 3.0 на 3.1

1. Обновите `openapi: 3.0.x` на `openapi: 3.1.0`
2. Замените `nullable: true` на `type: [string, "null"]`
3. Добавьте `jsonSchemaDialect` если используете JSON Schema features
4. Рассмотрите использование webhooks вместо callbacks
