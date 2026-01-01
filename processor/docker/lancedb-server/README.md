# LanceDB REST Server

A FastAPI REST server that provides HTTP access to LanceDB databases. This enables remote access to your processed RAG databases.

> **Note**: LanceDB is an embedded database (like SQLite) - no server is required for local use. This Docker server is only needed when you want remote HTTP access to your database.

## Quick Start

```bash
# Build the image
docker build -t lancedb-server docker/lancedb-server/

# Run with your database mounted (default port 9834)
docker run -d \
  -p 9834:9834 \
  -e PORT=9834 \
  -v /path/to/your/lancedb:/data \
  --name lancedb-server \
  lancedb-server
```

Or use docker-compose:

```bash
cd docker/lancedb-server

# Default (port 9834)
docker-compose up -d

# Custom port
LANCEDB_PORT=8080 docker-compose up -d

# Custom database path
LANCEDB_DATA=/path/to/db docker-compose up -d
```

## API Endpoints

### Health Check

```bash
GET /
GET /healthz
```

### List Tables

```bash
GET /tables
```

**Response:**
```json
{
  "tables": ["text_chunks", "code_chunks", "image_chunks"]
}
```

### Table Info

```bash
GET /tables/{table_name}
```

**Response:**
```json
{
  "name": "text_chunks",
  "row_count": 1500,
  "schema": "..."
}
```

### Table Schema

```bash
GET /tables/{table_name}/schema
```

**Response:**
```json
{
  "columns": [
    { "name": "id", "type": "string" },
    { "name": "content", "type": "string" },
    { "name": "vector", "type": "fixed_size_list<float>[1024]" }
  ]
}
```

### Vector Search

```bash
POST /tables/{table_name}/search
Content-Type: application/json

{
  "query_vector": [0.1, 0.2, ...],
  "limit": 10,
  "filter": "source_type = 'CODE_PYTHON'"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "abc123",
      "content": "...",
      "source_file": "/path/to/file.py",
      "_distance": 0.15
    }
  ],
  "count": 10
}
```

### Hybrid Search (Vector + Full-Text)

```bash
POST /tables/{table_name}/search/hybrid
Content-Type: application/json

{
  "query_vector": [0.1, 0.2, ...],
  "query_text": "caching implementation",
  "limit": 10,
  "filter": null
}
```

### Full-Text Search

```bash
POST /tables/{table_name}/search/text
Content-Type: application/json

{
  "query_text": "authentication middleware",
  "limit": 10
}
```

### Get Rows (Paginated)

```bash
GET /tables/{table_name}/rows?limit=50&offset=0
```

**Response:**
```json
{
  "rows": [...],
  "total": 1500,
  "offset": 0,
  "limit": 50
}
```

### Database Metadata

```bash
GET /metadata
```

Returns contents of the `_metadata` table if it exists.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LANCEDB_PATH` | `/data` | Path to LanceDB database inside container |
| `PORT` | `9834` | Server port |

### Docker-Compose Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LANCEDB_PORT` | `9834` | Host and container port |
| `LANCEDB_DATA` | `./lancedb` | Host path to mount as /data |

## Example Usage

### Python Client

```python
import httpx

# Get embeddings from your embedding service
query_vector = get_embedding("how does caching work")

# Search via REST API
response = httpx.post(
    "http://localhost:9834/tables/text_chunks/search",
    json={"query_vector": query_vector, "limit": 5}
)
results = response.json()["results"]
```

### cURL Examples

```bash
# List tables
curl http://localhost:9834/tables

# Get table info
curl http://localhost:9834/tables/text_chunks

# Full-text search
curl -X POST http://localhost:9834/tables/text_chunks/search/text \
  -H "Content-Type: application/json" \
  -d '{"query_text": "authentication", "limit": 5}'
```

## Notes

- **No embedding**: This server only provides search over pre-embedded data. You need to generate query embeddings separately using the same model used during processing.
- **Read-only**: The server is read-only - it cannot add or modify data.
- **CORS enabled**: The server allows requests from any origin for development convenience.

## Production Considerations

For production deployments:

1. **Disable CORS wildcards**: Modify `server.py` to restrict `allow_origins`
2. **Add authentication**: Implement API key or OAuth
3. **Use reverse proxy**: Put behind nginx/traefik for TLS
4. **Resource limits**: Set memory/CPU limits in docker-compose
