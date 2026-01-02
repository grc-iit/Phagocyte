# researcher-mcp

MCP (Model Context Protocol) server for AI-powered deep research operations using Gemini API.

## Installation

```bash
# From the researcher directory
cd researcher

# Option 1: Install with MCP support (editable mode)
uv pip install -e ".[mcp]"

# Option 2: Or use uv sync
uv sync --extra mcp
```

## Usage

```bash
# Start the server
uv run researcher-mcp
```

## Prerequisites

Set your Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key"
# or
export GOOGLE_API_KEY="your-api-key"
```

Get an API key from: https://aistudio.google.com/

## Editor Configuration

### Claude Desktop

**Config:** `~/.config/Claude/claude_desktop_config.json` (Linux) | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "researcher": {
      "command": "uv",
      "args": ["run", "researcher-mcp"],
      "cwd": "/path/to/researcher",
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Code (CLI)

```bash
# Add MCP with directory specification (recommended)
claude mcp add researcher -- uv --directory /path/to/researcher run researcher-mcp

# Or if running from researcher directory
cd /path/to/researcher
claude mcp add researcher -- uv run researcher-mcp
```

Or add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "researcher": {
      "command": "uv",
      "args": ["run", "researcher-mcp"],
      "cwd": "/path/to/researcher",
      "env": { "GEMINI_API_KEY": "your-api-key" }
    }
  }
}
```

### Cursor

**Config:** `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "researcher": {
      "command": "uv",
      "args": ["run", "researcher-mcp"],
      "cwd": "/path/to/researcher",
      "env": { "GEMINI_API_KEY": "your-api-key" }
    }
  }
}
```

### VS Code + GitHub Copilot

**Config:** `.vscode/settings.json` or User Settings

```json
{
  "mcp.servers": {
    "researcher": {
      "command": "uv",
      "args": ["run", "researcher-mcp"],
      "cwd": "${workspaceFolder}/researcher",
      "env": { "GEMINI_API_KEY": "${env:GEMINI_API_KEY}" }
    }
  }
}
```

### Windsurf

**Config:** `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "researcher": {
      "command": "uv",
      "args": ["run", "researcher-mcp"],
      "cwd": "/path/to/researcher",
      "env": { "GEMINI_API_KEY": "your-api-key" }
    }
  }
}
```

### Zed

**Config:** `~/.config/zed/settings.json`

```json
{
  "context_servers": {
    "researcher": {
      "command": { "path": "uv", "args": ["run", "researcher-mcp"], "env": { "GEMINI_API_KEY": "your-api-key" } },
      "settings": {}
    }
  }
}
```

---

## Available Tools

### deep_research

Conduct deep research on a topic using Gemini Deep Research API.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | Research topic or question |
| `output_dir` | string | `./output` | Output directory for results |
| `mode` | `undirected` \| `directed` \| `no-research` | `undirected` | Research mode |
| `artifacts` | string[] | `[]` | Supporting materials (URLs, files, text) |
| `output_format` | string | `null` | Custom output format instructions |
| `max_wait` | int (60-7200) | `3600` | Maximum wait time in seconds |
| `verbose` | bool | `false` | Enable verbose output with thinking steps |

**Research Modes:**
- `undirected`: Web-first discovery - searches broadly, good for exploration
- `directed`: Uses provided artifacts first, fills gaps with web search
- `no-research`: Analyzes only provided materials, no external search

**Returns:**
```json
{
  "success": true,
  "report_path": "/path/to/research/research_report.md",
  "metadata_path": "/path/to/research/research_metadata.json",
  "thinking_path": "/path/to/research/thinking_steps.md",
  "query": "HDF5 file format",
  "mode": "undirected",
  "duration_seconds": 245.5
}
```

**Examples:**
```
# Basic research
deep_research(query="HDF5 file format best practices")

# Directed research with artifacts
deep_research(
  query="Compare HDF5 vs Zarr",
  mode="directed",
  artifacts=["https://support.hdfgroup.org/", "https://zarr.dev/"]
)

# Document analysis only
deep_research(
  query="Summarize findings",
  mode="no-research",
  artifacts=["./paper.pdf", "./notes.txt"]
)
```

---

### check_api_key

Check if Gemini API key is configured.

**Parameters:** None

**Returns:**
```json
{
  "gemini_key_set": true,
  "google_key_set": false,
  "key_source": "GEMINI_API_KEY"
}
```

---

### list_research_outputs

List research outputs in a directory.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_dir` | string | `./output` | Directory to scan for research outputs |

**Returns:**
```json
{
  "output_dir": "./output",
  "sessions": [
    {
      "path": "./output/research",
      "report": "./output/research/research_report.md",
      "metadata": "./output/research/research_metadata.json",
      "thinking": "./output/research/thinking_steps.md",
      "query": "HDF5 file format",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

## Output Files

When research completes, the following files are created:

| File | Description |
|------|-------------|
| `research_report.md` | Main research report with citations |
| `research_metadata.json` | Query, timing, interaction metadata |
| `thinking_steps.md` | Agent reasoning steps (if verbose) |

## Example Workflow

```python
# 1. Check API key is configured
check_api_key()

# 2. Conduct research
result = deep_research(
    query="Best practices for scientific data storage with HDF5",
    mode="directed",
    artifacts=[
        "https://support.hdfgroup.org/documentation/",
        "https://github.com/HDFGroup/hdf5"
    ],
    verbose=True
)

# 3. List all research sessions
list_research_outputs(output_dir="./output")
```
