# Phase 4: Processor

RAG (Retrieval-Augmented Generation) document processing phase that chunks, embeds, and loads documents into LanceDB for semantic search.

## Overview

This phase takes all outputs from the previous pipeline stages (research reports, acquired papers, web content, and GitHub repositories) and creates a searchable vector database.

## Execution

**Date:** January 1, 2026

### Input Sources

| Source | Type | Files | Description |
|--------|------|-------|-------------|
| Research | Markdown | 2 | Research report and thinking steps from Gemini Deep Research |
| Papers | Markdown | 12 | Converted PDFs from Docling (4 full papers + logs) |
| Websites | Markdown | 38 | Web pages from HDF Group documentation |
| Codebases | Markdown | 1 | GitHub HDF5 repository extraction |

**Total:** 53 files processed

### Command

```bash
cd processor && uv run processor process ../pipeline_output/phase4_processor/input \
  -o ../pipeline_output/phase4_processor/lancedb \
  --text-profile low \
  --code-profile low \
  --table-mode separate \
  --full
```

### Configuration

- **Backend:** Ollama (local LLM server)
- **Text Embeddings:** Qwen3-Embedding-0.6B (1024 dimensions)
- **Code Embeddings:** jina-code-embeddings-0.5b (896 dimensions)
- **Table Mode:** Separate (text_chunks, code_chunks)
- **Incremental:** Full reprocess

## Results

### Database Statistics

| Table | Rows | Description |
|-------|------|-------------|
| text_chunks | 385 | Text content from papers, websites, research |
| code_chunks | 1162 | Code/technical content from HDF5 repo |
| _metadata | 3 | Database metadata |

**Total Chunks:** 1,547

### Processing Stats

- **Files Processed:** 53
- **Chunks Created:** 1,547
- **Images Processed:** 0 (text-only mode)
- **Errors:** 1 (text truncation on oversized chunk)

## Sample Search Queries

### Query 1: "asynchronous IO HDF5"

```
Result 1 (distance: 0.4159)
  Source: websites/support_hdfgroup_org_documentation_hdf5_latest_rel_spec_20_html.md
  Content: HDF5 Library and Tools 2.0.0

Result 2 (distance: 0.4302)
  Source: papers/Tang_2019_Enabling_Transparent_Asynchronous_IO_using_Backgro_pdf.md
  Content: Performance comparison between asynchronous-enabled HDF5 and the default HDF5...

Result 3 (distance: 0.4486)
  Source: papers/Byna_2020_ExaHDF5_Delivering_Efficient_Parallel_IO_on_Exasca_pdf.md
  Content: ExaHDF5: Delivering Efficient Parallel I/O on Exascale Computing Systems
```

### Query 2: "parallel file system IO performance"

```
Result 1 (distance: 0.4624)
  Source: papers/Byna_2020_ExaHDF5_Delivering_Efficient_Parallel_IO_on_Exasca_pdf.md
  
Result 2 (distance: 0.6093)  
  Source: papers/Tang_2022_Transparent_Asynchronous_Parallel_IO_Using_Backgro_pdf.md

Result 3 (distance: 0.6207)
  Source: research/research_report.md
```

## Output Structure

```
phase4_processor/
├── README.md                  # This file
├── process_execution.log      # Full processing log
├── input/                     # Input documents organized by type
│   ├── research/              # Research reports (2 files)
│   ├── papers/                # Converted PDF papers (12 files)
│   ├── websites/              # Web content (38 files)
│   └── codebases/             # GitHub repository (1 file)
└── lancedb/                   # Vector database
    ├── text_chunks.lance/     # Text embeddings
    ├── code_chunks.lance/     # Code embeddings
    └── _metadata.lance/       # Database metadata
```

## Usage

### Search the Database

```bash
# Text search
uv run processor search ./lancedb "your query" --table text_chunks -k 5

# Code search
uv run processor search ./lancedb "HDF5 dataset API" --table code_chunks -k 5

# Hybrid search (vector + BM25)
uv run processor search ./lancedb "query" --hybrid
```

### Database Operations

```bash
# View statistics
uv run processor stats ./lancedb

# Export to portable format
uv run processor export ./lancedb -o ./export --format lance

# Deploy web viewer
uv run processor deploy ./lancedb --port 8000
```

## Notes

- The processor successfully chunked 1,547 segments from 53 source documents
- Text and code are stored in separate tables with domain-specific embeddings
- The database supports both vector similarity and hybrid search
- One chunk required truncation due to exceeding token limits
