---
name: github-spec-kit
description: GitHub Spec Kit — инструменты GitHub для spec-driven development, включая Issue/PR templates, GitHub Actions для валидации спецификаций, Projects для управления спецификациями, и автоматизацию документации. Use when setting up GitHub workflows for specifications, creating templates for API changes, or automating spec validation.
---

# GitHub Spec Kit

Полный набор инструментов GitHub для Spec Driven Development — templates, workflows, automation и governance для управления спецификациями.

## Поддержка языков

- **Русский ввод** → Объяснения и примеры на **русском**
- **English input** → Explanations and examples in **English**
- Технические термины сохраняются в оригинале

**ВСЕ РЕЗУЛЬТАТЫ СОХРАНЯЮТСЯ В MARKDOWN НА РУССКОМ ЯЗЫКЕ**

## Когда использовать этот скилл

- Настройка GitHub workflows для валидации спецификаций
- Создание templates для API changes и ADR
- Автоматизация проверки breaking changes
- Настройка GitHub Projects для управления спецификациями
- Автоматическая генерация документации
- CI/CD для specification-first workflow

## Issue Templates

### ADR Proposal Template

```yaml
# .github/ISSUE_TEMPLATE/adr-proposal.yml
name: "📋 ADR Proposal"
description: "Propose an Architecture Decision Record"
title: "[ADR] "
labels: ["adr", "needs-review"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        ## Architecture Decision Record Proposal

        Используйте этот шаблон для предложения нового архитектурного решения.

  - type: input
    id: title
    attributes:
      label: "Название решения"
      description: "Краткое название архитектурного решения"
      placeholder: "Использование PostgreSQL для хранения пользовательских данных"
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: "Контекст"
      description: "Опишите ситуацию и факторы, требующие решения"
      placeholder: |
        - Какая проблема возникла?
        - Какие ограничения существуют?
        - Какие требования нужно учесть?
    validations:
      required: true

  - type: textarea
    id: decision
    attributes:
      label: "Предлагаемое решение"
      description: "Опишите предлагаемое архитектурное решение"
      placeholder: "Мы предлагаем использовать..."
    validations:
      required: true

  - type: textarea
    id: consequences
    attributes:
      label: "Последствия"
      description: "Опишите положительные и отрицательные последствия"
      placeholder: |
        **Положительные:**
        - ...

        **Отрицательные:**
        - ...
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: "Рассмотренные альтернативы"
      description: "Какие другие варианты были рассмотрены?"
      placeholder: |
        1. **Альтернатива A**: ...
           Причина отклонения: ...

        2. **Альтернатива B**: ...
           Причина отклонения: ...
    validations:
      required: true

  - type: dropdown
    id: impact
    attributes:
      label: "Уровень влияния"
      options:
        - "🟢 Низкий (один сервис)"
        - "🟡 Средний (несколько сервисов)"
        - "🔴 Высокий (вся платформа)"
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: "Чеклист"
      options:
        - label: "Я обсудил это решение с командой"
          required: true
        - label: "Я рассмотрел альтернативы"
          required: true
        - label: "Я оценил последствия"
          required: true
```

### API Change Request Template

```yaml
# .github/ISSUE_TEMPLATE/api-change.yml
name: "🔌 API Change Request"
description: "Request a change to an existing API"
title: "[API] "
labels: ["api-change", "needs-spec-review"]

body:
  - type: markdown
    attributes:
      value: |
        ## API Change Request

        Используйте этот шаблон для запроса изменений в API.

  - type: dropdown
    id: change-type
    attributes:
      label: "Тип изменения"
      options:
        - "➕ Добавление нового endpoint"
        - "✏️ Изменение существующего endpoint"
        - "🗑️ Удаление endpoint (breaking change)"
        - "📝 Изменение схемы данных"
        - "🔒 Изменение security/auth"
    validations:
      required: true

  - type: input
    id: endpoint
    attributes:
      label: "Affected Endpoint(s)"
      placeholder: "GET /api/v1/users, POST /api/v1/users/{id}"
    validations:
      required: true

  - type: dropdown
    id: breaking
    attributes:
      label: "Breaking Change?"
      options:
        - "❌ Нет (backward compatible)"
        - "⚠️ Да (требуется migration)"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: "Описание изменения"
      description: "Детальное описание предлагаемого изменения"
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: "Мотивация"
      description: "Почему это изменение необходимо?"
    validations:
      required: true

  - type: textarea
    id: spec-diff
    attributes:
      label: "OpenAPI Diff"
      description: "Покажите изменения в OpenAPI формате"
      render: yaml
      placeholder: |
        # Before
        /users/{id}:
          get:
            responses:
              '200':
                schema:
                  $ref: '#/components/schemas/User'

        # After
        /users/{id}:
          get:
            responses:
              '200':
                schema:
                  $ref: '#/components/schemas/UserV2'

  - type: textarea
    id: migration
    attributes:
      label: "Migration Plan"
      description: "Если breaking change — как мигрировать?"
      placeholder: |
        1. Deploy new version with old compatibility
        2. Update clients
        3. Remove old compatibility

  - type: checkboxes
    id: checklist
    attributes:
      label: "Checklist"
      options:
        - label: "Я обновил OpenAPI спецификацию"
        - label: "Я добавил примеры request/response"
        - label: "Я обновил changelog"
        - label: "Я создал migration guide (если breaking)"
```

