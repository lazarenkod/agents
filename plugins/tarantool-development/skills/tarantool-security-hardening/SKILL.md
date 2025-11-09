---
name: tarantool-security-hardening
description: Master Tarantool security hardening with authentication, authorization, TLS/SSL encryption, network security, data protection, and compliance best practices. Use when securing production deployments, implementing access controls, or meeting security requirements.
---

# Tarantool Security & Hardening

Complete guide to securing Tarantool databases with authentication, encryption, access control, and security best practices.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Implement defense-in-depth security for Tarantool databases to protect data confidentiality, integrity, and availability.

## When to Use This Skill

- Secure production deployments
- Implement user authentication
- Configure role-based access control (RBAC)
- Enable TLS/SSL encryption
- Harden network security
- Encrypt sensitive data
- Implement audit logging
- Meet compliance requirements (GDPR, HIPAA, PCI-DSS)
- Perform security assessments

## Core Concepts

### Authentication

**User Management**
```lua
-- Create admin user
box.schema.user.create('admin', {
    password = 'secure_password_here',
    if_not_exists = true
})

-- Grant all privileges
box.schema.user.grant('admin', 'read,write,execute', 'universe')

-- Create application user with limited privileges
box.schema.user.create('app_user', {
    password = 'app_password',
    if_not_exists = true
})

-- Grant specific space access
box.schema.user.grant('app_user', 'read,write', 'space', 'users')
box.schema.user.grant('app_user', 'read', 'space', 'products')

-- Create read-only user
box.schema.user.create('readonly_user', {
    password = 'readonly_password',
    if_not_exists = true
})

box.schema.user.grant('readonly_user', 'read', 'universe')
```

**Password Policy Enforcement**
```lua
local auth_module = {}

function auth_module.validate_password(password)
    -- Minimum length
    if #password < 12 then
        return false, "Password must be at least 12 characters"
    end

    -- Complexity requirements
    local has_upper = password:match("%u")
    local has_lower = password:match("%l")
    local has_digit = password:match("%d")
    local has_special = password:match("[^%w]")

    if not (has_upper and has_lower and has_digit and has_special) then
        return false, "Password must contain uppercase, lowercase, digit, and special character"
    end

    return true
end

function auth_module.create_user_secure(username, password)
    local valid, err = auth_module.validate_password(password)
    if not valid then
        error(err)
    end

    -- Hash password (use bcrypt or similar in production)
    local digest = require('digest')
    local salt = digest.urandom(16)
    local hashed = digest.pbkdf2(password, salt, 10000)

    box.schema.user.create(username, {
        password = digest.base64_encode(hashed)
    })

    -- Store password metadata
    box.space.user_credentials:insert{
        username,
        salt,
        os.time(),  -- created_at
        nil         -- last_changed
    }
end

return auth_module
```

**Multi-Factor Authentication (MFA)**
```lua
local mfa = {}

function mfa.generate_totp_secret()
    local digest = require('digest')
    return digest.base32_encode(digest.urandom(20))
end

function mfa.verify_totp(secret, token)
    local totp = require('totp')  -- External TOTP library
    return totp.verify(secret, token, {
        window = 1,  -- Allow 1 step before/after
        time_step = 30
    })
end

function mfa.login_with_mfa(username, password, totp_token)
    -- Verify password
    local user = box.space.users.index.username:get{username}
    if not user or not verify_password(password, user.password_hash) then
        return false, "Invalid credentials"
    end

    -- Verify TOTP
    if not mfa.verify_totp(user.totp_secret, totp_token) then
        return false, "Invalid MFA token"
    end

    -- Generate session token
    local session_token = generate_secure_token()
    box.space.sessions:insert{
        session_token,
        user.id,
        os.time() + 3600  -- 1 hour expiry
    }

    return true, session_token
end

return mfa
```

### Authorization & RBAC

