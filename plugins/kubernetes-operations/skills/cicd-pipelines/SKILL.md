---
name: cicd-pipelines
description: Comprehensive CI/CD pipeline patterns for Kubernetes. Use when designing or implementing continuous integration and delivery workflows with Tekton, Argo Workflows, GitHub Actions, or other pipeline tools for Kubernetes environments.
---

# CI/CD Pipelines for Kubernetes

## Язык / Language

This skill provides guidance in both **Russian** and **English**. Choose your preferred language below:

- **[English Version](#english-version)** - Complete CI/CD pipeline patterns and practices
- **[Русская версия](#russian-version)** - Полное руководство по CI/CD конвейерам

---

## English Version

### When to Use This Skill

Use this skill when you need to:
- Design cloud-native CI/CD pipelines for Kubernetes
- Implement Tekton Pipelines or Argo Workflows
- Integrate GitHub Actions with Kubernetes deployments
- Build container images securely within Kubernetes
- Implement GitOps deployment patterns
- Set up multi-cluster deployment pipelines
- Add security scanning and compliance checks
- Monitor and observe pipeline executions
- Implement supply chain security (SLSA, Sigstore)

### Core Concepts

#### 1. Kubernetes-Native CI/CD Architectures

**Tekton vs Argo Workflows vs External CI**

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Architecture Options                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Tekton     │      │    Argo      │      │ GitHub   │  │
│  │  Pipelines   │      │  Workflows   │      │ Actions  │  │
│  └──────────────┘      └──────────────┘      └──────────┘  │
│        │                      │                     │        │
│        │                      │                     │        │
│  ┌─────▼──────────────────────▼─────────────────────▼─────┐│
│  │           Kubernetes Cluster (Workloads)                ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             ││
│  │  │   Dev    │  │  Staging │  │   Prod   │             ││
│  │  └──────────┘  └──────────┘  └──────────┘             ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Selection Criteria:**

| Tool | Best For | Strengths | Considerations |
|------|----------|-----------|----------------|
| **Tekton** | Cloud-native, reusable pipelines | Kubernetes-native CRDs, vendor-neutral, reusable Tasks | Learning curve, verbose YAML |
| **Argo Workflows** | Complex DAGs, data pipelines | Powerful DAG engine, parameter passing, conditionals | Resource intensive |
| **GitHub Actions** | Git-centric workflows | Easy integration, large ecosystem | External dependency, cost at scale |
| **GitLab CI** | Integrated DevOps platform | All-in-one solution, Auto DevOps | Platform lock-in |
| **Jenkins X** | Legacy Jenkins migration | Familiar for Jenkins users | Legacy architecture patterns |

#### 2. Tekton Pipelines

**Core Resources:**

```yaml
# Task (reusable unit)
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: build-and-push
spec:
  params:
    - name: image
      type: string
    - name: context
      default: .
  workspaces:
    - name: source
  steps:
    - name: build
      image: gcr.io/kaniko-project/executor:latest
      command: ["/kaniko/executor"]
      args:
        - --context=$(workspaces.source.path)/$(params.context)
        - --destination=$(params.image)
```

**Pipeline Composition:**

```yaml
# Pipeline (orchestrates Tasks)
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-test-deploy
spec:
  params:
    - name: app-name
    - name: git-url
  workspaces:
    - name: shared-workspace
  tasks:
    - name: clone-repo
      taskRef:
        name: git-clone
      workspaces:
        - name: output
          workspace: shared-workspace
      params:
        - name: url
          value: $(params.git-url)

    - name: run-tests
      taskRef:
        name: golang-test
      runAfter:
        - clone-repo
      workspaces:
        - name: source
          workspace: shared-workspace

    - name: build-image
      taskRef:
        name: build-and-push
      runAfter:
        - run-tests
      workspaces:
        - name: source
          workspace: shared-workspace
      params:
        - name: image
          value: registry.example.com/$(params.app-name):$(tasks.clone-repo.results.commit)

    - name: deploy
      taskRef:
        name: kubectl-deploy
      runAfter:
        - build-image
      params:
        - name: manifest
          value: k8s/deployment.yaml
```

**EventListener and Triggers:**

```yaml
apiVersion: triggers.tekton.dev/v1beta1
kind: EventListener
metadata:
  name: github-listener
spec:
  serviceAccountName: tekton-triggers-sa
  triggers:
    - name: github-push
      interceptors:
        - ref:
            name: github
          params:
            - name: secretRef
              value:
                secretName: github-secret
                secretKey: secretToken
            - name: eventTypes
              value: ["push"]
      bindings:
        - ref: github-push-binding
      template:
        ref: pipeline-template
```

#### 3. Argo Workflows

**DAG-Based Workflows:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cicd-
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: repo
        value: https://github.com/org/repo
      - name: branch
        value: main

  templates:
    # Main DAG orchestration
    - name: main
      dag:
        tasks:
          - name: checkout
            template: git-clone

          - name: lint
            template: run-linter
            dependencies: [checkout]

          - name: test
            template: run-tests
            dependencies: [checkout]

          - name: security-scan
            template: security-scan
            dependencies: [checkout]

          - name: build
            template: build-image
            dependencies: [lint, test, security-scan]

          - name: deploy-dev
            template: deploy
            dependencies: [build]
            arguments:
              parameters:
                - name: environment
                  value: dev

          - name: integration-tests
            template: run-integration-tests
            dependencies: [deploy-dev]

          - name: deploy-staging
            template: deploy
            dependencies: [integration-tests]
            arguments:
              parameters:
                - name: environment
                  value: staging

          - name: deploy-prod
            template: deploy
            dependencies: [deploy-staging]
            arguments:
              parameters:
                - name: environment
                  value: prod
            when: "{{workflow.parameters.branch}} == main"

    # Template definitions
    - name: git-clone
      container:
        image: alpine/git
        command: [sh, -c]
        args:
          - git clone {{workflow.parameters.repo}} /workspace
        volumeMounts:
          - name: workspace
            mountPath: /workspace

    - name: build-image
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: ["/kaniko/executor"]
        args:
          - --context=/workspace
          - --destination=registry.example.com/app:{{workflow.uid}}
          - --cache=true
        volumeMounts:
          - name: workspace
            mountPath: /workspace
      outputs:
        parameters:
          - name: image-tag
            value: "{{workflow.uid}}"
```

**Retry and Error Handling:**

```yaml
templates:
  - name: flaky-task
    retryStrategy:
      limit: 3
      retryPolicy: Always
      backoff:
        duration: 1m
        factor: 2
        maxDuration: 10m
    container:
      image: appropriate/curl
      command: [sh, -c]
      args:
        - |
          curl -f https://api.example.com/health || exit 1
```

#### 4. GitHub Actions with Kubernetes

**Self-Hosted Runners in Kubernetes:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: github-runner
  namespace: ci-cd
spec:
  replicas: 3
  selector:
    matchLabels:
      app: github-runner
  template:
    metadata:
      labels:
        app: github-runner
    spec:
      containers:
        - name: runner
          image: myoung34/github-runner:latest
          env:
            - name: RUNNER_SCOPE
              value: "repo"
            - name: REPO_URL
              value: https://github.com/org/repo
            - name: ACCESS_TOKEN
              valueFrom:
                secretKeyRef:
                  name: github-token
                  key: token
            - name: RUNNER_WORKDIR
              value: /tmp/runner
          volumeMounts:
            - name: work
              mountPath: /tmp/runner
            - name: docker-sock
              mountPath: /var/run/docker.sock
      volumes:
        - name: work
          emptyDir: {}
        - name: docker-sock
          hostPath:
            path: /var/run/docker.sock
```

**Workflow with Kubernetes Deployment:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3

      - name: Set up buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBECONFIG }}" > $HOME/.kube/config

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp \
            myapp=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n production
          kubectl rollout status deployment/myapp -n production
