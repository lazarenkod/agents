---
name: contract-testing
description: Контрактное тестирование API — Pact, Spring Cloud Contract, Dredd, Schemathesis для consumer-driven contracts и specification validation. Use when implementing contract tests, setting up consumer-driven contract workflows, or validating API implementations against specifications.
---

# Contract Testing

Полное руководство по контрактному тестированию API — от consumer-driven contracts до specification-based validation.

## Поддержка языков

- **Русский ввод** → Объяснения и примеры на **русском**
- **English input** → Explanations and examples in **English**
- Технические термины сохраняются в оригинале

**ВСЕ РЕЗУЛЬТАТЫ СОХРАНЯЮТСЯ В MARKDOWN НА РУССКОМ ЯЗЫКЕ**

## Когда использовать этот скилл

- Настройка consumer-driven contract testing
- Валидация API против OpenAPI спецификации
- Интеграция contract tests в CI/CD
- Property-based API testing
- Mock server setup из спецификаций
- Pact Broker configuration

## Основные концепции

### Типы контрактного тестирования

| Тип | Описание | Инструменты |
|-----|----------|-------------|
| Consumer-Driven | Consumer определяет ожидания | Pact, Spring Cloud Contract |
| Provider-Driven | Provider публикует контракт | OpenAPI + Dredd/Prism |
| Bi-Directional | Оба направления | Pact + OpenAPI |
| Property-Based | Автоматическая генерация | Schemathesis, Hypothesis |

### Consumer-Driven Contracts Flow

```
┌─────────────┐                     ┌─────────────┐
│   Consumer  │                     │   Provider  │
│   (Client)  │                     │   (Server)  │
└──────┬──────┘                     └──────┬──────┘
       │                                   │
       │ 1. Write consumer test            │
       │ 2. Generate pact file             │
       ▼                                   │
┌─────────────────────────────────────────────────┐
│                   Pact Broker                    │
│  (stores and manages contract versions)         │
└─────────────────────────────────────────────────┘
       │                                   │
       │                                   │ 3. Fetch pact
       │                                   │ 4. Verify against impl
       │                                   │ 5. Publish results
       │                                   ▼
       │                           ┌─────────────┐
       │                           │ Verification│
       │                           │   Results   │
       │                           └─────────────┘
       │                                   │
       ▼                                   ▼
┌─────────────────────────────────────────────────┐
│              Can-I-Deploy Check                  │
│  (safe deployment validation)                   │
└─────────────────────────────────────────────────┘
```

## Pact

### Consumer Test (JavaScript)

