# Usage Examples

## Setup

```bash
# Set API key
export GOOGLE_API_KEY="your-google-api-key"
```

---

## CLI Commands

### Basic Research

```bash
# Simple research query
researcher research "What are the latest advances in quantum computing?"

# With custom output directory
researcher research "Compare transformer architectures" -o ./my_research

# With verbose output (shows thinking steps)
researcher research "Survey of LLM agents" -v
```

### Advanced Options

```bash
# Custom output format instructions
researcher research "Renewable energy trends" --format "Include comparison table and bullet points"

# Disable streaming (use polling instead)
researcher research "Climate change solutions" --no-stream

# Set maximum wait time (default: 3600 seconds)
researcher research "AI safety research" --max-wait 7200

# Full example with all options
researcher research "Retrieval Augmented Generation" \
    -o ./demo_output \
    --format "Include comparison table and key papers" \
    --max-wait 7200 \
    -v
```

---

## Example Research Topics

```bash
# AI/ML Research
researcher research "What is RAG (Retrieval Augmented Generation)?" -o ./rag_research
researcher research "Compare transformer architectures for NLP" -o ./transformers
researcher research "Survey of LLM agents and their architectures" -o ./llm_agents
researcher research "Machine learning for climate modeling" -o ./climate_ml

# Science & Technology
researcher research "Latest advances in quantum computing" -o ./quantum
researcher research "Renewable energy trends and technologies" -o ./renewable
researcher research "AI safety research: key trends and challenges" -o ./ai_safety

# Specific Analysis
researcher research "Compare GraphRAG vs traditional RAG approaches" \
    --format "Include comparison table with pros/cons" \
    -o ./graphrag_comparison
```

---

## Output Structure

After running a research command, you'll find:

```
output/research/
├── research_report.md       # Main research report with citations
├── research_metadata.json   # Query, timing, interaction info
└── thinking_steps.md        # Agent reasoning (if --verbose)
```

The `research_stream.md` file is also created in verbose mode to capture real-time output.

---

## Programmatic Usage

```python
import asyncio
from researcher.deep_research import DeepResearcher, ResearchConfig

async def main():
    # Configure research
    config = ResearchConfig(
        output_format="Include comparison tables",
        max_wait_time=3600,
        enable_streaming=True,
        enable_thinking=True,
    )
    
    # Create researcher
    researcher = DeepResearcher(config=config)
    
    # Progress callback
    def on_progress(text: str):
        if text.startswith("[Thinking]"):
            print(f"Thinking: {text}")
        else:
            print(text, end="")
    
    # Conduct research
    result = await researcher.research(
        "What are the latest advances in quantum computing?",
        on_progress=on_progress
    )
    
    if result.succeeded:
        print(f"\nResearch completed in {result.duration_seconds:.1f}s")
        result.save("./output/research")
    else:
        print(f"Research failed: {result.error}")

asyncio.run(main())
```

### Quick Convenience Function

```python
from researcher.deep_research import deep_research

result = await deep_research(
    "Key trends in AI safety research",
    output_format="Format as an executive summary with bullet points."
)
print(result.report)
```
