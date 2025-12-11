from typing import List
from backend.models.run_scan_models import RunScanRequest
from pathlib import Path
from typing import List, Dict

import pyarrow.parquet as pq  # make sure pyarrow is in your env


def get_parquet_table_schema(file_path: str) -> List[Dict]:
    """
    Inspect a Parquet file and return a simple column schema
    that scan_service can later turn into DimensionPreview/MetricPreview.

    Returns a list of dicts like:
      {"name": "column_name", "data_type": "int64", "nullable": True}
    """
    parquet_file = pq.ParquetFile(file_path)
    schema = parquet_file.schema_arrow  # Arrow schema object

    columns: List[Dict] = []
    for field in schema:
        columns.append(
            {
                "name": field.name,
                "data_type": str(field.type),
                "nullable": bool(field.nullable),
            }
        )

    # For now we just return the columns list; the caller can decide on table_name
    return columns

class SchemaColumn:
    """
    Simple in-memory representation of a column in a SQL table.
    Later we may promote this to a Pydantic model if we want to return it to the UI.
    """
    def __init__(self, name: str, data_type: str, nullable: bool):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable

    def __repr__(self) -> str:
        return f"SchemaColumn(name={self.name!r}, type={self.data_type!r}, nullable={self.nullable!r})"


from pathlib import Path

async def get_sql_table_schema(*args, **kwargs):
    """
    TEMP: instead of inspecting a real SQL DB, use the schema
    from our local health_records.parquet file.
    We keep this async so existing callers (await ...) still work.
    """
    project_root = Path(__file__).resolve().parents[2]
    parquet_path = project_root / "data" / "health_records.parquet"

    # This function should already be defined above in this same file.
    columns = get_parquet_table_schema(str(parquet_path))
    return columns