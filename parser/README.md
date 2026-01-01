# Parser

**Download academic papers automatically with full metadata resolution.**

Retrieves papers from multiple open access sources, converts DOIs to BibTeX, verifies citations, extracts references, and optionally accesses papers through your university subscription.

## Features

- 🔍 **Multi-source retrieval** - Searches 12+ sources including arXiv, Unpaywall, PubMed Central, OpenAlex
- 📄 **Smart metadata** - Downloads have descriptive filenames: `LeCun_2015_Deep_learning.pdf`
- 📚 **Batch processing** - Download hundreds of papers with progress tracking
- 🔄 **Reference extraction** - Parse DOIs, arXiv IDs, URLs from research documents (with automatic deduplication)
- 📖 **Citation tools** - Convert DOIs to BibTeX, verify citations, get citation graphs
- 🎓 **Institutional access** - Access paywalled papers via university VPN/EZProxy
- 🤖 **AI parsing** - Optional Claude/Gemini agents for complex documents

---

## Installation

```bash
git clone <repo-url>
cd parser

# Using uv (recommended)
uv sync
```

### Selenium Support (Optional)

For downloading from bot-protected sites (bioRxiv, Frontiers), the tool uses Selenium with headless Chrome as a fallback. This requires:
- **Chrome browser** installed on your system
- **ChromeDriver** (automatically managed by webdriver-manager)

The tool will automatically fall back to Selenium when direct HTTP downloads are blocked. No additional setup required if Chrome is installed.

---

## Quick Start

### 1. Create a config file

```bash
cp config.yaml.example config.yaml
```

Or initialize interactively:
```bash
parser init
```

### 2. Add your email

Edit `config.yaml` and set your email (required by APIs for polite access):

```yaml
user:
  email: "your.email@university.edu"
```

### 3. Download a paper

```bash
# By DOI (recommended - most reliable)
parser retrieve --doi "10.1038/nature12373"

# By arXiv ID
parser retrieve arXiv:1706.03762

# By title (less reliable - may find wrong paper)
parser retrieve --title "Attention Is All You Need"

# Specify where to save
parser retrieve --doi "10.1038/nature12373" -o ./papers

# Verbose output
parser retrieve --doi "10.1038/nature12373" -v
```

**Output:**
```
✓ Downloaded: LeCun_2015_Deep_learning.pdf
  Source: openalex
  Title: Deep learning
```

PDFs are saved with full metadata: `{first_author}_{year}_{title_short}.pdf`

---

## Commands Overview

| Command | Purpose | Example |
|---------|---------|---------|
| `retrieve` | Download single paper | `parser retrieve --doi "10.1038/nature14539"` |
| `batch` | Download multiple papers | `parser batch papers.txt -o ./downloads` |
| `parse-refs` | Extract references from docs | `parser parse-refs report.md` |
| `doi2bib` | Convert DOI to BibTeX/JSON | `parser doi2bib "10.1038/nature14539"` |
| `verify` | Verify BibTeX citations | `parser verify references.bib -o ./verified` |
| `citations` | Get citation graph | `parser citations "10.1038/nature14539"` |
| `sources` | List available sources | `parser sources` |
| `init` | Create config file | `parser init` |
| `auth` | Set up institutional access | `parser auth` |
| `config` | Sync config across machines | `parser config push` |

---

## Batch Processing

Have a list of papers? Put them in a file:

**Option 1: Text file (one identifier per line)**
```
10.1038/nature12373
10.1145/3292500.3330919
arXiv:1706.03762
```

**Option 2: CSV file**
```csv
doi,title
10.1038/nature12373,
,Attention Is All You Need
10.1145/3292500.3330919,
```

**Option 3: JSON file (from parse-refs)**
```json
[
  {"type": "doi", "value": "10.1038/nature12373", "title": "Deep Learning"},
  {"type": "arxiv", "value": "1706.03762", "title": "Attention Is All You Need"}
]
```

**Option 4: Batch format JSON**
```json
[
  {"doi": "10.1038/nature12373"},
  {"title": "Attention Is All You Need"},
  {"doi": "10.1145/3292500.3330919"}
]
```

Then run:
```bash
parser batch papers.txt -o ./downloads
parser batch papers.csv -o ./downloads
parser batch papers.json -o ./downloads --concurrent 5  # 5 parallel downloads
```

