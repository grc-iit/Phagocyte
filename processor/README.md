# Processor

RAG (Retrieval-Augmented Generation) document processor that chunks, embeds, and loads documents into LanceDB for semantic search.

## Features

- **Multi-format Support**: Code (26+ languages), papers, markdown, web content
- **AST-aware Chunking**: Structure-aware chunking using tree-sitter for code, header-aware for documents
- **Multiple Embedding Backends**: Ollama (default), Transformers, OpenCLIP for multimodal
- **Embedding Profiles**: Quality vs speed tradeoffs (low/medium/high)
- **LanceDB Storage**: Embedded vector database with hybrid search (vector + BM25)
- **Incremental Processing**: Skip unchanged files for fast re-processing
- **Portable Paths**: Database stores relative paths for cross-machine portability
- **MCP Servers**: Model Context Protocol servers for AI agent integration
- **Claude Skills**: Documentation for Claude Code users

## Quick Start

```bash
# 1. Install
uv sync

# 2. Check services
uv run processor check

# 3. Download embedding models
uv run processor setup

# 4. Process documents
uv run processor process ./my-docs -o ./lancedb

# 5. Search
uv run processor search ./lancedb "how does caching work"
```

## Installation

```bash
# Core (uses Ollama for embeddings)
uv sync

# With MCP servers
uv sync --extra mcp

# With Claude SDK (for HyDE optimization in rag-mcp)
uv sync --extra claude-sdk

# With GPU/transformers backend
uv sync --extra gpu

# With cross-encoder reranking
uv sync --extra reranker

# Everything
uv sync --all-extras
```

**Requirements:**
- Python 3.11+
- [Ollama](https://ollama.ai/) for embedding models

## CLI Commands

| Command | Description |
|---------|-------------|
| `processor setup` | Download required embedding models |
| `processor check` | Verify backend availability |
| `processor process` | Process files into LanceDB |
| `processor search` | Search the database |
| `processor stats` | Show database statistics |
| `processor export` | Export database to portable format |
| `processor import` | Import database from export |
| `processor server` | Deploy REST API via Docker |
| `processor deploy` | Launch web interface to browse database |
| `processor visualize` | Launch data viewer |
| `processor test-e2e` | Run end-to-end validation |

### Processing Options

```bash
uv run processor process ./input -o ./lancedb \
  --embedder ollama \
  --text-profile low \
  --code-profile low \
  --table-mode separate \
  --incremental
```

| Option | Values | Description |
|--------|--------|-------------|
| `--embedder` | ollama, transformers | Embedding backend |
| `--text-profile` | low, medium, high | Text embedding quality |
| `--code-profile` | low, high | Code embedding quality |
| `--multimodal-profile` | low, high | Image embedding quality (CLIP/SigLIP) |
| `--table-mode` | separate, unified, both | Table organization |
| `--incremental/--full` | - | Skip unchanged files |
| `--content-type` | auto, code, paper, markdown | Force content detection |
| `--hybrid` | - | Enable hybrid search (vector + BM25) |

## Embedding Models

### Text Models (Qwen3-Embedding via Ollama)

| Profile | Model | Dimensions | Context | Speed |
|---------|-------|------------|---------|-------|
| low | 0.6B | 1024 | 32K | Fastest |
| medium | 4B | 2560 | 32K | Balanced |
| high | 8B | 4096 | 32K | Best quality |

### Code Models (jina-code-embeddings via Ollama)

| Profile | Model | Dimensions | Languages |
|---------|-------|------------|-----------|
| low | 0.5B | 896 | 15+ |
| high | 1.5B | 1536 | 15+ |

### Multimodal Models (OpenCLIP via Transformers)

Used for image embeddings in `image_chunks` and unified tables:

| Profile | Model | Dimensions | Notes |
|---------|-------|------------|-------|
| low | CLIP-ViT-L-14 | 768 | Good quality, fast |
| high | CLIP-ViT-H-14 | 1024 | Best quality |

Requires: `uv sync --extra multimodal` or `--extra gpu`

## MCP Servers

Two MCP (Model Context Protocol) servers for AI agent integration:

### processor-mcp

Exposes document processing operations:

```bash
uv sync --extra mcp
uv run processor-mcp
```

**Tools:** `process_documents`, `check_services`, `setup_models`, `get_db_stats`, `export_db`, `import_db`

### rag-mcp

Exposes RAG search with retrieval-time optimizations:

```bash
uv run rag-mcp
uv run rag-mcp --config_generate  # Generate config template
```

**Tools:** `search`, `search_images`, `list_tables`, `generate_config`

**Search Optimizations:**

| Flag | Latency | Best For |
|------|---------|----------|
| `hybrid` | +10-30ms | Keyword-heavy queries |
| `use_hyde` | +200-500ms | Knowledge questions |
| `rerank` | +50-200ms | High precision needs |
| `expand_parents` | +5-20ms | Broader context |

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "processor": {
      "command": "uv",
      "args": ["run", "processor-mcp"],
      "cwd": "/path/to/processor"
    },
    "rag": {
      "command": "uv",
      "args": ["run", "rag-mcp"],
      "cwd": "/path/to/processor"
    }
  }
}
```

## Database Structure

LanceDB is file-based - no server needed!

```
lancedb/
├── text_chunks.lance/      # Papers, websites, markdown
├── code_chunks.lance/      # Source code
├── image_chunks.lance/     # Figures with dual embeddings
├── _metadata.lance/        # Database metadata
└── (optional) chunks.lance/  # Unified table
```

### Table Schemas

**text_chunks**: id, content, vector, source_file, source_type, section_path, citations, token_count

**code_chunks**: id, content, vector, source_file, language, symbol_name, symbol_type, imports

**image_chunks**: id, figure_id, caption, vlm_description, text_vector, visual_vector

## Docker REST API

For remote access to LanceDB databases, a FastAPI REST server is provided:

```bash
# Build and run (default port 9834)
docker build -t lancedb-server docker/lancedb-server/
docker run -d -p 9834:9834 -e PORT=9834 -v /path/to/lancedb:/data lancedb-server

