# ingestor-mcp

MCP (Model Context Protocol) server for comprehensive media-to-markdown ingestion.

## Installation

```bash
# From the ingestor directory
cd ingestor

# Option 1: Install with MCP support (editable mode)
uv pip install -e ".[mcp]"

# Option 2: Or use uv sync
uv sync --extra mcp

# Install format-specific extractors as needed
uv pip install -e ".[pdf]"       # PDF support
uv pip install -e ".[docx]"      # Word documents
uv pip install -e ".[pptx]"      # PowerPoint
uv pip install -e ".[epub]"      # eBooks
uv pip install -e ".[xlsx]"      # Excel
uv pip install -e ".[web]"       # Website crawling
uv pip install -e ".[youtube]"   # YouTube transcripts
uv pip install -e ".[audio]"     # Audio transcription (Whisper)
uv pip install -e ".[vlm]"       # Image descriptions (Ollama)

# Or install everything
uv pip install -e ".[all]"
```

## Usage

```bash
# Start the server
uv run ingestor-mcp
```

## Editor Configuration

### Claude Desktop

**Config:** `~/.config/Claude/claude_desktop_config.json` (Linux) | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "ingestor": {
      "command": "uv",
      "args": ["run", "ingestor-mcp"],
      "cwd": "/path/to/ingestor"
    }
  }
}
```

### Claude Code (CLI)

```bash
# Add MCP with directory specification (recommended)
claude mcp add ingestor -- uv --directory /path/to/ingestor run ingestor-mcp

# Or if running from ingestor directory
cd /path/to/ingestor
claude mcp add ingestor -- uv run ingestor-mcp
```

Or add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "ingestor": {
      "command": "uv",
      "args": ["run", "ingestor-mcp"],
      "cwd": "/path/to/ingestor"
    }
  }
}
```

### Cursor

**Config:** `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global)

```json
{
  "mcpServers": {
    "ingestor": {
      "command": "uv",
      "args": ["run", "ingestor-mcp"],
      "cwd": "/path/to/ingestor"
    }
  }
}
```

### VS Code + GitHub Copilot

**Config:** `.vscode/settings.json` or User Settings

```json
{
  "mcp.servers": {
    "ingestor": {
      "command": "uv",
      "args": ["run", "ingestor-mcp"],
      "cwd": "${workspaceFolder}/ingestor"
    }
  }
}
```

### Windsurf

**Config:** `~/.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "ingestor": {
      "command": "uv",
      "args": ["run", "ingestor-mcp"],
      "cwd": "/path/to/ingestor"
    }
  }
}
```

### Zed

**Config:** `~/.config/zed/settings.json`

```json
{
  "context_servers": {
    "ingestor": {
      "command": { "path": "uv", "args": ["run", "ingestor-mcp"] },
      "settings": {}
    }
  }
}
```

---

## Available Tools

### ingest_file

Convert a file to Markdown.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | string | required | File path or URL to ingest |
| `output_dir` | string | `./output` | Output directory |
| `keep_raw_images` | bool | `false` | Keep original image formats |
| `img_format` | string | `png` | Target image format |
| `generate_metadata` | bool | `false` | Generate JSON metadata |
| `describe_images` | bool | `false` | Generate VLM descriptions |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "output_path": "./output/paper.md",
  "source": "./paper.pdf",
  "media_type": "pdf",
  "image_count": 5
}
```

**Examples:**
```
ingest_file(input_path="./paper.pdf")
ingest_file(input_path="./presentation.pptx", describe_images=true)
```

---

### crawl_website

Deep crawl a website and convert to Markdown.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | Starting URL |
| `output_dir` | string | `./output` | Output directory |
| `strategy` | `bfs` \| `dfs` \| `bestfirst` | `bfs` | Crawl strategy |
| `max_depth` | int (0-10) | `2` | Maximum crawl depth |
| `max_pages` | int (1-500) | `50` | Maximum pages |
| `include_patterns` | string[] | `[]` | URL patterns to include |
| `exclude_patterns` | string[] | `[]` | URL patterns to exclude |
| `domain_only` | bool | `true` | Stay within same domain |
| `verbose` | bool | `false` | Verbose output |

**Crawl Strategies:**
- `bfs`: Breadth-first - explore level by level (good for sitemaps)
- `dfs`: Depth-first - follow links deep before backtracking
- `bestfirst`: Prioritize pages likely to have good content

**Returns:**
```json
{
  "success": true,
  "pages_crawled": 25,
  "output_dir": "./output",
  "files_created": ["./output/index.md", "./output/docs/intro.md", ...]
}
```

**Example:**
```
crawl_website(
  url="https://docs.example.com",
  max_depth=2,
  max_pages=100,
  strategy="bfs"
)
```

---

### ingest_youtube

Get transcript from a YouTube video.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | YouTube video/playlist URL |
| `output_dir` | string | `./output` | Output directory |
| `captions` | `auto` \| `manual` \| `any` | `auto` | Caption preference |
| `include_playlist` | bool | `false` | Process entire playlist |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "output_path": "./output/video_transcript.md",
  "video_title": "Video Title",
  "duration": "10:30"
}
```

**Example:**
```
ingest_youtube(url="https://youtube.com/watch?v=abc123")
```

---

### ingest_github

Clone and convert a GitHub repository.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | GitHub repository URL |
| `output_dir` | string | `./output` | Output directory |
| `branch` | string | `main` | Branch to clone |
| `include_patterns` | string[] | `["*.py", "*.js", ...]` | File patterns to include |
| `exclude_patterns` | string[] | `["node_modules/*", ...]` | File patterns to exclude |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "output_dir": "./output/repo",
  "repo_name": "repo-name",
  "files_processed": 45
}
```

