<p align="center">
  <img src="img/phagocyte_logo.png" alt="Phagocyte Logo" width="200"/>
</p>

<h1 align="center">Phagocyte</h1>

<p align="center">
  <em>End-to-end pipeline: Research → Parse References → Acquire Documents → Ingest → RAG Vector Store</em>
</p>

An automated workflow that conducts AI-powered research, extracts and acquires academic papers, converts them into structured markdown, and creates a searchable vector database for RAG applications.

---

## Pipeline Architecture

<p align="center">
  <img src="img/architecture.png" alt="Phagocyte Architecture" width="800"/>
</p>

---

## Modules

| Module | Description | Key Features |
|--------|-------------|--------------|
| **[researcher](src/researcher/)** | AI-powered deep research | Gemini Deep Research, citation extraction |
| **[parser](src/parser/)** | Reference extraction & acquisition | Regex + AI parsing, multi-source downloads, DOI→BibTeX |
| **[ingestor](src/ingestor/)** | Document → Markdown conversion | PDF, Web, GitHub, YouTube, Audio support |
| **[processor](src/processor/)** | RAG document processing | AST-aware chunking, embeddings, LanceDB vector store |

---

## Quick Start

```bash
# Install
git clone https://github.com/SIslamMun/Phagocyte.git
cd Phagocyte && uv sync

# Run pipeline
uv run phagocyte research "HDF5 best practices" -o ./output
uv run phagocyte parse refs ./output/research_report.md --export-batch
uv run phagocyte parse batch ./output/batch.json -o ./papers
uv run phagocyte ingest batch ./papers -o ./markdown
uv run phagocyte process run ./markdown -o ./lancedb
uv run phagocyte process search ./lancedb "chunking strategies"
```

---

## Commands

### Research
```bash
uv run phagocyte research <topic>         # Deep research with Gemini
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Output directory for research results |
| `--mode` | `-m` | Research mode: `undirected`, `directed`, `no-research` |
| `--artifact` | `-a` | Include specific artifacts in output |
| `--api-key` | | Google API key (or set `GOOGLE_API_KEY`) |
| `--verbose` | `-v` | Enable verbose logging |

### Parse (10 commands)
```bash
uv run phagocyte parse refs <file>        # Extract references from document
uv run phagocyte parse retrieve <id>      # Download single paper (DOI/arXiv/title)
uv run phagocyte parse batch <file>       # Batch download papers
uv run phagocyte parse doi2bib <doi>      # Convert DOI to BibTeX/JSON
uv run phagocyte parse verify <bib>       # Verify citations against CrossRef
uv run phagocyte parse citations <id>     # Get citation graph
uv run phagocyte parse sources            # List available paper sources
uv run phagocyte parse auth               # Authenticate with institution
uv run phagocyte parse init               # Initialize config file
uv run phagocyte parse config push/pull   # Sync config via GitHub gist
```

**Options:**
| Command | Option | Description |
|---------|--------|-------------|
| `refs` | `--agent` | AI agent: `none`, `claude`, `gemini` |
| `refs` | `--export-batch` | Export batch JSON for downloads |
| `refs` | `--export-dois` | Export DOI list only |
| `refs` | `--compare` | Compare AI vs regex extraction |
| `retrieve` | `--email` | Email for API rate limits |
| `batch` | `--concurrent` | Max concurrent downloads |
| `doi2bib` | `--format` | Output format: `bibtex`, `json`, `markdown` |
| `verify` | `--dry-run` | Preview without making changes |
| `citations` | `--direction` | Citation direction: `refs`, `cited-by`, `both` |

### Ingest (5 commands)
```bash
uv run phagocyte ingest file <source>     # Single file/URL to markdown
uv run phagocyte ingest batch <dir>       # Batch process folder
uv run phagocyte ingest crawl <url>       # Deep crawl website
uv run phagocyte ingest clone <repo>      # Clone and ingest git repo
uv run phagocyte ingest describe <path>   # Generate VLM image descriptions
```

**Options:**
| Command | Option | Description |
|---------|--------|-------------|
| `file` | `--describe-images` | Generate VLM descriptions for images |
| `file` | `--img-format` | Image format: `png`, `jpg`, `webp` |
| `batch` | `--recursive` | Process subdirectories |
| `batch` | `--concurrency` | Max parallel workers |
| `crawl` | `--max-pages` | Maximum pages to crawl |
| `crawl` | `--max-depth` | Maximum link depth |
| `crawl` | `--strategy` | Crawl strategy: `bfs`, `dfs`, `bestfirst` |
| `clone` | `--branch` | Git branch to clone |
| `clone` | `--shallow` | Shallow clone (faster) |
| `clone` | `--max-files` | Maximum files to process |

### Process (11 commands)
```bash
uv run phagocyte process run <input>      # Process into LanceDB
uv run phagocyte process search <db> <q>  # Search vector database
uv run phagocyte process stats <db>       # Show database statistics
uv run phagocyte process setup            # Download embedding models
uv run phagocyte process check            # Check service availability
uv run phagocyte process export <db> <out># Export database
uv run phagocyte process import <in> <db> # Import database
uv run phagocyte process visualize <db>   # Browse with lance-data-viewer
uv run phagocyte process deploy <db>      # Start web interface
uv run phagocyte process server <db>      # Deploy REST API via Docker
uv run phagocyte process test-e2e         # Run end-to-end validation
```

**Options:**
| Command | Option | Description |
|---------|--------|-------------|
| `run` | `--text-profile` | Chunking profile: `low`, `medium`, `high` |
| `run` | `--code-profile` | Code chunking: `low`, `medium`, `high` |
| `run` | `--table-mode` | Table handling: `separate`, `unified`, `both` |
| `run` | `--incremental` | Only process new/changed files |
| `run` | `--batch-size` | Documents per batch |
| `search` | `--limit` | Maximum results to return |
| `search` | `--table` | Table to search: `text_chunks`, `code_chunks` |
| `search` | `--hybrid` | Enable hybrid search (vector + FTS) |
| `search` | `--rerank` | Rerank results with cross-encoder |

---

## Installation

```bash
git clone https://github.com/SIslamMun/Phagocyte.git
cd Phagocyte
uv sync