```javascript
// consumer.pact.spec.js
const { Pact } = require('@pact-foundation/pact');
const { like, eachLike, term, integer } = require('@pact-foundation/pact').Matchers;
const path = require('path');

describe('User Service Consumer', () => {
  const provider = new Pact({
    consumer: 'WebApp',
    provider: 'UserService',
    port: 1234,
    log: path.resolve(process.cwd(), 'logs', 'pact.log'),
    dir: path.resolve(process.cwd(), 'pacts'),
    logLevel: 'INFO',
    spec: 3, // Pact specification v3
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  afterEach(() => provider.verify());

  describe('Получение пользователя по ID', () => {
    const expectedUser = {
      id: 'user-123',
      email: 'ivan@example.com',
      name: 'Иван Петров',
      status: 'active',
      roles: ['user'],
      createdAt: '2024-01-15T10:30:00Z',
    };

    beforeEach(() => {
      return provider.addInteraction({
        // Состояние провайдера
        state: 'пользователь с ID user-123 существует',
        // Описание взаимодействия
        uponReceiving: 'запрос на получение пользователя по ID',
        // Запрос
        withRequest: {
          method: 'GET',
          path: '/api/v1/users/user-123',
          headers: {
            'Authorization': 'Bearer valid-token',
            'Accept': 'application/json',
          },
        },
        // Ожидаемый ответ с matchers
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            id: 'user-123',
            email: like('ivan@example.com'),
            name: like('Иван Петров'),
            status: term({
              matcher: 'active|inactive|suspended',
              generate: 'active',
            }),
            roles: eachLike('user'),
            createdAt: term({
              matcher: '^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$',
              generate: '2024-01-15T10:30:00Z',
            }),
          },
        },
      });
    });

    it('возвращает пользователя', async () => {
      // Arrange
      const client = new UserClient('http://localhost:1234');

      // Act
      const user = await client.getUser('user-123');

      // Assert
      expect(user.id).toBe('user-123');
      expect(user.status).toBe('active');
      expect(user.roles).toContain('user');
    });
  });

  describe('Создание пользователя', () => {
    beforeEach(() => {
      return provider.addInteraction({
        state: 'email new@example.com не занят',
        uponReceiving: 'запрос на создание пользователя',
        withRequest: {
          method: 'POST',
          path: '/api/v1/users',
          headers: {
            'Authorization': 'Bearer valid-token',
            'Content-Type': 'application/json',
          },
          body: {
            email: 'new@example.com',
            name: 'Новый Пользователь',
            password: 'SecurePassword123!',
          },
        },
        willRespondWith: {
          status: 201,
          headers: {
            'Content-Type': 'application/json',
            'Location': like('/api/v1/users/user-456'),
          },
          body: {
            id: like('user-456'),
            email: 'new@example.com',
            name: 'Новый Пользователь',
            status: 'active',
            createdAt: like('2024-01-15T10:30:00Z'),
          },
        },
      });
    });

    it('создаёт пользователя', async () => {
      const client = new UserClient('http://localhost:1234');

      const user = await client.createUser({
        email: 'new@example.com',
        name: 'Новый Пользователь',
        password: 'SecurePassword123!',
      });

      expect(user.email).toBe('new@example.com');
      expect(user.status).toBe('active');
    });
  });

  describe('Список пользователей с пагинацией', () => {
    beforeEach(() => {
      return provider.addInteraction({
        state: 'существует несколько пользователей',
        uponReceiving: 'запрос на список пользователей',
        withRequest: {
          method: 'GET',
          path: '/api/v1/users',
          query: {
            limit: '20',
            status: 'active',
          },
          headers: {
            'Authorization': 'Bearer valid-token',
          },
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            data: eachLike({
              id: like('user-123'),
              email: like('user@example.com'),
              name: like('User Name'),
              status: 'active',
            }),
            pagination: {
              nextCursor: like('cursor-xyz'),
              hasMore: true,
              totalCount: integer(100),
            },
          },
        },
      });
    });

    it('возвращает список пользователей', async () => {
      const client = new UserClient('http://localhost:1234');

      const result = await client.listUsers({ limit: 20, status: 'active' });

      expect(result.data.length).toBeGreaterThan(0);
      expect(result.pagination.hasMore).toBe(true);
    });
  });

  describe('Обработка ошибок', () => {
    beforeEach(() => {
      return provider.addInteraction({
        state: 'пользователь с ID not-found не существует',
        uponReceiving: 'запрос на несуществующего пользователя',
        withRequest: {
          method: 'GET',
          path: '/api/v1/users/not-found',
          headers: {
            'Authorization': 'Bearer valid-token',
          },
        },
        willRespondWith: {
          status: 404,
          headers: {
            'Content-Type': 'application/json',
          },
          body: {
            code: 'USER_NOT_FOUND',
            message: like('Пользователь не найден'),
            requestId: like('req-123'),
          },
        },
      });
    });

    it('возвращает 404 для несуществующего пользователя', async () => {
      const client = new UserClient('http://localhost:1234');

      await expect(client.getUser('not-found'))
        .rejects
        .toThrow('USER_NOT_FOUND');
    });
  });
});
```

### Provider Verification (JavaScript)

