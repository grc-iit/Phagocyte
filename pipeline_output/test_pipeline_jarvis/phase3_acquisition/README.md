# Phase 3: Acquisition

## Command
```bash
uv run phagocyte parse batch \
  test_pipeline_jarvis/phase2_parser/step1_regular/batch.json \
  -o test_pipeline_jarvis/phase3_acquisition/papers \
  --concurrent 3
```

## Results
⚠️ **Partially Successful**
- Downloaded: 0
- Failed: 3 (papers not accessible via public sources)

## Note
Using existing Jarvis PDFs from `jarvis/` folder for ingestion instead.
