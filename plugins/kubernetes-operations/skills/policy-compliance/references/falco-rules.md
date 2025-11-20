# Falco Runtime Security Rules

## Table of Contents

- [Falco Architecture](#falco-architecture)
- [Rule Syntax](#rule-syntax)
- [Built-in Rules](#built-in-rules)
- [Custom Rules](#custom-rules)
- [Kubernetes Audit Rules](#kubernetes-audit-rules)
- [Alert Routing](#alert-routing)
- [Response Automation](#response-automation)
- [Tuning and Optimization](#tuning-and-optimization)

## Falco Architecture

### Components

**1. Data Sources:**
- **Syscall Events**: Kernel-level monitoring via eBPF or kernel module
- **Kubernetes Audit Log**: API server audit events
- **Plugin System**: CloudTrail, Okta, GitHub, custom sources

**2. Rule Engine:**
- **Rules**: Detection patterns written in YAML
- **Macros**: Reusable conditions
- **Lists**: Reusable value sets
- **Exceptions**: Override rules for specific scenarios

**3. Output:**
- **stdout/stderr**: Console output
- **syslog**: System log integration
- **HTTP**: Webhook endpoints
- **gRPC**: Falco Sidekick, custom consumers

### Installation

**DaemonSet Deployment:**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
    spec:
      serviceAccountName: falco
      hostNetwork: true
      hostPID: true
      containers:
      - name: falco
        image: falcosecurity/falco:0.36.2
        securityContext:
          privileged: true
        args:
        - /usr/bin/falco
        - -K
        - /var/run/secrets/kubernetes.io/serviceaccount/token
        - -k
        - https://kubernetes.default
        - -pk
        volumeMounts:
        - name: dev
          mountPath: /host/dev
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: boot
          mountPath: /host/boot
          readOnly: true
        - name: lib-modules
          mountPath: /host/lib/modules
          readOnly: true
        - name: usr
          mountPath: /host/usr
          readOnly: true
        - name: etc
          mountPath: /host/etc
          readOnly: true
        - name: config
          mountPath: /etc/falco
      volumes:
      - name: dev
        hostPath:
          path: /dev
      - name: proc
        hostPath:
          path: /proc
      - name: boot
        hostPath:
          path: /boot
      - name: lib-modules
        hostPath:
          path: /lib/modules
      - name: usr
        hostPath:
          path: /usr
      - name: etc
        hostPath:
          path: /etc
      - name: config
        configMap:
          name: falco-config
```

**Helm Installation:**

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=ebpf \
  --set tty=true \
  --set falco.jsonOutput=true \
  --set falco.jsonIncludeOutputProperty=true
```

## Rule Syntax

### Basic Rule Structure

```yaml
- rule: Rule Name
  desc: Human-readable description of what this rule detects
  condition: Boolean expression that triggers alert
  output: Alert message template with variables
  priority: EMERGENCY | ALERT | CRITICAL | ERROR | WARNING | NOTICE | INFORMATIONAL | DEBUG
  tags: [tag1, tag2, tag3]
  enabled: true | false
```

### Example Rule

```yaml
- rule: Write below root
  desc: Attempt to write to root filesystem
  condition: >
    evt.type = open and
    evt.dir = < and
    fd.name startswith / and
    not fd.name startswith /tmp and
    not fd.name startswith /var/tmp and
    container.id != host and
    proc.name != systemd
  output: >
    File below root opened for writing
    (user=%user.name
    command=%proc.cmdline
    file=%fd.name
    container_id=%container.id
    container_name=%container.name
    image=%container.image.repository)
  priority: ERROR
  tags: [filesystem, mitre_persistence]
```

### Condition Syntax

**Field Comparisons:**

```yaml
# Equality
condition: evt.type = open

# Inequality
condition: evt.type != close

# Less than / Greater than
condition: evt.latency > 1000000

# String operations
condition: proc.name startswith "python"
condition: fd.name endswith ".conf"
condition: proc.cmdline contains "bash -i"

# Regular expressions
condition: proc.name glob "python*"
condition: fd.name regex "/etc/.*\.conf$"

# IN operator
condition: evt.type in (open, openat, openat2)
condition: proc.name in (ls, ps, cat)

# NOT operator
condition: not proc.name = bash
```

**Boolean Logic:**

```yaml
# AND
condition: evt.type = open and fd.name = "/etc/passwd"

# OR
condition: proc.name = bash or proc.name = sh

# Complex expressions
condition: >
  (evt.type = open or evt.type = openat) and
  (fd.name startswith /etc or fd.name startswith /root) and
  not proc.name in (systemd, dockerd)
```

## Built-in Rules

### Container Security Rules

**1. Terminal Shell in Container:**

```yaml
- rule: Terminal shell in container
  desc: A shell was spawned in a container (interactive TTY)
  condition: >
    spawned_process and
    container and
    shell_procs and
    proc.tty != 0 and
    not user_expected_terminal_shell_in_container_conditions
  output: >
    Shell spawned in container
    (user=%user.name user_loginuid=%user.loginuid
    %container.info
    shell=%proc.name parent=%proc.pname
    cmdline=%proc.cmdline terminal=%proc.tty
    %container.info)
  priority: NOTICE
  tags: [container, shell, mitre_execution]
```

**2. Privileged Container:**

```yaml
- rule: Launch Privileged Container
  desc: Detect launch of a privileged container
  condition: >
    evt.type = container and
    container.privileged = true and
    not trusted_containers
  output: >
    Privileged container started
    (user=%user.name
    command=%proc.cmdline
    %container.info
    image=%container.image.repository:%container.image.tag)
  priority: WARNING
  tags: [container, cis, mitre_privilege_escalation]
```

**3. Sensitive Mount:**

```yaml
- rule: Launch Sensitive Mount Container
  desc: Container with sensitive host path mounts
  condition: >
    evt.type = container and
    container.mount.dest in (
      /proc, /var/run/docker.sock, /,
      /etc, /root, /var/run/crio/crio.sock,
      /run/containerd/containerd.sock,
      /var/lib/kubelet, /var/lib/kubelet/pki,
      /etc/kubernetes, /etc/kubernetes/manifests
    )
  output: >
    Container with sensitive mount started
    (user=%user.name
    command=%proc.cmdline
    %container.info
    mount_source=%container.mount.source
    mount_dest=%container.mount.dest
    image=%container.image.repository:%container.image.tag)
  priority: CRITICAL
  tags: [container, cis, mitre_persistence]
```

### Process Execution Rules

**1. Reverse Shell:**

```yaml
- rule: Reverse Shell
  desc: Detect bash/sh reverse shell connection
  condition: >
    spawned_process and
    shell_procs and
    proc.cmdline contains "-i" and
    (proc.cmdline contains "/dev/tcp/" or
     proc.cmdline contains "/dev/udp/" or
     proc.cmdline contains ">&" or
     proc.cmdline contains "2>&1")
  output: >
    Reverse shell detected
    (user=%user.name
    process=%proc.name
    parent=%proc.pname
    cmdline=%proc.cmdline
    terminal=%proc.tty
    %container.info
    image=%container.image.repository)
  priority: CRITICAL
  tags: [network, mitre_execution, T1059]
```

**2. Cryptocurrency Mining:**

```yaml
- rule: Detect crypto miners using Stratum protocol
  desc: Detect cryptocurrency miners based on network behavior
  condition: >
    net_miner_pool and
    not trusted_containers
  output: >
    Crypto miner detected
    (user=%user.name
    process=%proc.name
    connection=%fd.name
    %container.info
    image=%container.image.repository)
  priority: CRITICAL
  tags: [network, mitre_impact]

- macro: net_miner_pool
  condition: >
    (fd.sport in (3333, 4444, 5555, 7777, 8888, 9999) or
     fd.dport in (3333, 4444, 5555, 7777, 8888, 9999)) and
    fd.l4proto = tcp
```

**3. Suspicious Process Execution:**

```yaml
- rule: System user interactive
  desc: System user spawned an interactive shell
  condition: >
    spawned_process and
    system_users and
    interactive and
    not user_known_system_user_login
  output: >
    System user spawned shell
    (user=%user.name
    loginuid=%user.loginuid
    process=%proc.name
    parent=%proc.pname
    terminal=%proc.tty
    %container.info)
  priority: WARNING
  tags: [users, mitre_execution]

- list: system_users
  items: [bin, daemon, games, lp, mail, nobody, sshd, sync, uucp, www-data]
```

### File System Rules

**1. Write Below /etc:**

```yaml
- rule: Write below etc
  desc: Modification of critical system files
  condition: >
    evt.type in (open, openat, openat2) and
    evt.dir = < and
    fd.name startswith /etc and
    not fd.name in (
      /etc/ld.so.cache,
      /etc/resolv.conf,
      /etc/hostname,
      /etc/hosts
    ) and
    not proc.name in (
      dpkg, rpm, yum, apt-get,
      package-cleanup, dnf
    ) and
    not container.image.repository in (allowed_images)
  output: >
    File below /etc opened for writing
    (user=%user.name
    command=%proc.cmdline
    file=%fd.name
    parent=%proc.pname
    %container.info
    image=%container.image.repository)
  priority: ERROR
  tags: [filesystem, mitre_persistence]
```

**2. Read Sensitive Files:**

```yaml
- rule: Read sensitive file
  desc: Access to sensitive files
  condition: >
    open_read and
    sensitive_files and
    not proc.name in (
      awk, cat, curl, cut, diff, grep,
      head, sed, tail, tee, wget
    ) and
    not trusted_containers
  output: >
    Sensitive file accessed
    (user=%user.name
    command=%proc.cmdline
    file=%fd.name
    parent=%proc.pname
    %container.info)
  priority: WARNING
  tags: [filesystem, mitre_credential_access]

- macro: sensitive_files
  condition: >
    fd.name in (
      /etc/shadow, /etc/sudoers,
      /etc/pam.conf, /etc/security/pwquality.conf
    ) or
    fd.name startswith /etc/sudoers.d/ or
    fd.name startswith /root/.ssh/
```

### Network Rules

**1. Outbound Connection:**

```yaml
- rule: Outbound Connection to C2 Servers
  desc: Detect outbound connections to known C2 servers
  condition: >
    outbound and
    fd.sip in (c2_server_ips) and
    not trusted_containers
  output: >
    Outbound connection to C2 server
    (user=%user.name
    process=%proc.name
    connection=%fd.name
    %container.info
    image=%container.image.repository)
  priority: CRITICAL
  tags: [network, mitre_command_and_control]

- list: c2_server_ips
  items: [
    "192.0.2.1",
    "198.51.100.1",
    "203.0.113.1"
  ]
```

**2. Unexpected Network Traffic:**

```yaml
- rule: Unexpected outbound connection destination
  desc: Container opened unexpected connection
  condition: >
    outbound and
    container and
    not allowed_outbound_destination_lists and
    not user_known_outbound_connection_destination
  output: >
    Unexpected outbound connection
    (user=%user.name
    process=%proc.name
    connection=%fd.name
    %container.info
    image=%container.image.repository)
  priority: NOTICE
  tags: [network]

- macro: allowed_outbound_destination_lists
  condition: >
    fd.snet in (
      "10.0.0.0/8",
      "172.16.0.0/12",
      "192.168.0.0/16"
    )
```

## Custom Rules

### Macros and Lists

**Lists (Reusable Values):**

```yaml
# Executable binaries
- list: shell_binaries
  items: [ash, bash, csh, ksh, sh, tcsh, zsh]

# Sensitive directories
- list: sensitive_file_names
  items: [
    /etc/shadow,
    /etc/sudoers,
    /root/.ssh/id_rsa,
    /root/.ssh/id_dsa,
    /root/.aws/credentials,
    /root/.docker/config.json
  ]

# Trusted container images
- list: trusted_images
  items: [
    gcr.io/mycompany,
    registry.company.com,
    quay.io/company
  ]
```

**Macros (Reusable Conditions):**

```yaml
# Process spawned
- macro: spawned_process
  condition: evt.type = execve and evt.dir=<

# Container context
- macro: container
  condition: container.id != host

# Shell processes
- macro: shell_procs
  condition: proc.name in (shell_binaries)

# Network connection
- macro: inbound
  condition: >
    (evt.type in (accept, listen) and evt.dir=<)

- macro: outbound
  condition: >
    (evt.type = connect and evt.dir=< and
     (fd.typechar = 4 or fd.typechar = 6) and
     (fd.ip != "0.0.0.0" and fd.net != "127.0.0.0/8"))

# File operations
- macro: open_write
  condition: >
    (evt.type in (open, openat, openat2) and
     evt.is_open_write=true and
     fd.typechar='f' and
     fd.num>=0)

- macro: open_read
  condition: >
    (evt.type in (open, openat, openat2) and
     evt.is_open_read=true and
     fd.typechar='f' and
     fd.num>=0)
```

### Application-Specific Rules

**Database Access:**

```yaml
- rule: Unauthorized Database Access
  desc: Non-database process accessing database files
  condition: >
    open_read and
    fd.name glob "/var/lib/postgresql/*/base/*" and
    not proc.name in (postgres, pg_dump, pg_basebackup) and
    not container.image.repository contains "postgres"
  output: >
    Unauthorized database file access
    (user=%user.name
    process=%proc.name
    file=%fd.name
    %container.info)
  priority: CRITICAL
  tags: [database, filesystem]
```

**Web Server:**

```yaml
- rule: Web Server Spawned Shell
  desc: Web server process spawned a shell
  condition: >
    spawned_process and
    shell_procs and
    proc.pname in (nginx, httpd, apache, apache2, tomcat, java) and
    not proc.cmdline contains "logrotate"
  output: >
    Web server spawned shell (possible webshell)
    (user=%user.name
    shell=%proc.name
    parent=%proc.pname
    cmdline=%proc.cmdline
    %container.info)
  priority: CRITICAL
  tags: [webserver, mitre_persistence, T1505]
```

**Package Manager:**

```yaml
- rule: Package Management Process in Container
  desc: Package manager executed in container
  condition: >
    spawned_process and
    container and
    proc.name in (
      apt, apt-get, yum, dnf, rpm,
      apk, pip, pip3, npm, gem
    ) and
    not user_known_package_manager_in_container
  output: >
    Package manager in container
    (user=%user.name
    process=%proc.name
    cmdline=%proc.cmdline
    %container.info
    image=%container.image.repository)
  priority: WARNING
  tags: [container, software]
```

### Compliance Rules

**PCI-DSS:**

```yaml
- rule: PCI-DSS - Cardholder Data Access
  desc: Access to files containing cardholder data
  condition: >
    open_read and
    (fd.name glob "/data/cardholder/*" or
     fd.name glob "/var/lib/payment/*") and
    not proc.name in (approved_payment_apps) and
    not user_known_cardholder_data_access
  output: >
    Cardholder data accessed
    (user=%user.name
    process=%proc.name
    file=%fd.name
    %container.info)
  priority: CRITICAL
  tags: [pci_dss, compliance]

- list: approved_payment_apps
  items: [payment-processor, vault-service]
```

**HIPAA:**

```yaml
- rule: HIPAA - PHI Data Access
  desc: Access to Protected Health Information
  condition: >
    open_read and
    fd.name glob "/data/phi/*" and
    not proc.name in (approved_healthcare_apps) and
    not user_known_phi_access
  output: >
    PHI data accessed
    (user=%user.name
    process=%proc.name
    file=%fd.name
    %container.info)
  priority: CRITICAL
  tags: [hipaa, compliance]

- list: approved_healthcare_apps
  items: [ehr-service, patient-portal, billing-system]
```

## Kubernetes Audit Rules

### Enable Kubernetes Audit

**API Server Configuration:**

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
spec:
  containers:
  - name: kube-apiserver
    command:
    - kube-apiserver
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-log-maxage=30
    - --audit-log-maxbackup=10
    - --audit-log-maxsize=100
    # For Falco consumption:
    - --audit-webhook-config-file=/etc/kubernetes/audit-webhook.yaml
    - --audit-webhook-batch-max-size=100
    - --audit-webhook-batch-max-wait=5s
```

**Audit Webhook Configuration:**

```yaml
# /etc/kubernetes/audit-webhook.yaml
apiVersion: v1
kind: Config
clusters:
- name: falco
  cluster:
    server: http://falco-k8saudit.falco.svc.cluster.local:8765/k8s-audit
contexts:
- name: default
  context:
    cluster: falco
    user: ""
current-context: default
users: []
```

### Audit Rules

**1. ConfigMap/Secret Access:**

```yaml
- rule: Sensitive K8s ConfigMap or Secret Access
  desc: Detect access to sensitive ConfigMaps or Secrets
  condition: >
    kget and
    (ka.target.resource = "configmaps" or
     ka.target.resource = "secrets") and
    ka.target.name in (sensitive_k8s_config_names) and
    not ka.user.name in (allowed_k8s_users)
  output: >
    Sensitive K8s object accessed
    (user=%ka.user.name
    verb=%ka.verb
    resource=%ka.target.resource
    name=%ka.target.name
    namespace=%ka.target.namespace)
  priority: WARNING
  tags: [k8s_audit]

- list: sensitive_k8s_config_names
  items: [
    database-credentials,
    api-keys,
    tls-certificates,
    oauth-secrets
  ]
```

**2. Role/RoleBinding Changes:**

```yaml
- rule: K8s RBAC Modification
  desc: Detect changes to RBAC resources
  condition: >
    kevt and
    ka.verb in (create, update, patch, delete) and
    ka.target.resource in (
      roles, rolebindings,
      clusterroles, clusterrolebindings
    ) and
    not ka.user.name in (trusted_k8s_admins)
  output: >
    K8s RBAC resource modified
    (user=%ka.user.name
    verb=%ka.verb
    resource=%ka.target.resource
    name=%ka.target.name
    namespace=%ka.target.namespace)
  priority: WARNING
  tags: [k8s_audit, rbac]
```

**3. Exec into Pod:**

```yaml
- rule: Exec into Container
  desc: Detect kubectl exec into container
  condition: >
    kevt_started and
    ka.verb = create and
    ka.uri.param contains "exec"
  output: >
    Exec into container
    (user=%ka.user.name
    pod=%ka.target.name
    namespace=%ka.target.namespace
    command=%ka.uri.param)
  priority: NOTICE
  tags: [k8s_audit, exec]
```

**4. Privileged Pod Creation:**

```yaml
- rule: Create Privileged Pod
  desc: Detect creation of privileged pod
  condition: >
    kevt and
    ka.verb = create and
    ka.target.resource = pods and
    ka.req.pod.containers.privileged = true
  output: >
    Privileged pod created
    (user=%ka.user.name
    pod=%ka.target.name
    namespace=%ka.target.namespace
    image=%ka.req.pod.containers.image)
  priority: WARNING
  tags: [k8s_audit, privileged]
```

## Alert Routing

### Falco Sidekick

**Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: falco-sidekick
  namespace: falco
spec:
  replicas: 2
  selector:
    matchLabels:
      app: falco-sidekick
  template:
    metadata:
      labels:
        app: falco-sidekick
    spec:
      containers:
      - name: sidekick
        image: falcosecurity/falcosidekick:2.28.0
        env:
        # Slack
        - name: SLACK_WEBHOOKURL
          valueFrom:
            secretKeyRef:
              name: falco-sidekick-secrets
              key: slack-webhook
        - name: SLACK_MINIMUMPRIORITY
          value: "warning"

        # PagerDuty
        - name: PAGERDUTY_INTEGRATIONKEY
          valueFrom:
            secretKeyRef:
              name: falco-sidekick-secrets
              key: pagerduty-key
        - name: PAGERDUTY_MINIMUMPRIORITY
          value: "critical"

        # Elasticsearch
        - name: ELASTICSEARCH_HOSTPORT
          value: "elasticsearch:9200"
        - name: ELASTICSEARCH_INDEX
          value: "falco"
        - name: ELASTICSEARCH_MINIMUMPRIORITY
          value: "notice"

        # AWS SNS
        - name: AWS_SNS_TOPICARN
          value: "arn:aws:sns:us-east-1:123456789:falco-alerts"
        - name: AWS_SNS_MINIMUMPRIORITY
          value: "warning"

        ports:
        - containerPort: 2801
---
apiVersion: v1
kind: Service
metadata:
  name: falco-sidekick
  namespace: falco
spec:
  selector:
    app: falco-sidekick
  ports:
  - port: 2801
    targetPort: 2801
```

**Falco Configuration:**

```yaml
# falco.yaml
json_output: true
json_include_output_property: true
http_output:
  enabled: true
  url: "http://falco-sidekick:2801/"
```

### Custom Webhook

**Response Server Example (Python):**

```python
from flask import Flask, request
import json
import logging

app = Flask(__name__)

@app.route('/alerts', methods=['POST'])
def handle_alert():
    alert = request.json

    priority = alert.get('priority')
    rule = alert.get('rule')
    output = alert.get('output')

    # Log alert
    logging.warning(f"Falco Alert: {rule} - {output}")

    # Critical alerts
    if priority in ['CRITICAL', 'EMERGENCY']:
        # Create incident
        create_pagerduty_incident(alert)

        # Auto-remediate
        if rule == "Reverse Shell":
            kill_container(alert['output_fields']['container.id'])

    # High priority
    elif priority in ['ERROR', 'WARNING']:
        # Send to Slack
        send_slack_alert(alert)

    # All alerts to SIEM
    send_to_siem(alert)

    return {'status': 'ok'}, 200

def kill_container(container_id):
    """Kill malicious container"""
    import subprocess
    subprocess.run(['docker', 'kill', container_id])
    logging.info(f"Killed container {container_id}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Response Automation

### FalcoSidekick Response

**Kubernetes Response Engine:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: falcosidekick-kubeless
  namespace: falco
spec:
  replicas: 1
  selector:
    matchLabels:
      app: falcosidekick-kubeless
  template:
    spec:
      serviceAccountName: falcosidekick-kubeless
      containers:
      - name: kubeless
        image: falcosecurity/falcosidekick-kubeless:latest
        env:
        - name: FALCOSIDEKICK_KUBELESS_KUBECONFIG
          value: "/var/run/secrets/kubernetes.io/serviceaccount/token"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: falcosidekick-kubeless
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "delete"]
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: falcosidekick-kubeless
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: falcosidekick-kubeless
subjects:
- kind: ServiceAccount
  name: falcosidekick-kubeless
  namespace: falco
```

**Response Functions:**

```yaml
# Delete pod on critical alert
apiVersion: v1
kind: ConfigMap
metadata:
  name: response-functions
  namespace: falco
data:
  delete-pod.js: |
    const k8s = require('@kubernetes/client-node');

    module.exports = async (event, context) => {
      const alert = JSON.parse(event.data);

      if (alert.priority === 'CRITICAL') {
        const kc = new k8s.KubeConfig();
        kc.loadFromCluster();
        const k8sApi = kc.makeApiClient(k8s.CoreV1Api);

        const namespace = alert.output_fields['k8s.ns.name'];
        const pod = alert.output_fields['k8s.pod.name'];

        await k8sApi.deleteNamespacedPod(pod, namespace);
        console.log(`Deleted pod ${namespace}/${pod}`);
      }

      return { status: 'ok' };
    };
```

## Tuning and Optimization

### Rule Tuning

**Disable Noisy Rules:**

```yaml
# custom-rules.yaml
- rule: Terminal shell in container
  enabled: false

# Or append condition to exclude known cases
- rule: Terminal shell in container
  append: true
  condition: and not container.image.repository in (debug_images)

- list: debug_images
  items: [
    gcr.io/mycompany/debug,
    nicolaka/netshoot
  ]
```

**Adjust Priority:**

```yaml
# Override priority
- rule: Write below etc
  override:
    enabled: true
  priority: WARNING  # Changed from ERROR
```

**Add Exceptions:**

```yaml
# Add exception macro
- macro: user_expected_terminal_shell_in_container_conditions
  condition: >
    (container.image.repository = "gcr.io/mycompany/ops-tools" or
     k8s.ns.name = "development")

# Exception for specific users
- macro: user_known_system_user_login
  condition: user.name in (sysadmin, operator)
```

### Performance Optimization

**1. Rule Optimization:**

```yaml
# Bad: Multiple string comparisons
condition: >
  proc.name != "systemd" and
  proc.name != "dockerd" and
  proc.name != "containerd" and
  proc.name != "kubelet"

# Good: Use list
condition: not proc.name in (system_processes)

- list: system_processes
  items: [systemd, dockerd, containerd, kubelet]
```

**2. Event Dropping:**

```yaml
# /etc/falco/falco.yaml
syscall_event_drops:
  actions:
    - ignore  # or log, alert
  rate: 0.03333
  max_burst: 1

# Drop less important events
syscall_event_timeouts:
  max_consecutives: 1000
```

**3. Buffering:**

```yaml
# Increase buffer size
syscall_buf_size_preset: 8  # 1-8, higher = more memory
```

**4. Sampling:**

```yaml
# Sample events (not recommended for security)
base_syscalls:
  repair: false
  custom_set: []
```

### Monitoring Falco

**Prometheus Metrics:**

```yaml
# Falco exporter
apiVersion: apps/v1
kind: Deployment
metadata:
  name: falco-exporter
  namespace: falco
spec:
  replicas: 1
  selector:
    matchLabels:
      app: falco-exporter
  template:
    spec:
      containers:
      - name: exporter
        image: falcosecurity/falco-exporter:latest
        ports:
        - containerPort: 9376
          name: metrics
---
apiVersion: v1
kind: Service
metadata:
  name: falco-exporter
  namespace: falco
  labels:
    app: falco-exporter
spec:
  ports:
  - port: 9376
    name: metrics
  selector:
    app: falco-exporter
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: falco
  namespace: falco
spec:
  selector:
    matchLabels:
      app: falco-exporter
  endpoints:
  - port: metrics
```

**Key Metrics:**

```promql
# Alert rate
rate(falco_events_total[5m])

# Alerts by priority
sum by (priority) (falco_events_total)

# Dropped events
falco_events_dropped_total

# Rule evaluation latency
falco_rule_execution_duration_seconds
```

## References

- [Falco Documentation](https://falco.org/docs/)
- [Falco Rules Repository](https://github.com/falcosecurity/rules)
- [Falco Sidekick](https://github.com/falcosecurity/falcosidekick)
- [Falco Exporter](https://github.com/falcosecurity/falco-exporter)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