```

#### 5. Container Image Building Strategies

**A. Kaniko (Rootless, Kubernetes-Native)**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-build
spec:
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      args:
        - --context=git://github.com/org/repo.git#refs/heads/main
        - --context-sub-path=./
        - --destination=registry.example.com/app:latest
        - --cache=true
        - --cache-repo=registry.example.com/cache
        - --snapshot-mode=redo
        - --compressed-caching=false
        - --use-new-run
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker/
  volumes:
    - name: docker-config
      secret:
        secretName: regcred
        items:
          - key: .dockerconfigjson
            path: config.json
  restartPolicy: Never
```

**B. BuildKit with buildx**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: buildkit-build
spec:
  template:
    spec:
      containers:
        - name: buildkit
          image: moby/buildkit:latest
          args:
            - --addr
            - unix:///run/buildkit/buildkitd.sock
          securityContext:
            privileged: true
          volumeMounts:
            - name: buildkit-socket
              mountPath: /run/buildkit

        - name: builder
          image: docker:dind
          command: [sh, -c]
          args:
            - |
              export BUILDKIT_HOST=unix:///run/buildkit/buildkitd.sock
              docker buildx create --use --driver=remote unix:///run/buildkit/buildkitd.sock
              docker buildx build --push \
                --cache-from type=registry,ref=registry.example.com/app:cache \
                --cache-to type=registry,ref=registry.example.com/app:cache \
                -t registry.example.com/app:latest .
          volumeMounts:
            - name: buildkit-socket
              mountPath: /run/buildkit
      volumes:
        - name: buildkit-socket
          emptyDir: {}
