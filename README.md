# Phagocyte

> End-to-end pipeline: Research → Parse References → Acquire Documents → Ingest to Knowledge Store

An automated workflow that conducts AI-powered research, extracts and acquires academic papers, and converts them into structured markdown for knowledge management.

---

## Pipeline Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  RESEARCHER  │─────▶│    PARSER    │─────▶│   INGESTOR   │
│              │      │              │      │              │
│  AI Research │      │  Extract     │      │  Convert to  │
│  + Citations │      │  + Acquire   │      │  Markdown    │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## Modules

| Module | Description | Key Features |
|--------|-------------|--------------|
| **[researcher/](researcher/)** | AI-powered deep research | Gemini Deep Research, citation extraction |
| **[parser/](parser/)** | Reference extraction & acquisition | Regex + AI parsing, multi-source downloads, DOI→BibTeX |
| **[ingestor/](ingestor/)** | Document → Markdown conversion | PDF, Web, GitHub, YouTube, Audio support |

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
cd ../ingestor && uv sync
ingestor batch papers/ -o output/
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
```

### Requirements
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
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

---

## Documentation

- [researcher/README.md](researcher/README.md) - Research module docs
- [parser/README.md](parser/README.md) - Parser module docs  
- [ingestor/README.md](ingestor/README.md) - Ingestor module docs
- [pipeline_output/STATUS.md](pipeline_output/STATUS.md) - Test run status report

---

## License

MIT