The tool will download all papers, skipping any you've already got.

**Features:**
- ✅ Progress tracking with resume support
- ✅ Skips existing files automatically
- ✅ Parallel downloads (configurable concurrency)
- ✅ Full metadata in all filenames

---

## DOI to BibTeX

Convert DOIs and arXiv IDs to BibTeX citations:

```bash
# Single DOI
parser doi2bib 10.1038/nature12373

# arXiv ID
parser doi2bib arXiv:1706.03762

# Short arXiv format
parser doi2bib 1706.03762

# Save to file
parser doi2bib 10.1038/nature12373 -o reference.bib

# Different formats
parser doi2bib 10.1038/nature12373 --format json      # Full metadata JSON
parser doi2bib 10.1038/nature12373 --format markdown  # Formatted citation

# Process multiple from file
parser doi2bib -i dois.txt -o references.bib
```

**Output formats:**
- `bibtex` (default): Standard BibTeX format
- `json`: Full metadata as JSON
- `markdown`: Formatted citation with YAML frontmatter

---

## Citation Verification

Verify BibTeX entries against CrossRef and arXiv:

```bash
# Verify a .bib file
parser verify references.bib -o ./verified

# Verify a directory of .bib files
parser verify citations_dir/ -o ./output

# Skip specific entries (websites, manual entries, etc.)
parser verify refs.bib --skip-keys "website1,manual2"

# Skip entries from a file
parser verify refs.bib --skip-keys-file skip.txt

# Use pre-verified manual entries
parser verify refs.bib --manual manual.bib

# Dry run (don't write files)
parser verify refs.bib --dry-run -v
```

**Output:**
```
verified/
├── verified.bib    # Successfully verified
├── failed.bib      # Need manual attention
└── report.md       # Summary report with details
```

---

## Citation Graphs

Get papers that cite or are referenced by a given paper:

```bash
# Get both citations and references
parser citations "10.1038/nature12373" --direction both

# Get only papers that cite this paper
parser citations "10.1038/nature12373" --direction citations

# Get only papers referenced by this paper
parser citations "10.1038/nature12373" --direction references

# Limit results
parser citations "arXiv:2005.11401" -n 100

# Output as BibTeX
parser citations "10.1038/nature12373" --format bibtex -o refs.bib

# Output as JSON
parser citations "10.1038/nature12373" --format json -o citations.json
```

**Data source:** Semantic Scholar API (use `--s2-key` for higher rate limits)

---

## Parse References

Extract DOIs, arXiv IDs, and URLs from research documents:

```bash
# Parse references from a markdown file
parser parse-refs research_report.md

# Output to directory
parser parse-refs report.md -o ./refs

# Output formats
parser parse-refs report.md --format json    # JSON only
parser parse-refs report.md --format md      # Markdown only
parser parse-refs report.md --format both    # Both formats (default)

# Export for pipeline
parser parse-refs report.md --export-batch   # Creates batch.json for downloads
parser parse-refs report.md --export-dois    # Creates dois.txt for doi2bib
```

**What it extracts:**
- DOIs (e.g., `10.1038/nature12373`)
- arXiv IDs (e.g., `arXiv:1706.03762`, `1706.03762`)
- GitHub repositories (e.g., `pytorch/pytorch`)
- YouTube videos
- Book ISBNs
- URLs to papers and websites
- Paper citations (Author et al., Year)

**Output:**
```
references/
├── references.json    # Structured data
├── references.md      # Human-readable list
├── batch.json         # For parser batch (if --export-batch)
└── dois.txt           # For parser doi2bib (if --export-dois)
```

**Automatic deduplication:** Duplicate references are removed automatically.

---

## AI Agent Parsing (Advanced)

For more accurate reference extraction, use AI agents (Claude or Gemini) to parse documents. This is especially useful for:
- Complex documents with non-standard citation formats
- Documents with references embedded in prose
- When you need better context extraction

### Installation

Install with agent support:

```bash
# Claude Agent SDK (RECOMMENDED - NO API KEY NEEDED!)
pip install claude-agent-sdk
# or
uv add claude-agent-sdk

# Direct Anthropic API (requires API key)
pip install anthropic
# or
uv add anthropic

# Google Gemini
pip install google-generativeai
# or
uv add google-generativeai

# Google ADK (Agent Development Kit)
pip install google-adk
# or
uv add google-adk

# All agents at once
pip install parser[agents]
```

