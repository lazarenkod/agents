# Golden Paths Reference Guide

## Overview

Golden paths (also called "paved roads" or "well-lit paths") are the opinionated, production-ready paths that make the right thing the easy thing. This guide provides comprehensive templates and patterns for implementing golden paths in your platform.

## Philosophy

### Core Principles

1. **Opinionated but Escapable**: Strong defaults with override capabilities
2. **Complete Journey**: From local dev to production
3. **Production-Ready**: Battle-tested, secure, observable
4. **Self-Documenting**: Obvious what to do, why, and how
5. **Continuously Improved**: Feedback loops drive enhancements

### Golden Path Characteristics

```yaml
golden_path_checklist:
  defaults:
    - Production-ready configuration
    - Security best practices baked in
    - Observability instrumented
    - Testing framework included
    - CI/CD pipeline configured

  developer_experience:
    - Time to "hello world": < 5 minutes
    - Time to production: < 1 hour
    - Learning curve: minimal
    - Cognitive load: low

  flexibility:
    - Escape hatches for advanced use
    - Override mechanism documented
    - Support for "bring your own"
    - No forced adoption

  reliability:
    - Battle-tested in production
    - SLA defined and monitored
    - Failure modes handled
    - Rollback procedures clear
```

## Golden Path Templates

### 1. Service Creation Golden Path

#### Journey Map

```
Developer Journey: Create New Service
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Initialization (< 5 minutes)                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Open Backstage                                            │
│ 2. Click "Create Component"                                  │
│ 3. Select template (Node.js Microservice)                    │
│ 4. Fill form (5 fields: name, description, owner, db, repo) │
│ 5. Click "Create"                                            │
│                                                               │
│ Platform Actions (automated, 30-60 seconds):                 │
│  ✓ Create GitHub repository                                  │
│  ✓ Scaffold code (app + tests)                               │
│  ✓ Configure CI/CD                                           │
│  ✓ Generate K8s manifests                                    │
│  ✓ Provision database                                        │
│  ✓ Create secrets                                            │
│  ✓ Setup monitoring                                          │
│  ✓ Register in catalog                                       │
│                                                               │
│ Output: Working repo with CI/CD                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Local Development (< 2 minutes)                     │
├─────────────────────────────────────────────────────────────┤
│ 1. git clone <repo>                                          │
│ 2. npm install                                               │
│ 3. npm start                                                 │
│                                                               │
│ Platform Provides:                                           │
│  ✓ docker-compose.yml (local deps: db, redis)               │
│  ✓ .env.example (configuration)                              │
│  ✓ Sample data seeding                                       │
│  ✓ Hot reload enabled                                        │
│                                                               │
│ Output: Service running on localhost:3000                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 3: First Deployment (< 5 minutes)                      │
├─────────────────────────────────────────────────────────────┤
│ 1. Write code (implement endpoint)                           │
│ 2. Write test                                                │
│ 3. git commit -m "Add feature"                               │
│ 4. git push                                                  │
│                                                               │
│ Platform Actions (automated, 2-3 minutes):                   │
│  ✓ Run tests                                                 │
│  ✓ Run linter                                                │
│  ✓ Security scan (Snyk, Trivy)                              │
│  ✓ Build Docker image                                        │
│  ✓ Push to registry                                          │
│  ✓ Deploy to dev environment                                 │
│  ✓ Run smoke tests                                           │
│  ✓ Update Backstage status                                   │
│                                                               │
│ Output: Service live in dev (dev.company.com/user-service)   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Pull Request Preview (< 3 minutes)                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Create PR with changes                                    │
│ 2. Platform creates preview environment                      │
│                                                               │
│ Platform Actions (automated, 2-3 minutes):                   │
│  ✓ Create ephemeral namespace                                │
│  ✓ Deploy branch to preview env                              │
│  ✓ Provision preview database                                │
│  ✓ Generate preview URL                                      │
│  ✓ Comment URL on PR                                         │
│  ✓ Run integration tests                                     │
│                                                               │
│ Output: pr-123.preview.company.com                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 5: Production Deployment (< 10 minutes)                │
├─────────────────────────────────────────────────────────────┤
│ 1. Merge PR                                                  │
│ 2. Platform deploys to staging                               │
│ 3. Run smoke tests in staging                                │
│ 4. Click "Promote to Production" in Backstage                │
│                                                               │
│ Platform Actions (automated, 5-10 minutes):                  │
│  ✓ Blue/green deployment                                     │
│  ✓ Health checks pass                                        │
│  ✓ Smoke tests pass                                          │
│  ✓ Gradual traffic shift (0% → 10% → 50% → 100%)            │
│  ✓ Monitor error rates                                       │
│  ✓ Auto-rollback if errors spike                             │
│  ✓ Send Slack notification                                   │
│  ✓ Update Backstage status                                   │
│                                                               │
│ Output: Service live in production (api.company.com)         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 6: Post-Deployment (automatic)                         │
├─────────────────────────────────────────────────────────────┤
│ Platform Provides (no action needed):                        │
│  ✓ Grafana dashboard (requests, errors, latency)            │
│  ✓ Log aggregation (search in Backstage)                    │
│  ✓ Distributed tracing                                       │
│  ✓ Alerts configured (error rate, latency p99)              │
│  ✓ Cost tracking (by service)                                │
│  ✓ Security scanning (daily)                                 │
│                                                               │
│ Total Time: Idea to Production in < 30 minutes               │
└─────────────────────────────────────────────────────────────┘
```

