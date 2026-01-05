# Phase 3: Ingestor - Document Conversion to Markdown

## Overview
This phase uses the `ingestor` module to convert various document formats into clean, structured markdown with extracted images.

## Steps Executed

### Step 1: PDF Ingestion
Converted downloaded academic papers to markdown using Docling ML extraction.

```bash
cd ingestor && uv run ingestor batch \
  ../pipeline_output/phase2_parser/step4_acquisition/papers/ \
  -o ../pipeline_output/phase3_ingestor/pdfs \
  --recursive -v
```

### Step 2: GitHub Repository Ingestion
Extracted content from the HDF5 GitHub repository.

```bash
cd ingestor && uv run ingestor ingest \
  "https://github.com/HDFGroup/hdf5" \
  -o ../pipeline_output/phase3_ingestor/github -v
```

### Step 3: Web Documentation Crawling
Crawled the HDF Group documentation website.

```bash
cd ingestor && uv run ingestor crawl \
  "https://support.hdfgroup.org/documentation/" \
  -o ../pipeline_output/phase3_ingestor/web \
  --max-depth 2 --max-pages 20 -v
```

## Input

| Source Type | Input | Count |
|-------------|-------|-------|
| **PDFs** | Downloaded academic papers | 4 papers |
| **GitHub** | https://github.com/HDFGroup/hdf5 | 1 repo |
| **Web** | https://support.hdfgroup.org/documentation/ | 40 pages |

## Output Structure

```
phase3_ingestor/
├── pdfs/                           # PDF extractions
│   ├── Byna_2020_ExaHDF5_.../
│   │   ├── *.md                    # Extracted markdown
│   │   └── img/                    # Extracted figures
│   ├── Chowdhury_2023_.../
│   ├── Tang_2019_.../
│   └── Tang_2022_.../
├── github/                         # GitHub repo extraction
│   └── github_com_HDFGroup_hdf5/
│       └── github_com_HDFGroup_hdf5.md
├── web/                            # Web crawl results (40 pages)
│   ├── support_hdfgroup_org_documentation/
│   ├── support_hdfgroup_org_documentation_hdf5_latest/
│   └── ... (40 page directories)
├── pdfs_execution.log
├── github_execution.log
└── web_execution.log
```

## Results Summary

### PDF Ingestion

| Paper | Status | Time | Figures |
|-------|--------|------|---------|
| Byna 2020 (ExaHDF5) | ✅ | 63.5s | Yes |
| Chowdhury 2023 (Async I/O) | ✅ | 54.8s | Yes |
| Tang 2019 (Background Threads) | ✅ | 39.8s | Yes |
| Tang 2022 (Parallel I/O) | ✅ | 52.6s | Yes |

**Total**: 4 PDFs processed, 0 errors

### GitHub Repository

| Repository | Status | Output |
|------------|--------|--------|
| HDFGroup/hdf5 | ✅ | `github_com_HDFGroup_hdf5.md` |

### Web Crawling

| Metric | Value |
|--------|-------|
| **Pages crawled** | 40 |
| **Pages successful** | 37 |
| **Pages failed** | 3 (timeout) |
| **Strategy** | BFS |
| **Max depth** | 2 |

## Validation

| Check | Status | Notes |
|-------|--------|-------|
| PDF extraction | ✅ | 4/4 papers converted |
| Figure extraction | ✅ | Images extracted to img/ folders |
| GitHub ingestion | ✅ | Repository content extracted |
| Web crawling | ⚠️ | 37/40 pages (3 timeouts) |
| Markdown quality | ✅ | Structure preserved, citations linked |

## Features Used

### PDF Extraction (Docling)
- Multi-column layout handling
- Table extraction to markdown
- Figure extraction with captions
- Citation linking (`[7]` → `[[7]](#ref-7)`)
- LaTeX equation extraction
- OCR fallback for scanned content

### GitHub Extraction
- Repository metadata
- README content
- Key file extraction

### Web Crawling (Crawl4AI)
- BFS strategy
- Same-domain restriction
- Clean markdown output
- Link preservation

## Issues / Problems

| Issue | Severity | Description |
|-------|----------|-------------|
| OCR warnings | ℹ️ Info | RapidOCR empty results for some pages (normal for text-based PDFs) |
| Web timeouts | ⚠️ Warning | 3 pages timed out: forum.hdfgroup.org, www.hdfgroup.org, website-survey |
| Processing time | ℹ️ Info | PDF processing takes 40-65 seconds per paper on CPU |

## Output Statistics

| Type | Files | Total Size |
|------|-------|------------|
| PDF markdowns | 4 | ~200 KB |
| GitHub markdown | 1 | ~15 KB |
| Web markdowns | 37 | ~500 KB |
| Images | ~20 | ~5 MB |

## Next Step
→ Final: Create comprehensive pipeline README
