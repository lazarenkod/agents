# Backstage.io Comprehensive Guide

## Overview

Backstage is an open-source platform for building developer portals, created by Spotify. It provides a centralized place to manage all your software — services, libraries, data pipelines, websites, ML models, and more.

## Why Backstage?

### The Problem Backstage Solves

**Before Backstage:**
- Services scattered across multiple tools
- No single source of truth for ownership
- Inconsistent documentation
- Duplicated effort (reinventing scaffolding)
- Hard to discover APIs and services
- Context switching between tools

**After Backstage:**
- Unified software catalog
- Clear ownership and dependencies
- Documentation alongside code
- Standardized service creation
- Searchable service registry
- Single pane of glass

### Core Features

1. **Software Catalog**: Metadata about all software in your organization
2. **Software Templates**: Scaffolding for creating new services
3. **TechDocs**: Docs-like-code, Markdown documentation
4. **Plugins**: Extensible ecosystem for integrations
5. **Search**: Unified search across all entities
6. **Kubernetes**: View and manage K8s resources
7. **CI/CD Integration**: View pipeline status
8. **API Docs**: Auto-generated API documentation

## Architecture

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   Backstage Frontend                        │
│                      (React SPA)                            │
├────────────────────────────────────────────────────────────┤
│  Core Features:                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Catalog  │ │Templates │ │ TechDocs │ │  Search  │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│                                                             │
│  Plugins:                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │   K8s    │ │  ArgoCD  │ │  GitHub  │ │ PagerDuty│     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                   Backstage Backend                         │
│                     (Node.js)                               │
├────────────────────────────────────────────────────────────┤
│  Backend Services:                                          │
│  - Catalog Service (entities, relations)                   │
│  - Scaffolder Service (template execution)                 │
│  - TechDocs Service (docs generation)                      │
│  - Search Service (indexing, querying)                     │
│  - Auth Service (identity, permissions)                    │
│  - Proxy Service (external API access)                     │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  PostgreSQL  │  │    GitHub    │  │      K8s     │    │
│  │  (Catalog)   │  │  (Templates) │  │   (Deploy)   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Frontend:**
- React-based SPA
- Material-UI components
- Plugin system for UI extensions
- Routing and navigation

**Backend:**
- Node.js Express server
- Plugin system for API extensions
- Task scheduling (cron jobs)
- Database abstraction layer

**Plugins:**
- Frontend + Backend bundles
- Provide additional functionality
- Can integrate external services

## Installation and Setup

### Prerequisites

```bash
# Node.js 18+ and yarn
node --version  # v18.0.0 or higher
yarn --version  # 1.22.0 or higher

# Git
git --version
```

### Quick Start

```bash
# Create new Backstage app
npx @backstage/create-app@latest

# Follow prompts
? Enter a name for the app [required]: my-platform-portal

# Navigate to app
cd my-platform-portal

# Start development server
yarn dev

# Open browser
# Frontend: http://localhost:3000
# Backend: http://localhost:7007
```

### Production Setup

#### 1. Database Configuration

**PostgreSQL Setup:**

```bash
# Install PostgreSQL (production)
# Don't use SQLite in production!

# Create database
createdb backstage_catalog

# Connection string
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=backstage
export POSTGRES_PASSWORD=your-secure-password
```

**app-config.production.yaml:**

```yaml
backend:
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}
      database: backstage_catalog
      ssl:
        rejectUnauthorized: false  # Use proper certs in production
```

#### 2. Authentication Configuration

**GitHub OAuth Setup:**

```yaml
# app-config.yaml
auth:
  environment: production
  providers:
    github:
      production:
        clientId: ${GITHUB_CLIENT_ID}
        clientSecret: ${GITHUB_CLIENT_SECRET}
```

**Create GitHub OAuth App:**
1. Go to GitHub Settings → Developer Settings → OAuth Apps
2. Create new OAuth App
3. Homepage URL: `https://backstage.company.com`
4. Callback URL: `https://backstage.company.com/api/auth/github/handler/frame`
5. Copy Client ID and Client Secret

#### 3. Kubernetes Deployment

**Dockerfile:**