#### What's Included

**Repository Structure:**

```
user-service/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Run tests, lint, build
│       ├── deploy-dev.yml      # Auto-deploy to dev
│       ├── deploy-staging.yml  # Auto-deploy to staging
│       └── deploy-prod.yml     # Deploy to production
├── src/
│   ├── app.ts                  # Express app setup
│   ├── routes/
│   │   └── users.ts            # Example routes
│   ├── models/
│   │   └── user.ts             # Database models
│   ├── middleware/
│   │   ├── auth.ts             # JWT authentication
│   │   ├── error.ts            # Error handling
│   │   └── logging.ts          # Request logging
│   └── utils/
│       ├── db.ts               # Database connection
│       └── metrics.ts          # Prometheus metrics
├── tests/
│   ├── unit/
│   │   └── users.test.ts       # Unit tests
│   └── integration/
│       └── api.test.ts         # Integration tests
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml     # K8s deployment
│   │   ├── service.yaml        # K8s service
│   │   └── ingress.yaml        # Ingress config
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── production/
├── docs/
│   ├── index.md                # Service documentation
│   ├── api.md                  # API reference
│   └── runbooks/
│       ├── deployment.md
│       └── troubleshooting.md
├── Dockerfile                  # Multi-stage build
├── docker-compose.yml          # Local development
├── .env.example                # Environment variables
├── catalog-info.yaml           # Backstage catalog
├── mkdocs.yml                  # TechDocs config
├── package.json
├── tsconfig.json
└── README.md
```

**Key Files:**

**Dockerfile (Multi-stage, Optimized):**

```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm ci --only=development

# Copy source code
COPY src ./src

# Build TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine

# Security: non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy production dependencies
COPY --from=build --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
COPY --chown=nodejs:nodejs package.json ./

# Switch to non-root user
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

EXPOSE 3000

CMD ["node", "dist/app.js"]
```

**docker-compose.yml (Local Dev):**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://user:password@postgres:5432/userservice
      REDIS_URL: redis://redis:6379
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
    depends_on:
      - postgres
      - redis
    command: npm run dev

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: userservice
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/seed.sql:/docker-entrypoint-initdb.d/seed.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

**CI/CD Pipeline (.github/workflows/ci.yml):**

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Code coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -t ${{ secrets.REGISTRY }}/user-service:${{ github.sha }} .
          docker tag ${{ secrets.REGISTRY }}/user-service:${{ github.sha }} \
                     ${{ secrets.REGISTRY }}/user-service:latest

      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push ${{ secrets.REGISTRY }}/user-service:${{ github.sha }}
          docker push ${{ secrets.REGISTRY }}/user-service:latest

      - name: Deploy to dev
        if: github.ref == 'refs/heads/main'
        run: |
          # Trigger ArgoCD sync
          curl -X POST https://argocd.company.com/api/v1/applications/user-service-dev/sync \
            -H "Authorization: Bearer ${{ secrets.ARGOCD_TOKEN }}"