**Role-Based Access Control**
```lua
-- Define roles
box.schema.role.create('developer', {if_not_exists = true})
box.schema.role.create('analyst', {if_not_exists = true})
box.schema.role.create('operator', {if_not_exists = true})

-- Developer role: full CRUD on development spaces
box.schema.role.grant('developer', 'read,write,execute', 'space', 'users')
box.schema.role.grant('developer', 'read,write,execute', 'space', 'orders')
box.schema.role.grant('developer', 'create', 'space')

-- Analyst role: read-only access
box.schema.role.grant('analyst', 'read', 'space', 'users')
box.schema.role.grant('analyst', 'read', 'space', 'orders')
box.schema.role.grant('analyst', 'execute', 'function', 'analytics.*')

-- Operator role: limited operational access
box.schema.role.grant('operator', 'read', 'space', '_space')
box.schema.role.grant('operator', 'execute', 'function', 'health_check')

-- Assign roles to users
box.schema.user.grant('alice', 'developer')
box.schema.user.grant('bob', 'analyst')
box.schema.user.grant('charlie', 'operator')
```

**Function-Level Access Control**
```lua
local access_control = {}

function access_control.require_role(required_role)
    return function(fn)
        return function(...)
            local session = box.session.su('admin', function()
                return box.session.user()
            end)

            -- Check if user has required role
            local has_role = false
            for _, role in pairs(box.schema.user.info(session).roles) do
                if role == required_role then
                    has_role = true
                    break
                end
            end

            if not has_role then
                error(string.format("Access denied: requires role '%s'", required_role))
            end

            return fn(...)
        end
    end
end

-- Usage: protect sensitive functions
function delete_user(user_id)
    box.space.users:delete{user_id}
end

-- Wrap function with access control
delete_user = access_control.require_role('admin')(delete_user)
```

**Row-Level Security**
```lua
local rls = {}

function rls.filter_by_user(space_name, user_id)
    local space = box.space[space_name]
    local results = {}

    for _, tuple in space:pairs() do
        -- Only return rows owned by user
        if tuple.owner_id == user_id then
            table.insert(results, tuple)
        end
    end

    return results
end

-- Apply RLS to queries
function get_user_orders(user_id)
    local session_user = box.session.user()

    -- Regular users can only see their own orders
    if not has_role(session_user, 'admin') then
        return rls.filter_by_user('orders', session_user.id)
    end

    -- Admins see all orders
    return box.space.orders:select{user_id}
end
```

### TLS/SSL Encryption

**Server-Side TLS Configuration**
```lua
box.cfg{
    listen = {
        uri = '0.0.0.0:3301',
        params = {
            transport = 'ssl',
            ssl_key_file = '/etc/tarantool/certs/server-key.pem',
            ssl_cert_file = '/etc/tarantool/certs/server-cert.pem',
            ssl_ca_file = '/etc/tarantool/certs/ca-cert.pem',
            ssl_ciphers = 'HIGH:!aNULL:!MD5',  -- Strong ciphers only
            ssl_password = 'key_password'
        }
    }
}
```

**Client-Side TLS Connection**
```lua
local net_box = require('net.box')

local conn = net_box.connect({
    uri = 'username:password@host:3301',
    params = {
        transport = 'ssl',
        ssl_key_file = '/etc/tarantool/certs/client-key.pem',
        ssl_cert_file = '/etc/tarantool/certs/client-cert.pem',
        ssl_ca_file = '/etc/tarantool/certs/ca-cert.pem',
        ssl_verify_mode = 'peer',  -- Verify server certificate
        ssl_server_name = 'tarantool.example.com'
    }
})
```

**Certificate Generation (Development)**
```bash
# Generate CA private key and certificate
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -out ca-cert.pem

# Generate server private key and CSR
openssl genrsa -out server-key.pem 4096
openssl req -new -key server-key.pem -out server.csr

# Sign server certificate with CA
openssl x509 -req -days 365 -in server.csr -CA ca-cert.pem \
  -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

# Generate client certificates (similar process)
openssl genrsa -out client-key.pem 4096
openssl req -new -key client-key.pem -out client.csr
openssl x509 -req -days 365 -in client.csr -CA ca-cert.pem \
  -CAkey ca-key.pem -set_serial 02 -out client-cert.pem
```

### Data Encryption

