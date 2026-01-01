# processor-mcp

MCP (Model Context Protocol) server for document processing operations. Exposes the processor pipeline as tools for AI agents.

## Installation

```bash
# Install with MCP support
uv sync --extra mcp
```

## Usage

```bash
# Start the server
uv run processor-mcp
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "processor": {
      "command": "uv",
      "args": ["run", "processor-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

## Available Tools

### process_documents

Process documents through chunking, embedding, and loading into LanceDB.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | string | required | File or directory to process |
| `output_db` | string | `./lancedb` | LanceDB output path |
| `embedder` | `ollama` \| `transformers` | `ollama` | Embedding backend |
| `text_profile` | `low` \| `medium` \| `high` | `low` | Text embedding quality |
| `code_profile` | `low` \| `high` | `low` | Code embedding quality |
| `table_mode` | `separate` \| `unified` \| `both` | `separate` | Table organization |
| `batch_size` | int (1-256) | `32` | Embedding batch size |
| `incremental` | bool | `true` | Skip unchanged files |
| `content_type` | `auto` \| `code` \| `paper` \| `markdown` | `auto` | Force content detection |

**Returns:** `{ files_processed, chunks_created, images_processed, errors, output_path }`

**Example:**
```
process_documents(input_path="./my-codebase", output_db="./db", content_type="code")
```

---

### check_services

Check availability of embedding backends.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ollama_host` | string | `http://localhost:11434` | Ollama server URL |

**Returns:** `{ ollama_cli, ollama_server, available_models, transformers_available, openclip_available }`

---

### setup_models

Download required embedding models via Ollama.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `minimal` | bool | `true` | Only download qwen3-embedding:0.6b |
| `ollama_host` | string | `http://localhost:11434` | Ollama server URL |

**Models downloaded:**
- Minimal: `qwen3-embedding:0.6b` (text)
- Full: Also includes `jina-code-embeddings-0.5b`, `jina-code-embeddings-1.5b`

---

### get_db_stats

Get statistics for a LanceDB database.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | string | required | Path to LanceDB database |
| `table` | string | `null` | Specific table to inspect |

**Returns:** `{ path, tables: { name: { row_count, columns } } }`

---

### export_db

Export database to a portable format.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | string | required | Source database path |
| `output_path` | string | required | Output directory |
| `format` | `lance` \| `csv` | `lance` | Export format |
| `include_vectors` | bool | `false` | Include vectors in CSV |
| `tables` | list[string] | `null` | Tables to export (null = all) |

**Returns:** `{ format, tables, total_rows, output_path }`

---

### import_db

Import database from a Lance export.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `export_path` | string | required | Path to exported Lance directory |
| `output_path` | string | required | Target database path |
| `tables` | list[string] | `null` | Tables to import (null = all) |

**Returns:** `{ imported_tables, output_path }`

## Workflow

1. **Check services**: `check_services()` - Verify Ollama is running
2. **Setup models**: `setup_models()` - Download embedding models if needed
3. **Process documents**: `process_documents(input_path="./docs")` - Process files
4. **Verify results**: `get_db_stats(db_path="./lancedb")` - Check database

## Embedding Profiles

| Type | Profile | Model | Dimensions | Speed |
|------|---------|-------|------------|-------|
| text | low | Qwen3-Embedding-0.6B | 1024 | Fastest |
| text | medium | Qwen3-Embedding-4B | 2560 | Balanced |
| text | high | Qwen3-Embedding-8B | 4096 | Best quality |
| code | low | jina-code-0.5b | 896 | Fast |
| code | high | jina-code-1.5b | 1536 | Best quality |

## Prerequisites

- [Ollama](https://ollama.ai/) installed and running (`ollama serve`)
- Embedding models downloaded (use `setup_models` tool or `uv run processor setup`)