```

**Kubernetes Manifests (k8s/base/deployment.yaml):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  labels:
    app: user-service
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: user-service
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001

      containers:
      - name: app
        image: company/user-service:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
          name: http
          protocol: TCP

        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-db
              key: connection-string
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: user-service-redis
              key: url

        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1001
          capabilities:
            drop:
            - ALL

      # Horizontal Pod Autoscaling
      ---
      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: user-service
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: user-service
        minReplicas: 3
        maxReplicas: 10
        metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 70
        - type: Resource
          resource:
            name: memory
            target:
              type: Utilization
              averageUtilization: 80
```

**Application Code with Observability (src/app.ts):**

```typescript
import express from 'express';
import prometheus from 'prom-client';
import { trace } from '@opentelemetry/api';
import { logger } from './utils/logger';
import { connectDatabase } from './utils/db';
import userRoutes from './routes/users';
import { errorHandler } from './middleware/error';
import { requestLogger } from './middleware/logging';

const app = express();

// Prometheus metrics
const register = prometheus.register;
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
});

const httpRequestTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

// Middleware
app.use(express.json());
app.use(requestLogger);

// Metrics middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration.labels(req.method, req.route?.path || req.path, res.statusCode.toString()).observe(duration);
    httpRequestTotal.labels(req.method, req.route?.path || req.path, res.statusCode.toString()).inc();
  });
  next();
});

// Health checks
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.get('/ready', async (req, res) => {
  // Check database connection
  try {
    await connectDatabase();
    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// Routes
app.use('/api/users', userRoutes);

// Error handling
app.use(errorHandler);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

export default app;
```

### 2. Database Provisioning Golden Path

#### Journey Map

```
Developer Journey: Request Database
┌─────────────────────────────────────────────────────────────┐
│ Option A: Via Backstage Template (Preferred)                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Fill service template                                     │
│ 2. Select "PostgreSQL" from database dropdown                │
│ 3. Click create                                              │
│ 4. Platform provisions database automatically                │
│                                                               │
│ Time: < 30 seconds                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Option B: Standalone Database Request                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Open Backstage                                            │
│ 2. Navigate to "Create" → "Database"                         │
│ 3. Fill form:                                                │
│    - Database type: PostgreSQL                               │
│    - Name: user-db                                           │
│    - Environment: production                                 │
│    - Size: medium (auto-selected based on workload)          │
│ 4. Click "Provision"                                         │
│                                                               │
│ Platform Actions (automated, 3-5 minutes):                   │
│  ✓ Validate request (name unique, quotas)                   │
│  ✓ Create Crossplane claim                                   │
│  ✓ Provision RDS instance (or CloudNativePG)                │
│  ✓ Configure security group / network policies              │
│  ✓ Enable encryption at rest                                 │
│  ✓ Configure automated backups (daily, 30-day retention)    │
│  ✓ Create Vault secret with credentials                      │
│  ✓ Setup External Secret in K8s                              │
│  ✓ Create Grafana dashboard                                  │
│  ✓ Configure alerts (connections, replication lag)          │
│  ✓ Register resource in Backstage catalog                    │
│  ✓ Tag for cost allocation                                   │
│                                                               │
│ Output:                                                       │
│  - Secret name: user-db-credentials                          │
│  - Connection string available in app                        │
│  - Dashboard: grafana.company.com/d/user-db                  │
│                                                               │
│ Time: 3-5 minutes                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Option C: Declare in Code (Platform-as-Code)                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Add to score.yaml or platform config:                     │
│                                                               │
│    resources:                                                │
│      database:                                               │
│        type: postgres                                        │
│        properties:                                           │
│          version: "15"                                       │
│          size: medium                                        │
│                                                               │
│ 2. git commit && git push                                    │
│ 3. Platform detects change and provisions                    │
│                                                               │
│ Time: 3-5 minutes (automatic)                                │
└─────────────────────────────────────────────────────────────┘
```

#### What's Included

**Database Sizes:**

