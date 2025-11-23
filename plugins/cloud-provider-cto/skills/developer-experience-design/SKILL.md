---
name: developer-experience-design
description: Дизайн developer experience для облачных платформ. Use when designing APIs, creating SDKs, building developer portals, or improving developer productivity.
---

# Developer Experience Design

## Когда использовать

- Проектирование developer-friendly APIs
- Создание SDK и CLI tools
- Построение developer portals
- Improving developer productivity
- Gathering developer feedback

## API Design Principles

### RESTful Best Practices

```yaml
# Good API Design

GET /api/v1/servers
  - List all servers
  - Pagination: ?page=1&per_page=20
  - Filtering: ?status=running&region=us-east-1
  - Sorting: ?sort=created_at:desc

POST /api/v1/servers
  - Create new server
  - Body: {"name": "web-01", "instance_type": "m5.large"}

GET /api/v1/servers/{id}
  - Get server details

PUT /api/v1/servers/{id}
  - Full update

PATCH /api/v1/servers/{id}
  - Partial update

DELETE /api/v1/servers/{id}
  - Delete server

# Actions via POST
POST /api/v1/servers/{id}/start
POST /api/v1/servers/{id}/stop
POST /api/v1/servers/{id}/reboot
```

### Error Handling

```json
{
  "error": {
    "code": "INSUFFICIENT_QUOTA",
    "message": "You have exceeded your instance quota",
    "details": {
      "current": 10,
      "limit": 10,
      "requested": 1
    },
    "documentation_url": "https://docs.example.com/errors/quota",
    "request_id": "req_abc123"
  }
}
```

## SDK Development

```python
# Python SDK Example
class CloudClient:
    """User-friendly Python SDK"""

    def __init__(self, api_key):
        self.api_key = api_key

    def create_server(
        self,
        name,
        instance_type,
        region='us-east-1',
        **kwargs
    ):
        """Create new server

        Args:
            name: Server name
            instance_type: Instance type (m5.large, etc.)
            region: Region (default: us-east-1)

        Returns:
            Server: Created server object

        Example:
            >>> client = CloudClient(api_key='xxx')
            >>> server = client.create_server(
            ...     name='web-01',
            ...     instance_type='m5.large'
            ... )
            >>> server.wait_until_running()
        """
        # Implementation
        pass

# Usage feels natural
client = CloudClient(api_key=os.environ['API_KEY'])
server = client.create_server('web-01', 'm5.large')
server.start()
server.wait_until_running(timeout=300)
```

---

**Все DX материалы сохраняются в Markdown на русском языке.**