```dockerfile
# Multi-stage build
FROM node:18-bullseye-slim AS build

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --production

COPY . .
RUN yarn tsc
RUN yarn build:backend

# Production image
FROM node:18-bullseye-slim

WORKDIR /app
COPY --from=build /app/yarn.lock /app/package.json /app/
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/packages/backend/dist /app/packages/backend/dist

CMD ["node", "packages/backend/dist/index.js"]
```

**Kubernetes Manifests:**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backstage
  namespace: platform
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backstage
  template:
    metadata:
      labels:
        app: backstage
    spec:
      containers:
      - name: backstage
        image: company/backstage:latest
        ports:
        - containerPort: 7007
        env:
        - name: POSTGRES_HOST
          value: postgres-service
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: backstage-secrets
              key: postgres-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: backstage-secrets
              key: postgres-password
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: backstage-secrets
              key: github-token
        livenessProbe:
          httpGet:
            path: /healthcheck
            port: 7007
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthcheck
            port: 7007
          initialDelaySeconds: 30
          periodSeconds: 10
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2
            memory: 2Gi
---
apiVersion: v1
kind: Service
metadata:
  name: backstage
  namespace: platform
spec:
  type: ClusterIP
  ports:
  - port: 7007
    targetPort: 7007
  selector:
    app: backstage
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backstage
  namespace: platform
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - backstage.company.com
    secretName: backstage-tls
  rules:
  - host: backstage.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backstage
            port:
              number: 7007
```

## Software Catalog

### Entity Model

Backstage organizes everything as "entities":

```
Domain (Business Area)
  └─ System (Group of Components)
      ├─ Component (Service, Library, Website)
      ├─ API (REST, GraphQL, gRPC)
      └─ Resource (Database, Queue, Bucket)

Group (Team)
  └─ User (Engineer)

Template (Scaffolding Template)
```

### Entity Types

#### 1. Component

Represents software: service, library, website, data pipeline.

```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: user-service
  title: User Service
  description: Manages user accounts and authentication
  annotations:
    github.com/project-slug: company/user-service
    backstage.io/kubernetes-label-selector: 'app=user-service'
    backstage.io/techdocs-ref: dir:.
  tags:
    - nodejs
    - api
    - authentication
  links:
    - url: https://api.company.com/users
      title: Production API
      icon: api
    - url: https://datadog.com/dashboard/user-service
      title: Monitoring Dashboard
      icon: dashboard
spec:
  type: service
  lifecycle: production
  owner: team-backend
  system: user-management
  providesApis:
    - user-api
  consumesApis:
    - email-api
    - notification-api
  dependsOn:
    - resource:user-database
    - resource:redis-cache
```

**Component Types:**
- `service`: Microservice, API
- `website`: Frontend application
- `library`: Shared library, SDK
- `documentation`: Documentation site

**Lifecycle:**
- `experimental`: Proof of concept
- `production`: Live in production
- `deprecated`: Being phased out

#### 2. API

Represents an interface between components.

```yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: user-api
  title: User API
  description: RESTful API for user management
  annotations:
    github.com/project-slug: company/user-service
spec:
  type: openapi
  lifecycle: production
  owner: team-backend
  system: user-management
  definition: |
    openapi: 3.0.0
    info:
      title: User API
      version: 1.0.0
    paths:
      /users:
        get:
          summary: List users
          responses:
            '200':
              description: Success
```

**API Types:**
- `openapi`: REST API (OpenAPI spec)
- `graphql`: GraphQL API
- `grpc`: gRPC service
- `asyncapi`: Event-driven API

#### 3. Resource

Represents infrastructure: database, queue, storage.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: user-database
  title: User Database
  description: PostgreSQL database for user data
  annotations:
    aws.amazon.com/rds-instance-id: user-db-prod
spec:
  type: database
  owner: team-backend
  system: user-management
  dependencyOf:
    - component:user-service
```

**Resource Types:**
- `database`: PostgreSQL, MySQL, MongoDB
- `queue`: SQS, RabbitMQ, Kafka
- `storage`: S3, Azure Blob, GCS
- `cache`: Redis, Memcached

#### 4. System

Groups related components.

```yaml
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: user-management
  title: User Management System
  description: All services related to user accounts
spec:
  owner: team-backend
  domain: identity
```

