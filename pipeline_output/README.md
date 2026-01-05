# Pipeline Output Directory

This directory contains complete end-to-end test runs of the Phagocyte RAG pipeline system, demonstrating the full workflow from research to vector database creation.

## Overview

The Phagocyte pipeline transforms research topics into queryable knowledge bases through a systematic 5-6 phase process:

1. **Phase 1: Research** - AI-powered deep research using Gemini with artifacts
2. **Phase 2: Parser** - Reference extraction (regex and AI agent methods)
3. **Phase 3: Acquisition** - Paper download and bibliography management
4. **Phase 4: Ingestor** - Document conversion (PDF, GitHub, web) to markdown
5. **Phase 5: Processor** - Vector database creation with embeddings
6. **Phase 6: Access/Validation** - Database querying and quality assurance

---

## Test Pipelines

### 🔹 test_pipeline_hdf5/

**Topic**: HDF5 (Hierarchical Data Format 5) - High-performance parallel I/O library

**Research Focus**: Asynchronous I/O, parallel file systems, exascale computing

**Artifacts Processed**:
- 📄 5 research papers (HDF5 subfiling, async I/O, background threads)
- 🌐 40+ web pages (HDF Group documentation, specs, tools)
- 💻 GitHub repository: HDFGroup/hdf5 (core library)

**Pipeline Statistics**:
- **Research Duration**: 297.1 seconds (4.95 minutes)
- **References Extracted**: 16 (regex) + 14 (AI agent)
- **Papers Downloaded**: 5 PDFs successfully acquired
- **Markdown Files**: 68 documents ingested
- **Vector Database**: 2,048+ text chunks, 500+ code chunks
- **Embeddings Model**: Ollama nomic-embed-text

**Key Deliverables**:
- Comprehensive research report (18KB, 180 lines)
- Comparison report (regex vs AI agent parsing)
- BibTeX bibliography with verified citations
- Fully indexed LanceDB with semantic search

**Status**: ✅ Complete - Full 5-phase pipeline executed

**Documentation**: See [test_pipeline_hdf5/README.md](test_pipeline_hdf5/README.md)

---

### 🔹 test_pipeline_jarvis/

**Topic**: Jarvis-CD (Jarvis Continuous Deployment) - HPC runtime deployment system

**Research Focus**: Package orchestration, hardware abstraction, storage integration

**Artifacts Processed**:
- 📄 2 PDFs (academic paper + presentation slides)
- 🌐 2 documentation URLs (GRC IIT docs, GitHub)
- 💻 GitHub repository: iowarp/runtime-deployment (50 files)

**Pipeline Statistics**:
- **Research Duration**: 258.6 seconds (4.31 minutes)
- **References Extracted**: 14 (regex parsing only)
- **Papers Downloaded**: 0 (used local PDFs in artifacts/)
- **Markdown Files**: 5 documents ingested (~188KB total)
- **Vector Database**: 144 text chunks, 0 code chunks
- **Embeddings Model**: Ollama qwen3-embedding:0.6b

**Key Deliverables**:
- Comprehensive research report (15KB, 156 lines)
- Validation report (92% accuracy rating)
- Source PDFs archived in artifacts/
- Queryable LanceDB with validated claims

**Status**: ✅ Complete - Full 6-phase pipeline with validation

**Documentation**: See [test_pipeline_jarvis/README.md](test_pipeline_jarvis/README.md) and [VALIDATION.md](test_pipeline_jarvis/VALIDATION.md)

---

## Directory Structure

