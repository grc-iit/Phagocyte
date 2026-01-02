# Phagocyte

> End-to-end pipeline: Research → Parse References → Acquire Documents → Ingest → RAG Vector Store

An automated workflow that conducts AI-powered research, extracts and acquires academic papers, converts them into structured markdown, and creates a searchable vector database for RAG applications.

---

## Pipeline Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  RESEARCHER  │─────▶│    PARSER    │─────▶│   INGESTOR   │─────▶│  PROCESSOR   │
│              │      │              │      │              │      │              │
│  AI Research │      │  Extract     │      │  Convert to  │      │  Chunk/Embed │
│  + Citations │      │  + Acquire   │      │  Markdown    │      │  LanceDB     │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
```

---

## Modules

| Module | Description | Key Features |
|--------|-------------|--------------|
| **[researcher/](researcher/)** | AI-powered deep research | Gemini Deep Research, citation extraction |
| **[parser/](parser/)** | Reference extraction & acquisition | Regex + AI parsing, multi-source downloads, DOI→BibTeX |
| **[ingestor/](ingestor/)** | Document → Markdown conversion | PDF, Web, GitHub, YouTube, Audio support |
| **[processor/](processor/)** | RAG document processing | AST-aware chunking, embeddings, LanceDB vector store |

---

## Quick Start

```bash
# 1. Research a topic
cd researcher && uv sync
researcher research "Your topic" --mode directed -a "https://example.com"

# 2. Extract and download references
cd ../parser && uv sync
parser parse-refs research_report.md --export-batch
parser batch batch.json -o papers/

# 3. Convert to markdown
cd ../ingestor && uv sync --extra all-formats
ingestor batch papers/ -o output/

# 4. Create searchable vector database
cd ../processor && uv sync
processor process output/ -o ./lancedb --text-profile low
processor search ./lancedb "your query" -k 5
```

---

## Installation

```bash
git clone https://github.com/SIslamMun/Phagocyte.git
cd Phagocyte

# Install each module
cd researcher && uv sync && cd ..
cd parser && uv sync && cd ..
cd ingestor && uv sync --extra all-formats && cd ..
cd processor && uv sync && cd ..
```

### Requirements
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [Ollama](https://ollama.ai/) for embeddings (processor)
- API Keys: `GOOGLE_API_KEY` (researcher), `ANTHROPIC_API_KEY` (optional)

---

## Example Pipeline Run

See [pipeline_output/](pipeline_output/) for a complete test run on **HDF5 file format**:

| Phase | Output |
|-------|--------|
| Research | 17KB report, 45+ citations |
| Parse | 46 references extracted |
| Acquire | 5 papers downloaded |
| Ingest | 4 PDFs + GitHub repo + 40 web pages → Markdown |
| Process | 1,547 chunks in LanceDB vector store |

---

## Documentation

- [researcher/README.md](researcher/README.md) - Research module docs
- [parser/README.md](parser/README.md) - Parser module docs  
- [ingestor/README.md](ingestor/README.md) - Ingestor module docs
- [processor/README.md](processor/README.md) - Processor module docs
- [pipeline_output/README.md](pipeline_output/README.md) - Complete pipeline test run

---

## MCP Servers

MCP servers for AI agent integration (Claude, Cursor, VS Code Copilot, etc.):

```bash
uv run researcher-mcp  # Deep research
uv run parser-mcp      # Paper acquisition
uv run ingestor-mcp    # Document conversion
uv run processor-mcp   # Embedding pipeline
uv run rag-mcp         # Semantic search
```

See: [researcher-mcp](researcher/mcp/researcher_mcp/README.md) | [parser-mcp](parser/mcp/parser_mcp/README.md) | [ingestor-mcp](ingestor/mcp/ingestor_mcp/README.md) | [processor-mcp](processor/mcp/processor_mcp/README.md) | [rag-mcp](processor/mcp/rag_mcp/README.md)

---

## License

MIT