#### 5. Domain

Represents business capability areas.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: identity
  title: Identity Domain
  description: Authentication, authorization, and user management
spec:
  owner: group:engineering
```

#### 6. Group (Team)

```yaml
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: team-backend
  title: Backend Team
  description: Backend services and APIs
spec:
  type: team
  profile:
    displayName: Backend Team
    email: backend-team@company.com
    picture: https://avatars.company.com/backend-team
  parent: engineering
  children: []
  members:
    - alice
    - bob
    - charlie
```

#### 7. User

```yaml
apiVersion: backstage.io/v1alpha1
kind: User
metadata:
  name: alice
spec:
  profile:
    displayName: Alice Smith
    email: alice@company.com
    picture: https://avatars.company.com/alice
  memberOf:
    - team-backend
```

### Catalog Organization Strategies

#### Strategy 1: Monorepo

Single `catalog-info.yaml` at repo root, listing all components.

```yaml
# catalog-info.yaml (root)
apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: monorepo-root
spec:
  targets:
    - ./services/user-service/catalog-info.yaml
    - ./services/order-service/catalog-info.yaml
    - ./services/payment-service/catalog-info.yaml
```

#### Strategy 2: Polyrepo

Each repo has its own `catalog-info.yaml`.

```yaml
# Catalog configuration
catalog:
  locations:
    - type: url
      target: https://github.com/company/user-service/blob/main/catalog-info.yaml
    - type: url
      target: https://github.com/company/order-service/blob/main/catalog-info.yaml
```

#### Strategy 3: Auto-Discovery

Backstage automatically discovers repos with `catalog-info.yaml`.

```yaml
# app-config.yaml
catalog:
  providers:
    github:
      providerId:
        organization: 'company'
        catalogPath: '/catalog-info.yaml'
        filters:
          branch: 'main'
          repository: '.*'  # All repos
  rules:
    - allow: [Component, System, API, Resource, Location]
```

### Advanced Catalog Features

#### Relations and Dependencies

```yaml
# user-service depends on user-database
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: user-service
spec:
  dependsOn:
    - resource:user-database

---
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: user-database
spec:
  dependencyOf:
    - component:user-service
```

Backstage automatically creates bidirectional relationships:
- `dependsOn` / `dependencyOf`
- `providesApi` / `apiProvidedBy`
- `consumesApi` / `apiConsumedBy`
- `hasSubcomponent` / `subcomponentOf`

#### Annotations

Annotations integrate with external systems:

```yaml
metadata:
  annotations:
    # GitHub integration
    github.com/project-slug: company/user-service

    # Kubernetes integration
    backstage.io/kubernetes-label-selector: 'app=user-service'
    backstage.io/kubernetes-namespace: production

    # ArgoCD integration
    argocd/app-name: user-service-prod

    # TechDocs
    backstage.io/techdocs-ref: dir:.

    # PagerDuty
    pagerduty.com/service-id: PX7X8Y9

    # Datadog
    datadog/dashboard-url: https://datadog.com/dashboard/123

    # Sentry
    sentry.io/project-slug: user-service

    # Cost tracking
    aws.amazon.com/cost-allocation-tag: user-service

    # Ownership
    opsgenie.com/team: backend-team