### Usage

```bash
# Parse with Claude SDK (NO API KEY NEEDED! Uses Claude Code CLI)
parser parse-refs document.md --agent claude

# Direct Anthropic API (requires ANTHROPIC_API_KEY)
ANTHROPIC_API_KEY=xxx parser parse-refs document.md --agent anthropic

# Parse with Google ADK
GOOGLE_API_KEY=xxx parser parse-refs document.md --agent gemini

# Parse with direct Google API
GOOGLE_API_KEY=xxx parser parse-refs document.md --agent google

# Specify model
parser parse-refs document.md --agent claude --model claude-sonnet-4-20250514
parser parse-refs document.md --agent gemini --model gemini-2.0-flash

# Compare regular vs agent parsing
parser parse-refs document.md --compare --agent claude
```

### Agent Options

| Agent | Package | API Key Required? | Description |
|-------|---------|-------------------|-------------|
| `claude` | claude-agent-sdk | **NO** | Uses Claude Code CLI (recommended!) |
| `anthropic` | anthropic | YES | Direct Anthropic API |
| `gemini` | google-adk | YES | Google ADK framework |
| `google` | google-generativeai | YES | Direct Google Gemini API |

### Comparison Mode

Run both regex-based and AI-based parsing to compare results:

```bash
parser parse-refs report.md --compare --agent claude -o ./output
```

This creates:
```
output/
├── regular/           # Regex-based results
│   ├── references.json
│   └── references.md
├── agent/             # AI-based results
│   ├── references.json
│   ├── references.md
│   ├── agent_raw_response.txt
│   └── agent_result.json
└── comparison_report.md
```

### Configuration

Add API keys to `config.yaml`:

```yaml
agent:
  anthropic:
    api_key: null  # Or set ANTHROPIC_API_KEY env var
    model: "claude-sonnet-4-20250514"
  gemini:
    api_key: null  # Or set GOOGLE_API_KEY env var
    model: "gemini-2.0-flash"
```

### When to Use Agent vs Regular Parsing

| Aspect | Regular (Regex) | Agent (AI) |
|--------|-----------------|------------|
| **Speed** | Fast (milliseconds) | Slower (seconds) |
| **Cost** | Free | Free (claude) or API costs |
| **Accuracy** | Good for standard formats | Better for complex documents |
| **Context** | Limited | Rich context extraction |
| **Offline** | Works offline | Requires internet |

**Recommendation:** Use `--agent claude` for best results without any API costs (uses Claude Code CLI authentication).

---

## Sources (What Gets Searched)

The tool tries these sources in order:

| Priority | Source | What It Has |
|----------|--------|-------------|
| 1 | **Unpaywall** | Legal open access versions from publishers & repositories |
| 2 | **arXiv** | Preprints in physics, math, CS, quantitative biology |
| 3 | **PubMed Central** | Open access biomedical literature |
| 4 | **bioRxiv/medRxiv** | Biology and medical preprints (with Selenium fallback) |
| 5 | **Semantic Scholar** | Academic papers with open access PDFs |
| 6 | **ACL Anthology** | NLP papers from ACL, EMNLP, NAACL, etc. |
| 7 | **OpenAlex** | Open access aggregator |
| 8 | **Frontiers** | Gold open access publisher (with Selenium fallback) |
| 9 | **Institutional** | IEEE, ACM, Elsevier via your university (optional) |
| 10 | **Sci-Hub** | Gray area source (disabled by default) |
| 11 | **LibGen** | Gray area source (disabled by default) |
| 12 | **Web Search** | Google Scholar fallback (disabled by default) |

Check your current source status:
```bash
parser sources
```

You can enable/disable sources and change priorities in `config.yaml`.

---

## Retrieval Order & Smart Resolution

### How Papers Are Found

The retriever prioritizes **peer-reviewed papers** over preprints:

#### 1. Metadata Resolution (First Step)

When you provide a DOI or title, the system resolves metadata in this order:

| Priority | Source | Type | Why |
|----------|--------|------|-----|
| 1 | **CrossRef** | Peer-reviewed | Most authoritative for published papers |
| 2 | **Semantic Scholar** | Both | Good coverage, supports DOI/arXiv |
| 3 | **OpenAlex** | Both | Broad coverage fallback |
| 4 | **arXiv** | Preprints | Fallback when peer-reviewed not found |