# Install module extras as needed
cd ingestor && uv sync --extra all && cd ..
cd processor && uv sync && cd ..
```

### Requirements
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [Ollama](https://ollama.ai/) for embeddings (processor)
- API Keys: `GOOGLE_API_KEY` (researcher), `ANTHROPIC_API_KEY` (optional)

---

## Documentation

- [src/researcher/README.md](src/researcher/README.md) - Research module docs
- [src/parser/README.md](src/parser/README.md) - Parser module docs  
- [src/ingestor/README.md](src/ingestor/README.md) - Ingestor module docs
- [src/processor/README.md](src/processor/README.md) - Processor module docs

---

## MCP Servers

MCP servers for AI agent integration (Claude Desktop, Claude Code, Cursor, VS Code Copilot, Windsurf, Zed):

| Server | Tools | Description |
|--------|-------|-------------|
| `researcher-mcp` | 3 | Deep research, list topics, get report |
| `parser-mcp` | 7 | Retrieve paper, batch download, parse refs, doi2bib, verify, citations, sources |
| `ingestor-mcp` | 10 | Ingest file/URL, batch, crawl, clone repo, describe images, transcribe audio |
| `processor-mcp` | 6 | Process files, search, stats, setup, check, export |
| `rag-mcp` | 4 | Semantic search, hybrid search, list tables, get schema |

```bash
# Run from src/ directories
cd src/researcher && uv run researcher-mcp
cd src/parser && uv run parser-mcp
cd src/ingestor && uv run ingestor-mcp
cd src/processor && uv run processor-mcp
cd src/processor && uv run rag-mcp
```

**Documentation:**
- [researcher-mcp](src/researcher/mcp/researcher_mcp/README.md)
- [parser-mcp](src/parser/mcp/parser_mcp/README.md)
- [ingestor-mcp](src/ingestor/mcp/ingestor_mcp/README.md)
- [processor-mcp](src/processor/mcp/processor_mcp/README.md)
- [rag-mcp](src/processor/mcp/rag_mcp/README.md)

---

## License

MIT
