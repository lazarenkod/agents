# Tekton Patterns and Best Practices

This guide provides enterprise-grade patterns for Tekton Pipelines based on production experience at AWS, Azure, and Google Cloud.

## Table of Contents

- [Reusable Task Patterns](#reusable-task-patterns)
- [Pipeline Composition](#pipeline-composition)
- [Workspace Management](#workspace-management)
- [Parameter Strategies](#parameter-strategies)
- [Resource Management](#resource-management)
- [Error Handling](#error-handling)
- [Security Best Practices](#security-best-practices)
- [Performance Optimization](#performance-optimization)
- [Testing Strategies](#testing-strategies)

## Reusable Task Patterns

### Pattern 1: Git Clone Task with Authentication

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: git-clone-auth
  labels:
    app.kubernetes.io/version: "0.7"
spec:
  description: Clone a git repository with authentication support
  params:
    - name: url
      description: Git repository URL
      type: string
    - name: revision
      description: Git revision to checkout (branch, tag, sha, ref)
      type: string
      default: main
    - name: refspec
      description: Git refspec to fetch
      type: string
      default: ""
    - name: submodules
      description: Initialize and fetch git submodules
      type: string
      default: "true"
    - name: depth
      description: Perform a shallow clone with depth
      type: string
      default: "1"
    - name: sslVerify
      description: Verify SSL certificates
      type: string
      default: "true"
    - name: subdirectory
      description: Subdirectory inside workspace to clone to
      type: string
      default: ""
    - name: deleteExisting
      description: Delete existing directory before cloning
      type: string
      default: "true"
    - name: httpProxy
      description: HTTP proxy server
      type: string
      default: ""
    - name: httpsProxy
      description: HTTPS proxy server
      type: string
      default: ""
    - name: noProxy
      description: No proxy domains
      type: string
      default: ""
    - name: verbose
      description: Log git commands
      type: string
      default: "true"
    - name: gitInitImage
      description: Git init image
      type: string
      default: "gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/git-init:v0.40.2"

  workspaces:
    - name: output
      description: The git repo will be cloned onto this workspace
    - name: ssh-directory
      description: SSH credentials directory
      optional: true
    - name: basic-auth
      description: Basic auth credentials
      optional: true

  results:
    - name: commit
      description: The commit SHA that was fetched
    - name: url
      description: The URL that was fetched
    - name: committer-date
      description: The date of the commit

  steps:
    - name: clone
      image: $(params.gitInitImage)
      env:
        - name: PARAM_URL
          value: $(params.url)
        - name: PARAM_REVISION
          value: $(params.revision)
        - name: PARAM_REFSPEC
          value: $(params.refspec)
        - name: PARAM_SUBMODULES
          value: $(params.submodules)
        - name: PARAM_DEPTH
          value: $(params.depth)
        - name: PARAM_SSL_VERIFY
          value: $(params.sslVerify)
        - name: PARAM_SUBDIRECTORY
          value: $(params.subdirectory)
        - name: PARAM_DELETE_EXISTING
          value: $(params.deleteExisting)
        - name: PARAM_HTTP_PROXY
          value: $(params.httpProxy)
        - name: PARAM_HTTPS_PROXY
          value: $(params.httpsProxy)
        - name: PARAM_NO_PROXY
          value: $(params.noProxy)
        - name: PARAM_VERBOSE
          value: $(params.verbose)
        - name: WORKSPACE_OUTPUT_PATH
          value: $(workspaces.output.path)
        - name: WORKSPACE_SSH_DIRECTORY_BOUND
          value: $(workspaces.ssh-directory.bound)
        - name: WORKSPACE_SSH_DIRECTORY_PATH
          value: $(workspaces.ssh-directory.path)
        - name: WORKSPACE_BASIC_AUTH_DIRECTORY_BOUND
          value: $(workspaces.basic-auth.bound)
        - name: WORKSPACE_BASIC_AUTH_DIRECTORY_PATH
          value: $(workspaces.basic-auth.path)
      script: |
        #!/usr/bin/env sh
        set -eu

        if [ "${PARAM_VERBOSE}" = "true" ] ; then
          set -x
        fi

        if [ "${WORKSPACE_BASIC_AUTH_DIRECTORY_BOUND}" = "true" ] ; then
          cp "${WORKSPACE_BASIC_AUTH_DIRECTORY_PATH}/.git-credentials" "${HOME}/.git-credentials"
          cp "${WORKSPACE_BASIC_AUTH_DIRECTORY_PATH}/.gitconfig" "${HOME}/.gitconfig"
          chmod 400 "${HOME}/.git-credentials"
          chmod 400 "${HOME}/.gitconfig"
        fi

        if [ "${WORKSPACE_SSH_DIRECTORY_BOUND}" = "true" ] ; then
          cp -R "${WORKSPACE_SSH_DIRECTORY_PATH}" "${HOME}"/.ssh
          chmod 700 "${HOME}"/.ssh
          chmod -R 400 "${HOME}"/.ssh/*
        fi

        CHECKOUT_DIR="${WORKSPACE_OUTPUT_PATH}/${PARAM_SUBDIRECTORY}"

        cleandir() {
          if [ -d "${CHECKOUT_DIR}" ] ; then
            rm -rf "${CHECKOUT_DIR}"
          fi
        }

        if [ "${PARAM_DELETE_EXISTING}" = "true" ] ; then
          cleandir
        fi

        test -z "${PARAM_HTTP_PROXY}" || export HTTP_PROXY="${PARAM_HTTP_PROXY}"
        test -z "${PARAM_HTTPS_PROXY}" || export HTTPS_PROXY="${PARAM_HTTPS_PROXY}"
        test -z "${PARAM_NO_PROXY}" || export NO_PROXY="${PARAM_NO_PROXY}"

        /ko-app/git-init \
          -url="${PARAM_URL}" \
          -revision="${PARAM_REVISION}" \
          -refspec="${PARAM_REFSPEC}" \
          -path="${CHECKOUT_DIR}" \
          -sslVerify="${PARAM_SSL_VERIFY}" \
          -submodules="${PARAM_SUBMODULES}" \
          -depth="${PARAM_DEPTH}"
        cd "${CHECKOUT_DIR}"
        RESULT_SHA="$(git rev-parse HEAD)"
        EXIT_CODE="$?"
        if [ "${EXIT_CODE}" != 0 ] ; then
          exit "${EXIT_CODE}"
        fi

        printf "%s" "${RESULT_SHA}" > "$(results.commit.path)"
        printf "%s" "${PARAM_URL}" > "$(results.url.path)"
        printf "%s" "$(git log -1 --pretty=%ct)" > "$(results.committer-date.path)"
```

### Pattern 2: Kaniko Build Task with Multi-Registry Support

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: kaniko-multi-registry
  labels:
    app.kubernetes.io/version: "0.6"
spec:
  description: Build and push images using Kaniko to multiple registries
  params:
    - name: IMAGE
      description: Name (reference) of the image to build
    - name: DOCKERFILE
      description: Path to the Dockerfile
      default: ./Dockerfile
    - name: CONTEXT
      description: Build context
      default: ./
    - name: EXTRA_ARGS
      type: array
      default: []
    - name: BUILDER_IMAGE
      description: The image on which builds will run
      default: gcr.io/kaniko-project/executor:v1.11.0@sha256:f0d2f7a83c8f8c7e39e6c3d7f2a9e0e1f5b1e9e8f9a1f0e9b8c7d6e5f4a3b2c1
    - name: TARGET_REGISTRIES
      description: Comma-separated list of registries to push to
      type: string
      default: ""

  workspaces:
    - name: source
      description: Source code workspace
    - name: dockerconfig
      description: Docker config containing registry credentials
      mountPath: /kaniko/.docker
      optional: true

  results:
    - name: IMAGE_DIGEST
      description: Digest of the image just built
    - name: IMAGE_URL
      description: URL of the image just built

  steps:
    - name: build-and-push
      workingDir: $(workspaces.source.path)
      image: $(params.BUILDER_IMAGE)
      args:
        - $(params.EXTRA_ARGS)
        - --dockerfile=$(params.DOCKERFILE)
        - --context=$(params.CONTEXT)
        - --destination=$(params.IMAGE)
        - --digest-file=$(results.IMAGE_DIGEST.path)
        - --cache=true
        - --cache-ttl=24h
        - --snapshot-mode=redo
        - --compressed-caching=false
        - --use-new-run
        - --skip-unused-stages=true
      securityContext:
        runAsUser: 0

    - name: push-to-additional-registries
      image: gcr.io/go-containerregistry/crane:debug
      workingDir: $(workspaces.source.path)
      script: |
        #!/busybox/sh
        set -e

        # Read the image digest
        DIGEST=$(cat $(results.IMAGE_DIGEST.path))
        SOURCE_IMAGE="$(params.IMAGE)@${DIGEST}"

        # Parse additional registries
        IFS=',' read -ra REGISTRIES <<< "$(params.TARGET_REGISTRIES)"

        # Copy image to each registry
        for registry in "${REGISTRIES[@]}"; do
          if [ -n "$registry" ]; then
            TARGET_IMAGE="${registry}/$(basename $(params.IMAGE))"
            echo "Copying to ${TARGET_IMAGE}"
            crane copy "${SOURCE_IMAGE}" "${TARGET_IMAGE}"
          fi
        done

        # Write IMAGE_URL result
        printf "%s" "$(params.IMAGE)" | tee "$(results.IMAGE_URL.path)"
      volumeMounts:
        - name: dockerconfig
          mountPath: /root/.docker
          readOnly: true
```

### Pattern 3: Dynamic Test Task (Language Agnostic)

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: run-tests
  labels:
    app.kubernetes.io/version: "1.0"
spec:
  description: Run tests based on detected language/framework
  params:
    - name: test-command
      description: Command to run tests
      type: string
      default: ""
    - name: test-args
      description: Arguments for test command
      type: array
      default: []
    - name: source-dir
      description: Directory containing source code
      type: string
      default: "."

  workspaces:
    - name: source

  results:
    - name: test-status
      description: Status of tests (passed/failed)
    - name: coverage
      description: Test coverage percentage

  steps:
    - name: detect-language
      image: alpine:latest
      workingDir: $(workspaces.source.path)/$(params.source-dir)
      script: |
        #!/bin/sh
        set -e

        # Detect language and framework
        if [ -f "go.mod" ]; then
          echo "golang" > /tmp/language
        elif [ -f "package.json" ]; then
          if grep -q '"jest"' package.json; then
            echo "node-jest" > /tmp/language
          else
            echo "node-npm" > /tmp/language
          fi
        elif [ -f "Cargo.toml" ]; then
          echo "rust" > /tmp/language
        elif [ -f "pom.xml" ]; then
          echo "java-maven" > /tmp/language
        elif [ -f "build.gradle" ]; then
          echo "java-gradle" > /tmp/language
        elif [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
          echo "python" > /tmp/language
        else
          echo "unknown" > /tmp/language
        fi

        cat /tmp/language
      volumeMounts:
        - name: tmp
          mountPath: /tmp

    - name: run-tests
      workingDir: $(workspaces.source.path)/$(params.source-dir)
      script: |
        #!/bin/sh
        set -e

        LANGUAGE=$(cat /tmp/language)
        echo "Detected language: ${LANGUAGE}"

        # Execute tests based on language
        case "${LANGUAGE}" in
          golang)
            go test -v -coverprofile=coverage.out ./...
            COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}')
            ;;
          node-jest)
            npm test -- --coverage --coverageReporters=text-summary
            COVERAGE=$(cat coverage/coverage-summary.json | jq -r '.total.lines.pct')
            ;;
          node-npm)
            npm test
            COVERAGE="N/A"
            ;;
          rust)
            cargo test
            COVERAGE=$(cargo tarpaulin --out Stdout | grep -oP '\d+\.\d+%' | head -1)
            ;;
          java-maven)
            mvn test
            COVERAGE="N/A"
            ;;
          java-gradle)
            ./gradlew test
            COVERAGE="N/A"
            ;;
          python)
            pytest --cov --cov-report=term-missing
            COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}')
            ;;
          *)
            if [ -n "$(params.test-command)" ]; then
              $(params.test-command) $(params.test-args[*])
            else
              echo "Unknown language and no test command provided"
              exit 1
            fi
            COVERAGE="N/A"
            ;;
        esac

        TEST_EXIT_CODE=$?

        # Write results
        if [ $TEST_EXIT_CODE -eq 0 ]; then
          echo "passed" | tee $(results.test-status.path)
        else
          echo "failed" | tee $(results.test-status.path)
        fi

        echo "${COVERAGE}" | tee $(results.coverage.path)

        exit $TEST_EXIT_CODE
      volumeMounts:
        - name: tmp
          mountPath: /tmp

  volumes:
    - name: tmp
      emptyDir: {}
```

## Pipeline Composition

### Pattern 1: Matrix Testing Pipeline

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: matrix-testing
spec:
  description: Run tests across multiple versions/platforms
  params:
    - name: git-url
      type: string
    - name: git-revision
      type: string
      default: main

  workspaces:
    - name: shared-data

  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone-auth
      workspaces:
        - name: output
          workspace: shared-data
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)

    # Matrix: Test on multiple Go versions
    - name: test-go-1-19
      runAfter: [fetch-source]
      taskRef:
        name: golang-test
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: version
          value: "1.19"

    - name: test-go-1-20
      runAfter: [fetch-source]
      taskRef:
        name: golang-test
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: version
          value: "1.20"

    - name: test-go-1-21
      runAfter: [fetch-source]
      taskRef:
        name: golang-test
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: version
          value: "1.21"

    # Wait for all tests to complete
    - name: build-image
      runAfter:
        - test-go-1-19
        - test-go-1-20
        - test-go-1-21
      taskRef:
        name: kaniko-multi-registry
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: registry.example.com/myapp:$(tasks.fetch-source.results.commit)
```

### Pattern 2: Conditional Deployment Pipeline

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: conditional-deploy
spec:
  params:
    - name: git-url
    - name: git-revision
      default: main
    - name: deploy-to-prod
      type: string
      default: "false"

  workspaces:
    - name: shared-data

  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone-auth
      workspaces:
        - name: output
          workspace: shared-data
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)

    - name: run-tests
      runAfter: [fetch-source]
      taskRef:
        name: run-tests
      workspaces:
        - name: source
          workspace: shared-data

    - name: build-image
      runAfter: [run-tests]
      taskRef:
        name: kaniko-multi-registry
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: registry.example.com/myapp:$(tasks.fetch-source.results.commit)

    - name: deploy-to-dev
      runAfter: [build-image]
      taskRef:
        name: kubectl-deploy
      params:
        - name: namespace
          value: dev
        - name: image
          value: registry.example.com/myapp:$(tasks.fetch-source.results.commit)

    - name: deploy-to-staging
      runAfter: [deploy-to-dev]
      taskRef:
        name: kubectl-deploy
      params:
        - name: namespace
          value: staging
        - name: image
          value: registry.example.com/myapp:$(tasks.fetch-source.results.commit)

    - name: deploy-to-prod
      runAfter: [deploy-to-staging]
      when:
        - input: "$(params.deploy-to-prod)"
          operator: in
          values: ["true"]
      taskRef:
        name: kubectl-deploy
      params:
        - name: namespace
          value: production
        - name: image
          value: registry.example.com/myapp:$(tasks.fetch-source.results.commit)
```

### Pattern 3: Parallel Build Pipeline (Monorepo)

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: monorepo-parallel-build
spec:
  description: Build multiple services in parallel from monorepo
  params:
    - name: git-url
    - name: git-revision
      default: main

  workspaces:
    - name: shared-data

  tasks:
    - name: fetch-source
      taskRef:
        name: git-clone-auth
      workspaces:
        - name: output
          workspace: shared-data
      params:
        - name: url
          value: $(params.git-url)
        - name: revision
          value: $(params.git-revision)

    # Parallel builds for each service
    - name: build-frontend
      runAfter: [fetch-source]
      taskRef:
        name: kaniko-multi-registry
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: registry.example.com/frontend:$(tasks.fetch-source.results.commit)
        - name: CONTEXT
          value: ./services/frontend
        - name: DOCKERFILE
          value: ./services/frontend/Dockerfile

    - name: build-api
      runAfter: [fetch-source]
      taskRef:
        name: kaniko-multi-registry
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: registry.example.com/api:$(tasks.fetch-source.results.commit)
        - name: CONTEXT
          value: ./services/api
        - name: DOCKERFILE
          value: ./services/api/Dockerfile

    - name: build-worker
      runAfter: [fetch-source]
      taskRef:
        name: kaniko-multi-registry
      workspaces:
        - name: source
          workspace: shared-data
      params:
        - name: IMAGE
          value: registry.example.com/worker:$(tasks.fetch-source.results.commit)
        - name: CONTEXT
          value: ./services/worker
        - name: DOCKERFILE
          value: ./services/worker/Dockerfile

    # Deploy all services together after all builds complete
    - name: deploy-all
      runAfter:
        - build-frontend
        - build-api
        - build-worker
      taskRef:
        name: kubectl-deploy-multi
      params:
        - name: images
          value:
            - registry.example.com/frontend:$(tasks.fetch-source.results.commit)
            - registry.example.com/api:$(tasks.fetch-source.results.commit)
            - registry.example.com/worker:$(tasks.fetch-source.results.commit)
```

## Workspace Management

### Pattern 1: PVC Template for Dynamic Workspaces

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: build-run-
spec:
  pipelineRef:
    name: build-pipeline
  workspaces:
    - name: shared-data
      volumeClaimTemplate:
        spec:
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 10Gi
          storageClassName: fast-ssd
```

### Pattern 2: Persistent Workspace for Caching

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pipeline-cache
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: nfs-client
---
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: build-with-cache
spec:
  pipelineRef:
    name: build-pipeline
  workspaces:
    - name: source
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          resources:
            requests:
              storage: 10Gi
    - name: cache
      persistentVolumeClaim:
        claimName: pipeline-cache
```

### Pattern 3: EmptyDir for Ephemeral Data

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: test-run
spec:
  taskRef:
    name: run-tests
  workspaces:
    - name: source
      emptyDir: {}
```

## Parameter Strategies

### Pattern 1: Default Parameters with Overrides

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: configurable-pipeline
spec:
  params:
    # Build parameters
    - name: dockerfile
      type: string
      default: Dockerfile
      description: Path to Dockerfile
    - name: context
      type: string
      default: .
      description: Build context
    - name: build-args
      type: array
      default: []
      description: Build arguments

    # Test parameters
    - name: skip-tests
      type: string
      default: "false"
      description: Skip test execution
    - name: test-timeout
      type: string
      default: "30m"
      description: Test timeout duration

    # Deployment parameters
    - name: target-env
      type: string
      default: dev
      description: Target environment (dev/staging/prod)
    - name: replicas
      type: string
      default: "3"
      description: Number of replicas

  tasks:
    - name: build
      taskRef:
        name: kaniko-build
      params:
        - name: DOCKERFILE
          value: $(params.dockerfile)
        - name: CONTEXT
          value: $(params.context)
        - name: EXTRA_ARGS
          value: $(params.build-args[*])

    - name: test
      when:
        - input: "$(params.skip-tests)"
          operator: notin
          values: ["true"]
      taskRef:
        name: run-tests
      timeout: $(params.test-timeout)

    - name: deploy
      taskRef:
        name: deploy
      params:
        - name: environment
          value: $(params.target-env)
        - name: replicas
          value: $(params.replicas)
```

### Pattern 2: Parameter Validation Task

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: validate-params
spec:
  params:
    - name: environment
      type: string
    - name: image-tag
      type: string
    - name: replicas
      type: string

  steps:
    - name: validate
      image: alpine:latest
      script: |
        #!/bin/sh
        set -e

        # Validate environment
        case "$(params.environment)" in
          dev|staging|production)
            echo "✓ Valid environment: $(params.environment)"
            ;;
          *)
            echo "✗ Invalid environment: $(params.environment)"
            echo "  Must be one of: dev, staging, production"
            exit 1
            ;;
        esac

        # Validate image tag format
        if ! echo "$(params.image-tag)" | grep -qE '^[a-z0-9.-]+:[a-z0-9.-]+$'; then
          echo "✗ Invalid image tag format: $(params.image-tag)"
          echo "  Expected format: registry/image:tag"
          exit 1
        fi
        echo "✓ Valid image tag: $(params.image-tag)"

        # Validate replicas
        if ! echo "$(params.replicas)" | grep -qE '^[0-9]+$'; then
          echo "✗ Invalid replicas value: $(params.replicas)"
          echo "  Must be a positive integer"
          exit 1
        fi

        REPLICAS=$(params.replicas)
        if [ "$REPLICAS" -lt 1 ] || [ "$REPLICAS" -gt 100 ]; then
          echo "✗ Replicas out of range: $(params.replicas)"
          echo "  Must be between 1 and 100"
          exit 1
        fi
        echo "✓ Valid replicas: $(params.replicas)"

        echo ""
        echo "All parameters validated successfully!"
```

## Resource Management

### Pattern 1: Resource Quotas per Task

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: resource-aware-build
spec:
  steps:
    - name: build
      image: gradle:jdk11
      resources:
        requests:
          memory: 2Gi
          cpu: "1000m"
        limits:
          memory: 4Gi
          cpu: "2000m"
      script: |
        #!/usr/bin/env bash
        gradle build -Xmx3g

    - name: test
      image: gradle:jdk11
      resources:
        requests:
          memory: 1Gi
          cpu: "500m"
        limits:
          memory: 2Gi
          cpu: "1000m"
      script: |
        #!/usr/bin/env bash
        gradle test
```

### Pattern 2: Node Affinity for CI Workloads

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: build-on-ci-nodes
spec:
  pipelineRef:
    name: build-pipeline
  podTemplate:
    nodeSelector:
      workload: ci
    tolerations:
      - key: "ci-workload"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
    affinity:
      nodeAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
                - key: instance-type
                  operator: In
                  values:
                    - c5.2xlarge
                    - c5.4xlarge
```

### Pattern 3: Timeout Configuration

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: timeout-pipeline
spec:
  tasks:
    - name: quick-task
      timeout: "5m"
      taskRef:
        name: lint

    - name: normal-task
      timeout: "30m"
      taskRef:
        name: test

    - name: long-task
      timeout: "2h"
      taskRef:
        name: integration-test

  finally:
    - name: cleanup
      timeout: "10m"
      taskRef:
        name: cleanup-resources
```

## Error Handling

### Pattern 1: Retry on Failure

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: flaky-test-with-retry
spec:
  steps:
    - name: test
      image: maven:3.8-jdk-11
      onError: continue
      script: |
        #!/usr/bin/env bash
        set -e

        MAX_RETRIES=3
        RETRY_COUNT=0

        while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
          echo "Attempt $((RETRY_COUNT + 1)) of $MAX_RETRIES"

          if mvn test; then
            echo "Tests passed!"
            exit 0
          fi

          RETRY_COUNT=$((RETRY_COUNT + 1))
          if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "Tests failed. Retrying in 30 seconds..."
            sleep 30
          fi
        done

        echo "Tests failed after $MAX_RETRIES attempts"
        exit 1
```

### Pattern 2: Finally Tasks for Cleanup

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: pipeline-with-cleanup
spec:
  tasks:
    - name: setup
      taskRef:
        name: create-resources

    - name: test
      runAfter: [setup]
      taskRef:
        name: run-tests

    - name: deploy
      runAfter: [test]
      taskRef:
        name: deploy-app

  finally:
    - name: cleanup
      taskRef:
        name: delete-resources

    - name: notify
      taskRef:
        name: send-notification
      params:
        - name: status
          value: $(tasks.status)
        - name: pipeline-name
          value: $(context.pipelineRun.name)
```

### Pattern 3: Error Notification Task

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: notify-on-failure
spec:
  params:
    - name: pipeline-name
    - name: failed-task
    - name: webhook-url

  steps:
    - name: send-notification
      image: curlimages/curl:latest
      script: |
        #!/bin/sh
        set -e

        MESSAGE="Pipeline $(params.pipeline-name) failed at task $(params.failed-task)"

        curl -X POST $(params.webhook-url) \
          -H 'Content-Type: application/json' \
          -d "{
            \"text\": \"${MESSAGE}\",
            \"blocks\": [
              {
                \"type\": \"section\",
                \"text\": {
                  \"type\": \"mrkdwn\",
                  \"text\": \":x: *Pipeline Failure*\"
                }
              },
              {
                \"type\": \"section\",
                \"fields\": [
                  {
                    \"type\": \"mrkdwn\",
                    \"text\": \"*Pipeline:*\\n$(params.pipeline-name)\"
                  },
                  {
                    \"type\": \"mrkdwn\",
                    \"text\": \"*Failed Task:*\\n$(params.failed-task)\"
                  }
                ]
              }
            ]
          }"
```

## Security Best Practices

### Pattern 1: Secret Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-config>
---
apiVersion: v1
kind: Secret
metadata:
  name: git-ssh-key
type: kubernetes.io/ssh-auth
data:
  ssh-privatekey: <base64-encoded-key>
  known_hosts: <base64-encoded-known-hosts>
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tekton-pipeline-sa
secrets:
  - name: registry-credentials
  - name: git-ssh-key
---
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: secure-pipeline-run
spec:
  serviceAccountName: tekton-pipeline-sa
  pipelineRef:
    name: secure-pipeline
```

### Pattern 2: Non-Root Containers

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: secure-task
spec:
  steps:
    - name: build
      image: gcr.io/kaniko-project/executor:latest
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        allowPrivilegeEscalation: false
        runAsNonRoot: true
        capabilities:
          drop:
            - ALL
      script: |
        #!/busybox/sh
        /kaniko/executor \
          --context=dir://$(workspaces.source.path) \
          --destination=$(params.image)
```

### Pattern 3: Pod Security Standards

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: restricted-pipeline-run
spec:
  pipelineRef:
    name: build-pipeline
  podTemplate:
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
      fsGroup: 1000
      seccompProfile:
        type: RuntimeDefault
    volumes:
      - name: dockerconfig
        secret:
          secretName: regcred
          optional: false
```

## Performance Optimization

### Pattern 1: Layer Caching with Kaniko

```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: kaniko-cached-build
spec:
  params:
    - name: IMAGE
    - name: CACHE_REPO
      default: registry.example.com/cache

  workspaces:
    - name: source

  steps:
    - name: build-with-cache
      image: gcr.io/kaniko-project/executor:latest
      args:
        - --context=$(workspaces.source.path)
        - --destination=$(params.IMAGE)
        - --cache=true
        - --cache-repo=$(params.CACHE_REPO)
        - --cache-ttl=168h
        - --snapshot-mode=redo
        - --use-new-run
        - --compressed-caching=false
```

### Pattern 2: Parallel Task Execution

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: parallel-optimized
spec:
  tasks:
    # These run in parallel automatically
    - name: lint
      taskRef:
        name: golangci-lint

    - name: security-scan
      taskRef:
        name: gosec

    - name: unit-tests
      taskRef:
        name: go-test

    - name: integration-tests
      taskRef:
        name: integration-test

    # This waits for all parallel tasks
    - name: build
      runAfter:
        - lint
        - security-scan
        - unit-tests
        - integration-tests
      taskRef:
        name: kaniko-build
```

### Pattern 3: Workspace Optimization

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: optimized-workspace
spec:
  pipelineRef:
    name: build-pipeline
  workspaces:
    # Fast local storage for build artifacts
    - name: source
      volumeClaimTemplate:
        spec:
          accessModes: [ReadWriteOnce]
          storageClassName: fast-ssd
          resources:
            requests:
              storage: 10Gi

    # Shared cache on NFS for reusability
    - name: cache
      persistentVolumeClaim:
        claimName: shared-cache
```

## Testing Strategies

### Pattern 1: Pipeline Testing with dry-run

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: test-pipeline-dry-run
spec:
  pipelineRef:
    name: production-pipeline
  params:
    - name: dry-run
      value: "true"
    - name: git-url
      value: https://github.com/example/repo
  workspaces:
    - name: shared-data
      emptyDir: {}
```

### Pattern 2: Task Unit Testing

```yaml
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: test-git-clone-task
spec:
  taskRef:
    name: git-clone-auth
  params:
    - name: url
      value: https://github.com/tektoncd/pipeline
    - name: revision
      value: main
    - name: depth
      value: "1"
  workspaces:
    - name: output
      emptyDir: {}
```

### Pattern 3: Integration Testing Pipeline

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: integration-test-pipeline
spec:
  tasks:
    - name: deploy-test-environment
      taskRef:
        name: deploy-ephemeral-env

    - name: run-integration-tests
      runAfter: [deploy-test-environment]
      taskRef:
        name: run-tests
      params:
        - name: test-suite
          value: integration

    - name: run-e2e-tests
      runAfter: [deploy-test-environment]
      taskRef:
        name: run-tests
      params:
        - name: test-suite
          value: e2e

  finally:
    - name: cleanup-test-environment
      taskRef:
        name: delete-ephemeral-env
      params:
        - name: environment-id
          value: $(tasks.deploy-test-environment.results.env-id)
```

## Best Practices Summary

1. **Reusability**: Create generic, parameterized Tasks
2. **Security**: Use ServiceAccounts, run as non-root, manage secrets properly
3. **Performance**: Leverage caching, parallel execution, appropriate storage classes
4. **Reliability**: Implement retries, timeouts, and proper error handling
5. **Observability**: Use results, emit events, integrate with monitoring
6. **Maintainability**: Use clear naming, documentation, and consistent patterns
7. **Scalability**: Set resource limits, use node affinity, implement cleanup
8. **Testing**: Test pipelines and tasks in isolation before production use

## Additional Resources

- [Tekton Catalog](https://hub.tekton.dev/)
- [Tekton Documentation](https://tekton.dev/docs/)
- [Tekton GitHub](https://github.com/tektoncd/pipeline)
- [CD Foundation Best Practices](https://cd.foundation/blog/)