```yaml
# Platform-defined database sizes
database_sizes:
  small:
    aws: db.t3.small
    azure: B_Gen5_1
    gcp: db-f1-micro
    storage: 20GB
    connections: 100
    cost: ~$20/month
    use_case: Development, testing

  medium:
    aws: db.t3.medium
    azure: GP_Gen5_2
    gcp: db-n1-standard-2
    storage: 100GB
    connections: 500
    cost: ~$100/month
    use_case: Production (most services)

  large:
    aws: db.m5.large
    azure: GP_Gen5_4
    gcp: db-n1-standard-4
    storage: 500GB
    connections: 2000
    cost: ~$400/month
    use_case: High-traffic services

  xlarge:
    aws: db.m5.2xlarge
    azure: GP_Gen5_8
    gcp: db-n1-standard-8
    storage: 1TB
    connections: 5000
    cost: ~$800/month
    use_case: Critical, high-volume services
    requires_approval: true
```

**Production-Ready Configuration:**

```yaml
# Crossplane Composite Resource Definition
apiVersion: database.platform.company.com/v1alpha1
kind: PostgreSQLDatabase
metadata:
  name: user-db-prod
spec:
  parameters:
    version: "15"
    size: medium
    environment: production
    backup:
      enabled: true
      retention: 30
      window: "03:00-04:00"
    monitoring:
      enabled: true
      alerts:
        - high-connections
        - replication-lag
        - storage-full
    encryption:
      atRest: true
      inTransit: true
    highAvailability:
      enabled: true
      replicaCount: 2
    maintenance:
      window: "sun:04:00-sun:05:00"
      autoMinorVersionUpgrade: true
```

**Secret Management:**

```yaml
# External Secret (automatically created)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: user-db-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: user-db-credentials
    template:
      engineVersion: v2
      data:
        DATABASE_URL: "postgresql://{{ .username }}:{{ .password }}@{{ .host }}:{{ .port }}/{{ .database }}?sslmode=require"
        DB_HOST: "{{ .host }}"
        DB_PORT: "{{ .port }}"
        DB_NAME: "{{ .database }}"
        DB_USER: "{{ .username }}"
        DB_PASSWORD: "{{ .password }}"
  dataFrom:
  - extract:
      key: database/user-db-prod
```

**Application Usage:**

```typescript
// Database connection (automatic via env vars)
import { Sequelize } from 'sequelize';

const sequelize = new Sequelize(process.env.DATABASE_URL, {
  dialect: 'postgres',
  logging: false,
  pool: {
    max: 20,
    min: 5,
    acquire: 30000,
    idle: 10000,
  },
  ssl: process.env.NODE_ENV === 'production',
});

// Connection is automatically configured with:
// - Correct credentials (rotated automatically)
// - SSL enabled
// - Connection pooling
// - Retry logic
```

### 3. Preview Environments Golden Path

#### Journey Map

```
Developer Journey: Preview Environment
┌─────────────────────────────────────────────────────────────┐
│ Automatic on Pull Request                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. Developer creates PR                                      │
│ 2. Platform detects PR                                       │
│                                                               │
│ Platform Actions (automated, 2-3 minutes):                   │
│  ✓ Create namespace: pr-123                                  │
│  ✓ Deploy PR branch to namespace                             │
│  ✓ Provision preview database (ephemeral)                    │
│  ✓ Seed database with test data                              │
│  ✓ Create ingress with unique URL                            │
│  ✓ Run smoke tests                                           │
│  ✓ Comment URL on PR                                         │
│                                                               │
│ Output:                                                       │
│  - Preview URL: pr-123.preview.company.com                   │
│  - Comment on PR with link                                   │
│  - Preview ready for testing                                 │
│                                                               │
│ Lifecycle:                                                    │
│  - Auto-update on new commits                                │
│  - Auto-delete after PR merge                                │
│  - Auto-delete after 7 days of inactivity                    │
│  - Manual delete via comment: /platform delete-preview       │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation

**ArgoCD ApplicationSet:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: preview-environments
  namespace: argocd
spec:
  generators:
  - pullRequest:
      github:
        owner: company
        repo: user-service
        tokenRef:
          secretName: github-token
          key: token
      requeueAfterSeconds: 60

  template:
    metadata:
      name: 'user-service-pr-{{number}}'
      labels:
        environment: preview
        pr-number: '{{number}}'
      annotations:
        notifications.argoproj.io/subscribe.on-sync-succeeded.github: ''
    spec:
      project: default
      source:
        repoURL: https://github.com/company/user-service
        targetRevision: '{{head_sha}}'
        path: k8s/overlays/preview
        kustomize:
          namespace: 'pr-{{number}}'
          commonLabels:
            pr-number: '{{number}}'
          namePrefix: 'pr-{{number}}-'
          images:
          - 'company/user-service:pr-{{number}}'

      destination:
        server: https://kubernetes.default.svc
        namespace: 'pr-{{number}}'

      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true

      # Auto-cleanup after 7 days
      info:
      - name: 'Created'
        value: '{{createdAt}}'
```