**Encryption at Rest**
```lua
local crypto = require('crypto')

local encryption = {}

-- Encryption configuration
encryption.config = {
    algorithm = 'aes256',
    mode = 'cbc',
    key = os.getenv('ENCRYPTION_KEY')  -- Store securely
}

function encryption.encrypt_field(plaintext)
    local cipher = crypto.cipher.aes256.cbc.encrypt
    local iv = crypto.rand.bytes(16)  -- Random IV

    local encrypted = cipher(plaintext, encryption.config.key, iv)

    -- Return IV + encrypted data (both base64 encoded)
    local digest = require('digest')
    return digest.base64_encode(iv) .. ':' .. digest.base64_encode(encrypted)
end

function encryption.decrypt_field(ciphertext)
    local digest = require('digest')
    local parts = string.split(ciphertext, ':')

    local iv = digest.base64_decode(parts[1])
    local encrypted = digest.base64_decode(parts[2])

    local cipher = crypto.cipher.aes256.cbc.decrypt
    return cipher(encrypted, encryption.config.key, iv)
end

-- Usage: encrypt sensitive fields
function store_credit_card(user_id, card_number)
    local encrypted = encryption.encrypt_field(card_number)

    box.space.payment_methods:insert{
        user_id,
        encrypted,
        os.time()
    }
end

return encryption
```

**Field-Level Encryption with Key Rotation**
```lua
local encryption_v2 = {}

function encryption_v2.encrypt_with_version(plaintext, key_version)
    local key = get_encryption_key(key_version)
    local encrypted = encrypt_aes(plaintext, key)

    -- Prepend key version to ciphertext
    return string.format('v%d:%s', key_version, encrypted)
end

function encryption_v2.decrypt_with_version(ciphertext)
    -- Extract key version
    local version, encrypted = ciphertext:match('^v(%d+):(.+)$')
    version = tonumber(version)

    local key = get_encryption_key(version)
    return decrypt_aes(encrypted, key)
end

-- Key rotation process
function encryption_v2.rotate_keys(space_name, field_name)
    local space = box.space[space_name]
    local current_version = get_current_key_version()

    for _, tuple in space:pairs() do
        local encrypted_value = tuple[field_name]

        -- Decrypt with old key
        local plaintext = encryption_v2.decrypt_with_version(encrypted_value)

        -- Re-encrypt with new key
        local new_encrypted = encryption_v2.encrypt_with_version(
            plaintext,
            current_version
        )

        -- Update tuple
        space:update(tuple[1], {{'=', field_name, new_encrypted}})
    end
end

return encryption_v2
```

### Network Security

**IP Whitelisting**
```lua
local security = {}

security.allowed_ips = {
    '10.0.0.0/8',       -- Private network
    '172.16.0.0/12',    -- Private network
    '192.168.1.100',    -- Specific host
}

function security.is_ip_allowed(ip)
    for _, allowed in ipairs(security.allowed_ips) do
        if security.ip_in_cidr(ip, allowed) then
            return true
        end
    end
    return false
end

function security.ip_in_cidr(ip, cidr)
    -- Simple CIDR matching (use proper library in production)
    if not cidr:match('/') then
        return ip == cidr
    end
    -- Implement CIDR matching logic
    return false  -- Placeholder
end

-- Apply on connection
box.session.on_connect(function()
    local peer = box.session.peer()
    local ip = peer:match('([^:]+)')

    if not security.is_ip_allowed(ip) then
        log.warn('Blocked connection from ' .. ip)
        box.session.su('admin', function()
            box.session.close()
        end)
    end
end)

return security
```

**Rate Limiting**
```lua
local rate_limiter = {}

rate_limiter.limits = {}  -- {user_id -> {count, window_start}}

function rate_limiter.check_limit(user_id, max_requests, window_seconds)
    local now = fiber.time()
    local limit_info = rate_limiter.limits[user_id]

    if not limit_info or (now - limit_info.window_start) > window_seconds then
        -- New window
        rate_limiter.limits[user_id] = {
            count = 1,
            window_start = now
        }
        return true
    end

    if limit_info.count >= max_requests then
        return false, "Rate limit exceeded"
    end

    limit_info.count = limit_info.count + 1
    return true
end

-- Apply to functions
function create_order_rate_limited(user_id, order_data)
    local allowed, err = rate_limiter.check_limit(user_id, 100, 60)
    if not allowed then
        error(err)
    end

    return create_order(order_data)
end

return rate_limiter
```

### Audit Logging

