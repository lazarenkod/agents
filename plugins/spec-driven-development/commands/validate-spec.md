---
name: validate-spec
description: Валидация спецификаций — проверка OpenAPI, AsyncAPI, ADR на соответствие стандартам, обнаружение breaking changes, линтинг и генерация отчёта
---

# Валидация спецификации

Комплексная проверка спецификаций на соответствие стандартам и best practices.

## Поддержка языков

**ВСЕ РЕЗУЛЬТАТЫ СОХРАНЯЮТСЯ В MARKDOWN НА РУССКОМ ЯЗЫКЕ**

## Процесс валидации

### Шаг 1: Определение типа спецификации

Автоматическое определение по расширению и содержимому:
- `*.yaml` с `openapi:` → OpenAPI
- `*.yaml` с `asyncapi:` → AsyncAPI
- `*.graphql` → GraphQL Schema
- `*.proto` → Protocol Buffers
- `docs/adr/*.md` → ADR

### Шаг 2: Структурная валидация

Проверка корректности структуры:

```bash
# OpenAPI
npx @redocly/cli lint specs/openapi.yaml

# AsyncAPI
npx @asyncapi/cli validate specs/asyncapi.yaml

# GraphQL
npx graphql-schema-linter schema.graphql

# Protobuf
buf lint protos/
```

### Шаг 3: Стилевая валидация (Spectral)

Проверка на соответствие style guide:

```bash
npx @stoplight/spectral-cli lint specs/openapi.yaml \
  --ruleset .spectral.yaml \
  --format stylish
```

### Шаг 4: Breaking Change Detection

Сравнение с предыдущей версией:

```bash
# Получить предыдущую версию
git show HEAD~1:specs/openapi.yaml > previous.yaml

# Обнаружение breaking changes
oasdiff breaking previous.yaml specs/openapi.yaml
```

### Шаг 5: Генерация отчёта

Создание подробного отчёта на русском языке.

## Команды валидации

### OpenAPI

```bash
# Полная валидация
npm run validate:openapi

# Или вручную
npx @stoplight/spectral-cli lint specs/openapi.yaml \
  --ruleset .spectral.yaml \
  --format stylish \
  --format html --output reports/spectral-report.html
```

### AsyncAPI

```bash
# Валидация
npx @asyncapi/cli validate specs/asyncapi.yaml

# Генерация документации для проверки
npx @asyncapi/cli generate fromTemplate specs/asyncapi.yaml @asyncapi/html-template -o docs/
```

### ADR

```bash
# Проверка структуры ADR
for file in docs/adr/[0-9]*.md; do
  echo "Проверка $file"

  # Обязательные секции
  grep -q "^## Статус" "$file" || echo "❌ Нет секции Статус"
  grep -q "^## Контекст" "$file" || echo "❌ Нет секции Контекст"
  grep -q "^## Решение" "$file" || echo "❌ Нет секции Решение"
  grep -q "^## Последствия" "$file" || echo "❌ Нет секции Последствия"

  echo "✅ Проверка завершена"
done
```

## Spectral Configuration

```yaml
# .spectral.yaml
extends:
  - spectral:oas

rules:
  # Обязательные правила (error)
  operation-operationId: error
  operation-tags: error
  path-params: error
  no-$ref-siblings: error

  # Рекомендуемые правила (warn)
  operation-description: warn
  operation-summary: warn
  tag-description: warn

  # Кастомные правила
  path-kebab-case:
    severity: error
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: ^/[a-z0-9-/{}]+$

  response-examples:
    severity: warn
    given: $.paths.*.*.responses.*.content.application/json
    then:
      function: xor
      functionOptions:
        properties:
          - example
          - examples
```

## Отчёт о валидации

Формат отчёта на русском языке:

```markdown
# Отчёт о валидации спецификации

**Файл:** specs/openapi.yaml
**Дата:** 2024-01-15 10:30:00
**Версия:** 1.2.0

## Результаты

### Структурная валидация
✅ Спецификация валидна

### Стилевая валидация (Spectral)

| Уровень | Количество |
|---------|------------|
| ❌ Error | 0 |
| ⚠️ Warning | 3 |
| ℹ️ Info | 5 |

#### Предупреждения

1. **operation-description** (строка 45)
   - Операция GET /users не имеет description
   - Рекомендация: Добавьте описание операции

2. **response-examples** (строка 67)
   - Ответ 200 для GET /users/{id} не имеет примера
   - Рекомендация: Добавьте example или examples

### Breaking Changes
✅ Нет breaking changes

### Рекомендации

1. Добавьте описания для всех операций
2. Добавьте примеры для всех ответов
3. Рассмотрите добавление rate limiting headers

## Следующие шаги

- [ ] Исправить warnings
- [ ] Обновить документацию
- [ ] Создать PR для review
```

## Интеграция в CI/CD

```yaml
# .github/workflows/validate-specs.yml
name: Validate Specifications

on:
  pull_request:
    paths:
      - 'specs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate OpenAPI
        run: |
          npx @stoplight/spectral-cli lint specs/openapi.yaml \
            --format stylish \
            --format junit --output reports/spectral.xml

      - name: Check Breaking Changes
        run: |
          git show origin/${{ github.base_ref }}:specs/openapi.yaml > base.yaml
          oasdiff breaking base.yaml specs/openapi.yaml

      - name: Generate Report
        run: |
          echo "# Validation Report" > reports/VALIDATION.md
          echo "" >> reports/VALIDATION.md
          echo "## Spectral Results" >> reports/VALIDATION.md
          cat reports/spectral.xml >> reports/VALIDATION.md

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: reports/
```

## Примеры использования

```
/validate-spec specs/openapi.yaml
/validate-spec docs/adr/0042-event-sourcing.md
/validate-spec --breaking-changes specs/openapi.yaml
```