**GitHub Action (Post Preview URL):**

```yaml
name: Preview Environment

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  create-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Wait for preview deployment
        run: |
          # Wait for ArgoCD to sync
          sleep 120

      - name: Get preview URL
        id: preview-url
        run: |
          PR_NUMBER=${{ github.event.pull_request.number }}
          URL="https://pr-${PR_NUMBER}.preview.company.com"
          echo "url=${URL}" >> $GITHUB_OUTPUT

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.name,
              body: `## Preview Environment Ready! 🚀\n\n✅ Your preview environment is ready:\n\n🔗 **URL:** ${{ steps.preview-url.outputs.url }}\n\n### Testing\n- Runs on latest commit: \`${context.sha.substring(0, 7)}\`\n- Auto-updates on new commits\n- Auto-deletes after PR merge or 7 days\n\n### Commands\n- \`/platform refresh-preview\` - Redeploy\n- \`/platform delete-preview\` - Delete now`
            })

      - name: Run smoke tests
        run: |
          URL="${{ steps.preview-url.outputs.url }}"
          curl -f ${URL}/health || exit 1
```

## Escape Hatches

### Three Levels of Customization

#### Level 1: Configuration Overrides (Easy)

**Override resource limits:**

```yaml
# k8s/overlays/production/kustomization.yaml
resources:
- ../../base

patches:
- patch: |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: user-service
    spec:
      template:
        spec:
          containers:
          - name: app
            resources:
              requests:
                cpu: 200m  # Override default 100m
                memory: 256Mi  # Override default 128Mi
              limits:
                cpu: 1000m  # Override default 500m
                memory: 1Gi  # Override default 512Mi
```

**Override environment variables:**

```yaml
# Add custom environment variable
env:
- name: CUSTOM_FEATURE_FLAG
  value: "true"
- name: EXTERNAL_API_URL
  value: "https://api.partner.com"
```

#### Level 2: Custom Resources (Moderate)

**Add sidecar container:**

```yaml
# k8s/overlays/production/sidecar-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  template:
    spec:
      containers:
      - name: app
        # ... main container
      - name: log-shipper
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: logs
          mountPath: /var/log
```

**Add init container:**

```yaml
initContainers:
- name: migrations
  image: company/user-service-migrations:latest
  env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: user-db-credentials
        key: url
```

#### Level 3: Full Control (Advanced)

**Bring your own Helm chart:**

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-service-custom
spec:
  source:
    repoURL: https://github.com/company/user-service
    path: custom-helm-chart
    helm:
      values: |
        replicaCount: 5
        customConfig:
          specialFeature: enabled
```

**Opt out of platform (with documentation):**

```yaml
# catalog-info.yaml
metadata:
  annotations:
    platform.company.com/managed: "false"
    platform.company.com/reason: "Custom Kafka configuration required"
    platform.company.com/documentation: "docs/custom-deployment.md"
```

## Self-Service Workflows

### 1. Increase Database Size

```yaml
# Developer action
kind: DatabaseResizeRequest
metadata:
  name: user-db-prod
spec:
  currentSize: medium
  requestedSize: large
  justification: "Traffic increased 10x, query latency spiking"

# Platform handles:
#  1. Validate request (check quotas)
#  2. Create maintenance window
#  3. Take snapshot
#  4. Resize instance
#  5. Verify health
#  6. Update cost allocation
#  7. Notify developer
```

### 2. Add Secret

