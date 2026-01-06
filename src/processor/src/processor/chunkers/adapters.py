"""Adapters wrapping LlamaIndex chunkers with tree-sitter AST parsing."""

from pathlib import Path
from typing import Any

from llama_index.core import Document
from llama_index.core.node_parser import CodeSplitter, MarkdownNodeParser

from ..types import Chunk, ContentType
from .base import BaseChunker


class LlamaIndexCodeAdapter(BaseChunker):
    """Uses LlamaIndex CodeSplitter with tree-sitter for true AST-based chunking.

    This provides semantic code chunking that:
    - Respects function/class/method boundaries
    - Never splits mid-statement
    - Preserves docstrings with their functions
    - Supports 165+ languages via tree-sitter
    """

    content_types = [
        ContentType.CODE_CPP,
        ContentType.CODE_PYTHON,
        ContentType.CODE_SHELL,
        ContentType.CODE_JAVA,
        ContentType.CODE_JS,
        ContentType.CODE_TS,
        ContentType.CODE_GO,
        ContentType.CODE_RUST,
        ContentType.CODE_OTHER,
    ]

    # Map file extensions to tree-sitter language names
    LANGUAGE_MAP: dict[str, str] = {
        # Python
        ".py": "python",
        ".pyw": "python",
        ".pyi": "python",
        # JavaScript/TypeScript
        ".js": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        # Systems languages
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".hxx": "cpp",
        ".rs": "rust",
        ".go": "go",
        # JVM languages
        ".java": "java",
        ".kt": "kotlin",
        ".scala": "scala",
        # Other
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
        ".cs": "c_sharp",
        ".lua": "lua",
        ".pl": "perl",
        ".hs": "haskell",
        ".ex": "elixir",
        ".exs": "elixir",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
    }

    # Default chunking parameters optimized for code
    default_chunk_lines = 40
    default_chunk_overlap_lines = 15
    default_max_chars = 4000  # ~1024 tokens

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
        chunk_lines: int | None = None,
        chunk_overlap_lines: int | None = None,
    ):
        """Initialize code chunker.

        Args:
            chunk_size: Max characters per chunk (overrides default_max_chars)
            chunk_overlap: Not used for CodeSplitter (uses lines instead)
            chunk_lines: Target lines per chunk
            chunk_overlap_lines: Overlap lines between chunks
        """
        super().__init__(chunk_size, chunk_overlap)
        self.chunk_lines = chunk_lines or self.default_chunk_lines
        self.chunk_overlap_lines = chunk_overlap_lines or self.default_chunk_overlap_lines
        self.max_chars = chunk_size or self.default_max_chars

    def chunk(
        self,
        content: str,
        source_file: Path,
        metadata: dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """Chunk code using AST-based splitting via tree-sitter.

        Args:
            content: Source code content
            source_file: Path to source file
            metadata: Optional additional metadata

        Returns:
            List of Chunk objects with semantically coherent code
        """
        ext = source_file.suffix.lower()
        language = self.LANGUAGE_MAP.get(ext, "python")

        try:
            # Create AST-based splitter
            splitter = CodeSplitter(
                language=language,
                chunk_lines=self.chunk_lines,
                chunk_lines_overlap=self.chunk_overlap_lines,
                max_chars=self.max_chars,
            )

            # Create LlamaIndex document
            doc = Document(text=content, metadata={"source": str(source_file)})

            # Get AST-based nodes
            nodes = splitter.get_nodes_from_documents([doc])

            # Convert to our Chunk type
            chunks = []
            for _i, node in enumerate(nodes):
                content_type = self._get_content_type(ext)

                chunk = Chunk.create(
                    content=node.get_content(),
                    source_file=source_file,
                    source_type=content_type,
                    language=language,
                    **(metadata or {}),
                )
                chunks.append(chunk)

            return chunks

        except Exception as e:
            # Fallback to simple splitting if tree-sitter fails for this language
            return self._fallback_chunk(content, source_file, metadata, str(e))

    def _fallback_chunk(
        self,
        content: str,
        source_file: Path,
        metadata: dict[str, Any] | None,
        error: str,
    ) -> list[Chunk]:
        """Fallback chunking when tree-sitter parsing fails."""
        # Simple line-based splitting
        lines = content.split("\n")
        chunks = []
        current_chunk_lines: list[str] = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            if current_size + line_size > self.max_chars and current_chunk_lines:
                # Save current chunk
                chunk_content = "\n".join(current_chunk_lines)
                chunk = Chunk.create(
                    content=chunk_content,
                    source_file=source_file,
                    source_type=self._get_content_type(source_file.suffix.lower()),
                    language=source_file.suffix.lstrip("."),
                    **(metadata or {}),
                )
                chunks.append(chunk)

                # Start new chunk with overlap
                overlap_lines = current_chunk_lines[-self.chunk_overlap_lines:]
                current_chunk_lines = overlap_lines
                current_size = sum(len(line) + 1 for line in current_chunk_lines)

            current_chunk_lines.append(line)
            current_size += line_size

        # Save remaining content
        if current_chunk_lines:
            chunk_content = "\n".join(current_chunk_lines)
            chunk = Chunk.create(
                content=chunk_content,
                source_file=source_file,
                source_type=self._get_content_type(source_file.suffix.lower()),
                language=source_file.suffix.lstrip("."),
                **(metadata or {}),
            )
            chunks.append(chunk)

        return chunks

    def _get_content_type(self, ext: str) -> ContentType:
        """Get ContentType from file extension."""
        ext_map = {
            ".cpp": ContentType.CODE_CPP,
            ".cc": ContentType.CODE_CPP,
            ".c": ContentType.CODE_CPP,
            ".h": ContentType.CODE_CPP,
            ".hpp": ContentType.CODE_CPP,
            ".py": ContentType.CODE_PYTHON,
            ".pyw": ContentType.CODE_PYTHON,
            ".sh": ContentType.CODE_SHELL,
            ".bash": ContentType.CODE_SHELL,
            ".java": ContentType.CODE_JAVA,
            ".js": ContentType.CODE_JS,
            ".ts": ContentType.CODE_TS,
            ".go": ContentType.CODE_GO,
            ".rs": ContentType.CODE_RUST,
        }
        return ext_map.get(ext, ContentType.CODE_OTHER)

    def supports(self, content_type: ContentType) -> bool:
        return content_type in self.content_types


class LlamaIndexMarkdownAdapter(BaseChunker):
    """Uses LlamaIndex's MarkdownNodeParser for markdown and paper documents.

    Provides header-hierarchy aware splitting that respects markdown structure.
    Now also used for papers since they come from the ingestor with proper structure.
    """

    content_types = [
        ContentType.MARKDOWN,
        ContentType.WEBSITE,
        ContentType.BOOK,
        ContentType.YOUTUBE,
        ContentType.PAPER,
        ContentType.TEXT,
    ]

    default_chunk_size = 4000  # ~1024 tokens
    default_chunk_overlap = 500  # ~128 tokens

    def chunk(
        self,
        content: str,
        source_file: Path,
        metadata: dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """Chunk markdown/paper using header-based splitting."""
        try:
            # Create LlamaIndex document
            doc = Document(text=content, metadata={"source": str(source_file)})

            # Parse with markdown-aware parser
            parser = MarkdownNodeParser()
            nodes = parser.get_nodes_from_documents([doc])

            chunks = []
            for _i, node in enumerate(nodes):
                # Extract section path from metadata if available
                section_path = None
                if hasattr(node, "metadata"):
                    headers = []
                    for key in ["Header_1", "Header_2", "Header_3"]:
                        if key in node.metadata:
                            headers.append(node.metadata[key])
                    if headers:
                        section_path = " > ".join(headers)

                # Extract citations for papers
                citations = []
                node_content = node.get_content()
                if self._get_content_type(source_file) == ContentType.PAPER:
                    citations = self._extract_citations(node_content)

                chunk = Chunk.create(
                    content=node_content,
                    source_file=source_file,
                    source_type=self._get_content_type(source_file),
                    section_path=section_path,
                    citations=citations if citations else None,
                    **(metadata or {}),
                )
                chunks.append(chunk)

            return chunks

        except ImportError:
            # Fallback to simple markdown splitting if LlamaIndex not available
            return self._fallback_chunk(content, source_file, metadata)

    def _extract_citations(self, text: str) -> list[str]:
        """Extract citation references from text."""
        import re

        # Match common citation patterns: [1], [ref-1], [[1]], etc.
        patterns = [
            r"\[(\d+)\]",  # [1]
            r"\[\[(\d+)\]\]",  # [[1]]
            r"\[ref-(\d+)\]",  # [ref-1]
        ]

        citations = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            citations.update(matches)

        return sorted(list(citations), key=lambda x: int(x) if x.isdigit() else x)

    def _fallback_chunk(
        self,
        content: str,
        source_file: Path,
        metadata: dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """Fallback to header-based splitting without LlamaIndex."""
        import re

        # Split on headers
        header_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

        sections = []
        last_end = 0
        current_path: list[str] = []

        for match in header_pattern.finditer(content):
            # Save content before this header
            if last_end < match.start():
                section_text = content[last_end : match.start()].strip()
                if section_text:
                    sections.append(
                        {
                            "content": section_text,
                            "path": " > ".join(current_path) if current_path else None,
                        }
                    )

            # Update path based on header level
            level = len(match.group(1))
            title = match.group(2).strip()

            # Trim path to current level
            current_path = current_path[: level - 1]
            current_path.append(title)

            last_end = match.end()

        # Add remaining content
        if last_end < len(content):
            section_content = content[last_end:].strip()
            if section_content:
                sections.append(
                    {
                        "content": section_content,
                        "path": " > ".join(current_path) if current_path else None,
                    }
                )

        # Convert sections to chunks
        chunks = []
        for section in sections:
            section_text_content: str = section["content"] or ""

            # Further split if section is too large
            if len(section_text_content) > self.chunk_size:
                # Simple character-based splitting for oversized sections
                for i in range(0, len(section_text_content), self.chunk_size - self.chunk_overlap):
                    sub_content = section_text_content[i:i + self.chunk_size]
                    chunk = Chunk.create(
                        content=sub_content,
                        source_file=source_file,
                        source_type=self._get_content_type(source_file),
                        section_path=section["path"],
                        **(metadata or {}),
                    )
                    chunks.append(chunk)
            else:
                chunk = Chunk.create(
                    content=section_text_content,
                    source_file=source_file,
                    source_type=self._get_content_type(source_file),
                    section_path=section["path"],
                    **(metadata or {}),
                )
                chunks.append(chunk)

        return chunks

    def _get_content_type(self, source_file: Path) -> ContentType:
        """Determine content type from file path."""
        path_str = str(source_file).lower()
        if "paper" in path_str:
            return ContentType.PAPER
        elif "website" in path_str:
            return ContentType.WEBSITE
        elif "book" in path_str:
            return ContentType.BOOK
        elif "youtube" in path_str:
            return ContentType.YOUTUBE
        return ContentType.MARKDOWN

    def supports(self, content_type: ContentType) -> bool:
        return content_type in self.content_types