**Why peer-reviewed first?** Published papers in journals have undergone peer review and are more authoritative than preprints.

#### 2. Per-Source Download Order

Each source uses the most reliable method first:

**arXiv:**
1. **arXiv ID** (from DOI like `10.48550/arXiv.1706.03762`)
2. **arXiv URL** (if present in input)
3. **Title search** (with 70% similarity threshold)

**Sci-Hub / LibGen:**
1. **Title first** (configurable - better hit rate for some papers)
2. **DOI fallback**

Configure in `config.yaml`:
```yaml
download:
  lookup_priority:
    - title  # Try title first
    - doi    # Then DOI if title fails
```

### DOI Validation

The system automatically filters problematic DOIs:

| DOI Type | Pattern | Publisher | Action |
|----------|---------|-----------|--------|
| **Peer Review** | `10.14293/...sor-...` | ScienceOpen | Skipped |
| **Peer Review** | `10.3410/f....` | Faculty Opinions | Skipped |
| **Book Chapter** | `10.1007/978-...` | Springer | Skipped |
| **Book Chapter** | `10.1016/b978-...` | Elsevier | Skipped |
| **Book Chapter** | `10.1201/978...` | Taylor & Francis | Skipped |
| **Book Chapter** | `10.1002/978...` | Wiley | Skipped |
| **Book Chapter** | `10.1017/978...` | Cambridge UP | Skipped |
| **Book Chapter** | `10.1093/...978...` | Oxford UP | Skipped |
| **Dataset** | `10.5281/zenodo...` | Zenodo | Skipped |

### Title Mismatch Detection

Catches false-positive matches for confusing terms:

| Query | False Match | Detection |
|-------|-------------|-----------|
| "LLaMA 3" | Book about llama animals | ✓ Detected ("camelid", "animal") |
| "BERT: Pre-training..." | "Bert the Turtle" | ✓ Detected (no AI context) |
| "Falcon LLM" | Falcon bird paper | ✓ Detected ("raptor", "ornithology") |

**How it works:** The system checks for AI-related keywords (e.g., "language model", "transformer", "neural") vs false context (e.g., "animal", "camelid", "bird").

---

## University/Institutional Access

If you have a university subscription, you can download papers from IEEE, ACM, Elsevier, and other publishers.

### Two Options

**Option A: VPN Mode (Recommended)**

If your university provides VPN access, simply connect to it and enable VPN mode:

```yaml
institutional:
  enabled: true
  vpn_enabled: true
```

That's it! Once connected to your university VPN, papers download directly.

If you want to automate VPN connection, create a script:

```bash
# Example: scripts/vpn-connect.sh
#!/bin/bash
# Your VPN connection command here
# Examples:
# openconnect vpn.youruni.edu
# sudo openvpn --config ~/vpn/university.ovpn
# nmcli connection up "University VPN"
```

Then configure it:

```yaml
institutional:
  enabled: true
  vpn_enabled: true
  vpn_script: "./scripts/vpn-connect.sh"
  vpn_disconnect_script: "./scripts/vpn-disconnect.sh"  # optional
```

Run authentication to connect:
```bash
parser auth
```

**Option B: EZProxy Mode (No VPN needed)**

If you can't use VPN, use your university's EZProxy:

```yaml
institutional:
  enabled: true
  vpn_enabled: false
  proxy_url: "https://ezproxy.gl.iit.edu/login?url="  # Your university's URL
```

Then authenticate once:
```bash
parser auth
```

This opens a browser where you log in through your university. Your session is saved for future use.

### Finding Your Proxy URL

Your proxy URL usually looks like:
- `https://ezproxy.youruni.edu/login?url=`
- `https://proxy.library.youruni.edu/login?url=`

Ask your library or check your library's website for "off-campus access" instructions.

---

## Configuration Reference

### Full config.yaml example

