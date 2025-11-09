---
name: tarantool-migration-strategies
description: Master Tarantool database migrations, zero-downtime schema evolution, data transformations, version management, and rollback procedures. Use when implementing database migrations, evolving schemas, or managing data transformations in production.
---

# Tarantool Migration Strategies

Complete guide to implementing safe, zero-downtime migrations and schema evolution in Tarantool databases.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Implement safe, reversible database migrations that evolve schemas and transform data without downtime or data loss.

## When to Use This Skill

- Implement schema changes in production
- Migrate data between formats or structures
- Add, modify, or remove indexes
- Change space formats or data types
- Manage migration versioning
- Plan rollback strategies
- Execute zero-downtime deployments
- Coordinate migrations across clusters

## Core Concepts

### Migration Framework Architecture

**Migration Module Structure**
```lua
local migrations = {
    version = 0,
    registry = {}
}

function migrations.register(version, up, down)
    table.insert(migrations.registry, {
        version = version,
        up = up,
        down = down
    })
end

function migrations.get_current_version()
    local schema_space = box.space._schema
    local version_tuple = schema_space:get{'schema_version'}
    return version_tuple and version_tuple[2] or 0
end

function migrations.set_version(version)
    box.space._schema:replace{'schema_version', version}
end

function migrations.migrate_to(target_version)
    local current = migrations.get_current_version()

    if target_version > current then
        -- Migrate up
        for _, migration in ipairs(migrations.registry) do
            if migration.version > current and migration.version <= target_version then
                log.info('Applying migration %d', migration.version)
                migration.up()
                migrations.set_version(migration.version)
            end
        end
    elseif target_version < current then
        -- Migrate down (rollback)
        for i = #migrations.registry, 1, -1 do
            local migration = migrations.registry[i]
            if migration.version <= current and migration.version > target_version then
                log.info('Rolling back migration %d', migration.version)
                migration.down()
                migrations.set_version(migration.version - 1)
            end
        end
    end
end

return migrations
```

### Zero-Downtime Schema Evolution

**Phase 1: Add New Fields (Backward Compatible)**
```lua
migrations.register(1, function()
    -- Add new optional field without affecting existing data
    local users = box.space.users

    -- Extend format with new field
    users:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'phone', type = 'string', is_nullable = true},  -- New field
        {name = 'created_at', type = 'integer'}
    })

    -- No data transformation needed - new field is nullable
end, function()
    -- Rollback: remove new field from format
    local users = box.space.users
    users:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'created_at', type = 'integer'}
    })
end)
```

**Phase 2: Data Backfill (Populate New Fields)**
```lua
migrations.register(2, function()
    local users = box.space.users
    local batch_size = 1000
    local processed = 0

    -- Backfill in batches to avoid long transactions
    for _, tuple in users:pairs(nil, {iterator = box.index.ALL}) do
        if tuple.phone == nil then
            local new_tuple = tuple:transform(4, 0, '')  -- Add empty phone
            users:replace(new_tuple)
        end

        processed = processed + 1
        if processed % batch_size == 0 then
            fiber.yield()  -- Allow other operations
        end
    end
end, function()
    -- Rollback: set phone to nil
    local users = box.space.users
    for _, tuple in users:pairs() do
        local new_tuple = tuple:transform(4, 1, box.NULL)
        users:replace(new_tuple)
    end
end)
```

**Phase 3: Make Field Required**
```lua
migrations.register(3, function()
    local users = box.space.users

    -- Now make phone field non-nullable
    users:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'phone', type = 'string', is_nullable = false},
        {name = 'created_at', type = 'integer'}
    })
end, function()
    local users = box.space.users
    users:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'phone', type = 'string', is_nullable = true},
        {name = 'created_at', type = 'integer'}
    })
end)
```

### Index Migrations

**Adding Indexes (Safe Operation)**
```lua
migrations.register(4, function()
    local users = box.space.users

    -- Add secondary index on phone
    users:create_index('phone', {
        parts = {'phone'},
        unique = false,
        if_not_exists = true
    })
end, function()
    local users = box.space.users
    users.index.phone:drop()
end)
```

**Changing Index Structure (Requires Rebuild)**
```lua
migrations.register(5, function()
    local orders = box.space.orders

    -- Change from single-field to composite index
    local old_index = orders.index.user_id
    if old_index then
        old_index:drop()
    end

    orders:create_index('user_created', {
        parts = {
            {field = 'user_id', type = 'unsigned'},
            {field = 'created_at', type = 'integer'}
        },
        unique = false
    })
end, function()
    local orders = box.space.orders

    orders.index.user_created:drop()
    orders:create_index('user_id', {
        parts = {'user_id'},
        unique = false
    })
end)
```

### Data Transformations

**Type Migration (String to Number)**
```lua
migrations.register(6, function()
    local products = box.space.products
    local fiber = require('fiber')

    -- Step 1: Add new field with correct type
    products:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'price_old', type = 'string'},
        {name = 'price', type = 'number', is_nullable = true}
    })

    -- Step 2: Transform data
    local batch_size = 500
    local processed = 0

    for _, tuple in products:pairs() do
        local price_num = tonumber(tuple.price_old)
        local updated = tuple:update{{'=', 4, price_num}}
        products:replace(updated)

        processed = processed + 1
        if processed % batch_size == 0 then
            fiber.yield()
        end
    end

    -- Step 3: Remove old field (in next migration)
end, function()
    local products = box.space.products

    -- Rollback: remove new field
    products:format({
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'price_old', type = 'string'}
    })
end)
```

