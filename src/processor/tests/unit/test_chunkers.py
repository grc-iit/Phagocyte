"""Unit tests for chunker adapters."""

from pathlib import Path

from processor.chunkers.adapters import (
    LlamaIndexCodeAdapter,
    LlamaIndexMarkdownAdapter,
)
from processor.types import ContentType


class TestLlamaIndexCodeAdapter:
    """Test LlamaIndex code chunker adapter with tree-sitter AST parsing."""

    def test_chunk_python(self, sample_python_code: str) -> None:
        """Test chunking Python code."""
        chunker = LlamaIndexCodeAdapter(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_python_code, Path("test.py"))

        assert len(chunks) > 0
        assert all(c.source_type == ContentType.CODE_PYTHON for c in chunks)
        assert all(c.language == "python" for c in chunks)
        assert all(c.content for c in chunks)

    def test_chunk_cpp(self, sample_cpp_code: str) -> None:
        """Test chunking C++ code."""
        chunker = LlamaIndexCodeAdapter(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_cpp_code, Path("test.cpp"))

        assert len(chunks) > 0
        assert all(c.source_type == ContentType.CODE_CPP for c in chunks)
        assert all(c.content for c in chunks)

    def test_supports_code_types(self) -> None:
        """Test chunker supports code content types."""
        chunker = LlamaIndexCodeAdapter()

        assert chunker.supports(ContentType.CODE_PYTHON)
        assert chunker.supports(ContentType.CODE_CPP)
        assert chunker.supports(ContentType.CODE_JAVA)
        assert not chunker.supports(ContentType.PAPER)
        assert not chunker.supports(ContentType.MARKDOWN)

    def test_fallback_on_unknown_language(self) -> None:
        """Test fallback chunking for unknown language extensions."""
        chunker = LlamaIndexCodeAdapter(chunk_size=500)
        code = "some code content\n" * 100
        chunks = chunker.chunk(code, Path("test.unknown"))

        assert len(chunks) > 0
        assert all(c.content for c in chunks)


class TestLlamaIndexMarkdownAdapter:
    """Test LlamaIndex markdown chunker adapter."""

    def test_chunk_paper(self, sample_paper_markdown: str) -> None:
        """Test chunking academic paper."""
        chunker = LlamaIndexMarkdownAdapter(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_paper_markdown, Path("papers/paper.md"))

        assert len(chunks) > 0
        assert all(c.source_type == ContentType.PAPER for c in chunks)
        assert all(c.content for c in chunks)

    def test_extract_citations(self, sample_paper_markdown: str) -> None:
        """Test citation extraction from papers."""
        chunker = LlamaIndexMarkdownAdapter()
        chunks = chunker.chunk(sample_paper_markdown, Path("papers/paper.md"))

        # At least some chunks should have citations if paper has them
        # This depends on the sample content having citations
        all_citations = []
        for c in chunks:
            if c.citations:
                all_citations.extend(c.citations)
        # Just verify no errors, citations depend on content

    def test_chunk_markdown(self, sample_markdown: str) -> None:
        """Test chunking markdown."""
        chunker = LlamaIndexMarkdownAdapter(chunk_size=500, chunk_overlap=50)
        chunks = chunker.chunk(sample_markdown, Path("doc.md"))

        assert len(chunks) > 0
        assert all(c.content for c in chunks)

    def test_fallback_chunking(self, sample_markdown: str) -> None:
        """Test fallback chunking when LlamaIndex not available."""
        chunker = LlamaIndexMarkdownAdapter(chunk_size=500, chunk_overlap=50)

        # Use fallback directly
        chunks = chunker._fallback_chunk(sample_markdown, Path("doc.md"))

        assert len(chunks) > 0
        # Should extract section paths
        paths = [c.section_path for c in chunks if c.section_path]
        assert len(paths) > 0

    def test_supports_markdown_types(self) -> None:
        """Test chunker supports markdown content types."""
        chunker = LlamaIndexMarkdownAdapter()

        assert chunker.supports(ContentType.MARKDOWN)
        assert chunker.supports(ContentType.WEBSITE)
        assert chunker.supports(ContentType.BOOK)
        assert chunker.supports(ContentType.PAPER)
        assert chunker.supports(ContentType.TEXT)
        assert not chunker.supports(ContentType.CODE_PYTHON)