```yaml
# Paper PDF Retriever Configuration
# Copy this file to config.yaml and edit with your settings

# Your identification (required for polite API access)
user:
  email: "your.email@university.edu"  # Your email (required for API access)
  name: ""                      # Your name (optional)

# API Keys (optional but recommended for higher rate limits)
api_keys:
  # NCBI API key for PubMed Central - get from https://www.ncbi.nlm.nih.gov/account/settings/
  ncbi: null
  # Semantic Scholar API key - get from https://www.semanticscholar.org/product/api
  semantic_scholar: null
  # CrossRef Plus API key (if you have institutional access)
  crossref_plus: null

# Institutional Access (for IEEE, ACM, Elsevier via your university)
#
# Two modes available:
#   1. VPN mode: Set vpn_enabled: true when connected to university VPN
#   2. EZProxy mode: Set proxy_url, then run 'parser auth' to login
#
institutional:
  enabled: false

  # VPN Mode - set to true when connected to university VPN
  vpn_enabled: false
  vpn_script: null              # e.g., "./scripts/vpn-connect.sh"
  vpn_disconnect_script: null   # e.g., "./scripts/vpn-disconnect.sh"

  # EZProxy Mode - browser-based Shibboleth/SAML login
  proxy_url: null               # e.g., "https://ezproxy.youruniversity.edu/login?url="
  cookies_file: ".institutional_cookies.pkl"

  university: ""                # Your university name (for reference)

# Source configuration (lower priority number = tried first)
# Open Access sources are enabled by default
# Restricted sources (institutional, scihub, libgen) are disabled by default
sources:
  unpaywall:
    enabled: true
    priority: 1
  arxiv:
    enabled: true
    priority: 2
  pmc:
    enabled: true
    priority: 3
  biorxiv:
    enabled: true
    priority: 4
  semantic_scholar:
    enabled: true
    priority: 5
  acl_anthology:
    enabled: true
    priority: 6
  openalex:
    enabled: true
    priority: 7
  frontiers:
    enabled: true
    priority: 8
  institutional:
    enabled: false              # Enable when using university VPN/EZProxy
    priority: 9
  scihub:
    enabled: false              # ⚠️ Legal gray area - use at your own risk
    priority: 10
  libgen:
    enabled: false              # ⚠️ Legal gray area - use at your own risk
    priority: 11
  web_search:
    enabled: false
    priority: 12

# Unofficial sources (require explicit opt-in)
# ⚠️ WARNING: Use at your own risk. May be illegal in your jurisdiction.
unofficial:
  disclaimer_accepted: false    # Must set to true to enable scihub/libgen
  scihub:
    enabled: false
    proxy: null                 # SOCKS5 proxy if needed (e.g., "socks5://127.0.0.1:9050")
  libgen:
    enabled: false
    mirror: "li"                # LibGen mirror: "li", "is", "rs", "st"

# Download settings
download:
  output_dir: "./downloads"
  filename_format: "{first_author}_{year}_{title_short}.pdf"
  max_title_length: 50
  create_subfolders: false
  skip_existing: true

# Rate limiting (seconds between requests)
# Respects API guidelines - do not reduce below these values
rate_limits:
  global_delay: 1.0
  per_source_delays:
    crossref: 0.5               # CrossRef: be polite
    unpaywall: 0.1              # Unpaywall: fast
    arxiv: 3.0                  # arXiv: strict rate limit
    pmc: 0.34                   # PMC: 3 requests/second max
    semantic_scholar: 3.0       # S2: strict without API key
    biorxiv: 1.0                # bioRxiv: moderate
    scihub: 5.0                 # Sci-Hub: be careful
    libgen: 3.0                 # LibGen: moderate

# Batch processing settings
batch:
  max_concurrent: 3             # Max parallel downloads
  retry_failed: true            # Retry failed downloads
  max_retries: 2                # Max retry attempts
  save_progress: true           # Save progress for resume
  progress_file: ".retrieval_progress.json"

# AI Agent Settings for parse-refs --agent
# Enable AI-powered reference extraction using Claude or Gemini
# Usage: parser parse-refs document.md --agent claude
#        parser parse-refs document.md --agent gemini
agent:
  # Anthropic Claude Settings
  # Get API key from: https://console.anthropic.com/
  anthropic:
    api_key: null               # Or set ANTHROPIC_API_KEY env var
    model: "claude-sonnet-4-20250514"
    # Available models:
    # - claude-sonnet-4-20250514 (recommended, fast + capable)
    # - claude-opus-4-20250514 (most capable, slower)
    # - claude-3-haiku-20240307 (fastest, less capable)

  # Google Gemini Settings
  # Get API key from: https://aistudio.google.com/apikey
  gemini:
    api_key: null               # Or set GOOGLE_API_KEY env var
    model: "gemini-2.0-flash"
    # Available models:
    # - gemini-2.0-flash (recommended, fast + capable)
    # - gemini-1.5-pro (more capable, slower)
    # - gemini-1.5-flash (fast, good for simple docs)

  # Default agent when --agent is used without specifying type
  default: "claude"             # "claude" or "gemini"

# Logging
logging:
  level: "INFO"                 # DEBUG, INFO, WARNING, ERROR
  file: null                    # Set to a path to log to file (e.g., "parser.log")
```