**Example:**
```
ingest_github(
  url="https://github.com/user/repo",
  branch="main",
  include_patterns=["*.py", "*.md"]
)
```

---

### batch_ingest

Process all files in a directory.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_dir` | string | required | Directory to process |
| `output_dir` | string | `./output` | Output directory |
| `recursive` | bool | `true` | Process subdirectories |
| `concurrency` | int (1-20) | `5` | Max concurrent extractions |
| `describe_images` | bool | `false` | Generate VLM descriptions |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "total_files": 20,
  "processed": 18,
  "failed": 2,
  "output_dir": "./output",
  "results": [...]
}
```

**Example:**
```
batch_ingest(input_dir="./documents", recursive=true, concurrency=5)
```

---

### list_supported_formats

List all supported file formats.

**Returns:**
```json
{
  "documents": ["pdf", "docx", "pptx", "epub", "txt", "md"],
  "spreadsheets": ["xlsx", "xls", "csv"],
  "web": ["html", "url", "youtube"],
  "code": ["py", "js", "ts", "github"],
  "data": ["json", "xml", "yaml"],
  "audio": ["mp3", "wav", "m4a"]
}
```

---

### detect_file_type

Detect file type using AI-powered detection.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | string | required | Path to the file |

**Returns:**
```json
{
  "file_path": "./document.pdf",
  "media_type": "pdf",
  "extension": ".pdf",
  "can_process": true
}
```

---

### clone_repo

Clone and ingest a git repository with advanced options.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repo` | string | required | Repository URL (HTTPS/SSH) or local path |
| `output_dir` | string | `./output` | Output directory |
| `shallow` | bool | `true` | Use shallow clone |
| `depth` | int | `1` | Clone depth for shallow clones |
| `branch` | string | `null` | Clone specific branch |
| `tag` | string | `null` | Clone specific tag |
| `commit` | string | `null` | Checkout specific commit |
| `token` | string | `null` | Git token for private repos |
| `submodules` | bool | `false` | Include git submodules |
| `max_files` | int (1-5000) | `500` | Maximum files to process |
| `max_file_size` | int | `500000` | Maximum file size in bytes |
| `include_binary` | bool | `false` | Include binary file metadata |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "output_path": "./output/repo.md",
  "repo_name": "flask",
  "files_processed": 150,
  "files_skipped": 10,
  "image_count": 5
}
```

**Examples:**
```
clone_repo(repo="https://github.com/pallets/flask")
clone_repo(repo="git@github.com:user/private.git", token="ghp_xxx")
clone_repo(repo="https://github.com/user/repo", branch="develop", max_files=200)
```

---

### describe_images

Generate VLM descriptions for images using Ollama.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | string | required | Image file or directory |
| `vlm_model` | string | `llava:7b` | VLM model for descriptions |
| `ollama_host` | string | `http://localhost:11434` | Ollama server URL |
| `output_file` | string | `null` | Optional output JSON file |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "images_processed": 5,
  "descriptions": [
    {
      "file": "./images/figure1.png",
      "filename": "figure1.png",
      "description": "A flowchart showing the system architecture..."
    }
  ],
  "output_file": "./descriptions.json"
}
```

**Examples:**
```
describe_images(input_path="./figure.png")
describe_images(input_path="./images/", vlm_model="llava:13b")
describe_images(input_path="./diagrams/", output_file="./descriptions.json")
```

---

### transcribe_audio

Transcribe audio to text using Whisper.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_path` | string | required | Audio file path |
| `output_dir` | string | `./output` | Output directory |
| `whisper_model` | string | `turbo` | Whisper model (tiny/base/small/medium/large/turbo) |
| `language` | string | `null` | Force language (auto-detect if not set) |
| `verbose` | bool | `false` | Verbose output |

**Returns:**
```json
{
  "success": true,
  "output_path": "./output/lecture.md",
  "duration": "45:30",
  "language": "en"
}
```

**Examples:**
```
transcribe_audio(input_path="./lecture.mp3")
transcribe_audio(input_path="./audio.wav", whisper_model="large", language="en")
```

## Supported Formats

| Category | Formats | Extra Required |
|----------|---------|----------------|
| Documents | PDF, DOCX, PPTX, EPUB, TXT, MD, RST | `pdf`, `docx`, `pptx`, `epub` |
| Spreadsheets | XLSX, XLS, CSV | `xlsx`, `xls` |
| Web | HTML, Websites | `web` |
| Video | YouTube | `youtube` |
| Code | GitHub repos, local code | (built-in) |
| Audio | MP3, WAV, M4A | `audio` |
| Data | JSON, XML, YAML | (built-in) |

## Example Workflow

```python
# 1. Check supported formats
formats = list_supported_formats()

# 2. Detect file type
info = detect_file_type(file_path="./document.pdf")

# 3. Ingest the file
result = ingest_file(
    input_path="./document.pdf",
    output_dir="./markdown",
    describe_images=True
)

# 4. Crawl documentation site
docs = crawl_website(
    url="https://docs.example.com",
    max_depth=2,
    max_pages=50
)

# 5. Batch process a folder
batch = batch_ingest(
    input_dir="./papers",
    output_dir="./output",
    concurrency=5
)
```

## VLM Image Descriptions

To enable AI-powered image descriptions:

1. Install Ollama: https://ollama.ai
2. Pull a vision model: `ollama pull llava:7b`
3. Set `describe_images=true` in tool calls

This will generate semantic descriptions of images in documents,
useful for RAG applications and accessibility.
