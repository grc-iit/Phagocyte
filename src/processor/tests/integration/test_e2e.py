"""End-to-end integration tests for processor pipeline."""

import json
from pathlib import Path

import lancedb
import pytest

from processor.database.exporter import DatabaseExporter, DatabaseImporter


class TestDatabaseExport:
    """Test database export functionality."""

    @pytest.fixture
    def sample_db(self, tmp_path: Path) -> Path:
        """Create a sample LanceDB with test data."""
        db_path = tmp_path / "test_db"
        db = lancedb.connect(str(db_path))

        # Create text_chunks table
        text_data = [
            {
                "id": "text-1",
                "content": "Sample text chunk content",
                "hash": "abc123",
                "vector": [0.1] * 768,
                "source_file": "test.md",
                "source_type": "markdown",
            },
            {
                "id": "text-2",
                "content": "Another text chunk",
                "hash": "def456",
                "vector": [0.2] * 768,
                "source_file": "test2.md",
                "source_type": "paper",
            },
        ]
        db.create_table("text_chunks", text_data)

        # Create code_chunks table
        code_data = [
            {
                "id": "code-1",
                "content": "def hello(): pass",
                "hash": "ghi789",
                "vector": [0.3] * 768,
                "source_file": "test.py",
                "language": "python",
            },
        ]
        db.create_table("code_chunks", code_data)

        return db_path

    def test_list_tables(self, sample_db: Path) -> None:
        """Test listing tables."""
        exporter = DatabaseExporter(str(sample_db))
        tables = exporter.list_tables()

        assert "text_chunks" in tables
        assert "code_chunks" in tables

    def test_get_table_stats(self, sample_db: Path) -> None:
        """Test getting table statistics."""
        exporter = DatabaseExporter(str(sample_db))
        stats = exporter.get_table_stats()

        assert "text_chunks" in stats
        assert stats["text_chunks"]["row_count"] == 2

        assert "code_chunks" in stats
        assert stats["code_chunks"]["row_count"] == 1

    def test_export_to_lance(self, sample_db: Path, tmp_path: Path) -> None:
        """Test exporting to Lance format."""
        exporter = DatabaseExporter(str(sample_db))
        output_dir = tmp_path / "export"

        result = exporter.export_to_lance(output_dir)

        assert result["text_chunks"] == 2
        assert result["code_chunks"] == 1

        # Verify exported database
        exported_db = lancedb.connect(str(output_dir))
        assert "text_chunks" in exported_db.table_names()
        assert exported_db.open_table("text_chunks").count_rows() == 2

    def test_export_to_csv(self, sample_db: Path, tmp_path: Path) -> None:
        """Test exporting to CSV format."""
        exporter = DatabaseExporter(str(sample_db))
        output_dir = tmp_path / "export_csv"

        result = exporter.export_to_csv(output_dir, include_vectors=False)

        assert result["text_chunks"] == 2
        assert result["code_chunks"] == 1

        # Verify CSV files exist
        assert (output_dir / "text_chunks.csv").exists()
        assert (output_dir / "code_chunks.csv").exists()

    def test_export_manifest(self, sample_db: Path, tmp_path: Path) -> None:
        """Test writing export manifest."""
        exporter = DatabaseExporter(str(sample_db))
        output_dir = tmp_path / "export"
        output_dir.mkdir(parents=True)

        tables = {"text_chunks": 2, "code_chunks": 1}
        manifest_path = exporter.export_manifest(output_dir, "lance", tables)

        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text())

        assert manifest["format"] == "lance"
        assert manifest["tables"] == tables
        assert manifest["total_rows"] == 3

    def test_export_specific_tables(self, sample_db: Path, tmp_path: Path) -> None:
        """Test exporting specific tables only."""
        exporter = DatabaseExporter(str(sample_db))
        output_dir = tmp_path / "export"

        result = exporter.export_to_lance(output_dir, tables=["text_chunks"])

        assert "text_chunks" in result
        assert "code_chunks" not in result


class TestDatabaseImport:
    """Test database import functionality."""

    @pytest.fixture
    def exported_db(self, tmp_path: Path) -> Path:
        """Create an exported database to import from."""
        export_dir = tmp_path / "export"
        db = lancedb.connect(str(export_dir))

        data = [
            {
                "id": "import-1",
                "content": "Imported content",
                "vector": [0.5] * 768,
            },
        ]
        db.create_table("imported_table", data)

        # Write manifest
        manifest = {
            "export_time": "2024-01-01T00:00:00",
            "source_database": "/original/path",
            "format": "lance",
            "tables": {"imported_table": 1},
            "total_rows": 1,
        }
        (export_dir / "export_manifest.json").write_text(json.dumps(manifest))

        return export_dir

    def test_import_from_lance(self, exported_db: Path, tmp_path: Path) -> None:
        """Test importing from Lance format."""
        target_path = tmp_path / "imported"
        importer = DatabaseImporter(str(target_path))

        result = importer.import_from_lance(exported_db)

        assert "imported_table" in result
        assert result["imported_table"] == 1

        # Verify imported data
        db = lancedb.connect(str(target_path))
        assert "imported_table" in db.table_names()

    def test_read_manifest(self, exported_db: Path, tmp_path: Path) -> None:
        """Test reading export manifest."""
        importer = DatabaseImporter(str(tmp_path / "target"))
        manifest = importer.read_manifest(exported_db)

        assert manifest is not None
        assert manifest["format"] == "lance"
        assert manifest["total_rows"] == 1


