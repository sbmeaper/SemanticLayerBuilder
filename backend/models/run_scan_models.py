from typing import List, Optional
from pydantic import BaseModel  # keep this if it's already there; add if missing


class SchemaColumn(BaseModel):
    name: str
    data_type: str
    nullable: bool = True

class RunScanRequest(BaseModel):
    """
    This matches (roughly) what the frontend will send
    when the user clicks Run Builder.
    """
    source_type: str              # "sql" or "xml"
    sql_host: Optional[str] = None
    sql_port: Optional[int] = None
    sql_database: Optional[str] = None
    sql_username: Optional[str] = None
    sql_password: Optional[str] = None
    sql_table: Optional[str] = None

    xml_path: Optional[str] = None

    sampling_mode: str            # "first_n" or "every_nth"
    sampling_value: int
    exclude_columns: List[str] = []
    allow_pii: bool = False


class DimensionPreview(BaseModel):
    name: str
    label: str
    type: str
    source: str
    nullable: bool
    pii: bool


class MetricPreview(BaseModel):
    name: str
    label: str
    aggregation: str
    expression: str
    nullable: bool


class RunScanResponse(BaseModel):
    status: str                    # e.g. "simulated", "success", "error"
    message: str
    dimensions: List[DimensionPreview]
    metrics: List[MetricPreview]