from typing import List, Dict
from pathlib import Path

import pyarrow.parquet as pq  # make sure pyarrow is in your env

from backend.models.run_scan_models import SchemaColumn


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

    return columns


async def get_sql_table_schema(*args, **kwargs) -> List[SchemaColumn]:
    """
    TEMP: instead of inspecting a real SQL DB, use the schema
    from our local health_records.parquet file.
    We keep this async so existing callers (await ...) still work.

    Returns a list of SchemaColumn objects, which is what scan_service expects.
    """
    project_root = Path(__file__).resolve().parents[2]
    parquet_path = project_root / "data" / "health_records.parquet"

    # Get raw column dicts from the Parquet file
    column_dicts = get_parquet_table_schema(str(parquet_path))

    # Wrap each dict into a SchemaColumn instance
    schema_columns: List[SchemaColumn] = [
        SchemaColumn(
            name=col["name"],
            data_type=col["data_type"],
            nullable=col.get("nullable", True),
        )
        for col in column_dicts
    ]

    return schema_columns