### RFC Template

```yaml
# .github/ISSUE_TEMPLATE/rfc.yml
name: "📝 RFC"
description: "Request for Comments on a technical proposal"
title: "[RFC] "
labels: ["rfc", "discussion"]

body:
  - type: markdown
    attributes:
      value: |
        ## Request for Comments

        RFC для обсуждения технических предложений.
        После обсуждения RFC будет преобразован в Design Doc и/или ADR.

  - type: textarea
    id: summary
    attributes:
      label: "Summary"
      description: "Краткое описание предложения (2-3 предложения)"
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: "Motivation"
      description: "Почему это необходимо? Какую проблему решает?"
    validations:
      required: true

  - type: textarea
    id: proposal
    attributes:
      label: "Detailed Proposal"
      description: "Детальное описание предложения"
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: "Alternatives"
      description: "Какие альтернативы рассмотрены?"

  - type: textarea
    id: risks
    attributes:
      label: "Risks"
      description: "Какие риски несёт это изменение?"

  - type: textarea
    id: questions
    attributes:
      label: "Open Questions"
      description: "Вопросы для обсуждения"
```

## Pull Request Templates

### Default PR Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## Description

<!-- Описание изменений -->

## Type of Change

- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentation update
- [ ] 🔧 Configuration change
- [ ] 📋 Specification change

## Related Issues

<!-- Closes #123, Fixes #456 -->

## Checklist

### General
- [ ] Code follows project style guidelines
- [ ] Self-review performed
- [ ] Tests added/updated
- [ ] Documentation updated

### If Specification Change
- [ ] OpenAPI spec updated
- [ ] Examples added/updated
- [ ] Changelog updated
- [ ] No breaking changes (or migration plan provided)
- [ ] Spectral linting passes

