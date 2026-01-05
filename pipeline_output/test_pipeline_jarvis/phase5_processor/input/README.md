# Phase 4: Ingestor

## Commands
```bash
# Ingest PDFs
uv run phagocyte ingest file jarvis/cernuda2024jarvis.pdf \
  -o test_pipeline_jarvis/phase4_ingestor/pdfs/cernuda2024jarvis

uv run phagocyte ingest file jarvis/pdsw24_wip_session2_wip1.pdf \
  -o test_pipeline_jarvis/phase4_ingestor/pdfs/pdsw24_wip

# Clone and ingest GitHub repo
uv run phagocyte ingest clone https://github.com/iowarp/runtime-deployment \
  -o test_pipeline_jarvis/phase4_ingestor/github/runtime-deployment \
  --shallow --max-files 50
```

## Results
✅ **Completed Successfully**

## Output
- `pdfs/cernuda2024jarvis/` - Jarvis paper markdown
- `pdfs/pdsw24_wip/` - PDSW WIP slides markdown
- `github/runtime-deployment/` - 50 files from GitHub repo

## Next Step
Phase 5: Process markdown into LanceDB vector database