### Filename Format

Downloaded PDFs use this format by default: `{first_author}_{year}_{title_short}.pdf`

**Examples:**
- `LeCun_2015_Deep_learning.pdf`
- `Achiam_2023_GPT-4_Technical_Report.pdf`
- `Vaswani_2017_Attention_is_All_you_Need.pdf`

Metadata is automatically resolved from CrossRef, Semantic Scholar, or OpenAlex.

**Available placeholders:**
- `{first_author}` - First author's last name
- `{year}` - Publication year
- `{title_short}` - Truncated title (max 7 words)
- `{title}` - Full title
- `{doi}` - DOI with `/` and `.` replaced by `_`

### Environment Variables

You can also set these via environment variables:

| Variable | Purpose |
|----------|---------|
| `PAPER_EMAIL` | Your email (overrides config) |
| `NCBI_API_KEY` | PubMed/PMC API key |
| `S2_API_KEY` | Semantic Scholar API key |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `GOOGLE_API_KEY` | Google Gemini API key |
| `GITHUB_TOKEN` | For config sync (needs gist scope) |

---

## CLI Commands Reference

### retrieve - Download single paper

```bash
parser retrieve [OPTIONS] [IDENTIFIER]

Options:
  -d, --doi TEXT                  Paper DOI
  -t, --title TEXT                Paper title
  -o, --output TEXT               Output directory (uses config if not set)
  -e, --email TEXT                Email for API access
  --s2-key TEXT                   Semantic Scholar API key
  --skip-existing / --no-skip-existing
                                  Skip if PDF exists (uses config if not set)
  -v, --verbose                   Verbose output

Examples:
  parser retrieve --doi "10.1038/nature12373"
  parser retrieve --title "Attention Is All You Need"
  parser retrieve -d "10.1038/nature12373" -o ./papers -e you@email.com
  parser retrieve arXiv:2005.11401 -o ./papers
```

### batch - Download multiple papers

```bash
parser batch [OPTIONS] INPUT_FILE

Options:
  -o, --output TEXT         Output directory (uses config if not set)
  --email TEXT              Email for API access
  --s2-key TEXT             Semantic Scholar API key
  -n, --concurrent INTEGER  Max concurrent downloads (uses config if not set)
  -v, --verbose             Verbose output

Examples:
  parser batch papers.json -o ./papers
  parser batch dois.txt -o ./papers --concurrent 3
  parser batch papers.csv -o ./downloads
  parser batch references.json -o ./downloads -n 5 -v
```

### parse-refs - Extract references from documents

```bash
parser parse-refs [OPTIONS] INPUT_FILE

Options:
  -o, --output TEXT               Output directory
  --format [json|md|both]         Output format (default: both)
  --agent [none|claude|anthropic|gemini|google]
                                  AI agent for parsing
  --api-key TEXT                  API key for agent (not needed for claude)
  --model TEXT                    Model to use for agent parsing
  --compare                       Run both regular and agent parsing
  --export-batch                  Export JSON for 'parser batch'
  --export-dois                   Export DOI/arXiv IDs for 'parser doi2bib -i'

Examples:
  parser parse-refs research_report.md
  parser parse-refs report.md -o ./refs --format json
  parser parse-refs document.md --agent claude
  parser parse-refs report.md --compare --agent claude
  parser parse-refs report.md --export-batch --export-dois
```

### doi2bib - Convert DOI to BibTeX/JSON/Markdown

```bash
parser doi2bib [OPTIONS] [IDENTIFIER]

Options:
  -i, --input PATH                File with DOIs (txt, json from parse-refs)
  -o, --output PATH               Output file
  --format [bibtex|json|markdown] Output format
  --email TEXT                    Email for API access
  --s2-key TEXT                   Semantic Scholar API key

Examples:
  parser doi2bib 10.1038/nature12373
  parser doi2bib arXiv:1605.08695 --format json
  parser doi2bib 1912.01703 --format markdown
  parser doi2bib -i dois.txt -o references.bib
  parser doi2bib -i batch.json -o references.bib
```

