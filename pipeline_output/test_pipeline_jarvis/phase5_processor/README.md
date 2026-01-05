# Phase 5: Processor

## Command
```bash
uv run phagocyte process run \
  /home/shazzadul/Illinois_Tech/Spring26/RA/Github/new/Phagocyte/test_pipeline_jarvis/phase5_processor/input \
  -o /home/shazzadul/Illinois_Tech/Spring26/RA/Github/new/Phagocyte/test_pipeline_jarvis/phase5_processor/lancedb \
  --batch-size 50
```

## Input Files
- `research_report.md` - AI-generated research report (15KB)
- `github_com_iowarp_runtime-deployment.md` - GitHub repo (172KB, 50 files)
- `cernuda2024jarvis_pdf.md` - Jarvis paper
- `pdsw24_wip_session2_wip1_pdf.md` - PDSW WIP slides
- `README.md` - GitHub README

## Processing
✅ **In Progress**

- Files: 5
- Chunks created: 144
- Backend: Ollama (nomic-embed-text)
- Mode: Incremental
- Tables: Separate (text_chunks, code_chunks)

## Next Step
Phase 6: Search and validate the vector database