### If ADR
- [ ] ADR follows template
- [ ] Alternatives documented
- [ ] Consequences listed
- [ ] Architect review requested
```

### Specification Change PR Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE/spec-change.md -->

## Specification Change

### Summary

<!-- Краткое описание изменения спецификации -->

### Changed Files

- [ ] `specs/openapi.yaml`
- [ ] `specs/asyncapi.yaml`
- [ ] `docs/adr/*.md`

### Type of Change

- [ ] ➕ New endpoint/operation
- [ ] ✏️ Modified endpoint/operation
- [ ] 🗑️ Removed endpoint/operation (breaking)
- [ ] 📝 Schema change
- [ ] 🔒 Security change

### Breaking Change

- [ ] ❌ No breaking changes
- [ ] ⚠️ Yes, breaking change

<!-- If breaking, describe migration -->

### Changelog Entry

```markdown
## [Unreleased]

### Added
- ...

### Changed
- ...

### Removed
- ...
```

### Validation Results

<!-- Paste spectral/redocly output -->

```
spectral lint specs/openapi.yaml
...
```

### Checklist

- [ ] OpenAPI spec is valid (spectral passes)
- [ ] Examples are updated
- [ ] Changelog is updated
- [ ] No breaking changes OR migration guide provided
- [ ] Documentation is updated
- [ ] Contract tests pass
```

## GitHub Actions Workflows

### Specification Validation

```yaml
# .github/workflows/spec-validation.yml
name: Specification Validation

on:
  pull_request:
    paths:
      - 'specs/**'
      - 'api/**'
      - '.spectral.yaml'
  push:
    branches:
      - main

jobs:
  lint:
    name: Lint Specifications
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint OpenAPI
        run: |
          npx @stoplight/spectral-cli lint specs/openapi.yaml \
            --ruleset .spectral.yaml \
            --format stylish \
            --format junit --output reports/spectral-openapi.xml

      - name: Lint AsyncAPI
        if: hashFiles('specs/asyncapi.yaml') != ''
        run: |
          npx @stoplight/spectral-cli lint specs/asyncapi.yaml \
            --ruleset .spectral.yaml \
            --format stylish

      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: lint-results
          path: reports/

      - name: Annotate PR
        uses: dorny/test-reporter@v1
        if: always() && github.event_name == 'pull_request'
        with:
          name: Spectral Lint
          path: reports/*.xml
          reporter: java-junit

  validate:
    name: Validate Schema
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Redocly CLI
        run: npm install -g @redocly/cli

      - name: Validate OpenAPI
        run: redocly lint specs/openapi.yaml --config redocly.yaml

      - name: Bundle Specification
        run: |
          redocly bundle specs/openapi.yaml \
            --output dist/openapi-bundled.yaml

      - name: Upload Bundled Spec
        uses: actions/upload-artifact@v4
        with:
          name: bundled-spec
          path: dist/

  breaking-changes:
    name: Breaking Change Detection
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install oasdiff
        run: |
          curl -sSL https://github.com/Tufin/oasdiff/releases/latest/download/oasdiff_linux_amd64.tar.gz | tar xz
          sudo mv oasdiff /usr/local/bin/

      - name: Get base spec
        run: |
          git show origin/${{ github.base_ref }}:specs/openapi.yaml > base-spec.yaml 2>/dev/null || echo "No base spec"

      - name: Detect Breaking Changes
        id: breaking
        run: |
          if [ -f base-spec.yaml ]; then
            oasdiff breaking base-spec.yaml specs/openapi.yaml \
              --format json > breaking-changes.json || true

            if [ -s breaking-changes.json ] && [ "$(cat breaking-changes.json)" != "[]" ]; then
              echo "has_breaking=true" >> $GITHUB_OUTPUT
              echo "::warning::Breaking changes detected!"
              cat breaking-changes.json | jq .
            else
              echo "has_breaking=false" >> $GITHUB_OUTPUT
              echo "No breaking changes detected"
            fi
          else
            echo "has_breaking=false" >> $GITHUB_OUTPUT
            echo "No base spec to compare"
          fi

      - name: Comment on PR
        if: steps.breaking.outputs.has_breaking == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const changes = JSON.parse(fs.readFileSync('breaking-changes.json', 'utf8'));

            let body = '## ⚠️ Breaking Changes Detected\n\n';
            body += 'This PR contains breaking changes:\n\n';

            for (const change of changes) {
              body += `- **${change.path}**: ${change.message}\n`;
            }

            body += '\n### Required Actions:\n';
            body += '1. Update API version\n';
            body += '2. Create migration guide\n';
            body += '3. Get architect approval\n';

            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });

      - name: Add Breaking Change Label
        if: steps.breaking.outputs.has_breaking == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['breaking-change']
            });

  contract-tests:
    name: Contract Tests
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Start Mock Server
        run: |
          npx @stoplight/prism-cli mock specs/openapi.yaml --port 4010 &
          sleep 5

      - name: Run Contract Tests
        run: npm run test:contract

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: contract-test-results
          path: reports/
```

### Documentation Generation

```yaml
# .github/workflows/docs-generation.yml
name: Documentation Generation

on:
  push:
    branches:
      - main
    paths:
      - 'specs/**'
      - 'docs/**'
  workflow_dispatch:

jobs:
  generate-docs:
    name: Generate API Documentation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Redocly CLI
        run: npm install -g @redocly/cli

      - name: Bundle OpenAPI
        run: |
          redocly bundle specs/openapi.yaml \
            --output docs/api/openapi.yaml

      - name: Generate Redoc
        run: |
          redocly build-docs docs/api/openapi.yaml \
            --output docs/api/index.html \
            --title "API Reference"

      - name: Generate Changelog
        run: |
          npx oasdiff changelog \
            docs/api/openapi.yaml \
            specs/openapi.yaml \
            --format markdown > docs/api/CHANGELOG.md || true

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/api
          destination_dir: api

  generate-adr-site:
    name: Generate ADR Site
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Log4brains
        run: npm install -g log4brains

      - name: Build ADR Site
        run: log4brains build --basePath /adr

      - name: Deploy ADR Site
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./.log4brains/out
          destination_dir: adr
```

### ADR Workflow

```yaml
# .github/workflows/adr.yml
name: ADR Workflow

on:
  pull_request:
    paths:
      - 'docs/adr/**'

jobs:
  validate-adr:
    name: Validate ADR Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate ADR Structure
        run: |
          for file in docs/adr/[0-9]*.md; do
            echo "Validating $file"

            # Check required sections
            sections=("Статус" "Контекст" "Решение" "Последствия")
            for section in "${sections[@]}"; do
              if ! grep -q "^## $section" "$file"; then
                echo "::error file=$file::Missing section: $section"
                exit 1
              fi
            done

            # Check status is valid
            status=$(grep "^## Статус" -A 2 "$file" | tail -1)
            valid_statuses="Proposed|Accepted|Deprecated|Superseded"
            if ! echo "$status" | grep -qE "$valid_statuses"; then
              echo "::warning file=$file::Invalid status: $status"
            fi
          done

      - name: Check Numbering
        run: |
          expected=1
          for file in $(ls docs/adr/[0-9]*.md | sort); do
            num=$(basename "$file" | grep -oE '^[0-9]+')
            formatted=$(printf '%04d' $expected)
            if [ "$num" != "$formatted" ]; then
              echo "::error::Expected ADR-$formatted, found $num"
            fi
            expected=$((expected + 1))
          done

  require-architect:
    name: Require Architect Approval
    runs-on: ubuntu-latest
    steps:
      - name: Check Reviewers
        uses: actions/github-script@v6
        with:
          script: |
            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });

            const architects = ['architect1', 'architect2'];
            const approved = reviews.some(
              r => r.state === 'APPROVED' && architects.includes(r.user.login)
            );

            if (!approved) {
              await github.rest.pulls.requestReviewers({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.issue.number,
                reviewers: architects
              });

              core.notice('Architect review requested for ADR');
            }
```

## GitHub Projects

### Specification Backlog Template

```yaml
# .github/project-templates/spec-backlog.yml
name: Specification Backlog
description: Track API and specification changes

columns:
  - name: "📥 Inbox"
    cards:
      - note: "New specification requests go here"

  - name: "📋 RFC"
    cards:
      - note: "RFCs under discussion"

  - name: "✍️ Drafting"
    cards:
      - note: "Specifications being written"

  - name: "👀 Review"
    cards:
      - note: "Ready for technical review"

  - name: "✅ Approved"
    cards:
      - note: "Approved, ready for implementation"

  - name: "🚀 Implemented"
    cards:
      - note: "Implemented and deployed"

automation:
  - trigger: issue_labeled
    label: rfc
    action: move_to_column
    column: "📋 RFC"

  - trigger: issue_labeled
    label: spec-draft
    action: move_to_column
    column: "✍️ Drafting"

  - trigger: pull_request_opened
    action: move_to_column
    column: "👀 Review"

  - trigger: pull_request_merged
    action: move_to_column
    column: "🚀 Implemented"
```

## Repository Structure

```
.github/
├── ISSUE_TEMPLATE/
│   ├── adr-proposal.yml
│   ├── api-change.yml
│   ├── rfc.yml
│   └── bug-report.yml
├── PULL_REQUEST_TEMPLATE/
│   ├── default.md
│   └── spec-change.md
├── workflows/
│   ├── spec-validation.yml
│   ├── docs-generation.yml
│   ├── adr.yml
│   └── release.yml
├── CODEOWNERS
└── dependabot.yml

specs/
├── openapi.yaml
├── asyncapi.yaml
└── components/
    ├── schemas/
    ├── parameters/
    └── responses/

docs/
├── adr/
│   ├── 0001-use-postgresql.md
│   ├── 0002-event-sourcing.md
│   └── README.md
├── rfc/
│   └── 2024-001-new-auth-system.md
└── api/
    └── README.md

.spectral.yaml
redocly.yaml
.log4brains.yml
```

### CODEOWNERS

```
# .github/CODEOWNERS

# Specifications require API team review
/specs/ @api-team

# ADRs require architect review
/docs/adr/ @architects

# RFCs require tech lead review
/docs/rfc/ @tech-leads

# Workflows require platform team review
/.github/workflows/ @platform-team
```

## Ресурсы

- **references/github-actions-patterns.md** — Паттерны GitHub Actions
- **references/issue-template-examples.md** — Примеры шаблонов
- **assets/spectral-config.yaml** — Конфигурация Spectral
- **assets/redocly-config.yaml** — Конфигурация Redocly

## Частые ошибки

1. **Нет валидации в CI** — Всегда валидируйте спецификации автоматически
2. **Игнорирование breaking changes** — Используйте oasdiff для detection
3. **Нет code owners** — Назначайте ответственных за specs
4. **Ручное обновление docs** — Автоматизируйте генерацию документации
5. **Нет связи issues и specs** — Используйте labels и templates