```javascript
// provider.pact.spec.js
const { Verifier } = require('@pact-foundation/pact');
const { app } = require('../src/app');

describe('User Service Provider', () => {
  let server;

  beforeAll(async () => {
    server = app.listen(3000);
  });

  afterAll(() => {
    server.close();
  });

  it('validates the expectations of WebApp', async () => {
    const opts = {
      provider: 'UserService',
      providerBaseUrl: 'http://localhost:3000',

      // Pact Broker configuration
      pactBrokerUrl: process.env.PACT_BROKER_URL,
      pactBrokerUsername: process.env.PACT_BROKER_USERNAME,
      pactBrokerPassword: process.env.PACT_BROKER_PASSWORD,

      // Or use local pacts
      // pactUrls: ['./pacts/webapp-userservice.json'],

      // Provider version
      providerVersion: process.env.GIT_COMMIT || '1.0.0',
      providerVersionBranch: process.env.GIT_BRANCH || 'main',

      // Publish verification results
      publishVerificationResult: process.env.CI === 'true',

      // Consumer version selectors
      consumerVersionSelectors: [
        { mainBranch: true },
        { deployedOrReleased: true },
      ],

      // State handlers
      stateHandlers: {
        'пользователь с ID user-123 существует': async () => {
          await db.users.create({
            id: 'user-123',
            email: 'ivan@example.com',
            name: 'Иван Петров',
            status: 'active',
            roles: ['user'],
          });
        },

        'email new@example.com не занят': async () => {
          await db.users.deleteByEmail('new@example.com');
        },

        'существует несколько пользователей': async () => {
          await db.users.createMany([
            { id: 'user-1', email: 'user1@example.com', name: 'User 1', status: 'active' },
            { id: 'user-2', email: 'user2@example.com', name: 'User 2', status: 'active' },
            { id: 'user-3', email: 'user3@example.com', name: 'User 3', status: 'active' },
          ]);
        },

        'пользователь с ID not-found не существует': async () => {
          await db.users.deleteById('not-found');
        },
      },

      // Teardown after each interaction
      afterEach: async () => {
        await db.users.deleteAll();
      },

      // Request filter (add auth, modify headers)
      requestFilter: (req, res, next) => {
        // Validate token format but accept test tokens
        if (req.headers.authorization === 'Bearer valid-token') {
          req.user = { id: 'test-user', role: 'admin' };
        }
        next();
      },
    };

    return new Verifier(opts).verifyProvider();
  });
});
```

### Pact Broker Configuration

```yaml
# docker-compose.yml
version: '3'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: pact
      POSTGRES_PASSWORD: pact
      POSTGRES_DB: pact
    volumes:
      - pact-postgres:/var/lib/postgresql/data

  pact-broker:
    image: pactfoundation/pact-broker:latest
    depends_on:
      - postgres
    environment:
      PACT_BROKER_DATABASE_URL: postgres://pact:pact@postgres/pact
      PACT_BROKER_BASIC_AUTH_USERNAME: admin
      PACT_BROKER_BASIC_AUTH_PASSWORD: admin
      PACT_BROKER_ALLOW_PUBLIC_READ: 'true'
    ports:
      - "9292:9292"

volumes:
  pact-postgres:
```

### CI/CD Integration

```yaml
# .github/workflows/contract-tests.yml
name: Contract Tests

on:
  push:
    branches: [main, develop]
  pull_request:

env:
  PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
  PACT_BROKER_USERNAME: ${{ secrets.PACT_BROKER_USERNAME }}
  PACT_BROKER_PASSWORD: ${{ secrets.PACT_BROKER_PASSWORD }}

jobs:
  consumer-tests:
    name: Consumer Contract Tests
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

      - name: Run consumer tests
        run: npm run test:pact:consumer

      - name: Publish pacts to broker
        run: |
          npx pact-broker publish pacts \
            --broker-base-url $PACT_BROKER_URL \
            --broker-username $PACT_BROKER_USERNAME \
            --broker-password $PACT_BROKER_PASSWORD \
            --consumer-app-version ${{ github.sha }} \
            --branch ${{ github.ref_name }} \
            --tag-with-git-branch

  provider-verification:
    name: Provider Verification
    runs-on: ubuntu-latest
    needs: consumer-tests
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Start service
        run: |
          npm run start:test &
          sleep 10

      - name: Verify provider
        run: npm run test:pact:provider
        env:
          GIT_COMMIT: ${{ github.sha }}
          GIT_BRANCH: ${{ github.ref_name }}
          CI: true

  can-i-deploy:
    name: Can I Deploy?
    runs-on: ubuntu-latest
    needs: [consumer-tests, provider-verification]
    steps:
      - name: Check deployment safety
        run: |
          npx pact-broker can-i-deploy \
            --broker-base-url $PACT_BROKER_URL \
            --broker-username $PACT_BROKER_USERNAME \
            --broker-password $PACT_BROKER_PASSWORD \
            --pacticipant "WebApp" \
            --version ${{ github.sha }} \
            --to-environment production

      - name: Record deployment
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker record-deployment \
            --broker-base-url $PACT_BROKER_URL \
            --broker-username $PACT_BROKER_USERNAME \
            --broker-password $PACT_BROKER_PASSWORD \
            --pacticipant "WebApp" \
            --version ${{ github.sha }} \
            --environment production
```