```yaml
# Developer action (via Backstage form or CLI)
$ platform secret create \
    --name api-key \
    --service user-service \
    --environment production \
    --value <masked>

# Platform handles:
#  1. Store in Vault
#  2. Create ExternalSecret
#  3. Inject into pods
#  4. Notify via Slack
```

### 3. Request Production Access

```yaml
# Developer action (via Backstage)
kind: AccessRequest
metadata:
  name: alice-prod-access
spec:
  user: alice
  environment: production
  duration: 4h
  justification: "Debugging production issue #1234"

# Platform handles:
#  1. Notify manager for approval (auto-approve if < 1h)
#  2. Grant temporary RBAC role
#  3. Log access for audit
#  4. Auto-revoke after duration
#  5. Send summary of actions taken
```

## Metrics and Success Criteria

### Golden Path Effectiveness Metrics

```yaml
metrics:
  adoption:
    - golden_path_usage_rate: 85%  # Target: > 80%
    - new_services_using_platform: 95%  # Target: > 90%
    - legacy_services_migrated: 60%  # Target: > 50%

  developer_experience:
    - time_to_first_deployment: 30min  # Target: < 1h
    - time_to_hello_world: 3min  # Target: < 5min
    - developer_satisfaction: 8.5/10  # Target: > 8/10

  platform_performance:
    - template_success_rate: 98%  # Target: > 95%
    - average_provision_time: 4min  # Target: < 5min
    - platform_uptime: 99.9%  # Target: > 99.9%

  operational:
    - support_tickets_per_month: 12  # Target: < 20
    - time_to_resolve_issue: 2h  # Target: < 4h
    - escape_hatch_usage: 5%  # Target: < 10%
```

### Feedback Collection

**Quantitative:**

```typescript
// Instrumented in platform
analytics.track('template_used', {
  template: 'nodejs-microservice',
  user: 'alice',
  success: true,
  duration: 45,  // seconds
});

analytics.track('escape_hatch_used', {
  service: 'user-service',
  reason: 'custom_kafka_config',
  level: 3,  // full control
});
```

**Qualitative:**

```yaml
# Post-template survey (optional, after first use)
questions:
  - "How satisfied are you with the service creation experience? (1-10)"
  - "What was confusing or difficult?"
  - "What would you like to see improved?"

# Quarterly platform survey
questions:
  - "How would you rate the platform overall? (1-10)"
  - "What capability would help you most?"
  - "What's your biggest pain point?"
```

## Continuous Improvement

### Iteration Cycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Observe                                                    │
│    - Track metrics                                            │
│    - Monitor support tickets                                  │
│    - Read feedback surveys                                    │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Identify Pain Points                                       │
│    - High support volume for X                                │
│    - Low adoption of capability Y                             │
│    - Developers bypassing platform for Z                      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Prioritize                                                 │
│    - Impact vs effort matrix                                  │
│    - User research (talk to developers)                       │
│    - Align with platform roadmap                              │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Implement                                                  │
│    - Update templates                                         │
│    - Improve documentation                                    │
│    - Add new capability                                       │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Communicate                                                │
│    - Announce improvements                                    │
│    - Update documentation                                     │
│    - Run workshop if needed                                   │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Measure Impact                                             │
│    - Did metric improve?                                      │
│    - Did adoption increase?                                   │
│    - What did we learn?                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         └─────────► Back to step 1
```

### Versioning Golden Paths

```yaml
# Support multiple template versions
templates:
  - name: nodejs-microservice-v1
    status: deprecated
    deprecation_date: 2024-12-31
    migration_guide: docs/migration-v1-to-v2.md

  - name: nodejs-microservice-v2
    status: active
    recommended: true
    features:
      - TypeScript by default
      - OpenTelemetry instrumentation
      - Structured logging

  - name: nodejs-microservice-v3
    status: experimental
    features:
      - Fastify instead of Express
      - Native ESM
```

## Resources

- **Backstage Templates**: https://backstage.io/docs/features/software-templates
- **Team Topologies**: https://teamtopologies.com
- **Platform Engineering**: https://platformengineering.org
- **Score Specification**: https://score.dev
- **Crossplane**: https://crossplane.io