**Comprehensive Audit Trail**
```lua
local audit = {}

function audit.init()
    box.schema.space.create('audit_log', {
        if_not_exists = true,
        format = {
            {name = 'id', type = 'unsigned'},
            {name = 'timestamp', type = 'number'},
            {name = 'user', type = 'string'},
            {name = 'action', type = 'string'},
            {name = 'resource', type = 'string'},
            {name = 'result', type = 'string'},
            {name = 'ip_address', type = 'string'},
            {name = 'details', type = 'string'}  -- JSON
        }
    })

    box.space.audit_log:create_index('primary', {
        parts = {'id'},
        sequence = 'audit_log_seq'
    })

    box.space.audit_log:create_index('timestamp', {
        parts = {'timestamp'},
        unique = false
    })
end

function audit.log(action, resource, result, details)
    local user = box.session.user()
    local peer = box.session.peer()
    local ip = peer and peer:match('([^:]+)') or 'unknown'

    box.space.audit_log:insert{
        nil,  -- Auto-increment
        fiber.time(),
        user,
        action,
        resource,
        result,
        ip,
        require('json').encode(details or {})
    }
end

-- Wrapper for audited operations
function audit.wrap(fn, action, resource)
    return function(...)
        local ok, result = pcall(fn, ...)

        audit.log(
            action,
            resource,
            ok and 'SUCCESS' or 'FAILURE',
            {error = not ok and result or nil}
        )

        if not ok then
            error(result)
        end

        return result
    end
end

-- Usage
delete_user = audit.wrap(delete_user, 'DELETE', 'users')

return audit
```

## Security Patterns

### Pattern 1: Defense in Depth

```
Layer 1: Network (Firewall, VPN)
         ↓
Layer 2: TLS Encryption
         ↓
Layer 3: Authentication (Password + MFA)
         ↓
Layer 4: Authorization (RBAC)
         ↓
Layer 5: Data Encryption (at rest)
         ↓
Layer 6: Audit Logging
```

### Pattern 2: Least Privilege Principle

```lua
-- Create minimal permission sets
function create_application_user(app_name)
    local username = 'app_' .. app_name

    box.schema.user.create(username, {
        password = generate_secure_password()
    })

    -- Only grant what's needed
    box.schema.user.grant(username, 'read', 'space', app_name .. '_data')
    box.schema.user.grant(username, 'write', 'space', app_name .. '_data')

    -- No admin privileges, no universe access
end
```

### Pattern 3: Secrets Management

```lua
-- Never hardcode secrets
local secrets = {}

function secrets.load_from_vault()
    -- Use HashiCorp Vault, AWS Secrets Manager, etc.
    local vault = require('vault_client')

    return {
        db_password = vault.get('tarantool/db_password'),
        encryption_key = vault.get('tarantool/encryption_key'),
        api_key = vault.get('tarantool/api_key')
    }
end

-- Use environment variables as fallback
function secrets.get(key)
    local vault_secrets = secrets.load_from_vault()
    return vault_secrets[key] or os.getenv(key:upper())
end
```

## Best Practices

1. **Authentication**
   - Use strong password policies (12+ chars, complexity)
   - Implement MFA for admin accounts
   - Rotate credentials regularly
   - Use secure password hashing (bcrypt, argon2)

2. **Authorization**
   - Apply principle of least privilege
   - Use RBAC for permission management
   - Implement row-level security for multi-tenant
   - Audit permission changes

3. **Network Security**
   - Always use TLS in production
   - Implement IP whitelisting
   - Use VPN for administrative access
   - Isolate database network

4. **Data Protection**
   - Encrypt sensitive data at rest
   - Use TLS for data in transit
   - Implement key rotation
   - Secure key storage (HSM, vault)

5. **Monitoring**
   - Log all authentication attempts
   - Alert on failed logins
   - Monitor privilege escalation
   - Track data access patterns

## Common Pitfalls

- **Default Credentials**: Change default 'guest' user password
- **Unencrypted Connections**: Always use TLS in production
- **Overly Permissive**: Don't grant 'universe' to app users
- **Secrets in Code**: Use vault or environment variables
- **Missing Audit Logs**: Enable comprehensive logging
- **Weak Passwords**: Enforce strong password policies
- **No MFA**: Critical for admin accounts

## Related Skills

- `tarantool-architecture` - Security architecture design
- `lua-development` - Implementing security modules
- `tarantool-monitoring-observability` - Security monitoring
- `cartridge-framework` - Cluster security
- `compliance-frameworks` - GDPR, HIPAA, PCI-DSS

## References

- [Tarantool Security](https://www.tarantool.io/en/doc/latest/book/admin/security/)
- [Access Control](https://www.tarantool.io/en/doc/latest/book/box/authentication/)
- [TLS Configuration](https://www.tarantool.io/en/doc/latest/book/admin/ssl/)
- [OWASP Database Security](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)