### verify - Verify BibTeX citations

```bash
parser verify [OPTIONS] INPUT_PATH

Options:
  -o, --output TEXT      Output directory
  --email TEXT           Email for CrossRef
  --skip-keys TEXT       Comma-separated keys to skip verification
  --skip-keys-file PATH  File with keys to skip (one per line)
  --manual PATH          Manual.bib with pre-verified entries
  --dry-run              Don't write files, just show what would happen
  -v, --verbose          Verbose output

Examples:
  parser verify references.bib -o ./verified
  parser verify citations_dir/ -o ./output
  parser verify refs.bib --skip-keys "website1,manual2"
  parser verify refs.bib --skip-keys-file skip.txt
  parser verify refs.bib --manual manual.bib
  parser verify refs.bib --dry-run -v
```

### citations - Get citation graph

```bash
parser citations [OPTIONS] IDENTIFIER

Options:
  -d, --direction [both|citations|references]
                                  Citation direction
  -n, --limit INTEGER             Max results
  --format [json|bibtex]          Output format
  -o, --output PATH               Output file
  --s2-key TEXT                   Semantic Scholar API key

Examples:
  parser citations "10.1038/nature12373" --direction both
  parser citations "arXiv:2005.11401" --direction citations -n 100
  parser citations "10.1038/nature12373" --format bibtex -o refs.bib
```

### sources - List available sources

```bash
parser sources

Example:
  parser sources
```

### init - Create config file

```bash
parser init

Example:
  parser init
```

### auth - Set up institutional access

```bash
parser auth

Example:
  parser auth
```

### config - Sync config across machines

```bash
parser config [push|pull]

Commands:
  push  Push config to a private GitHub gist
  pull  Pull config from a private GitHub gist

Examples:
  parser config push
  parser config pull
```

---

## Troubleshooting

### "Email required" error

Add your email to `config.yaml` under `user.email` or use the `-e` flag:
```bash
parser retrieve -d "10.1038/nature12373" -e you@email.com
```

### Paper not found

The tool only searches open access sources by default. If the paper is behind a paywall:
1. Enable institutional access (see above)
2. Or try the paper's arXiv preprint (many papers have one)
3. Enable Sci-Hub as a fallback (gray area)

### Rate limiting

If you're getting blocked, the tool is making requests too fast. Increase delays in `config.yaml`:

```yaml
rate_limits:
  global_delay: 2.0  # Increase this
```

### Institutional auth not working

1. Make sure your `proxy_url` is correct
2. Clear old cookies: delete `.institutional_cookies.pkl`
3. Run `parser auth` again
4. Complete the login fully before pressing Enter

### bioRxiv downloads fail

bioRxiv uses Cloudflare protection that may block automated downloads. The tool automatically falls back to Selenium (headless Chrome) when direct downloads fail. If Selenium fallback also fails:
- Ensure Chrome is installed on your system
- Check if webdriver-manager can download ChromeDriver
- Try connecting to university VPN

### Verification fails for valid entries

Some reasons verification might fail:
- DOI is incorrect or misformatted
- Entry has no DOI (add one manually)
- CrossRef has different metadata (check the report.md)

Use `--skip-keys` for entries you've manually verified.

### Filename shows "XXXX" instead of year

This means metadata resolution failed. The paper still downloads but with generic name. More common for:
- Very old DOIs
- Non-standard publishers
- Papers not in CrossRef/Semantic Scholar/OpenAlex

**Recommendation:** Use `--doi` or `--arxiv` instead of `--title` for better metadata.

---

## Limitations & Known Issues

### Sources That Don't Work

| Source | Status | Why |
|--------|--------|-----|
| **ScienceDirect/Elsevier** | Not supported | Aggressive bot detection (Incapsula/Imperva). Use institutional access. |
| **Springer** | Not supported | No public API for PDF access. Requires institutional subscription. |
| **Wiley** | Not supported | Same as Springer. |
| **Taylor & Francis** | Not supported | No public PDF API. |

### Sources With Caveats