```

**C. Cloud Native Buildpacks**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: buildpacks
spec:
  params:
    - name: image
    - name: source-url
  steps:
    - name: build
      image: paketobuildpacks/builder:base
      command: [/cnb/lifecycle/creator]
      args:
        - -app=$(params.source-url)
        - -tag=$(params.image)
        - -process-type=web
      env:
        - name: DOCKER_CONFIG
          value: /tekton/home/.docker
```

#### 6. Security Scanning Integration

**Multi-Stage Security Pipeline:**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: secure-pipeline
spec:
  workspaces:
    - name: source
  tasks:
    # 1. SAST - Static Application Security Testing
    - name: sast-scan
      taskRef:
        name: sonarqube-scan
      workspaces:
        - name: source
          workspace: source

    # 2. Secret Detection
    - name: secret-scan
      taskRef:
        name: trufflehog-scan
      workspaces:
        - name: source
          workspace: source

    # 3. Dependency Scanning
    - name: dependency-scan
      taskRef:
        name: snyk-scan
      workspaces:
        - name: source
          workspace: source
      params:
        - name: severity-threshold
          value: high

    # 4. Build Image
    - name: build-image
      runAfter: [sast-scan, secret-scan, dependency-scan]
      taskRef:
        name: kaniko-build
      workspaces:
        - name: source
          workspace: source

    # 5. Image Scanning
    - name: image-scan
      runAfter: [build-image]
      taskRef:
        name: trivy-scan
      params:
        - name: image
          value: $(tasks.build-image.results.image)
        - name: severity
          value: CRITICAL,HIGH

    # 6. SBOM Generation
    - name: generate-sbom
      runAfter: [build-image]
      taskRef:
        name: syft-sbom
      params:
        - name: image
          value: $(tasks.build-image.results.image)

    # 7. Sign Image
    - name: sign-image
      runAfter: [image-scan, generate-sbom]
      taskRef:
        name: cosign-sign
      params:
        - name: image
          value: $(tasks.build-image.results.image)
```

**Trivy Scanning Task:**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: trivy-scan
spec:
  params:
    - name: image
    - name: severity
      default: CRITICAL,HIGH
  steps:
    - name: scan
      image: aquasec/trivy:latest
      command: [trivy]
      args:
        - image
        - --severity=$(params.severity)
        - --exit-code=1
        - --no-progress
        - $(params.image)
```

#### 7. GitOps Integration Patterns