```
pipeline_output/
├── README.md                          # This file
│
├── test_pipeline_hdf5/                # HDF5 pipeline test
│   ├── README.md                      # Pipeline summary
│   ├── STATUS.md                      # Execution status
│   ├── phase1_research/               # AI research phase
│   │   ├── README.md
│   │   ├── research_stream.md
│   │   └── research/
│   │       ├── research_report.md     # Main research output
│   │       ├── research_metadata.json
│   │       └── thinking_steps.md
│   ├── phase2_parser/                 # Reference extraction
│   │   ├── README.md
│   │   ├── step1_regular/             # Regex parsing
│   │   ├── step2_agent/               # AI agent parsing
│   │   ├── step3_comparison/          # Method comparison
│   │   ├── step4_acquisition/         # Paper downloads
│   │   └── step5_doi2bib/             # BibTeX generation
│   ├── phase3_ingestor/               # Document ingestion
│   │   ├── README.md
│   │   ├── pdfs/                      # PDF → markdown
│   │   ├── github/                    # GitHub repos
│   │   └── web/                       # Web pages
│   ├── phase4_processor/              # Vector DB creation
│   │   ├── README.md
│   │   ├── input/                     # Preprocessed markdown
│   │   ├── lancedb/                   # Vector database
│   │   └── lancedb_test/              # Test database
│   └── *.log                          # Execution logs
│
└── test_pipeline_jarvis/              # Jarvis-CD pipeline test
    ├── VALIDATION.md                  # Research validation report
    ├── artifacts/                     # Source materials
    │   └── jarvis/
    │       ├── cernuda2024jarvis.pdf
    │       └── pdsw24_wip_session2_wip1.pdf
    ├── phase1_research/               # AI research phase
    │   ├── README.md
    │   └── research/
    │       ├── research_report.md     # Main research output
    │       └── research_metadata.json
    ├── phase2_parser/                 # Reference extraction
    │   ├── README.md
    │   └── step1_regular/             # Regex parsing
    ├── phase3_acquisition/            # Paper downloads
    │   └── README.md
    ├── phase4_ingestor/               # Document ingestion
    │   ├── README.md
    │   ├── pdfs/                      # PDF → markdown
    │   └── github/                    # GitHub repo
    ├── phase5_processor/              # Vector DB creation
    │   ├── README.md
    │   ├── input/                     # Preprocessed markdown
    │   └── lancedb/                   # Vector database
    └── phase6_access/                 # Access documentation
        └── README.md                  # 6 access methods
```

---

## Using the Pipeline Results

### Accessing Research Reports

Both pipelines produce comprehensive research reports synthesized by Gemini Deep Research:

**HDF5 Report**:
```bash
cat test_pipeline_hdf5/phase1_research/research/research_report.md
```

**Jarvis Report**:
```bash
cat test_pipeline_jarvis/phase1_research/research/research_report.md
```

### Querying Vector Databases

#### HDF5 Knowledge Base

```bash
# Search the HDF5 database
uv run phagocyte process search \
  pipeline_output/test_pipeline_hdf5/phase4_processor/lancedb \
  "How does HDF5 handle parallel I/O?" --limit 5

# Get database statistics
uv run phagocyte process stats \
  pipeline_output/test_pipeline_hdf5/phase4_processor/lancedb
```

#### Jarvis Knowledge Base

```bash
# Search the Jarvis database
uv run phagocyte process search \
  pipeline_output/test_pipeline_jarvis/phase5_processor/lancedb \
  "What are the three package types in Jarvis?" --limit 5

# Get database statistics
uv run phagocyte process stats \
  pipeline_output/test_pipeline_jarvis/phase5_processor/lancedb
```

### Python API Access

```python
import lancedb

# Connect to HDF5 database
db_hdf5 = lancedb.connect("pipeline_output/test_pipeline_hdf5/phase4_processor/lancedb")
text_table = db_hdf5.open_table("text_chunks")

# Semantic search
results = text_table.search("asynchronous I/O") \
    .metric("cosine") \
    .limit(5) \
    .to_pandas()

print(results[['text', '_distance']])
```

### Web UI Access

Start the processor web interface:

```bash
cd src/processor
uv run streamlit run src/phagocyte_processor/ui/app.py
```

Then open `http://localhost:8501` and select the database path.

---

## Comparison: HDF5 vs Jarvis Pipelines

