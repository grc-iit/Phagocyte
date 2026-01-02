# parser-mcp

MCP (Model Context Protocol) server for scientific paper acquisition, reference parsing, and citation management.

## Installation

```bash
# From the parser directory
cd parser

# Option 1: Install with MCP support (editable mode)
uv pip install -e ".[mcp]"

# Option 2: Or use uv sync
uv sync --extra mcp

# Optional: Install AI agents for enhanced parsing
uv pip install -e ".[claude-sdk]"  # Claude agent (recommended)
uv pip install -e ".[gemini]"      # Gemini agent
```

## Usage

```bash
# Start the server
uv run parser-mcp
```

## Editor Configuration

### Claude Desktop

**Config:** `~/.config/Claude/claude_desktop_config.json` (Linux) | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "parser": {
      "command": "uv",
      "args": ["run", "parser-mcp"],
      "cwd": "/path/to/parser",
      "env": {
        "PAPER_EMAIL": "your@email.com",
        "S2_API_KEY": "optional-semantic-scholar-key"
      }
    }
  }
}
```

### Claude Code (CLI)

```bash
# Add MCP with directory specification (recommended)
claude mcp add parser -- uv --directory /path/to/parser run parser-mcp

# Or if running from parser directory
cd /path/to/parser
claude mcp add parser -- uv run parser-mcp
```

Or add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "parser": {
      "command": "uv",
      "args": ["run", "parser-mcp"],
      "cwd": "/path/to/parser",
      "env": { "PAPER_EMAIL": "your@email.com" }
    }
  }
}
```

### Cursor

**Config:** `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "parser": {
      "command": "uv",
      "args": ["run", "parser-mcp"],
      "cwd": "/path/to/parser",
      "env": { "PAPER_EMAIL": "your@email.com" }
    }
  }
}
```

### VS Code + GitHub Copilot

**Config:** `.vscode/settings.json` or User Settings

```json
{
  "mcp.servers": {
    "parser": {
      "command": "uv",
      "args": ["run", "parser-mcp"],
      "cwd": "${workspaceFolder}/parser",
      "env": { "PAPER_EMAIL": "${env:PAPER_EMAIL}" }
    }
  }
}
```

### Windsurf

**Config:** `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "parser": {
      "command": "uv",
      "args": ["run", "parser-mcp"],
      "cwd": "/path/to/parser",
      "env": { "PAPER_EMAIL": "your@email.com" }
    }
  }
}
```

### Zed

**Config:** `~/.config/zed/settings.json`

```json
{
  "context_servers": {
    "parser": {
      "command": { "path": "uv", "args": ["run", "parser-mcp"] },
      "settings": {}
    }
  }
}
```

---

## Available Tools (7)

1. **retrieve_paper** - Retrieve a single paper PDF
2. **batch_retrieve** - Batch download papers from file
3. **parse_references** - Extract references from documents
4. **doi_to_bibtex** - Convert DOIs to BibTeX
5. **list_sources** - List available paper sources
6. **verify_citations** - Verify BibTeX against CrossRef/arXiv
7. **get_citations** - Get citation graph for a paper

---

### retrieve_paper

Retrieve a single paper PDF by DOI, title, or arXiv ID.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `identifier` | string | required | DOI, arXiv ID, or paper title |
| `output_dir` | string | `./papers` | Output directory for PDF |
| `email` | string | `null` | Email for API access (improves rate limits) |
| `skip_existing` | bool | `true` | Skip if PDF already exists |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "pdf_path": "./papers/paper.pdf",
  "source": "unpaywall",
  "title": "Paper Title"
}
```

**Examples:**
```
retrieve_paper(identifier="10.1038/nature12373")
retrieve_paper(identifier="arXiv:2005.11401", output_dir="./arxiv")
retrieve_paper(identifier="Attention Is All You Need")
```

---

### batch_retrieve

Batch download papers from a file.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_file` | string | required | Path to batch file (JSON, CSV, or text) |
| `output_dir` | string | `./papers` | Output directory for PDFs |
| `email` | string | `null` | Email for API access |
| `concurrent` | int (1-10) | `3` | Max concurrent downloads |
| `verbose` | bool | `false` | Verbose output |

**Input File Formats:**
- JSON: `[{"doi": "10.1234/..."}, {"title": "Paper Title"}]`
- CSV: Columns `doi`, `title`
- Text: One identifier per line

**Returns:**
```json
{
  "total": 10,
  "succeeded": 8,
  "failed": 1,
  "skipped": 1,
  "results": [...]
}
```

---

### parse_references