| Source | Issue | Workaround |
|--------|-------|------------|
| **Semantic Scholar** | Aggressive rate limiting (429 errors) | Use 3+ second delays. Get an API key for higher limits. |
| **bioRxiv/medRxiv** | Cloudflare protection | Automatic Selenium fallback when direct download fails. |
| **Frontiers** | Cloudflare protection | Automatic Selenium fallback for bot-protected pages. |
| **Institutional** | Requires active session | Re-run `parser auth` if cookies expire. VPN mode is more reliable. |
| **LibGen** | Often blocked by universities | May not work on university networks. |

### What This Means

For paywalled papers not in open access repositories, you'll need:
1. **Institutional access** via VPN or EZProxy (if your university provides it)
2. **Check arXiv** - many papers have preprint versions
3. **Email the authors** - most are happy to share PDFs directly
4. **Interlibrary loan** - your library can usually get any paper

### Gray Area Sources

Sci-Hub and LibGen clients exist but are disabled by default. These sources operate in legal gray areas depending on jurisdiction. Enable at your own discretion:

```yaml
unofficial:
  disclaimer_accepted: true  # Must accept to enable

sources:
  scihub:
    enabled: true  # Use at your own risk
  libgen:
    enabled: true  # Use at your own risk
```

---

## Rate Limits

The tool respects API rate limits to avoid getting blocked:

| Source | Rate Limit | Notes |
|--------|------------|-------|
| CrossRef | 50 req/sec (shared pool) | Uses polite pool with email |
| Unpaywall | 100,000/day | Very permissive |
| arXiv | 1 request/3 sec | Official limit |
| PubMed Central | 3 req/sec (10 with key) | Get API key for more |
| Semantic Scholar | 100 req/5 min | Free API key available |
| bioRxiv | ~1 req/sec | Uses Selenium fallback |
| ACL Anthology | ~1 req/sec | Direct download |
| Frontiers | ~1 req/sec | Uses Selenium fallback |
| Sci-Hub | Be careful | Use 5+ second delays |
| LibGen | ~1 req/3 sec | No official limit |

---

## FAQ

**Q: What's the difference between `retrieve` and `batch`?**
- `retrieve`: Download one paper at a time
- `batch`: Download multiple papers from a file with progress tracking and resume support

**Q: Can I download paywalled papers?**
- Yes, if you have institutional access via VPN or EZProxy
- Alternatively, check if paper has arXiv preprint
- Sci-Hub available but disabled by default (gray area)

**Q: Why does my filename have "XXXX" instead of year?**
- Metadata resolution failed for that DOI
- Paper still downloads successfully
- More common with old DOIs or non-standard publishers
- **Fix:** Use `--doi` or `--arxiv` instead of `--title` for better metadata

**Q: What's the best way to download papers?**
1. Use DOI or arXiv ID (not title)
2. Enable institutional access if available
3. Use batch mode for multiple papers
4. Check parse-refs output before batch download

**Q: Is there a CLI command for validation?**
- **NO.** validation.py is an internal module used by parse-refs
- It validates DOIs, arXiv IDs, URLs, and years automatically
- Not exposed as a CLI command
- Used behind the scenes to ensure reference quality

**Q: How do I extract references from my document?**
```bash
parser parse-refs my_document.md
# Creates references.json and references.md
# Then use references.json with batch:
parser batch references.json -o ./papers
```

**Q: What does validation.py do?**
- Internal module for reference validation (not a CLI command)
- Validates DOI format (`10.XXXX/suffix`)
- Validates arXiv IDs (new: `YYMM.NNNNN`, old: `archive/YYMMNNN`)
- Validates URLs (scheme, balanced parentheses)
- Validates GitHub repos (`owner/repo`)
- Validates year ranges (1900-2099, warns if >2030)
- Automatically used by `parse-refs` command

**Q: Title-based download - how reliable is it?**
- **Less reliable** than DOI/arXiv ID
- May find wrong paper if title is ambiguous
- Metadata resolution works better with DOI/arXiv
- **Recommendation:** Always use DOI or arXiv ID when available

**Q: Why do some papers have full metadata and others just "XXXX"?**
- Metadata resolution tries multiple sources (CrossRef, Semantic Scholar, OpenAlex)
- If all sources fail, falls back to `{doi_prefix}_XXXX_paper.pdf`
- Success rate: ~100% for DOI/arXiv, lower for title-only searches
- The paper still downloads successfully even with XXXX

---

## Development

```bash
git clone <repo-url>
cd parser
uv sync --extra dev
uv run pytest
```

---

## License

MIT