| Metric | HDF5 Pipeline | Jarvis Pipeline |
|--------|--------------|-----------------|
| **Research Time** | 297.1s (4.95m) | 258.6s (4.31m) |
| **References Found** | 30 (regex+agent) | 14 (regex only) |
| **Papers Downloaded** | 5 PDFs | 0 (used local) |
| **Documents Ingested** | 68 files | 5 files |
| **Vector Chunks** | 2,048+ text<br>500+ code | 144 text<br>0 code |
| **Database Size** | ~50MB | ~5MB |
| **Embedding Model** | nomic-embed-text | qwen3-embedding:0.6b |
| **Validation** | Not performed | 92% accuracy |
| **Special Features** | - Agent comparison<br>- BibTeX generation<br>- Large codebase | - Artifacts folder<br>- Validation report<br>- Access docs |

**Key Observations**:
- HDF5 pipeline is more comprehensive (larger corpus, code indexing)
- Jarvis pipeline includes quality validation and access documentation
- Both demonstrate successful end-to-end RAG workflows
- Jarvis used faster embedding model but smaller dataset

---

## Pipeline Execution Guide

### Running a New Pipeline Test

```bash
# 1. Create output directory
mkdir -p pipeline_output/test_pipeline_[topic]
cd pipeline_output/test_pipeline_[topic]

# 2. Phase 1: Research (from project root)
uv run phagocyte research \
  --mode directed \
  --artifacts [url1] [url2] [pdf1.pdf] \
  --output pipeline_output/test_pipeline_[topic]/phase1_research

# 3. Phase 2: Parse references
uv run phagocyte parse refs \
  /absolute/path/to/phase1_research/research/research_report.md \
  --output /absolute/path/to/phase2_parser/step1_regular

# 4. Phase 3: Acquire papers (if needed)
uv run phagocyte parse batch \
  /absolute/path/to/phase2_parser/step1_regular/batch.json \
  --output /absolute/path/to/phase3_acquisition

# 5. Phase 4: Ingest documents
uv run phagocyte ingest file [pdf_file] -o /absolute/path/to/phase4_ingestor/pdfs
uv run phagocyte ingest clone [github_url] -o /absolute/path/to/phase4_ingestor/github

# 6. Phase 5: Process into vector DB
uv run phagocyte process run \
  /absolute/path/to/phase5_processor/input \
  -o /absolute/path/to/phase5_processor/lancedb

# 7. Phase 6: Search and validate
uv run phagocyte process search \
  /absolute/path/to/phase5_processor/lancedb \
  "your search query" --limit 5
```

**Important Notes**:
- Use **absolute paths** for all module commands to avoid path resolution issues
- Each module (researcher, parser, ingestor, processor) may run from its own src/ directory
- Create README.md files at each phase to document commands and results
- Consider validation for quality assurance (see Jarvis VALIDATION.md)

---

## Authentication

For paper acquisition, institutional authentication may be required:

```bash
# Configure EZProxy authentication
uv run phagocyte parse auth

# Follow prompts to enter:
# - Institution name
# - EZProxy URL
# - Username and password
```

Credentials are stored in `~/.config/phagocyte_parser/ezproxy_credentials.json`.

---

## Database Statistics

### HDF5 Database

```
Tables: 3
├── text_chunks: 2,048+ entries
├── code_chunks: 500+ entries  
└── _metadata: 3 entries

Embedding Dimensions: 768
Backend: Ollama (nomic-embed-text)
Chunking: AST-aware (code), semantic (text)
```

### Jarvis Database

```
Tables: 2
├── text_chunks: 144 entries
└── _metadata: 3 entries

Embedding Dimensions: 1024
Backend: Ollama (qwen3-embedding:0.6b)
Chunking: Semantic (text only)
```

---

## Search Methods

Both databases support multiple search strategies:

1. **Vector Similarity Search** - Semantic matching via embeddings
2. **Hybrid Search** - Combines vector + full-text search (FTS)
3. **Reranking** - Re-scores results using cross-encoder models
4. **CLI Search** - Command-line interface (fastest)
5. **Python API** - Programmatic access (most flexible)
6. **Web UI** - Streamlit interface (most user-friendly)
7. **REST API** - HTTP endpoints (best for integration)
8. **MCP Server** - Model Context Protocol (AI assistant access)

See [test_pipeline_jarvis/phase6_access/README.md](test_pipeline_jarvis/phase6_access/README.md) for detailed examples.

---

## Quality Validation

The Jarvis pipeline includes comprehensive validation (see [VALIDATION.md](test_pipeline_jarvis/VALIDATION.md)):

**Validation Results**:
- ✅ Core technical claims verified (92% accuracy)
- ✅ Citations cross-referenced with sources
- ✅ Architecture details confirmed
- ✅ Command syntax validated
- ⚠️ PDF extraction had limitations (minimal text)

**Validation Process**:
1. Identify key claims from research report
2. Search vector database for supporting evidence
3. Calculate semantic distance scores
4. Cross-reference with source documents
5. Document findings with confidence ratings

This validation approach ensures research reports are accurate and well-sourced.

---

## Troubleshooting

### Common Issues

**1. Output files appear in src/ directories**
- **Solution**: Use absolute paths or manually move files to project root

**2. Parser can't find input files**
- **Solution**: Provide absolute paths: `/home/user/.../file.md`

**3. Paper downloads fail**
- **Solution**: Configure EZProxy authentication or use local PDFs

**4. Embeddings generation slow**
- **Solution**: Reduce batch size: `--batch-size 25`

**5. Search returns no results**
- **Solution**: Check database path, verify table names, try broader queries

### Logs

Execution logs are saved at each phase:
- `phase1_research/execution.log`
- `phase2_parser/step*/execution.log`
- `phase3_ingestor/*_execution.log`
- `phase4_processor/process_execution.log`

Review logs for detailed error messages and debugging information.

---

## Future Enhancements

**Planned Improvements**:
- [ ] Automated phase chaining (single command pipeline)
- [ ] Relative path support for all modules
- [ ] Better PDF extraction (OCR integration)
- [ ] Incremental database updates
- [ ] Multi-modal embeddings (text + images)
- [ ] Distributed processing for large corpora
- [ ] Docker containerization
- [ ] CI/CD integration for continuous research

**Research Topics for Testing**:
- Apache Spark (distributed computing)
- Kubernetes (container orchestration)
- TensorFlow (machine learning)
- PostgreSQL (database systems)
- LLVM (compiler infrastructure)

---

## References

**Phagocyte Pipeline**:
- Main Repository: `/home/shazzadul/Illinois_Tech/Spring26/RA/Github/new/Phagocyte`
- Researcher Module: `src/researcher/`
- Parser Module: `src/parser/`
- Ingestor Module: `src/ingestor/`
- Processor Module: `src/processor/`

**External Resources**:
- LanceDB Documentation: https://lancedb.github.io/lancedb/
- Ollama Models: https://ollama.com/library
- Gemini API: https://ai.google.dev/

**Test Pipeline Documentation**:
- [HDF5 Pipeline](test_pipeline_hdf5/README.md)
- [Jarvis Pipeline](test_pipeline_jarvis/README.md)
- [Jarvis Validation](test_pipeline_jarvis/VALIDATION.md)

---

## Summary

This directory demonstrates the Phagocyte pipeline's ability to:
1. ✅ Conduct AI-powered research on complex technical topics
2. ✅ Extract and validate references from unstructured text
3. ✅ Acquire academic papers with authentication
4. ✅ Ingest multi-format documents (PDF, web, GitHub)
5. ✅ Create queryable vector databases with embeddings
6. ✅ Validate research accuracy against sources
7. ✅ Provide multiple access methods for knowledge retrieval

Both test pipelines serve as templates for future research automation and knowledge base creation workflows.

---

**Last Updated**: January 5, 2026  
**Pipeline Version**: 1.0  
**Total Test Pipelines**: 2 (HDF5, Jarvis)