# Or use docker-compose
cd docker/lancedb-server
docker-compose up -d                           # Default port 9834
LANCEDB_PORT=8080 docker-compose up -d         # Custom port
```

**Endpoints:**
- `GET /tables` - List tables
- `GET /tables/{name}` - Table info
- `POST /tables/{name}/search` - Vector search
- `POST /tables/{name}/search/hybrid` - Hybrid search
- `POST /tables/{name}/search/text` - Full-text search

See [docker/lancedb-server/README.md](docker/lancedb-server/README.md) for full API documentation.

> **Note**: LanceDB is embedded (like SQLite) - no server needed for local use. The Docker server is only for remote HTTP access.

## Project Structure

```
processor/
├── src/processor/           # Core library
│   ├── cli.py              # CLI commands
│   ├── config.py           # Configuration
│   ├── types.py            # Data types (Chunk, ContentType)
│   ├── pipeline/           # Processing pipeline
│   ├── chunkers/           # AST-aware chunking
│   ├── embedders/          # Ollama, Transformers, OpenCLIP
│   ├── database/           # LanceDB operations
│   └── core/               # Content detection/routing
├── mcp/                    # MCP servers (separate packages)
│   ├── processor_mcp/      # Processing MCP
│   └── rag_mcp/            # RAG search MCP
│       └── optimizations/  # HyDE, reranking, etc.
├── .claude/skills/         # Claude Code skills
├── configs/                # Configuration templates
├── docker/                 # Docker deployments
└── tests/                  # Test suite
```

## Library Usage

```python
from processor.config import load_config
from processor.pipeline.processor import Pipeline
from pathlib import Path
import asyncio

async def main():
    config = load_config()
    pipeline = Pipeline(config)
    result = await pipeline.process(Path("./input"))
    print(f"Processed {result['files_processed']} files")
    print(f"Created {result['chunks_created']} chunks")

asyncio.run(main())
```

## Configuration

Create `processor.yaml` or use `--config`:

```yaml
content_mapping:
  codebases: code
  papers: paper
  websites: markdown

chunking:
  code_chunk_size: 1024
  paper_chunk_size: 2048
  markdown_chunk_size: 1024

embedding:
  backend: ollama
  text_profile: low
  code_profile: low
  ollama_host: "http://localhost:11434"

database:
  uri: "./lancedb"
  table_mode: separate
```

## Development

```bash
# Setup
uv sync --extra dev

# Tests
uv run pytest
uv run pytest tests/unit/
uv run pytest --cov=processor

# Lint
uv run ruff check src/
uv run ruff format src/
uv run mypy src/processor/

# E2E test
uv run processor test-e2e
```

## License

MIT