Parse and extract references from a research document.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_file` | string | required | Path to research document |
| `output_dir` | string | `./parsed` | Output directory |
| `agent` | `none` \| `claude` \| `gemini` | `none` | AI agent for enhanced parsing |
| `export_batch` | bool | `true` | Export batch.json for acquisition |
| `export_dois` | bool | `true` | Export dois.txt file |
| `format` | `json` \| `markdown` \| `both` | `both` | Output format |

**Returns:**
```json
{
  "success": true,
  "total_references": 25,
  "json_path": "./parsed/references.json",
  "markdown_path": "./parsed/references.md",
  "batch_path": "./parsed/batch.json",
  "dois_path": "./parsed/dois.txt",
  "agent_used": "claude"
}
```

**Examples:**
```
# Basic parsing (regex only)
parse_references(input_file="./research_report.md")

# Enhanced parsing with Claude
parse_references(input_file="./research_report.md", agent="claude")

# Custom output directory
parse_references(input_file="./paper.md", output_dir="./refs", format="json")
```

---

### doi_to_bibtex

Convert DOIs to BibTeX format.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dois` | string[] | required | List of DOIs to convert |
| `output_file` | string | `null` | Output BibTeX file path |

**Returns:**
```json
{
  "success": true,
  "total": 5,
  "converted": 4,
  "failed": 1,
  "bibtex": "@article{...}\n\n@inproceedings{...}",
  "output_path": "./refs.bib",
  "errors": ["10.invalid/doi: Not found"]
}
```

**Example:**
```
doi_to_bibtex(
  dois=["10.1038/nature12373", "10.1145/3065386"],
  output_file="./references.bib"
)
```

---

### list_sources

List available paper sources and their status.

**Parameters:** None

**Returns:**
```json
[
  {
    "source": "unpaywall",
    "available": true,
    "requires_auth": false,
    "notes": "Open access papers via DOI. Set email for better rates."
  },
  {
    "source": "arxiv",
    "available": true,
    "requires_auth": false,
    "notes": "Preprints from arXiv.org"
  }
]
```

---

### verify_citations

Verify BibTeX citations against CrossRef and arXiv.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | string | required | Path to BibTeX file or directory |
| `output_dir` | string | `./verified` | Output directory |
| `skip_keys` | array | `[]` | Citation keys to skip |
| `email` | string | `null` | Email for CrossRef API |
| `dry_run` | bool | `false` | Report only, don't write files |

**Returns:**
```json
{
  "success": true,
  "verified": 45,
  "arxiv": 12,
  "searched": 5,
  "website": 3,
  "manual": 2,
  "failed": 8,
  "total_verified": 67,
  "verified_path": "./verified/verified.bib",
  "failed_path": "./verified/failed.bib",
  "report_path": "./verified/report.md"
}
```

**Example:**
```
verify_citations(
  input_path="./references.bib",
  output_dir="./verified",
  email="your@email.com"
)
```

---

### get_citations

Get citation graph for a paper via Semantic Scholar.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `identifier` | string | required | DOI or arXiv ID |
| `direction` | string | `both` | `citations`, `references`, or `both` |
| `limit` | int | `50` | Max papers to retrieve (1-1000) |
| `s2_api_key` | string | `null` | Semantic Scholar API key |

**Returns:**
```json
{
  "success": true,
  "paper_id": "DOI:10.1038/nature12373",
  "citations": [
    {
      "title": "A citing paper",
      "authors": ["Author One", "Author Two"],
      "year": 2023,
      "doi": "10.xxx/yyy"
    }
  ],
  "references": [
    {
      "title": "A referenced paper",
      "authors": ["First Author"],
      "year": 2010,
      "doi": "10.aaa/bbb"
    }
  ]
}
```

**Example:**
```
get_citations(
  identifier="10.1038/nature12373",
  direction="both",
  limit=100
)
```

---

## Paper Sources

The retriever tries sources in priority order:

| Source | Auth Required | Notes |
|--------|---------------|-------|
| Unpaywall | No (email helps) | Open access via DOI |
| arXiv | No | Preprints |
| PMC | No | PubMed Central |
| Semantic Scholar | No (API key helps) | Academic search |
| CrossRef | No | Metadata + some OA |
| CORE | Yes (API key) | Aggregated OA |

## Example Workflow

```python
# 1. Parse references from research report
refs = parse_references(
    input_file="./research_report.md",
    agent="claude",
    export_batch=True
)

# 2. Batch download papers
papers = batch_retrieve(
    input_file=refs.batch_path,
    output_dir="./papers",
    concurrent=3
)

# 3. Convert DOIs to BibTeX
bibtex = doi_to_bibtex(
    dois=["10.1038/nature12373"],
    output_file="./references.bib"
)
```