```

## Software Templates (Scaffolder)

### Template Structure

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: nodejs-microservice
  title: Node.js Microservice
  description: Create a production-ready Node.js microservice
  tags:
    - recommended
    - nodejs
    - typescript
spec:
  owner: platform-team
  type: service

  # Input form for developers
  parameters:
    - title: Service Information
      required:
        - name
        - owner
      properties:
        name:
          title: Service Name
          type: string
          description: Unique name for this service
          ui:autofocus: true
          ui:options:
            rows: 5
        description:
          title: Description
          type: string
          description: What does this service do?
        owner:
          title: Owner
          type: string
          description: Team that owns this service
          ui:field: OwnerPicker
          ui:options:
            allowedKinds:
              - Group

    - title: Service Configuration
      properties:
        database:
          title: Database
          type: string
          description: Does this service need a database?
          default: postgres
          enum:
            - postgres
            - mysql
            - mongodb
            - none
          enumNames:
            - PostgreSQL
            - MySQL
            - MongoDB
            - No Database
        cache:
          title: Cache
          type: boolean
          description: Include Redis cache?
          default: false
        queue:
          title: Message Queue
          type: boolean
          description: Include message queue (SQS)?
          default: false

    - title: Repository
      required:
        - repoUrl
      properties:
        repoUrl:
          title: Repository Location
          type: string
          ui:field: RepoUrlPicker
          ui:options:
            allowedHosts:
              - github.com
            allowedOwners:
              - company

  # Execution steps
  steps:
    # Step 1: Fetch template from GitHub
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./templates/nodejs-microservice
        values:
          name: ${{ parameters.name }}
          description: ${{ parameters.description }}
          owner: ${{ parameters.owner }}
          database: ${{ parameters.database }}
          cache: ${{ parameters.cache }}
          queue: ${{ parameters.queue }}

    # Step 2: Create GitHub repository
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        description: ${{ parameters.description }}
        repoUrl: ${{ parameters.repoUrl }}
        repoVisibility: internal
        defaultBranch: main
        protectDefaultBranch: true
        deleteBranchOnMerge: true

    # Step 3: Provision database (conditional)
    - id: create-database
      if: ${{ parameters.database !== 'none' }}
      name: Provision Database
      action: http:backstage:request
      input:
        method: POST
        path: /api/platform/database
        body:
          type: ${{ parameters.database }}
          name: ${{ parameters.name }}-db
          owner: ${{ parameters.owner }}

    # Step 4: Setup CI/CD
    - id: create-cicd
      name: Create CI/CD Pipeline
      action: github:actions:dispatch
      input:
        repoUrl: ${{ parameters.repoUrl }}
        workflowId: setup-pipeline.yml
        branchOrTagName: main
        workflowInputs:
          service_name: ${{ parameters.name }}

    # Step 5: Create Kubernetes namespace
    - id: create-namespace
      name: Create K8s Namespace
      action: kubernetes:apply
      input:
        manifestPath: ./manifests/namespace.yaml
        namespaced: false

    # Step 6: Register in catalog
    - id: register
      name: Register Component in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  # Output links displayed to user
  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
        icon: github
      - title: View in Catalog
        url: /catalog/default/component/${{ parameters.name }}
        icon: catalog
      - title: CI/CD Pipeline
        url: ${{ steps.publish.output.remoteUrl }}/actions
        icon: github
      - title: Open in Editor
        entityRef: ${{ steps.register.output.entityRef }}
```

### Template Actions

**Built-in Actions:**

```yaml
# Fetch template from filesystem or Git
- action: fetch:template
  input:
    url: ./templates/nodejs-service
    values:
      name: my-service

# Publish to GitHub
- action: publish:github
  input:
    repoUrl: github.com?owner=company&repo=my-service

# Register in catalog
- action: catalog:register
  input:
    catalogInfoPath: /catalog-info.yaml

# Execute custom script
- action: debug:log
  input:
    message: 'Creating service ${{ parameters.name }}'

# Make HTTP request
- action: http:backstage:request
  input:
    method: POST
    path: /api/custom-endpoint
    body:
      key: value
```

**Custom Actions:**

```typescript
// packages/backend/src/plugins/scaffolder/actions/provision-database.ts
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';

export const provisionDatabaseAction = createTemplateAction<{
  type: 'postgres' | 'mysql' | 'mongodb';
  name: string;
  size: 'small' | 'medium' | 'large';
}>({
  id: 'platform:database:provision',
  description: 'Provisions a database via Crossplane',
  schema: {
    input: {
      required: ['type', 'name'],
      type: 'object',
      properties: {
        type: { type: 'string', enum: ['postgres', 'mysql', 'mongodb'] },
        name: { type: 'string' },
        size: { type: 'string', enum: ['small', 'medium', 'large'], default: 'small' },
      },
    },
    output: {
      type: 'object',
      properties: {
        connectionString: { type: 'string' },
        secretName: { type: 'string' },
      },
    },
  },
  async handler(ctx) {
    const { type, name, size } = ctx.input;

    ctx.logger.info(`Provisioning ${type} database: ${name} (${size})`);

    // Call Crossplane API or Kubernetes API
    const manifest = {
      apiVersion: 'database.platform.company.com/v1alpha1',
      kind: 'Database',
      metadata: { name },
      spec: { type, size },
    };

    // Apply manifest (use Kubernetes client)
    // ...

    ctx.output('connectionString', `${type}://user:pass@host:5432/${name}`);
    ctx.output('secretName', `${name}-credentials`);
  },
});
```

**Register Custom Action:**

```typescript
// packages/backend/src/plugins/scaffolder.ts
import { provisionDatabaseAction } from './actions/provision-database';

