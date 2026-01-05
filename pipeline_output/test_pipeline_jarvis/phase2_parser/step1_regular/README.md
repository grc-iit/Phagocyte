# Phase 2: Parser - Regular Parsing (Regex)

## Command
```bash
uv run phagocyte parse refs \
  /home/shazzadul/Illinois_Tech/Spring26/RA/Github/new/Phagocyte/test_pipeline_jarvis/phase1_research/research/research_report.md \
  -o /home/shazzadul/Illinois_Tech/Spring26/RA/Github/new/Phagocyte/test_pipeline_jarvis/phase2_parser/step1_regular \
  --export-batch --export-dois
```

## Results
✅ **Completed Successfully**

Found **14 references**:
- GitHub: 2
- Papers: 3
- PDFs: 3
- Books: 1
- Websites: 5

## Output Files
- `references.json` - Structured JSON with all references
- `references.md` - Human-readable markdown format
- `batch.json` - 3 papers ready for download
- `dois.txt` - 0 DOIs for BibTeX conversion

## Next Step
Phase 3: Acquire papers from batch.json
