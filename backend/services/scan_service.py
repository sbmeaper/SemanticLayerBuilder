from backend.models.run_scan_models import (
    RunScanRequest,
    RunScanResponse,
    DimensionPreview,
    MetricPreview,
)
from backend.services.db_sampling import get_sql_table_schema


def _infer_dimension_type(sql_type: str) -> str:
    """
    Very tiny heuristic. Later: use better rules or the Builder Agent.
    """
    sql_type = sql_type.lower()

    if "int" in sql_type:
        return "numeric"
    if "dec" in sql_type or "num" in sql_type or "float" in sql_type:
        return "numeric"
    if "timestamp" in sql_type or "date" in sql_type or "time" in sql_type:
        return "time"
    if "bool" in sql_type:
        return "boolean"

    return "categorical"

def _is_metric_candidate(col_name: str, sql_type: str) -> bool:
    """
    Heuristic: numeric columns whose names suggest amounts/totals
    are treated as metric candidates instead of dimensions.
    """
    dim_type = _infer_dimension_type(sql_type)
    if dim_type != "numeric":
        return False

    name = col_name.lower()
    metric_keywords = [
        "total",
        "amount",
        "revenue",
        "price",
        "cost",
        "qty",
        "quantity",
        "sales",
    ]

    return any(word in name for word in metric_keywords)

async def run_scan_for_payload(request: RunScanRequest) -> RunScanResponse:
    """
    First real step:
    - If source_type == "sql", call get_sql_table_schema() to retrieve a stubbed schema.
    - Build DimensionPreview objects from that schema.
    - For now, metrics are still fake.

    Later this function will:
    - use the real schema & sampled rows to build the Builder Agent payload
    - call the LLM
    - write YAML to disk
    - return real previews
    """

    schema_columns = []
    schema_info = None

    # Call schema helper for SQL sources
    if request.source_type == "sql":
        schema_columns = await get_sql_table_schema(request)
        schema_info = [repr(col) for col in schema_columns]

    # Build dimensions based on schema (real first step)
    dims = []
    if request.source_type == "sql":
        dims = [
            DimensionPreview(
                name=col.name,
                label=col.name.replace("_", " ").title(),     # simple label heuristic
                type=_infer_dimension_type(col.data_type),    # infer type from SQL type
                source=f"{request.sql_table}.{col.name}" if request.sql_table else col.name,
                nullable=col.nullable,
                pii=False,  # PII detection comes later
            )
            for col in schema_columns
        ]

    # Still using fake metrics for now
    fake_metrics = [
        MetricPreview(
            name="total_order_amount",
            label="Total Order Amount",
            aggregation="sum",
            expression="order_total",
            nullable=False,
        ),
        MetricPreview(
            name="order_count",
            label="Order Count",
            aggregation="count",
            expression="*",
            nullable=False,
        ),
    ]

    # Build a message that includes (for now) some schema info for debugging
    if schema_info:
        msg = (
            "scan_service.run_scan_for_payload is using stubbed SQL schema "
            "and returning schema-derived dimensions. "
            f"Stubbed SQL schema: {schema_info}"
        )
    else:
        msg = (
            "scan_service.run_scan_for_payload did not receive a SQL source. "
            "No schema-derived dimensions generated."
        )

    return RunScanResponse(
        status="schema_only",
        message=msg,
        dimensions=dims,
        metrics=fake_metrics,
    )