const actions = [
  ...builtInActions,
  provisionDatabaseAction(),
];

return await createRouter({
  actions,
  // ...
});
```

### Template Best Practices

1. **Keep Templates Simple**
   - Start with minimal options
   - Add complexity based on feedback

2. **Validate Input**
   - Use JSON schema validation
   - Provide helpful error messages

3. **Idempotent Actions**
   - Templates should be re-runnable
   - Handle existing resources gracefully

4. **Clear Output**
   - Provide links to created resources
   - Show next steps

5. **Test Templates**
   - Create test instances
   - Verify end-to-end flow

## TechDocs

### Setup TechDocs

**app-config.yaml:**

```yaml
techdocs:
  builder: 'local'  # or 'external'
  generator:
    runIn: 'docker'  # or 'local'
  publisher:
    type: 'local'  # or 'awsS3', 'azureBlobStorage', 'googleGcs'
```

### Creating Documentation

**1. Add mkdocs.yaml to repo:**

```yaml
# mkdocs.yaml
site_name: 'User Service Documentation'
site_description: 'Documentation for the User Service'

nav:
  - Home: index.md
  - Architecture: architecture.md
  - API Reference: api.md
  - Runbooks:
    - Deployment: runbooks/deployment.md
    - Troubleshooting: runbooks/troubleshooting.md

plugins:
  - techdocs-core

theme:
  name: material
  palette:
    primary: indigo
```

**2. Write Markdown docs:**

```markdown
<!-- docs/index.md -->
# User Service

## Overview

The User Service handles user authentication and profile management.

## Quick Start

\`\`\`bash
npm install
npm start
\`\`\`

## Architecture

![Architecture Diagram](./images/architecture.png)

## API Endpoints

- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/:id` - Get user by ID
```

**3. Link in catalog-info.yaml:**

```yaml
metadata:
  annotations:
    backstage.io/techdocs-ref: dir:.
```

**4. Preview locally:**

```bash
npx @techdocs/cli serve
```

## Plugins

### Essential Plugins

#### 1. Kubernetes Plugin

View and manage Kubernetes resources.

**Installation:**

```bash
yarn add --cwd packages/app @backstage/plugin-kubernetes
yarn add --cwd packages/backend @backstage/plugin-kubernetes-backend
```

**Configuration:**

```yaml
# app-config.yaml
kubernetes:
  serviceLocatorMethod:
    type: 'multiTenant'
  clusterLocatorMethods:
    - type: 'config'
      clusters:
        - name: production
          url: https://k8s-prod.company.com
          authProvider: 'serviceAccount'
          serviceAccountToken: ${K8S_PROD_TOKEN}
        - name: staging
          url: https://k8s-staging.company.com
          authProvider: 'serviceAccount'
          serviceAccountToken: ${K8S_STAGING_TOKEN}
```

**Usage in catalog:**

```yaml
metadata:
  annotations:
    backstage.io/kubernetes-label-selector: 'app=user-service'
```

#### 2. ArgoCD Plugin

View ArgoCD application status.

```yaml
metadata:
  annotations:
    argocd/app-selector: 'app=user-service'
```

#### 3. GitHub Actions Plugin

View CI/CD pipeline status.

```yaml
metadata:
  annotations:
    github.com/project-slug: company/user-service
```

#### 4. PagerDuty Plugin

View on-call and incidents.

```yaml
metadata:
  annotations:
    pagerduty.com/integration-key: abc123