**ArgoCD Sync from Pipeline:**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: argocd-sync
spec:
  params:
    - name: app-name
    - name: argocd-server
      default: argocd-server.argocd.svc.cluster.local
  steps:
    - name: update-image
      image: argoproj/argocd:latest
      script: |
        #!/usr/bin/env bash
        set -e

        # Login to ArgoCD
        argocd login $(params.argocd-server) \
          --username admin \
          --password $ARGOCD_PASSWORD \
          --grpc-web

        # Update image tag
        argocd app set $(params.app-name) \
          --kustomize-image myapp=$NEW_IMAGE

        # Sync application
        argocd app sync $(params.app-name) --prune

        # Wait for sync
        argocd app wait $(params.app-name) --health
      env:
        - name: ARGOCD_PASSWORD
          valueFrom:
            secretKeyRef:
              name: argocd-creds
              key: password
```

**Flux Image Update Automation:**

```yaml
# Image Repository
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  image: registry.example.com/myapp
  interval: 1m
---
# Image Policy
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: 1.x.x
---
# Image Update Automation
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  sourceRef:
    kind: GitRepository
    name: fleet-infra
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: fluxcdbot@example.com
        name: fluxcdbot
      messageTemplate: 'Update image to {{range .Updated.Images}}{{println .}}{{end}}'
    push:
      branch: main
  update:
    path: ./clusters/production
    strategy: Setters
```

#### 8. Multi-Cluster Deployments

**Progressive Delivery Pipeline:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: multi-cluster-deploy-
spec:
  entrypoint: progressive-deploy

  templates:
    - name: progressive-deploy
      steps:
        # Stage 1: Deploy to dev cluster
        - - name: deploy-dev
            template: deploy-to-cluster
            arguments:
              parameters:
                - name: cluster
                  value: dev
                - name: namespace
                  value: default

        # Stage 2: Run smoke tests
        - - name: smoke-tests
            template: run-tests
            arguments:
              parameters:
                - name: cluster
                  value: dev

        # Stage 3: Deploy to staging cluster
        - - name: deploy-staging
            template: deploy-to-cluster
            arguments:
              parameters:
                - name: cluster
                  value: staging
                - name: namespace
                  value: default

        # Stage 4: Integration tests
        - - name: integration-tests
            template: run-tests
            arguments:
              parameters:
                - name: cluster
                  value: staging

        # Stage 5: Deploy to prod clusters (canary)
        - - name: deploy-prod-us-east-canary
            template: deploy-canary
            arguments:
              parameters:
                - name: cluster
                  value: prod-us-east
                - name: percentage
                  value: "10"
          - name: deploy-prod-eu-west-canary
            template: deploy-canary
            arguments:
              parameters:
                - name: cluster
                  value: prod-eu-west
                - name: percentage
                  value: "10"

        # Stage 6: Monitor canary
        - - name: monitor-canary
            template: monitor-metrics
            arguments:
              parameters:
                - name: duration
                  value: "10m"

        # Stage 7: Full rollout or rollback
        - - name: promote-or-rollback
            template: promote-or-rollback

    - name: deploy-to-cluster
      inputs:
        parameters:
          - name: cluster
          - name: namespace
      script:
        image: bitnami/kubectl:latest
        command: [bash]
        source: |
          #!/usr/bin/env bash
          set -e

          # Switch context
          kubectl config use-context {{inputs.parameters.cluster}}

          # Apply manifests
          kubectl apply -f /manifests/ -n {{inputs.parameters.namespace}}

          # Wait for rollout
          kubectl rollout status deployment/myapp -n {{inputs.parameters.namespace}}
```

**Cluster Inventory with External Secrets:**

```yaml
# External Secrets for multi-cluster credentials
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: cluster-credentials
  namespace: ci-cd
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: kubeconfigs
    template:
      data:
        prod-us-east: "{{ .prod_us_east | b64dec }}"
        prod-eu-west: "{{ .prod_eu_west | b64dec }}"
        staging: "{{ .staging | b64dec }}"
  dataFrom:
    - extract:
        key: kubernetes/clusters
```