## OpenAPI Contract Testing

### Dredd

```yaml
# dredd.yml
dry-run: false
hookfiles: ./test/dredd-hooks.js
language: nodejs
server: npm start
server-wait: 5
reporter: apiary
custom:
  apiaryApiKey: env:APIARY_API_KEY
  apiaryApiName: myapi
blueprint: specs/openapi.yaml
endpoint: http://localhost:3000
header:
  - "Authorization: Bearer test-token"
names: false
only: []
sorted: true
```

```javascript
// test/dredd-hooks.js
const hooks = require('hooks');
const db = require('../src/db');

// Before all tests
hooks.beforeAll(async (transactions, done) => {
  await db.migrate();
  done();
});

// Before each transaction
hooks.beforeEach(async (transaction, done) => {
  // Setup test data based on transaction name
  if (transaction.name.includes('GET /users/{id}')) {
    await db.users.create({ id: 'test-user', email: 'test@example.com' });
  }
  done();
});

// After each transaction
hooks.afterEach(async (transaction, done) => {
  await db.users.deleteAll();
  done();
});

// Skip specific transactions
hooks.before('Users > Create user > 409', (transaction, done) => {
  // Setup duplicate email scenario
  db.users.create({ id: 'existing', email: 'existing@example.com' })
    .then(() => done());
});

// Modify request
hooks.before('Users > List users', (transaction) => {
  transaction.request.headers['X-Custom-Header'] = 'value';
});

// Validate response
hooks.after('Users > Get user', (transaction, done) => {
  const response = JSON.parse(transaction.real.body);
  if (!response.id) {
    transaction.fail = 'Response missing id field';
  }
  done();
});
```

### Schemathesis (Property-Based Testing)

```python
# test_api.py
import schemathesis
from hypothesis import settings, Phase

# Load schema from file or URL
schema = schemathesis.from_path("specs/openapi.yaml")
# Or: schema = schemathesis.from_uri("http://localhost:3000/openapi.json")

@schema.parametrize()
@settings(
    max_examples=100,
    phases=[Phase.explicit, Phase.reuse, Phase.generate],
    deadline=None,
)
def test_api(case):
    """
    Автоматически генерирует тесты для всех endpoints.
    Проверяет:
    - Валидность response schema
    - Отсутствие 5xx ошибок
    - Content-Type соответствие
    """
    response = case.call_and_validate()

    # Additional assertions
    assert response.status_code < 500

@schema.parametrize(endpoint="/users")
def test_users_endpoint(case):
    """Тесты специфичные для /users endpoint"""
    response = case.call_and_validate()

    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert "pagination" in data

@schema.parametrize(method="POST")
def test_post_operations(case):
    """Тесты для всех POST операций"""
    response = case.call_and_validate()

    if response.status_code == 201:
        assert "Location" in response.headers or "id" in response.json()
```

```bash
# CLI usage
schemathesis run specs/openapi.yaml \
  --base-url http://localhost:3000 \
  --checks all \
  --hypothesis-max-examples 100 \
  --report junit-xml

# With authentication
schemathesis run specs/openapi.yaml \
  --base-url http://localhost:3000 \
  --header "Authorization: Bearer $TOKEN"

# Stateful testing (follows links between operations)
schemathesis run specs/openapi.yaml \
  --base-url http://localhost:3000 \
  --stateful=links
```

### Prism Mock Server

