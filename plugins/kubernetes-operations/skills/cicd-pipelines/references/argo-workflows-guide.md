# Argo Workflows Guide

Comprehensive guide to Argo Workflows patterns based on enterprise production experience.

## Table of Contents

- [Core Concepts](#core-concepts)
- [DAG Workflows](#dag-workflows)
- [Steps Workflows](#steps-workflows)
- [Template Types](#template-types)
- [Parameter Passing](#parameter-passing)
- [Conditionals and Loops](#conditionals-and-loops)
- [Retry and Error Handling](#retry-and-error-handling)
- [Artifacts and Outputs](#artifacts-and-outputs)
- [Resource Management](#resource-management)
- [Advanced Patterns](#advanced-patterns)
- [Monitoring and Observability](#monitoring-and-observability)

## Core Concepts

### Workflow Structure

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: example-
spec:
  entrypoint: main              # Starting point
  arguments:                    # Input parameters
    parameters:
      - name: message
        value: "hello world"

  templates:                    # Reusable templates
    - name: main
      container:
        image: alpine:latest
        command: [echo]
        args: ["{{workflow.parameters.message}}"]
```

### Template Types

| Type | Purpose | Use Case |
|------|---------|----------|
| **container** | Run a container | Execute commands, build images |
| **script** | Run inline script | Complex logic in bash/python |
| **resource** | Create/manage K8s resources | Deploy applications |
| **dag** | Direct Acyclic Graph | Parallel task orchestration |
| **steps** | Sequential steps | Linear workflows |
| **suspend** | Pause workflow | Manual approval gates |
| **http** | HTTP requests | API integration |
| **data** | Transform data | Process workflow data |

## DAG Workflows

### Pattern 1: Parallel Execution with Dependencies

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: parallel-dag-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          # Independent parallel tasks
          - name: lint-frontend
            template: lint
            arguments:
              parameters:
                - name: path
                  value: "/frontend"

          - name: lint-backend
            template: lint
            arguments:
              parameters:
                - name: path
                  value: "/backend"

          - name: lint-api
            template: lint
            arguments:
              parameters:
                - name: path
                  value: "/api"

          # Run after all linting completes
          - name: run-tests
            dependencies: [lint-frontend, lint-backend, lint-api]
            template: test-all

          # Parallel builds after tests pass
          - name: build-frontend
            dependencies: [run-tests]
            template: build
            arguments:
              parameters:
                - name: service
                  value: "frontend"

          - name: build-backend
            dependencies: [run-tests]
            template: build
            arguments:
              parameters:
                - name: service
                  value: "backend"

          - name: build-api
            dependencies: [run-tests]
            template: build
            arguments:
              parameters:
                - name: service
                  value: "api"

          # Deploy after all builds complete
          - name: deploy
            dependencies: [build-frontend, build-backend, build-api]
            template: deploy-all

    - name: lint
      inputs:
        parameters:
          - name: path
      container:
        image: golangci/golangci-lint:latest
        command: [golangci-lint]
        args: ["run", "{{inputs.parameters.path}}"]

    - name: test-all
      container:
        image: golang:1.21
        command: [go]
        args: ["test", "./..."]

    - name: build
      inputs:
        parameters:
          - name: service
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: [/kaniko/executor]
        args:
          - --context=/workspace/{{inputs.parameters.service}}
          - --destination=registry.example.com/{{inputs.parameters.service}}:{{workflow.uid}}

    - name: deploy-all
      resource:
        action: apply
        manifest: |
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: myapp
          spec:
            replicas: 3
            template:
              spec:
                containers:
                  - name: frontend
                    image: registry.example.com/frontend:{{workflow.uid}}
                  - name: backend
                    image: registry.example.com/backend:{{workflow.uid}}
                  - name: api
                    image: registry.example.com/api:{{workflow.uid}}
```

### Pattern 2: Diamond DAG (Fan-out/Fan-in)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: diamond-
spec:
  entrypoint: diamond

  templates:
    - name: diamond
      dag:
        tasks:
          - name: A
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Starting workflow"

          # Fan-out: B, C, D run in parallel
          - name: B
            dependencies: [A]
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Branch B"

          - name: C
            dependencies: [A]
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Branch C"

          - name: D
            dependencies: [A]
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Branch D"

          # Fan-in: E waits for all branches
          - name: E
            dependencies: [B, C, D]
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Completing workflow"

    - name: echo
      inputs:
        parameters:
          - name: message
      container:
        image: alpine:latest
        command: [echo]
        args: ["{{inputs.parameters.message}}"]
```

### Pattern 3: Complex Multi-Stage CI/CD Pipeline

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: cicd-complex-
spec:
  entrypoint: cicd-pipeline
  arguments:
    parameters:
      - name: repo-url
        value: https://github.com/org/repo
      - name: branch
        value: main

  volumeClaimTemplates:
    - metadata:
        name: workspace
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi

  templates:
    - name: cicd-pipeline
      dag:
        tasks:
          # Stage 1: Source checkout
          - name: checkout
            template: git-clone

          # Stage 2: Parallel security scans
          - name: secret-scan
            dependencies: [checkout]
            template: trufflehog-scan

          - name: sast-scan
            dependencies: [checkout]
            template: sonar-scan

          - name: dependency-scan
            dependencies: [checkout]
            template: snyk-scan

          # Stage 3: Build and unit test (after scans pass)
          - name: unit-test
            dependencies: [secret-scan, sast-scan, dependency-scan]
            template: run-unit-tests

          # Stage 4: Build container image
          - name: build-image
            dependencies: [unit-test]
            template: kaniko-build

          # Stage 5: Parallel image analysis
          - name: image-scan
            dependencies: [build-image]
            template: trivy-scan
            arguments:
              parameters:
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

          - name: generate-sbom
            dependencies: [build-image]
            template: syft-sbom
            arguments:
              parameters:
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

          # Stage 6: Sign image
          - name: sign-image
            dependencies: [image-scan, generate-sbom]
            template: cosign-sign
            arguments:
              parameters:
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

          # Stage 7: Deploy to dev
          - name: deploy-dev
            dependencies: [sign-image]
            template: deploy
            arguments:
              parameters:
                - name: environment
                  value: dev
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

          # Stage 8: Integration tests
          - name: integration-test
            dependencies: [deploy-dev]
            template: run-integration-tests
            arguments:
              parameters:
                - name: environment
                  value: dev

          # Stage 9: Deploy to staging
          - name: deploy-staging
            dependencies: [integration-test]
            template: deploy
            arguments:
              parameters:
                - name: environment
                  value: staging
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

          # Stage 10: Smoke tests on staging
          - name: smoke-test
            dependencies: [deploy-staging]
            template: run-smoke-tests
            arguments:
              parameters:
                - name: environment
                  value: staging

          # Stage 11: Production deployment (conditional)
          - name: deploy-prod
            dependencies: [smoke-test]
            when: "{{workflow.parameters.branch}} == main"
            template: deploy
            arguments:
              parameters:
                - name: environment
                  value: production
                - name: image
                  value: "{{tasks.build-image.outputs.parameters.image}}"

    # Template definitions
    - name: git-clone
      container:
        image: alpine/git:latest
        command: [sh, -c]
        args:
          - |
            git clone {{workflow.parameters.repo-url}} /workspace/source
            cd /workspace/source
            git checkout {{workflow.parameters.branch}}
        volumeMounts:
          - name: workspace
            mountPath: /workspace

    - name: trufflehog-scan
      container:
        image: trufflesecurity/trufflehog:latest
        command: [trufflehog]
        args:
          - filesystem
          - /workspace/source
          - --fail
        volumeMounts:
          - name: workspace
            mountPath: /workspace

    - name: sonar-scan
      container:
        image: sonarsource/sonar-scanner-cli:latest
        command: [sonar-scanner]
        args:
          - -Dsonar.projectBaseDir=/workspace/source
        volumeMounts:
          - name: workspace
            mountPath: /workspace
        env:
          - name: SONAR_HOST_URL
            valueFrom:
              secretKeyRef:
                name: sonar-config
                key: url
          - name: SONAR_TOKEN
            valueFrom:
              secretKeyRef:
                name: sonar-config
                key: token

    - name: snyk-scan
      container:
        image: snyk/snyk:golang
        command: [snyk]
        args:
          - test
          - --severity-threshold=high
          - /workspace/source
        volumeMounts:
          - name: workspace
            mountPath: /workspace
        env:
          - name: SNYK_TOKEN
            valueFrom:
              secretKeyRef:
                name: snyk-token
                key: token

    - name: run-unit-tests
      container:
        image: golang:1.21
        command: [sh, -c]
        args:
          - |
            cd /workspace/source
            go test -v -coverprofile=coverage.out ./...
        volumeMounts:
          - name: workspace
            mountPath: /workspace

    - name: kaniko-build
      outputs:
        parameters:
          - name: image
            valueFrom:
              path: /tmp/image-tag
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: [sh, -c]
        args:
          - |
            IMAGE="registry.example.com/myapp:{{workflow.uid}}"
            /kaniko/executor \
              --context=/workspace/source \
              --destination=$IMAGE \
              --cache=true
            echo -n $IMAGE > /tmp/image-tag
        volumeMounts:
          - name: workspace
            mountPath: /workspace
          - name: docker-config
            mountPath: /kaniko/.docker

    - name: trivy-scan
      inputs:
        parameters:
          - name: image
      container:
        image: aquasec/trivy:latest
        command: [trivy]
        args:
          - image
          - --severity=CRITICAL,HIGH
          - --exit-code=1
          - "{{inputs.parameters.image}}"

    - name: syft-sbom
      inputs:
        parameters:
          - name: image
      container:
        image: anchore/syft:latest
        command: [syft]
        args:
          - "{{inputs.parameters.image}}"
          - -o=spdx-json
          - --file=/tmp/sbom.json

    - name: cosign-sign
      inputs:
        parameters:
          - name: image
      container:
        image: gcr.io/projectsigstore/cosign:latest
        command: [cosign]
        args:
          - sign
          - --key=/secrets/cosign.key
          - "{{inputs.parameters.image}}"
        env:
          - name: COSIGN_PASSWORD
            valueFrom:
              secretKeyRef:
                name: cosign-keys
                key: password

    - name: deploy
      inputs:
        parameters:
          - name: environment
          - name: image
      resource:
        action: apply
        manifest: |
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: myapp
            namespace: {{inputs.parameters.environment}}
          spec:
            replicas: 3
            selector:
              matchLabels:
                app: myapp
            template:
              metadata:
                labels:
                  app: myapp
              spec:
                containers:
                  - name: myapp
                    image: {{inputs.parameters.image}}
                    ports:
                      - containerPort: 8080

    - name: run-integration-tests
      inputs:
        parameters:
          - name: environment
      container:
        image: golang:1.21
        command: [sh, -c]
        args:
          - |
            cd /workspace/source
            export TEST_ENV={{inputs.parameters.environment}}
            go test -v -tags=integration ./...
        volumeMounts:
          - name: workspace
            mountPath: /workspace

    - name: run-smoke-tests
      inputs:
        parameters:
          - name: environment
      container:
        image: appropriate/curl:latest
        command: [sh, -c]
        args:
          - |
            ENDPOINT="http://myapp.{{inputs.parameters.environment}}.svc.cluster.local:8080"
            curl -f $ENDPOINT/health || exit 1
            curl -f $ENDPOINT/ready || exit 1
```

## Steps Workflows

### Pattern 1: Sequential Pipeline

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: sequential-
spec:
  entrypoint: main

  templates:
    - name: main
      steps:
        - - name: step1
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Step 1"

        - - name: step2
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Step 2"

        - - name: step3
            template: echo
            arguments:
              parameters:
                - name: message
                  value: "Step 3"

    - name: echo
      inputs:
        parameters:
          - name: message
      container:
        image: alpine:latest
        command: [echo]
        args: ["{{inputs.parameters.message}}"]
```

### Pattern 2: Parallel Steps within Sequence

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: parallel-steps-
spec:
  entrypoint: main

  templates:
    - name: main
      steps:
        # Step 1: Checkout (sequential)
        - - name: checkout
            template: git-clone

        # Step 2: Parallel tests
        - - name: unit-test
            template: test
            arguments:
              parameters:
                - name: suite
                  value: unit
          - name: integration-test
            template: test
            arguments:
              parameters:
                - name: suite
                  value: integration
          - name: e2e-test
            template: test
            arguments:
              parameters:
                - name: suite
                  value: e2e

        # Step 3: Build (sequential, after all tests)
        - - name: build
            template: kaniko-build

        # Step 4: Parallel deployments
        - - name: deploy-us-east
            template: deploy
            arguments:
              parameters:
                - name: region
                  value: us-east-1
          - name: deploy-us-west
            template: deploy
            arguments:
              parameters:
                - name: region
                  value: us-west-2
          - name: deploy-eu-west
            template: deploy
            arguments:
              parameters:
                - name: region
                  value: eu-west-1

    - name: git-clone
      container:
        image: alpine/git
        command: [git, clone, "https://github.com/example/repo"]

    - name: test
      inputs:
        parameters:
          - name: suite
      container:
        image: golang:1.21
        command: [go, test]
        args: ["-tags", "{{inputs.parameters.suite}}"]

    - name: kaniko-build
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: [/kaniko/executor]

    - name: deploy
      inputs:
        parameters:
          - name: region
      container:
        image: bitnami/kubectl:latest
        command: [kubectl, apply, -f, deployment.yaml]
        env:
          - name: AWS_REGION
            value: "{{inputs.parameters.region}}"
```

## Parameter Passing

### Pattern 1: Global Parameters

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: params-
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: environment
        value: production
      - name: image-tag
        value: v1.2.3
      - name: replicas
        value: "5"

  templates:
    - name: main
      steps:
        - - name: deploy
            template: deploy-app
            arguments:
              parameters:
                - name: env
                  value: "{{workflow.parameters.environment}}"
                - name: tag
                  value: "{{workflow.parameters.image-tag}}"
                - name: replicas
                  value: "{{workflow.parameters.replicas}}"

    - name: deploy-app
      inputs:
        parameters:
          - name: env
          - name: tag
          - name: replicas
      container:
        image: bitnami/kubectl:latest
        command: [sh, -c]
        args:
          - |
            kubectl set image deployment/myapp \
              myapp=registry.example.com/myapp:{{inputs.parameters.tag}} \
              -n {{inputs.parameters.env}}
            kubectl scale deployment/myapp \
              --replicas={{inputs.parameters.replicas}} \
              -n {{inputs.parameters.env}}
```

### Pattern 2: Output Parameters

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: outputs-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: generate-version
            template: version-generator

          - name: build
            dependencies: [generate-version]
            template: build-image
            arguments:
              parameters:
                - name: version
                  value: "{{tasks.generate-version.outputs.parameters.version}}"

          - name: tag-latest
            dependencies: [build]
            template: tag-image
            arguments:
              parameters:
                - name: source-image
                  value: "{{tasks.build.outputs.parameters.image}}"

    - name: version-generator
      outputs:
        parameters:
          - name: version
            valueFrom:
              path: /tmp/version
      script:
        image: alpine:latest
        command: [sh]
        source: |
          #!/bin/sh
          VERSION="v$(date +%Y%m%d)-$(git rev-parse --short HEAD)"
          echo -n $VERSION > /tmp/version
          echo "Generated version: $VERSION"

    - name: build-image
      inputs:
        parameters:
          - name: version
      outputs:
        parameters:
          - name: image
            valueFrom:
              path: /tmp/image
      script:
        image: gcr.io/kaniko-project/executor:latest
        command: [sh]
        source: |
          #!/busybox/sh
          IMAGE="registry.example.com/myapp:{{inputs.parameters.version}}"
          /kaniko/executor --destination=$IMAGE
          echo -n $IMAGE > /tmp/image

    - name: tag-image
      inputs:
        parameters:
          - name: source-image
      container:
        image: gcr.io/go-containerregistry/crane:latest
        command: [crane]
        args:
          - tag
          - "{{inputs.parameters.source-image}}"
          - latest
```

### Pattern 3: JSON Parameter Passing

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: json-params-
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: config
        value: |
          {
            "services": [
              {"name": "frontend", "replicas": 3},
              {"name": "backend", "replicas": 5},
              {"name": "worker", "replicas": 2}
            ],
            "environment": "production"
          }

  templates:
    - name: main
      steps:
        - - name: deploy-services
            template: deploy-from-json
            arguments:
              parameters:
                - name: config
                  value: "{{workflow.parameters.config}}"

    - name: deploy-from-json
      inputs:
        parameters:
          - name: config
      script:
        image: python:3.11-alpine
        command: [python]
        source: |
          import json
          import subprocess

          config = json.loads('''{{inputs.parameters.config}}''')

          for service in config['services']:
              name = service['name']
              replicas = service['replicas']
              env = config['environment']

              print(f"Deploying {name} with {replicas} replicas to {env}")

              subprocess.run([
                  'kubectl', 'scale', f'deployment/{name}',
                  f'--replicas={replicas}',
                  f'-n={env}'
              ], check=True)
```

## Conditionals and Loops

### Pattern 1: Conditional Execution

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: conditional-
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: environment
        value: production
      - name: deploy-to-prod
        value: "true"

  templates:
    - name: main
      dag:
        tasks:
          - name: build
            template: build-image

          - name: deploy-dev
            dependencies: [build]
            template: deploy
            arguments:
              parameters:
                - name: env
                  value: dev

          - name: deploy-staging
            dependencies: [deploy-dev]
            template: deploy
            arguments:
              parameters:
                - name: env
                  value: staging

          - name: deploy-prod
            dependencies: [deploy-staging]
            when: "{{workflow.parameters.deploy-to-prod}} == true"
            template: deploy
            arguments:
              parameters:
                - name: env
                  value: production

          - name: skip-prod-notification
            dependencies: [deploy-staging]
            when: "{{workflow.parameters.deploy-to-prod}} == false"
            template: notify
            arguments:
              parameters:
                - name: message
                  value: "Production deployment skipped"

    - name: build-image
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: [/kaniko/executor]

    - name: deploy
      inputs:
        parameters:
          - name: env
      container:
        image: bitnami/kubectl:latest
        command: [kubectl, apply, -f, deployment.yaml, -n, "{{inputs.parameters.env}}"]

    - name: notify
      inputs:
        parameters:
          - name: message
      container:
        image: curlimages/curl:latest
        command: [curl]
        args: [-X, POST, "https://slack.com/webhook", -d, "{{inputs.parameters.message}}"]
```

### Pattern 2: WithItems Loop

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: loop-
spec:
  entrypoint: main

  templates:
    - name: main
      steps:
        - - name: deploy-to-regions
            template: deploy
            arguments:
              parameters:
                - name: region
                  value: "{{item}}"
            withItems:
              - us-east-1
              - us-west-2
              - eu-west-1
              - ap-southeast-1

    - name: deploy
      inputs:
        parameters:
          - name: region
      container:
        image: bitnami/kubectl:latest
        command: [sh, -c]
        args:
          - |
            echo "Deploying to {{inputs.parameters.region}}"
            kubectl apply -f deployment.yaml \
              --context={{inputs.parameters.region}}
```

### Pattern 3: WithParam Dynamic Loop

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: dynamic-loop-
spec:
  entrypoint: main

  templates:
    - name: main
      steps:
        - - name: discover-services
            template: list-services

        - - name: test-services
            template: test-service
            arguments:
              parameters:
                - name: service
                  value: "{{item.name}}"
                - name: endpoint
                  value: "{{item.endpoint}}"
            withParam: "{{steps.discover-services.outputs.result}}"

    - name: list-services
      script:
        image: python:3.11-alpine
        command: [python]
        source: |
          import json
          services = [
            {"name": "frontend", "endpoint": "http://frontend:8080"},
            {"name": "backend", "endpoint": "http://backend:8080"},
            {"name": "api", "endpoint": "http://api:8080"}
          ]
          print(json.dumps(services))

    - name: test-service
      inputs:
        parameters:
          - name: service
          - name: endpoint
      container:
        image: appropriate/curl:latest
        command: [sh, -c]
        args:
          - |
            echo "Testing {{inputs.parameters.service}}"
            curl -f {{inputs.parameters.endpoint}}/health
```

## Retry and Error Handling

### Pattern 1: Retry Strategy

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: retry-
spec:
  entrypoint: main

  templates:
    - name: main
      retryStrategy:
        limit: 3
        retryPolicy: Always
        backoff:
          duration: "1m"
          factor: 2
          maxDuration: "10m"
      container:
        image: appropriate/curl:latest
        command: [sh, -c]
        args:
          - |
            curl -f https://api.example.com/health || exit 1
```

### Pattern 2: Selective Retry

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: selective-retry-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: flaky-task
            template: flaky-test
            retryStrategy:
              limit: 5
              retryPolicy: OnFailure
              backoff:
                duration: "30s"
                factor: 2

          - name: critical-task
            dependencies: [flaky-task]
            template: deploy
            retryStrategy:
              limit: 0  # No retries for deployment

    - name: flaky-test
      container:
        image: golang:1.21
        command: [go, test, ./...]

    - name: deploy
      container:
        image: bitnami/kubectl:latest
        command: [kubectl, apply, -f, deployment.yaml]
```

### Pattern 3: Error Handling with OnExit

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: error-handling-
spec:
  entrypoint: main
  onExit: exit-handler

  templates:
    - name: main
      dag:
        tasks:
          - name: step1
            template: run-command

          - name: step2
            dependencies: [step1]
            template: run-command

    - name: run-command
      container:
        image: alpine:latest
        command: [sh, -c]
        args: ["echo hello && exit 0"]

    - name: exit-handler
      steps:
        - - name: notify-success
            template: notify
            when: "{{workflow.status}} == Succeeded"
            arguments:
              parameters:
                - name: message
                  value: "Workflow succeeded!"

        - - name: notify-failure
            template: notify
            when: "{{workflow.status}} != Succeeded"
            arguments:
              parameters:
                - name: message
                  value: "Workflow failed: {{workflow.failures}}"

        - - name: cleanup
            template: cleanup

    - name: notify
      inputs:
        parameters:
          - name: message
      container:
        image: curlimages/curl:latest
        command: [sh, -c]
        args:
          - |
            curl -X POST https://slack.com/webhook \
              -H 'Content-Type: application/json' \
              -d '{"text": "{{inputs.parameters.message}}"}'

    - name: cleanup
      container:
        image: bitnami/kubectl:latest
        command: [kubectl, delete, pod, --all, -n, ci-cd]
```

## Artifacts and Outputs

### Pattern 1: Artifact Passing

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: artifacts-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: generate
            template: generate-artifact

          - name: consume
            dependencies: [generate]
            template: consume-artifact
            arguments:
              artifacts:
                - name: data
                  from: "{{tasks.generate.outputs.artifacts.result}}"

    - name: generate-artifact
      outputs:
        artifacts:
          - name: result
            path: /tmp/output.txt
      container:
        image: alpine:latest
        command: [sh, -c]
        args:
          - |
            echo "Generated data" > /tmp/output.txt
            echo "More data" >> /tmp/output.txt

    - name: consume-artifact
      inputs:
        artifacts:
          - name: data
            path: /tmp/input.txt
      container:
        image: alpine:latest
        command: [sh, -c]
        args:
          - |
            echo "Consuming artifact:"
            cat /tmp/input.txt
```

### Pattern 2: S3 Artifact Repository

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: s3-artifacts-
spec:
  entrypoint: main
  artifactRepositoryRef:
    configMap: artifact-repositories
    key: s3-artifacts

  templates:
    - name: main
      dag:
        tasks:
          - name: build
            template: build-binary

          - name: upload
            dependencies: [build]
            template: upload-binary
            arguments:
              artifacts:
                - name: binary
                  from: "{{tasks.build.outputs.artifacts.binary}}"

    - name: build-binary
      outputs:
        artifacts:
          - name: binary
            path: /workspace/app
            archive:
              none: {}
      container:
        image: golang:1.21
        command: [sh, -c]
        args:
          - |
            go build -o /workspace/app main.go

    - name: upload-binary
      inputs:
        artifacts:
          - name: binary
            path: /tmp/app
      container:
        image: amazon/aws-cli:latest
        command: [sh, -c]
        args:
          - |
            aws s3 cp /tmp/app s3://artifacts-bucket/app-{{workflow.uid}}
```

## Resource Management

### Pattern 1: Resource Limits

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: resources-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: memory-intensive
            template: heavy-task

          - name: cpu-intensive
            template: compute-task

    - name: heavy-task
      container:
        image: java:11
        command: [java]
        args: ["-Xmx4g", "-jar", "app.jar"]
        resources:
          requests:
            memory: 4Gi
            cpu: "2000m"
          limits:
            memory: 8Gi
            cpu: "4000m"

    - name: compute-task
      container:
        image: python:3.11
        command: [python, compute.py]
        resources:
          requests:
            memory: 2Gi
            cpu: "4000m"
          limits:
            memory: 4Gi
            cpu: "8000m"
```

### Pattern 2: Node Affinity

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: affinity-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: gpu-task
            template: ml-training

          - name: regular-task
            template: build

    - name: ml-training
      nodeSelector:
        accelerator: nvidia-tesla-v100
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: instance-type
                    operator: In
                    values:
                      - p3.2xlarge
                      - p3.8xlarge
      container:
        image: tensorflow/tensorflow:latest-gpu
        command: [python, train.py]
        resources:
          limits:
            nvidia.com/gpu: 1

    - name: build
      nodeSelector:
        workload: ci
      container:
        image: golang:1.21
        command: [go, build]
```

## Advanced Patterns

### Pattern 1: Suspend for Manual Approval

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: approval-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: build
            template: build-image

          - name: deploy-staging
            dependencies: [build]
            template: deploy
            arguments:
              parameters:
                - name: env
                  value: staging

          - name: approval
            dependencies: [deploy-staging]
            template: approval-gate

          - name: deploy-prod
            dependencies: [approval]
            template: deploy
            arguments:
              parameters:
                - name: env
                  value: production

    - name: build-image
      container:
        image: gcr.io/kaniko-project/executor:latest
        command: [/kaniko/executor]

    - name: deploy
      inputs:
        parameters:
          - name: env
      container:
        image: bitnami/kubectl:latest
        command: [kubectl, apply, -f, deployment.yaml]

    - name: approval-gate
      suspend: {}
```

### Pattern 2: HTTP Template

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: http-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: create-release
            template: github-release

          - name: notify-slack
            dependencies: [create-release]
            template: slack-notification
            arguments:
              parameters:
                - name: release-url
                  value: "{{tasks.create-release.outputs.parameters.url}}"

    - name: github-release
      outputs:
        parameters:
          - name: url
            valueFrom:
              jqFilter: .html_url
      http:
        url: https://api.github.com/repos/org/repo/releases
        method: POST
        headers:
          - name: Authorization
            value: "Bearer {{workflow.parameters.github-token}}"
          - name: Content-Type
            value: application/json
        body: |
          {
            "tag_name": "v1.0.0",
            "name": "Release v1.0.0",
            "body": "Release notes"
          }
        successCondition: "response.statusCode == 201"

    - name: slack-notification
      inputs:
        parameters:
          - name: release-url
      http:
        url: https://hooks.slack.com/services/XXX/YYY/ZZZ
        method: POST
        headers:
          - name: Content-Type
            value: application/json
        body: |
          {
            "text": "New release created: {{inputs.parameters.release-url}}"
          }
```

### Pattern 3: Daemon Containers (Sidecars)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: daemon-
spec:
  entrypoint: main

  templates:
    - name: main
      dag:
        tasks:
          - name: with-database
            template: test-with-db

    - name: test-with-db
      daemon: true
      container:
        name: postgres
        image: postgres:14
        env:
          - name: POSTGRES_PASSWORD
            value: password
        readinessProbe:
          tcpSocket:
            port: 5432
          initialDelaySeconds: 5
          periodSeconds: 5

    - name: test-with-db
      steps:
        - - name: run-tests
            template: integration-tests

    - name: integration-tests
      container:
        image: golang:1.21
        command: [sh, -c]
        args:
          - |
            export DB_HOST=localhost
            export DB_PORT=5432
            go test -tags=integration ./...
```

## Monitoring and Observability

### Pattern 1: Prometheus Metrics

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: workflow-controller-configmap
  namespace: argo
data:
  config: |
    metricsConfig:
      enabled: true
      path: /metrics
      port: 9090
---
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: argo-workflows
  namespace: argo
spec:
  selector:
    matchLabels:
      app: workflow-controller
  endpoints:
    - port: metrics
      interval: 30s
```

**Key Metrics:**

```promql
# Workflow success rate
rate(argo_workflows_count{status="Succeeded"}[5m])
/
rate(argo_workflows_count[5m])

# Workflow duration
histogram_quantile(0.95,
  rate(argo_workflows_duration_seconds_bucket[5m])
)

# Active workflows
argo_workflows_running_count

# Failed workflows
argo_workflows_count{status="Failed"}
```

### Pattern 2: OpenTelemetry Integration

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: traced-
spec:
  entrypoint: main

  templates:
    - name: main
      metadata:
        annotations:
          trace: "true"
      dag:
        tasks:
          - name: task1
            template: traced-task
          - name: task2
            dependencies: [task1]
            template: traced-task

    - name: traced-task
      container:
        image: myapp:latest
        env:
          - name: OTEL_EXPORTER_OTLP_ENDPOINT
            value: "http://otel-collector:4317"
          - name: OTEL_SERVICE_NAME
            value: "{{workflow.name}}"
          - name: OTEL_RESOURCE_ATTRIBUTES
            value: "workflow.name={{workflow.name}},task.name={{pod.name}}"
```

## Best Practices

1. **Use DAGs for complex dependencies** - Better visibility and parallelization
2. **Implement proper retry strategies** - Handle transient failures gracefully
3. **Set resource limits** - Prevent resource exhaustion
4. **Use workspaceSecurityContext** - Run as non-root when possible
5. **Implement timeouts** - Prevent hanging workflows
6. **Archive artifacts appropriately** - Balance storage costs with needs
7. **Use output parameters** - Pass data between templates efficiently
8. **Implement exit handlers** - Always cleanup resources
9. **Monitor workflows** - Track success rates and duration
10. **Version control workflow templates** - Treat as infrastructure as code

## Additional Resources

- [Argo Workflows Documentation](https://argoproj.github.io/argo-workflows/)
- [Argo Workflows Examples](https://github.com/argoproj/argo-workflows/tree/master/examples)
- [Argo Community](https://argoproj.github.io/community/)