#### 9. Pipeline Monitoring and Observability

**Prometheus Metrics for Tekton:**

```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: tekton-pipelines
  namespace: tekton-pipelines
spec:
  selector:
    matchLabels:
      app: tekton-pipelines-controller
  endpoints:
    - port: metrics
      interval: 30s
```

**Key Metrics to Track:**

```promql
# Pipeline success rate
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count{status="success"}[5m])
/
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count[5m])

# Average pipeline duration
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_sum[5m])
/
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count[5m])

# Failed pipelines
tekton_pipelines_controller_pipelinerun_count{status="failed"}

# Task duration by name
histogram_quantile(0.95,
  rate(tekton_pipelines_controller_taskrun_duration_seconds_bucket[5m])
)
```

**Grafana Dashboard Definition:**

```json
{
  "dashboard": {
    "title": "CI/CD Pipeline Metrics",
    "panels": [
      {
        "title": "Pipeline Success Rate",
        "targets": [
          {
            "expr": "rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count{status=\"success\"}[5m]) / rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count[5m])"
          }
        ]
      },
      {
        "title": "Pipeline Duration (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(tekton_pipelines_controller_pipelinerun_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Active Pipelines",
        "targets": [
          {
            "expr": "tekton_pipelines_controller_running_pipelineruns_count"
          }
        ]
      }
    ]
  }
}
```

**OpenTelemetry Tracing:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: ci-cd
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317

    processors:
      batch:
        timeout: 10s

      attributes:
        actions:
          - key: pipeline.name
            action: insert
            from_attribute: tekton.dev/pipeline
          - key: task.name
            action: insert
            from_attribute: tekton.dev/task

    exporters:
      jaeger:
        endpoint: jaeger-collector:14250
        tls:
          insecure: true

      prometheus:
        endpoint: 0.0.0.0:8889

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch, attributes]
          exporters: [jaeger]
        metrics:
          receivers: [otlp]
          processors: [batch]
          exporters: [prometheus]
```

### Advanced Patterns

#### Pipeline as Code with Templating

**Helm Chart for Pipeline Templates:**

```yaml
# templates/pipeline.yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: {{ .Values.appName }}-pipeline
spec:
  params:
    - name: git-url
      default: {{ .Values.git.url }}
    - name: git-revision
      default: {{ .Values.git.branch }}

  workspaces:
    - name: shared-data

  tasks:
    {{- range .Values.pipeline.tasks }}
    - name: {{ .name }}
      taskRef:
        name: {{ .taskRef }}
      {{- if .runAfter }}
      runAfter:
        {{- range .runAfter }}
        - {{ . }}
        {{- end }}
      {{- end }}
      {{- if .params }}
      params:
        {{- range .params }}
        - name: {{ .name }}
          value: {{ .value }}
        {{- end }}
      {{- end }}
    {{- end }}
```

#### Dynamic Pipeline Generation

**Operator Pattern for Pipeline Creation:**

```go
// Custom Resource Definition
type PipelineTemplate struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   PipelineTemplateSpec   `json:"spec"`
    Status PipelineTemplateStatus `json:"status,omitempty"`
}

type PipelineTemplateSpec struct {
    Language       string            `json:"language"`
    Framework      string            `json:"framework"`
    Tests          []TestConfig      `json:"tests"`
    Deployments    []DeploymentTarget `json:"deployments"`
    SecurityScans  []SecurityScan    `json:"securityScans"`
}

