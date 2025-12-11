from typing import List
from backend.models.run_scan_models import RunScanRequest


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


async def get_sql_table_schema(request: RunScanRequest) -> List[SchemaColumn]:
    """
    Stub implementation for SQL schema profiling.

    Ultimately this will:
      - connect to the SQL database described by `request`
      - query INFORMATION_SCHEMA (or equivalent) for column names, types, nullability
      - return a list[SchemaColumn]

    For now, it returns a hard-coded example so we can wire the flow end-to-end.
    """

    # TODO: replace this with real database logic.
    # For now we just pretend the table looks like an "orders" table.
    return [
        SchemaColumn(name="order_id", data_type="integer", nullable=False),
        SchemaColumn(name="customer_id", data_type="integer", nullable=False),
        SchemaColumn(name="order_total", data_type="numeric", nullable=False),
        SchemaColumn(name="created_at", data_type="timestamp", nullable=False),
        SchemaColumn(name="notes", data_type="text", nullable=True),
    ]