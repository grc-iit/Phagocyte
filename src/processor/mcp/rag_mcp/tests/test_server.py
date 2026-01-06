"""Unit tests for RAG MCP server."""


from rag_mcp.server import (
    ImageSearchResult,
    ListTablesResponse,
    SearchInput,
    SearchResponse,
    SearchResult,
    TableInfo,
)


class TestSearchInput:
    """Test SearchInput model."""

    def test_default_values(self) -> None:
        """Test default input values."""
        input = SearchInput(query="How does caching work?")

        assert input.query == "How does caching work?"
        assert input.db_path == "./lancedb"
        assert input.table == "text_chunks"
        assert input.limit == 5
        assert input.hybrid is False
        assert input.use_hyde is False
        assert input.rerank is False
        assert input.rerank_top_k == 20
        assert input.expand_parents is False

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input = SearchInput(
            query="Python async patterns",
            db_path="/custom/db",
            table="code_chunks",
            limit=20,
            hybrid=True,
            use_hyde=True,
            rerank=True,
            rerank_top_k=50,
            expand_parents=True,
        )

        assert input.db_path == "/custom/db"
        assert input.table == "code_chunks"
        assert input.limit == 20
        assert input.hybrid is True
        assert input.use_hyde is True
        assert input.rerank is True

    def test_table_options(self) -> None:
        """Test table options."""
        for table in ["text_chunks", "code_chunks", "chunks", "image_chunks"]:
            input = SearchInput(query="test", table=table)
            assert input.table == table

    def test_optimization_combinations(self) -> None:
        """Test various optimization combinations."""
        # Fast search (no optimizations)
        input1 = SearchInput(query="test")
        assert not any([input1.hybrid, input1.use_hyde, input1.rerank])

        # Hybrid only
        input2 = SearchInput(query="test", hybrid=True)
        assert input2.hybrid is True
        assert input2.use_hyde is False

        # Full optimizations
        input3 = SearchInput(query="test", hybrid=True, use_hyde=True, rerank=True)
        assert all([input3.hybrid, input3.use_hyde, input3.rerank])


class TestSearchResult:
    """Test SearchResult model."""

    def test_result_creation(self) -> None:
        """Test creating search result."""
        result = SearchResult(
            content="This is the content of the chunk.",
            source_file="document.md",
            score=0.85,
            chunk_id="doc-chunk-001",
            metadata={"section": "Introduction"},
        )

        assert result.content == "This is the content of the chunk."
        assert result.source_file == "document.md"
        assert result.score == 0.85
        assert result.chunk_id == "doc-chunk-001"
        assert result.metadata["section"] == "Introduction"

    def test_minimal_result(self) -> None:
        """Test minimal result without metadata."""
        result = SearchResult(
            content="Content",
            source_file="file.md",
            score=0.5,
            chunk_id="id",
        )

        assert result.metadata == {}


class TestSearchResponse:
    """Test SearchResponse model."""

    def test_response_with_results(self) -> None:
        """Test search response with results."""
        results = [
            SearchResult(
                content="Result 1",
                source_file="doc1.md",
                score=0.9,
                chunk_id="id1",
            ),
            SearchResult(
                content="Result 2",
                source_file="doc2.md",
                score=0.8,
                chunk_id="id2",
            ),
        ]

        response = SearchResponse(
            results=results,
            query="test query",
            optimizations_used=["hybrid", "hyde"],
            total_time_ms=150.5,
        )

        assert len(response.results) == 2
        assert response.query == "test query"
        assert "hybrid" in response.optimizations_used
        assert response.total_time_ms == 150.5

    def test_empty_response(self) -> None:
        """Test empty search response."""
        response = SearchResponse(
            results=[],
            query="no results",
            optimizations_used=[],
            total_time_ms=25.0,
        )

        assert len(response.results) == 0


class TestImageSearchResult:
    """Test ImageSearchResult model."""

    def test_image_result(self) -> None:
        """Test image search result."""
        result = ImageSearchResult(
            figure_id="paper-fig1",
            caption="Figure 1: System Architecture",
            vlm_description="A flowchart showing the system components.",
            image_path="/papers/paper/img/fig1.png",
            source_paper="author-2024-paper",
            score=0.92,
        )

        assert result.figure_id == "paper-fig1"
        assert result.caption == "Figure 1: System Architecture"
        assert result.score == 0.92


class TestTableInfo:
    """Test TableInfo model."""

    def test_table_info(self) -> None:
        """Test table info."""
        info = TableInfo(
            name="text_chunks",
            row_count=10000,
            searchable=True,
        )

        assert info.name == "text_chunks"
        assert info.row_count == 10000
        assert info.searchable is True


class TestListTablesResponse:
    """Test ListTablesResponse model."""

    def test_tables_response(self) -> None:
        """Test tables listing response."""
        response = ListTablesResponse(
            db_path="/path/to/lancedb",
            tables={
                "text_chunks": TableInfo(name="text_chunks", row_count=1000, searchable=True),
                "code_chunks": TableInfo(name="code_chunks", row_count=500, searchable=True),
            },
        )

        assert response.db_path == "/path/to/lancedb"
        assert "text_chunks" in response.tables
        assert response.tables["text_chunks"].row_count == 1000


class TestMCPTools:
    """Test MCP tool registration."""

    def test_server_instantiation(self) -> None:
        """Test MCP server can be imported."""
        from rag_mcp.server import mcp

        assert mcp is not None
        assert mcp.name == "rag-mcp"

    def test_tools_registered(self) -> None:
        """Test key tools are registered."""
        from rag_mcp.server import (
            list_tables,
            search,
            search_images,
        )

        assert search is not None
        assert search_images is not None
        assert list_tables is not None


class TestOptimizations:
    """Test optimization flags combinations."""

    def test_fast_search_no_optimizations(self) -> None:
        """Test fast search configuration."""
        input = SearchInput(query="test")

        optimizations = [input.hybrid, input.use_hyde, input.rerank, input.expand_parents]
        assert not any(optimizations)

    def test_better_recall_hybrid(self) -> None:
        """Test hybrid search for better recall."""
        input = SearchInput(query="test", hybrid=True)

        assert input.hybrid is True
        assert input.use_hyde is False

    def test_knowledge_questions_config(self) -> None:
        """Test configuration for knowledge questions."""
        input = SearchInput(
            query="What are the best practices for caching?",
            use_hyde=True,
            rerank=True,
        )

        assert input.use_hyde is True
        assert input.rerank is True

    def test_code_search_config(self) -> None:
        """Test configuration for code search."""
        input = SearchInput(
            query="async def fetch_data",
            table="code_chunks",
            hybrid=True,
        )

        assert input.table == "code_chunks"
        assert input.hybrid is True

    def test_maximum_precision_config(self) -> None:
        """Test configuration for maximum precision."""
        input = SearchInput(
            query="complex query",
            hybrid=True,
            use_hyde=True,
            rerank=True,
            rerank_top_k=50,
        )

        assert all([input.hybrid, input.use_hyde, input.rerank])
        assert input.rerank_top_k == 50
