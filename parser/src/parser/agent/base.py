"""Base classes for agent-based reference parsing."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..parser import ReferenceType, ParsedReference


@dataclass
class AgentParseResult:
    """Result from agent-based parsing."""
    
    references: list[ParsedReference]
    raw_response: str
    model: str
    agent_type: str
    tokens_used: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "references": [
                {
                    "type": ref.type.value,
                    "value": ref.value,
                    "title": ref.title,
                    "authors": ref.authors,
                    "year": ref.year,
                    "url": ref.url,
                    "context": ref.context,
                    "metadata": ref.metadata,
                }
                for ref in self.references
            ],
            "raw_response": self.raw_response,
            "model": self.model,
            "agent_type": self.agent_type,
            "tokens_used": self.tokens_used,
            "metadata": self.metadata,
        }


class AgentParser(ABC):
    """Abstract base class for agent-based reference parsing."""
    
    # System prompt for reference extraction
    SYSTEM_PROMPT = """You are an expert research assistant specialized in extracting and categorizing references from research documents.

Your task is to analyze the provided research document and extract ALL references mentioned in it. Categorize each reference into one of these types:

1. **github** - GitHub repositories (format: owner/repo)
2. **arxiv** - arXiv papers (format: XXXX.XXXXX)
3. **doi** - DOI identifiers (format: 10.XXXX/XXXXX)
4. **paper** - ONLY peer-reviewed academic papers published in journals/conferences (include title, authors, year)
5. **blog** - Blog posts and technical articles (Towards Data Science, Medium, dev.to, company blogs)
6. **pdf** - Direct PDF links (ANY URL ending in .pdf)
7. **youtube** - YouTube videos (video ID or URL)
8. **podcast** - Podcast references
9. **book** - Books (include ISBN if available) - NOT academic papers
10. **website** - General websites, documentation, tutorials

IMPORTANT RULES FOR PAPER vs BLOG:
- Use "paper" ONLY for peer-reviewed academic papers with authors like "Author et al."
- Use "blog" for articles on: Towards Data Science, Medium, dev.to, company tech blogs, personal blogs
- Use "website" for documentation, tutorials, and general websites
- Books are only for actual books (with ISBN), not research papers
- PDF URLs are any URL ending in .pdf - extract these as type "pdf"

For each reference, extract:
- type: One of the categories above
- value: The identifier/URL/title
- title: Title if available
- authors: Authors if available  
- year: Publication year if available
- url: Full URL if available (ALWAYS include URLs when present)
- context: Brief context of how it's mentioned

Return your response as a JSON array of objects with these fields. Be thorough and extract EVERY reference mentioned in the document, including those in footnotes, references sections, and inline citations.

Pay special attention to:
- Direct PDF links (e.g., openaccess.thecvf.com/.../.pdf)
- Documentation sites (e.g., huggingface.co/docs, pytorch.org/tutorials)
- Blog posts (e.g., jalammar.github.io, towardsdatascience.com)
- Wikipedia articles
- Conference paper URLs (papers.nips.cc, aclanthology.org, openreview.net)

Example output format:
```json
[
  {
    "type": "arxiv",
    "value": "2301.00234",
    "title": "Some Paper Title",
    "authors": "Vaswani et al.",
    "year": "2017",
    "url": "https://arxiv.org/abs/2301.00234",
    "context": "The transformer architecture introduced in..."
  },
  {
    "type": "pdf",
    "value": "https://example.com/paper.pdf",
    "title": "",
    "authors": "",
    "year": "",
    "url": "https://example.com/paper.pdf",
    "context": "Available at..."
  },
  {
    "type": "website",
    "value": "https://jalammar.github.io/illustrated-transformer/",
    "title": "The Illustrated Transformer",
    "authors": "Jay Alammar",
    "year": "2018",
    "url": "https://jalammar.github.io/illustrated-transformer/",
    "context": "Visual explanation available at..."
  }
]
```

Extract ALL references - be comprehensive. Do not miss any URLs."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        """Initialize the agent.
        
        Args:
            api_key: API key for the agent service
            model: Model to use (e.g., 'claude-sonnet-4-20250514', 'gemini-2.0-flash')
        """
        self.api_key = api_key
        self.model = model or self.default_model
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model for this agent."""
        pass
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Type identifier for this agent."""
        pass
    
    @abstractmethod
    async def parse_async(self, text: str) -> AgentParseResult:
        """Parse text asynchronously and extract references.
        
        Args:
            text: Document text to parse
            
        Returns:
            AgentParseResult with extracted references
        """
        pass
    
    def parse(self, text: str) -> AgentParseResult:
        """Parse text synchronously and extract references.
        
        Args:
            text: Document text to parse
            
        Returns:
            AgentParseResult with extracted references
        """
        import asyncio
        return asyncio.run(self.parse_async(text))
    
    def parse_file(self, file_path: Path) -> AgentParseResult:
        """Parse a file and extract references.
        
        Args:
            file_path: Path to file
            
        Returns:
            AgentParseResult with extracted references
        """
        file_path = Path(file_path)
        
        if file_path.suffix == ".json":
            import json
            with open(file_path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                text = data.get("report", data.get("content", str(data)))
                if text is None:
                    text = str(data)
            else:
                text = str(data)
        else:
            text = file_path.read_text()
        
        return self.parse(str(text))
    
    def _parse_response_json(self, response_text: str) -> list[ParsedReference]:
        """Parse JSON response from agent into ParsedReference list.
        
        Args:
            response_text: Raw response from agent
            
        Returns:
            List of ParsedReference objects
        """
        import json
        import re
        
        # Try to extract JSON from the response
        # Look for JSON array in the response
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if not json_match:
            # Try to find JSON in code blocks
            json_match = re.search(r'```(?:json)?\s*(\[[\s\S]*?\])\s*```', response_text)
            if json_match:
                json_str = json_match.group(1)
            else:
                return []
        else:
            json_str = json_match.group(0)
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            # Try to fix common JSON issues
            json_str = json_str.replace("'", '"')
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                return []
        
        references = []
        type_map = {
            "github": ReferenceType.GITHUB,
            "arxiv": ReferenceType.ARXIV,
            "doi": ReferenceType.DOI,
            "paper": ReferenceType.PAPER,
            "blog": ReferenceType.BLOG,
            "pdf": ReferenceType.PDF,
            "youtube": ReferenceType.YOUTUBE,
            "podcast": ReferenceType.PODCAST,
            "book": ReferenceType.BOOK,
            "website": ReferenceType.WEBSITE,
        }
        
        for item in data:
            if not isinstance(item, dict):
                continue
            
            ref_type_str = item.get("type", "website").lower()
            ref_type = type_map.get(ref_type_str, ReferenceType.WEBSITE)
            
            ref = ParsedReference(
                type=ref_type,
                value=item.get("value", ""),
                title=item.get("title", ""),
                authors=item.get("authors", ""),
                year=item.get("year", ""),
                url=item.get("url"),
                context=item.get("context", ""),
                metadata={"source": "agent", "agent_type": self.agent_type},
            )
            
            if ref.value:  # Only add if value is not empty
                references.append(ref)
        
        return references