// Reconciler generates Tekton Pipeline
func (r *PipelineTemplateReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    template := &PipelineTemplate{}
    if err := r.Get(ctx, req.NamespacedName, template); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    pipeline := r.generatePipeline(template)

    if err := r.Create(ctx, pipeline); err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

### References

For detailed examples and advanced patterns:

- [Tekton Patterns and Best Practices](references/tekton-patterns.md)
- [Argo Workflows Guide](references/argo-workflows-guide.md)
- [Pipeline Security Practices](references/pipeline-security.md)

### Example Assets

Production-ready pipeline examples:

- [Complete Tekton Pipeline](assets/tekton-pipeline.yaml)
- [Argo Workflow DAG](assets/argo-workflow.yaml)
- [GitHub Actions Kubernetes Deployment](assets/github-actions-k8s.yaml)

---

## Russian Version

### Когда использовать этот навык

Используйте этот навык когда вам необходимо:
- Проектировать облачные CI/CD конвейеры для Kubernetes
- Внедрять Tekton Pipelines или Argo Workflows
- Интегрировать GitHub Actions с развертыванием в Kubernetes
- Безопасно собирать образы контейнеров внутри Kubernetes
- Реализовывать паттерны GitOps развертывания
- Настраивать конвейеры для мульти-кластерного развертывания
- Добавлять проверки безопасности и соответствия требованиям
- Мониторить и наблюдать за выполнением конвейеров
- Внедрять безопасность цепочки поставок (SLSA, Sigstore)

### Основные концепции

#### 1. Kubernetes-нативные CI/CD архитектуры

**Выбор между Tekton, Argo Workflows и внешними CI системами**

**Критерии выбора:**

| Инструмент | Лучше всего для | Преимущества | Особенности |
|------------|----------------|--------------|-------------|
| **Tekton** | Облачные, переиспользуемые конвейеры | Kubernetes-нативные CRD, vendor-neutral, переиспользуемые Task | Кривая обучения, многословный YAML |
| **Argo Workflows** | Сложные DAG, конвейеры данных | Мощный DAG движок, передача параметров, условия | Ресурсоемкий |
| **GitHub Actions** | Git-центричные рабочие процессы | Простая интеграция, большая экосистема | Внешняя зависимость, стоимость на масштабе |
| **GitLab CI** | Интегрированная DevOps платформа | Все-в-одном решение, Auto DevOps | Привязка к платформе |

#### 2. Tekton Pipelines - Основы

**Базовые ресурсы:**

Tekton использует Kubernetes Custom Resources для определения конвейеров:

- **Task** - Переиспользуемая единица работы (как функция)
- **Pipeline** - Оркестрация нескольких Task (как программа)
- **PipelineRun** - Экземпляр выполнения Pipeline
- **Workspace** - Общее хранилище между Task
- **Trigger** - Автоматический запуск на события (webhooks)

**Пример композиции Pipeline:**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-test-deploy
spec:
  params:
    - name: app-name
    - name: git-url
  workspaces:
    - name: shared-workspace
  tasks:
    - name: clone-repo
      taskRef:
        name: git-clone
      params:
        - name: url
          value: $(params.git-url)

    - name: run-tests
      runAfter: [clone-repo]
      taskRef:
        name: golang-test

    - name: build-image
      runAfter: [run-tests]
      taskRef:
        name: kaniko-build

    - name: deploy
      runAfter: [build-image]
      taskRef:
        name: kubectl-deploy
```

#### 3. Argo Workflows - DAG паттерны

**Преимущества Argo Workflows:**

- Мощный движок DAG (направленный ациклический граф)
- Поддержка условий и циклов
- Передача параметров между шагами
- Визуализация выполнения в реальном времени
- Механизмы повторных попыток и обработки ошибок

**Основные шаблоны:**

```yaml
templates:
  - name: main
    dag:
      tasks:
        - name: checkout
          template: git-clone

        - name: parallel-tests
          dependencies: [checkout]
          template: test-suite
          withParam: "{{tasks.checkout.outputs.parameters.modules}}"

        - name: build
          dependencies: [parallel-tests]
          template: build-image

        - name: security-scan
          dependencies: [build]
          template: trivy-scan

        - name: deploy
          dependencies: [security-scan]
          template: deploy-to-k8s
```

#### 4. Стратегии сборки образов контейнеров

**A. Kaniko - Без привилегий, Kubernetes-нативный**

Преимущества:
- Не требует Docker daemon
- Работает без root прав
- Идеален для Kubernetes
- Поддержка кеширования слоев

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-build
spec:
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:latest
      args:
        - --dockerfile=Dockerfile
        - --context=git://github.com/org/repo.git
        - --destination=registry.example.com/app:latest
        - --cache=true
        - --cache-repo=registry.example.com/cache
```

**B. BuildKit - Продвинутая сборка Docker**

Преимущества:
- Параллельная сборка
- Продвинутое кеширование
- Секреты во время сборки
- Multi-platform builds

**C. Cloud Native Buildpacks - Без Dockerfile**

Преимущества:
- Автоматическое определение языка
- Встроенные best practices
- Регулярные обновления безопасности
- Стандартизация образов

#### 5. Интеграция проверок безопасности

**Многоуровневый конвейер безопасности:**

```
┌─────────────────────────────────────────────────────────┐
│                  Этапы безопасности                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. SAST → 2. Secret Scan → 3. Dependency Check         │
│                     ↓                                     │
│              4. Build Image                              │
│                     ↓                                     │
│  5. Container Scan → 6. SBOM → 7. Sign Image            │
│                     ↓                                     │
│              8. Deploy                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Инструменты безопасности:**

- **Trivy** - Сканирование уязвимостей образов
- **Snyk** - Проверка зависимостей
- **TruffleHog** - Поиск секретов в коде
- **Cosign** - Подпись образов
- **Syft** - Генерация SBOM
- **SonarQube** - SAST анализ

#### 6. GitOps интеграция

**Паттерн: Pull-based deployment**

```
┌──────────────┐         ┌──────────────┐
│   CI Pipeline│         │  Git Repo    │
│   (Build)    │────────>│  (Manifests) │
└──────────────┘         └──────────────┘
                               │
                               │ Pull
                               ▼
                         ┌──────────────┐
                         │  ArgoCD /    │
                         │  Flux CD     │
                         └──────────────┘
                               │
                               │ Apply
                               ▼
                         ┌──────────────┐
                         │  Kubernetes  │
                         │  Cluster     │
                         └──────────────┘
```

**Преимущества GitOps:**

- Git как единый источник правды
- Декларативная инфраструктура
- Автоматическая синхронизация
- Простой откат изменений
- Audit trail из коммитов
- Безопасность через Pull модель

#### 7. Мульти-кластерное развертывание

**Стратегии развертывания:**

```yaml
# Progressive Delivery Pipeline
stages:
  1. Dev cluster → smoke tests
  2. Staging cluster → integration tests
  3. Production clusters:
     - Canary (10%) → monitor
     - Progressive (25%, 50%, 100%)
     - Multi-region rollout
```

**Canary развертывание:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {duration: 10m}
        - setWeight: 25
        - pause: {duration: 10m}
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 75
        - pause: {duration: 10m}
```

#### 8. Мониторинг и наблюдаемость конвейеров

**Ключевые метрики:**

```
1. Частота развертываний (Deployment Frequency)
2. Время выполнения конвейера (Lead Time)
3. Процент успешных сборок (Success Rate)
4. Время восстановления (MTTR)
5. Процент откатов (Rollback Rate)
```

**Prometheus метрики для Tekton:**

```promql
# Успешность конвейеров
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count{status="success"}[5m])
/
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count[5m])

# Среднее время выполнения
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_sum[5m])
/
rate(tekton_pipelines_controller_pipelinerun_duration_seconds_count[5m])

# Неудачные конвейеры
tekton_pipelines_controller_pipelinerun_count{status="failed"}
```

**Алерты для конвейеров:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: pipeline-alerts
spec:
  groups:
    - name: cicd
      interval: 30s
      rules:
        - alert: HighPipelineFailureRate
          expr: |
            rate(tekton_pipelines_controller_pipelinerun_count{status="failed"}[5m])
            /
            rate(tekton_pipelines_controller_pipelinerun_count[5m])
            > 0.2
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "High pipeline failure rate"
            description: "Pipeline failure rate is above 20%"

        - alert: PipelineTooSlow
          expr: |
            histogram_quantile(0.95,
              rate(tekton_pipelines_controller_pipelinerun_duration_seconds_bucket[5m])
            ) > 1800
          for: 15m
          labels:
            severity: warning
          annotations:
            summary: "Pipeline taking too long"
            description: "P95 pipeline duration is above 30 minutes"
```

### Продвинутые паттерны

#### Параллельное выполнение задач

**Tekton - параллельные Tasks:**

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: parallel-pipeline
spec:
  tasks:
    # Эти задачи выполняются параллельно
    - name: unit-tests
      taskRef:
        name: run-unit-tests

    - name: integration-tests
      taskRef:
        name: run-integration-tests

    - name: lint
      taskRef:
        name: run-linter

    # Эта задача ждет завершения всех предыдущих
    - name: build
      runAfter:
        - unit-tests
        - integration-tests
        - lint
      taskRef:
        name: build-image
```

#### Условное выполнение

**Argo Workflows - when условия:**

```yaml
templates:
  - name: conditional-deploy
    dag:
      tasks:
        - name: deploy-dev
          template: deploy
          arguments:
            parameters:
              - name: env
                value: dev

        - name: deploy-prod
          template: deploy
          dependencies: [deploy-dev]
          when: "{{workflow.parameters.branch}} == main"
          arguments:
            parameters:
              - name: env
                value: prod
```

#### Повторные попытки и обработка ошибок

**Стратегии повторов:**

```yaml
templates:
  - name: flaky-task
    retryStrategy:
      limit: 3                  # Максимум 3 попытки
      retryPolicy: Always       # Повторять при любой ошибке
      backoff:
        duration: 1m            # Начальная задержка
        factor: 2               # Экспоненциальный рост
        maxDuration: 10m        # Максимальная задержка
    container:
      image: myapp:latest
      command: [./run-tests.sh]
```

### Лучшие практики

#### 1. Оптимизация производительности

- Используйте кеширование слоев Docker
- Параллелизируйте независимые задачи
- Переиспользуйте базовые образы
- Оптимизируйте размер образов (multi-stage builds)
- Используйте локальные Docker registry кеши

#### 2. Безопасность

- Сканируйте образы на каждом этапе
- Используйте подпись образов (Cosign/Notary)
- Храните секреты в Vault/External Secrets
- Ограничивайте права ServiceAccount
- Генерируйте и проверяйте SBOM
- Внедряйте SLSA уровень 3+

#### 3. Надежность

- Настройте retry механизмы
- Реализуйте health checks
- Используйте timeouts для задач
- Мониторьте метрики конвейеров
- Настройте алерты на сбои
- Документируйте процесс rollback

#### 4. Масштабируемость

- Используйте автоскейлинг для runners
- Оптимизируйте использование ресурсов
- Настройте resource limits и requests
- Используйте node affinity для CI workloads
- Реализуйте queue management

### Справочные материалы

Подробные примеры и продвинутые паттерны:

- [Паттерны и лучшие практики Tekton](references/tekton-patterns.md)
- [Руководство по Argo Workflows](references/argo-workflows-guide.md)
- [Практики безопасности конвейеров](references/pipeline-security.md)

### Примеры

Готовые к production примеры конвейеров:

- [Полный Tekton Pipeline](assets/tekton-pipeline.yaml)
- [Argo Workflow DAG](assets/argo-workflow.yaml)
- [GitHub Actions развертывание в Kubernetes](assets/github-actions-k8s.yaml)

---

## Conclusion / Заключение

**English**: This skill provides comprehensive guidance for implementing modern CI/CD pipelines in Kubernetes environments. Choose the right tools for your use case, prioritize security, and follow GitOps principles for reliable deployments.

**Русский**: Этот навык предоставляет всестороннее руководство по внедрению современных CI/CD конвейеров в Kubernetes окружениях. Выбирайте правильные инструменты для вашего случая, приоритизируйте безопасность и следуйте принципам GitOps для надежных развертываний.
