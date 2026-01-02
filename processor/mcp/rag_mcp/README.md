# rag-mcp

MCP (Model Context Protocol) server for RAG search operations. Provides semantic search over LanceDB vector databases with retrieval-time optimizations.

## Installation

```bash
# From the processor directory
cd processor

# Option 1: Install with MCP support (editable mode)
uv pip install -e ".[mcp]"

# Option 2: Or use uv sync
uv sync --extra mcp

# Optional: Install Claude SDK for HyDE optimization
uv pip install -e ".[claude-sdk]"

# Optional: Install cross-encoder for reranking
uv pip install -e ".[reranker]"
```

## Usage

```bash
# Start the server
uv run rag-mcp

# Generate config template
uv run rag-mcp --config_generate

# Use custom config
uv run rag-mcp --config ./my_config.yaml
```

## Editor Configuration

### Claude Desktop

**Config:** `~/.config/Claude/claude_desktop_config.json` (Linux) | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### Claude Code (CLI)

```bash
# Add MCP with directory specification (recommended)
claude mcp add rag -- uv --directory /path/to/processor run rag-mcp

# Or if running from processor directory
cd /path/to/processor
claude mcp add rag -- uv run rag-mcp
```

Or add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### Cursor

**Config:** `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### VS Code + GitHub Copilot

**Config:** `.vscode/settings.json` or User Settings

```json
{
  "mcp.servers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "${workspaceFolder}/processor"
    }
  }
}
```

### Windsurf

**Config:** `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

### Zed

**Config:** `~/.config/zed/settings.json`

```json
{
  "context_servers": {
    "rag": {
      "command": { "path": "uv", "args": ["run", "rag-mcp"] },
      "settings": {}
    }
  }
}
```

---

## Available Tools

### search

Search the RAG database for relevant documents.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | Search query |
| `db_path` | string | `./lancedb` | LanceDB database path |
| `table` | `text_chunks` \| `code_chunks` \| `chunks` \| `image_chunks` | `text_chunks` | Table to search |
| `limit` | int (1-100) | `5` | Number of results |
| `hybrid` | bool | `false` | Use hybrid search (vector + BM25) |
| `use_hyde` | bool | `false` | Use HyDE query transformation |
| `rerank` | bool | `false` | Rerank with cross-encoder |
| `rerank_top_k` | int (5-100) | `20` | Candidates for reranking |
| `expand_parents` | bool | `false` | Expand to parent documents |

**Returns:**
```json
{
  "results": [
    {
      "content": "...",
      "source_file": "/path/to/file",
      "score": 0.85,
      "chunk_id": "abc123",
      "metadata": { "language": "python", ... }
    }
  ],
  "query": "original query",
  "optimizations_used": ["hybrid_rrf", "hyde"],
  "total_time_ms": 150.5
}
```

**Example:**
```
search(query="how does caching work", hybrid=true, limit=10)
```

---

### search_images

Search for relevant images/figures from processed papers.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | Text description to search for |
| `db_path` | string | `./lancedb` | LanceDB database path |
| `limit` | int | `5` | Number of results |

**Returns:**
```json
[
  {
    "figure_id": "1",
    "caption": "Figure 1: System architecture",
    "vlm_description": "A flowchart showing...",
    "image_path": "./img/figure1.png",
    "source_paper": "paper-name",
    "score": 0.82
  }
]
```

---

### list_tables

List available tables in the RAG database.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `db_path` | string | `./lancedb` | LanceDB database path |

**Returns:**
```json
{
  "db_path": "./lancedb",
  "tables": {
    "text_chunks": { "name": "text_chunks", "row_count": 1500, "searchable": true },
    "code_chunks": { "name": "code_chunks", "row_count": 800, "searchable": true }
  }
}
```

---

### generate_config

Generate a template RAG configuration file.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_path` | string | `./rag_config.yaml` | Where to write the config |

**Returns:** Confirmation message

## Search Optimizations

| Optimization | Flag | Latency | Best For |
|--------------|------|---------|----------|
| Hybrid Search | `hybrid=true` | +10-30ms | Keyword-heavy queries, code search |
| HyDE | `use_hyde=true` | +100-500ms | Knowledge questions ("What is...", "How does...") |
| Reranking | `rerank=true` | +50-200ms (GPU) | High precision requirements |
| Parent Expansion | `expand_parents=true` | +5-20ms | Broader context needs |

### Recommended Combinations

**Fast search (default):**
No optimizations - pure vector similarity

**Better recall:**
```
search(query="...", hybrid=true)
```

**Knowledge questions:**
```
search(query="what is dependency injection", use_hyde=true, rerank=true)
```

**Code search:**
```
search(query="authentication middleware", table="code_chunks", hybrid=true)
```

**Maximum precision:**
```
search(query="...", hybrid=true, use_hyde=true, rerank=true)
```

## Configuration

Generate a config template:
```bash
uv run rag-mcp --config_generate
```

Edit `rag_config.yaml`:
```yaml
# Database
default_db_path: "./lancedb"

# Embedding profiles (MUST match processor config!)
text_profile: "low"
code_profile: "low"
ollama_host: "http://localhost:11434"

# Search defaults
default_limit: 5
default_hybrid: false

# HyDE (Hypothetical Document Embeddings)
hyde:
  enabled: false
  backend: "claude_sdk"  # claude_sdk (default) or ollama
  claude_model: "haiku"  # haiku, sonnet, opus
  ollama_model: "llama3.2:latest"  # fallback
  max_tokens: 256

# Cross-Encoder Reranking
reranker:
  enabled: false
  model: "BAAI/bge-reranker-v2-m3"
  top_k: 20
  top_n: 5
  device: "auto"

# Parent Expansion
expand_parents: false
```

## HyDE Backends

HyDE (Hypothetical Document Embeddings) generates a hypothetical answer to your query and embeds that instead of the raw query. This improves results for knowledge-seeking questions.

Two backends are supported:

| Backend | Description | Requirements |
|---------|-------------|--------------|
| `claude_sdk` | Uses Claude Code Agent SDK (default) | `uv sync --extra claude-sdk` |
| `ollama` | Uses local Ollama model | Ollama with llama3.2 |

The system automatically falls back to Ollama if Claude SDK is not available.

## Important Notes

- **Embedding profiles must match**: The `text_profile` and `code_profile` in your RAG config must match the profiles used when processing documents, or search quality will be poor.
- **Database must exist**: Process documents first with `processor-mcp` or `uv run processor process`.
- **FTS index required for hybrid**: Hybrid search requires FTS index created during processing (`create_fts_index: true` in processor config).