**Denormalization Migration**
```lua
migrations.register(7, function()
    local orders = box.space.orders
    local users = box.space.users

    -- Add denormalized user_name to orders
    orders:format({
        {name = 'id', type = 'unsigned'},
        {name = 'user_id', type = 'unsigned'},
        {name = 'user_name', type = 'string', is_nullable = true},
        {name = 'amount', type = 'number'},
        {name = 'created_at', type = 'integer'}
    })

    -- Backfill user names
    for _, order in orders:pairs() do
        local user = users:get{order.user_id}
        if user then
            local updated = order:update{{'=', 3, user.name}}
            orders:replace(updated)
        end
    end
end, function()
    local orders = box.space.orders

    orders:format({
        {name = 'id', type = 'unsigned'},
        {name = 'user_id', type = 'unsigned'},
        {name = 'amount', type = 'number'},
        {name = 'created_at', type = 'integer'}
    })
end)
```

### Version Management

**Migration Metadata Tracking**
```lua
local migration_tracker = {}

function migration_tracker.init()
    box.schema.space.create('_migrations', {
        if_not_exists = true,
        format = {
            {name = 'version', type = 'unsigned'},
            {name = 'name', type = 'string'},
            {name = 'applied_at', type = 'integer'},
            {name = 'status', type = 'string'},
            {name = 'error', type = 'string', is_nullable = true}
        }
    })

    box.space._migrations:create_index('primary', {
        parts = {'version'},
        if_not_exists = true
    })
end

function migration_tracker.record_migration(version, name, status, error)
    box.space._migrations:replace{
        version,
        name,
        fiber.time64(),
        status,
        error
    }
end

function migration_tracker.is_applied(version)
    local record = box.space._migrations:get{version}
    return record ~= nil and record.status == 'success'
end

return migration_tracker
```

## Migration Patterns

### Pattern 1: Expand-Contract Pattern

**Expand Phase: Add New Structure**
```lua
-- Migration 1: Add new field/structure
migrations.register(10, function()
    box.space.users:format({
        -- existing fields...
        {name = 'address_json', type = 'string', is_nullable = true}  -- New
    })
end, rollback_fn)
```

**Dual-Write Phase: Write to Both**
```lua
-- Application code writes to both old and new fields
function update_user_address(user_id, address)
    local user = box.space.users:get{user_id}
    user:update{
        {'=', 'address', address.street},  -- Old field
        {'=', 'address_json', json.encode(address)}  -- New field
    }
end
```

**Contract Phase: Remove Old Structure**
```lua
-- Migration 2: Remove old field
migrations.register(11, function()
    box.space.users:format({
        -- existing fields...
        {name = 'address_json', type = 'string'}  -- Old field removed
    })
end, rollback_fn)
```

### Pattern 2: Online Index Rebuild

```lua
migrations.register(12, function()
    local users = box.space.users
    local fiber = require('fiber')

    -- Create new index with different name first
    users:create_index('email_v2', {
        parts = {'email'},
        unique = true,
        if_not_exists = true
    })

    -- Wait for index to build (asynchronous)
    while users.index.email_v2:len() < users:len() do
        fiber.sleep(0.1)
    end

    -- Drop old index
    users.index.email:drop()

    -- Rename new index
    users.index.email_v2:rename('email')
end, function()
    -- Rollback logic
end)
```

### Pattern 3: Feature Toggles for Migrations

```lua
local feature_flags = {
    use_new_schema = false
}

function get_user(user_id)
    local user = box.space.users:get{user_id}

    if feature_flags.use_new_schema then
        -- Use new schema fields
        return {
            id = user.id,
            name = user.name,
            contact = json.decode(user.contact_json)
        }
    else
        -- Use old schema fields
        return {
            id = user.id,
            name = user.name,
            email = user.email,
            phone = user.phone
        }
    end
end
```

## Best Practices

1. **Always Use Transactions**
   - Wrap migrations in atomic transactions
   - Use `box.begin()` and `box.commit()`
   - Handle errors with `box.rollback()`

2. **Batch Large Operations**
   - Process data in chunks (1000-10000 records)
   - Use `fiber.yield()` to avoid blocking
   - Monitor memory usage during backfills

3. **Test Migrations**
   - Test both up and down migrations
   - Verify data integrity after migration
   - Test rollback procedures
   - Use staging environments

4. **Version Control**
   - Sequential version numbers
   - Never skip versions
   - Document migration purpose
   - Track applied migrations

5. **Zero-Downtime Deployments**
   - Use expand-contract pattern
   - Deploy in phases
   - Maintain backward compatibility
   - Use feature flags

6. **Monitoring**
   - Log migration start/completion
   - Track migration duration
   - Monitor replication lag
   - Alert on failures

## Common Pitfalls

- **Long-Running Migrations**: Block other operations, break into batches
- **Forgetting Rollbacks**: Always implement down migrations
- **Breaking Backward Compatibility**: Use expand-contract pattern
- **Insufficient Testing**: Test on production-like data volumes
- **Ignoring Replication**: Migrations must work on replicas
- **Memory Exhaustion**: Large backfills can exhaust memory
- **Lock Contention**: Migrations can block reads/writes

## Related Skills

- `tarantool-architecture` - Understanding space and index design
- `lua-development` - Lua programming for migrations
- `tarantool-performance` - Optimizing migration performance
- `tarantool-monitoring-observability` - Monitoring migration progress
- `cartridge-framework` - Cluster-wide migration coordination

## References

- [Tarantool Schema Management](https://www.tarantool.io/en/doc/latest/book/box/data_model/)
- [Space Format API](https://www.tarantool.io/en/doc/latest/reference/reference_lua/box_space/format/)
- [Migrations Best Practices](https://www.tarantool.io/en/doc/latest/book/admin/upgrades/)