```bash
# Start mock server
npx @stoplight/prism-cli mock specs/openapi.yaml --port 4010

# With dynamic responses
npx @stoplight/prism-cli mock specs/openapi.yaml \
  --port 4010 \
  --dynamic

# Validation proxy mode
npx @stoplight/prism-cli proxy specs/openapi.yaml \
  http://localhost:3000 \
  --port 4010 \
  --errors
```

```javascript
// test/api.integration.spec.js
describe('API Integration Tests with Prism Mock', () => {
  const MOCK_URL = 'http://localhost:4010';

  it('should match OpenAPI spec response', async () => {
    const response = await fetch(`${MOCK_URL}/api/v1/users/123`);
    const data = await response.json();

    // Response from Prism matches OpenAPI examples
    expect(response.status).toBe(200);
    expect(data).toHaveProperty('id');
    expect(data).toHaveProperty('email');
  });

  it('should validate request against spec', async () => {
    const response = await fetch(`${MOCK_URL}/api/v1/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        // Missing required field 'email'
        name: 'Test User',
      }),
    });

    // Prism returns validation error
    expect(response.status).toBe(422);
  });
});
```

## Spring Cloud Contract

```groovy
// contracts/user/shouldReturnUser.groovy
Contract.make {
    description "should return user by id"

    request {
        method GET()
        url '/api/v1/users/user-123'
        headers {
            header('Authorization', 'Bearer valid-token')
            header('Accept', 'application/json')
        }
    }

    response {
        status OK()
        headers {
            contentType applicationJson()
        }
        body([
            id: 'user-123',
            email: $(producer(regex(email())), consumer('ivan@example.com')),
            name: $(producer(regex('.+')), consumer('Иван Петров')),
            status: $(producer(regex('active|inactive')), consumer('active')),
            createdAt: $(producer(regex(isoDateTime())), consumer('2024-01-15T10:30:00Z'))
        ])
    }
}
```

```java
// Generated test (consumer side)
@SpringBootTest
@AutoConfigureStubRunner(
    stubsMode = StubRunnerProperties.StubsMode.LOCAL,
    ids = "com.example:user-service:+:stubs:8080"
)
class UserClientContractTest {

    @Autowired
    private UserClient userClient;

    @Test
    void shouldReturnUser() {
        User user = userClient.getUser("user-123");

        assertThat(user.getId()).isEqualTo("user-123");
        assertThat(user.getStatus()).isEqualTo("active");
    }
}
```

## Best Practices

### 1. Contract Design

```markdown
## Правила проектирования контрактов

### DO ✅
- Используйте matchers вместо конкретных значений
- Документируйте provider states
- Тестируйте edge cases (errors, pagination)
- Версионируйте контракты

### DON'T ❌
- Не тестируйте бизнес-логику в контрактах
- Не дублируйте unit tests
- Не используйте production данные
- Не игнорируйте breaking changes
```

### 2. Matchers

```javascript
const { like, eachLike, term, integer, decimal, boolean, uuid } = Matchers;

// Type matchers
like('example')           // Matches any string
integer(123)              // Matches any integer
decimal(12.34)            // Matches any decimal
boolean(true)             // Matches any boolean
uuid()                    // Matches UUID format

// Array matchers
eachLike({ id: like('123') })  // Array with at least 1 element

// Regex matchers
term({
  matcher: '^[a-z]+$',
  generate: 'abc'
})

// Date/time matchers
term({
  matcher: '^\\d{4}-\\d{2}-\\d{2}$',
  generate: '2024-01-15'
})
```

## Ресурсы

- **references/pact-matchers-guide.md** — Руководство по Pact matchers
- **references/spring-cloud-contract-dsl.md** — Spring Cloud Contract DSL
- **assets/pact-broker-docker.yml** — Docker compose для Pact Broker
- **assets/dredd-hooks-template.js** — Шаблон Dredd hooks

## Частые ошибки

1. **Слишком строгие контракты** — Используйте matchers
2. **Игнорирование provider states** — Всегда настраивайте состояние
3. **Тестирование логики** — Контракты не для unit tests
4. **Отсутствие CI/CD** — Автоматизируйте верификацию
5. **Нет can-i-deploy** — Используйте для безопасных деплоев
