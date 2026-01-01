"""Database export functionality."""

import json
import shutil
from datetime import datetime
from pathlib import Path

import lancedb
import pyarrow as pa
import pyarrow.csv as pv_csv


class DatabaseExporter:
    """Export LanceDB tables to various formats."""

    def __init__(self, db_path: str):
        """Initialize exporter.

        Args:
            db_path: Path to LanceDB database
        """
        self.db_path = Path(db_path)
        self._db: lancedb.DBConnection | None = None

    def connect(self) -> lancedb.DBConnection:
        """Connect to LanceDB."""
        if self._db is None:
            self._db = lancedb.connect(str(self.db_path))
        return self._db

    def _get_table_names(self, db: lancedb.DBConnection) -> list[str]:
        """Get table names from database, handling API differences."""
        result = db.table_names()
        # Handle both old API (returns list) and new API (returns response object)
        if hasattr(result, 'tables'):
            return result.tables
        return list(result)

    def list_tables(self) -> list[str]:
        """List all tables in the database."""
        db = self.connect()
        return self._get_table_names(db)

    def get_table_stats(self) -> dict[str, dict]:
        """Get statistics for all tables."""
        db = self.connect()
        stats = {}

        for table_name in self._get_table_names(db):
            table = db.open_table(table_name)
            schema = table.schema

            stats[table_name] = {
                "row_count": table.count_rows(),
                "columns": [field.name for field in schema],
                "vector_columns": [
                    field.name
                    for field in schema
                    if pa.types.is_fixed_size_list(field.type)
                ],
            }

        return stats

    def export_to_lance(
        self,
        output_dir: Path,
        tables: list[str] | None = None,
    ) -> dict[str, int]:
        """Export tables to Lance format (copy).

        Args:
            output_dir: Output directory
            tables: Specific tables to export (None = all)

        Returns:
            Dictionary of table names to row counts
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        db = self.connect()
        result = {}

        all_tables = self._get_table_names(db)
        export_tables = tables or all_tables

        for table_name in export_tables:
            if table_name not in all_tables:
                continue

            # Read table data
            table = db.open_table(table_name)
            data = table.to_arrow()

            # Create new Lance table in output directory
            output_db = lancedb.connect(str(output_dir))
            output_db.create_table(table_name, data, mode="overwrite")

            result[table_name] = table.count_rows()

        return result

    def export_to_csv(
        self,
        output_dir: Path,
        tables: list[str] | None = None,
        include_vectors: bool = False,
    ) -> dict[str, int]:
        """Export tables to CSV format.

        Args:
            output_dir: Output directory
            tables: Specific tables to export (None = all)
            include_vectors: Whether to include vector columns (large!)

        Returns:
            Dictionary of table names to row counts
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        db = self.connect()
        result = {}

        all_tables = self._get_table_names(db)
        export_tables = tables or all_tables

        for table_name in export_tables:
            if table_name not in all_tables:
                continue

            table = db.open_table(table_name)
            arrow_table = table.to_arrow()

            # Optionally remove vector columns (they're huge in CSV)
            if not include_vectors:
                schema = arrow_table.schema
                non_vector_cols = [
                    field.name
                    for field in schema
                    if not pa.types.is_fixed_size_list(field.type)
                ]
                arrow_table = arrow_table.select(non_vector_cols)

            # Write to CSV
            csv_path = output_dir / f"{table_name}.csv"
            pv_csv.write_csv(arrow_table, csv_path)

            result[table_name] = table.count_rows()

        return result

    def export_manifest(
        self,
        output_dir: Path,
        format: str,
        tables: dict[str, int],
        config_path: Path | None = None,
    ) -> Path:
        """Write export manifest file.

        Args:
            output_dir: Output directory
            format: Export format used
            tables: Dictionary of exported tables and row counts
            config_path: Optional config file that was bundled

        Returns:
            Path to manifest file
        """
        manifest = {
            "export_time": datetime.now().isoformat(),
            "source_database": str(self.db_path),
            "format": format,
            "tables": tables,
            "total_rows": sum(tables.values()),
        }

        if config_path:
            manifest["config_file"] = config_path.name

        manifest_path = output_dir / "export_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        return manifest_path

    def bundle_config(
        self,
        output_dir: Path,
        config_path: Path | None = None,
    ) -> Path | None:
        """Bundle processor config with export.

        Args:
            output_dir: Output directory
            config_path: Config file to bundle (uses default if None)

        Returns:
            Path to bundled config or None
        """
        # Try to find config file
        if config_path and config_path.exists():
            source_config = config_path
        else:
            # Look for default config locations
            candidates = [
                Path("configs/default.yaml"),
                Path("processor.yaml"),
                self.db_path.parent / "processor_config.yaml",
            ]
            source_config = None
            for candidate in candidates:
                if candidate.exists():
                    source_config = candidate
                    break

        if source_config is None:
            return None

        # Copy config to output
        dest_path = output_dir / "processor_config.yaml"
        shutil.copy(source_config, dest_path)

        return dest_path


class DatabaseImporter:
    """Import LanceDB tables from exported formats."""

    def __init__(self, db_path: str):
        """Initialize importer.

        Args:
            db_path: Path to target LanceDB database
        """
        self.db_path = Path(db_path)

    def _get_table_names(self, db: lancedb.DBConnection) -> list[str]:
        """Get table names from database, handling API differences."""
        result = db.table_names()
        # Handle both old API (returns list) and new API (returns response object)
        if hasattr(result, 'tables'):
            return result.tables
        return list(result)

    def import_from_lance(
        self,
        export_dir: Path,
        tables: list[str] | None = None,
    ) -> dict[str, int]:
        """Import tables from Lance format export.

        Args:
            export_dir: Directory containing exported Lance tables
            tables: Specific tables to import (None = all)

        Returns:
            Dictionary of table names to row counts
        """
        self.db_path.mkdir(parents=True, exist_ok=True)
        result = {}

        # Connect to export directory as source
        source_db = lancedb.connect(str(export_dir))
        target_db = lancedb.connect(str(self.db_path))

        all_tables = self._get_table_names(source_db)
        import_tables = tables or all_tables

        for table_name in import_tables:
            if table_name not in all_tables:
                continue

            # Read from source
            source_table = source_db.open_table(table_name)
            data = source_table.to_arrow()

            # Write to target
            target_db.create_table(table_name, data, mode="overwrite")

            result[table_name] = source_table.count_rows()

        return result

    def read_manifest(self, export_dir: Path) -> dict | None:
        """Read export manifest if present.

        Args:
            export_dir: Export directory

        Returns:
            Manifest data or None
        """
        manifest_path = export_dir / "export_manifest.json"
        if manifest_path.exists():
            return json.loads(manifest_path.read_text())
        return None