class TestInputReduced:
    """Test with input_reduced sample data."""

    def test_input_reduced_structure(self, input_reduced_dir: Path) -> None:
        """Test that input_reduced has expected structure."""
        if not input_reduced_dir.exists():
            pytest.skip("input_reduced/ not found")

        # Check expected directories exist
        expected = ["papers", "codebases", "websites"]
        for dirname in expected:
            dir_path = input_reduced_dir / dirname
            assert dir_path.exists(), f"Missing: {dirname}"
            assert dir_path.is_dir()

    def test_papers_have_content(self, input_reduced_dir: Path) -> None:
        """Test that papers have markdown content."""
        if not input_reduced_dir.exists():
            pytest.skip("input_reduced/ not found")

        papers_dir = input_reduced_dir / "papers"
        if not papers_dir.exists():
            pytest.skip("No papers in input_reduced")

        md_files = list(papers_dir.rglob("*.md"))
        assert len(md_files) > 0, "No markdown files in papers"

    def test_codebases_have_code(self, input_reduced_dir: Path) -> None:
        """Test that codebases have source code."""
        if not input_reduced_dir.exists():
            pytest.skip("input_reduced/ not found")

        codebases_dir = input_reduced_dir / "codebases"
        if not codebases_dir.exists():
            pytest.skip("No codebases in input_reduced")

        code_extensions = {".py", ".ts", ".js", ".go", ".rs", ".cpp", ".h"}
        code_files = []
        for ext in code_extensions:
            code_files.extend(codebases_dir.rglob(f"*{ext}"))

        assert len(code_files) > 0, "No code files in codebases"

    def test_websites_have_markdown(self, input_reduced_dir: Path) -> None:
        """Test that websites have markdown content."""
        if not input_reduced_dir.exists():
            pytest.skip("input_reduced/ not found")

        websites_dir = input_reduced_dir / "websites"
        if not websites_dir.exists():
            pytest.skip("No websites in input_reduced")

        md_files = list(websites_dir.rglob("*.md"))
        assert len(md_files) > 0, "No markdown files in websites"


class TestExportImportRoundTrip:
    """Test complete export/import round-trip."""

    @pytest.fixture
    def populated_db(self, tmp_path: Path) -> Path:
        """Create a populated test database."""
        db_path = tmp_path / "source_db"
        db = lancedb.connect(str(db_path))

        # Create realistic data
        text_data = [
            {
                "id": f"text-{i}",
                "content": f"Text chunk content {i}",
                "hash": f"hash{i}",
                "vector": [float(i) / 10] * 768,
                "source_file": f"file{i}.md",
                "source_type": "markdown",
                "section_path": f"Section {i}",
            }
            for i in range(5)
        ]
        db.create_table("text_chunks", text_data)

        code_data = [
            {
                "id": f"code-{i}",
                "content": f"def func{i}(): pass",
                "hash": f"codehash{i}",
                "vector": [float(i) / 20] * 768,
                "source_file": f"file{i}.py",
                "language": "python",
                "symbol_name": f"func{i}",
                "symbol_type": "function",
            }
            for i in range(3)
        ]
        db.create_table("code_chunks", code_data)

        return db_path

    def test_lance_round_trip(self, populated_db: Path, tmp_path: Path) -> None:
        """Test export and import preserves data."""
        export_dir = tmp_path / "exported"
        import_path = tmp_path / "imported"

        # Export
        exporter = DatabaseExporter(str(populated_db))
        export_result = exporter.export_to_lance(export_dir)

        assert export_result["text_chunks"] == 5
        assert export_result["code_chunks"] == 3

        # Import
        importer = DatabaseImporter(str(import_path))
        import_result = importer.import_from_lance(export_dir)

        assert import_result["text_chunks"] == 5
        assert import_result["code_chunks"] == 3

        # Verify data integrity
        source_db = lancedb.connect(str(populated_db))
        imported_db = lancedb.connect(str(import_path))

        source_text = source_db.open_table("text_chunks").to_arrow()
        imported_text = imported_db.open_table("text_chunks").to_arrow()

        # Check content matches (using pyarrow)
        source_ids = set(source_text.column("id").to_pylist())
        imported_ids = set(imported_text.column("id").to_pylist())
        assert source_ids == imported_ids

        source_content = set(source_text.column("content").to_pylist())
        imported_content = set(imported_text.column("content").to_pylist())
        assert source_content == imported_content