```

### Creating Custom Plugins

**Generate plugin:**

```bash
yarn new --select plugin
# Plugin ID: platform-metrics
# Plugin owner: platform-team
```

**File structure:**

```
plugins/
└── platform-metrics/
    ├── src/
    │   ├── components/
    │   │   └── MetricsCard/
    │   │       ├── MetricsCard.tsx
    │   │       └── index.ts
    │   ├── api/
    │   │   ├── PlatformMetricsApi.ts
    │   │   └── PlatformMetricsClient.ts
    │   ├── plugin.ts
    │   └── index.ts
    └── package.json
```

**Example plugin:**

```typescript
// plugins/platform-metrics/src/plugin.ts
import { createPlugin, createComponentExtension } from '@backstage/core-plugin-api';

export const platformMetricsPlugin = createPlugin({
  id: 'platform-metrics',
});

export const EntityPlatformMetricsCard = platformMetricsPlugin.provide(
  createComponentExtension({
    name: 'EntityPlatformMetricsCard',
    component: {
      lazy: () => import('./components/MetricsCard').then(m => m.MetricsCard),
    },
  })
);
```

```typescript
// plugins/platform-metrics/src/components/MetricsCard/MetricsCard.tsx
import React from 'react';
import { InfoCard } from '@backstage/core-components';
import { useEntity } from '@backstage/plugin-catalog-react';

export const MetricsCard = () => {
  const { entity } = useEntity();

  return (
    <InfoCard title="Platform Metrics">
      <p>Deployment Frequency: 12/day</p>
      <p>Lead Time: 45 minutes</p>
      <p>MTTR: 30 minutes</p>
    </InfoCard>
  );
};
```

**Add to entity page:**

```typescript
// packages/app/src/components/catalog/EntityPage.tsx
import { EntityPlatformMetricsCard } from '@internal/plugin-platform-metrics';

const serviceEntityPage = (
  <EntityLayout>
    <EntityLayout.Route path="/" title="Overview">
      <Grid container spacing={3}>
        <Grid item md={6}>
          <EntityAboutCard variant="gridItem" />
        </Grid>
        <Grid item md={6}>
          <EntityPlatformMetricsCard />
        </Grid>
      </Grid>
    </EntityLayout.Route>
  </EntityLayout>
);
```

## Search

### Configure Search

```yaml
# app-config.yaml
search:
  pg:
    highlightOptions:
      useHighlight: true
      maxWord: 35
      minWord: 15
      maxFragments: 3
      fragmentDelimiter: ' ... '
```

### Indexing

Backstage automatically indexes:
- Catalog entities
- TechDocs
- Custom collators

**Custom collator:**

```typescript
// packages/backend/src/plugins/search.ts
import { CatalogCollatorFactory } from '@backstage/plugin-catalog-backend';

const catalogCollator = CatalogCollatorFactory.fromConfig(config, {
  discovery,
  tokenManager,
});
```

## Best Practices

### 1. Catalog Organization

- Use consistent naming (kebab-case)
- Define clear ownership
- Document all entities
- Keep annotations minimal and purposeful

### 2. Templates

- Start simple, iterate
- Validate all inputs
- Provide escape hatches
- Test end-to-end

### 3. TechDocs

- Keep docs close to code
- Use ADRs (Architecture Decision Records)
- Include runbooks
- Auto-generate what you can (API docs)

### 4. Performance

- Limit catalog entities (< 10,000)
- Use catalog refresh intervals
- Cache external API calls
- Horizontal scaling for backend

### 5. Security

- Implement RBAC (Role-Based Access Control)
- Use OAuth providers
- Rotate tokens regularly
- Audit access logs

## Troubleshooting

### Catalog not updating

```bash
# Force catalog refresh
curl -X POST http://localhost:7007/api/catalog/refresh

# Check catalog processing
kubectl logs -n backstage backstage-backend | grep catalog
```

### Template failing

```bash
# Check scaffolder logs
kubectl logs -n backstage backstage-backend | grep scaffolder

# Validate template YAML
backstage-cli repo schema openapi verify
```

### TechDocs not generating

```bash
# Check TechDocs logs
kubectl logs -n backstage backstage-backend | grep techdocs

# Validate mkdocs.yaml
mkdocs build
```

## Resources

- **Official Docs**: https://backstage.io/docs
- **GitHub**: https://github.com/backstage/backstage
- **Discord**: https://discord.gg/backstage
- **Roadmap**: https://backstage.io/docs/overview/roadmap
