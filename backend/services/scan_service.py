from backend.models.run_scan_models import (
    RunScanRequest,
    RunScanResponse,
    DimensionPreview,
    MetricPreview,
)
from backend.services.db_sampling import get_sql_table_schema


async def run_scan_for_payload(request: RunScanRequest) -> RunScanResponse:
    """
    First real step:
    - If source_type == "sql", call get_sql_table_schema() to retrieve a stubbed schema.
    - For now, we still return hard-coded dimensions/metrics so the UI feels alive.

    Later this function will:
    - use the real schema & sampled rows to build the Builder Agent payload
    - call the LLM
    - write YAML to disk
    - return real previews
    """

    # In this step, just demonstrate calling the schema helper for SQL sources.
    schema_info = None
    if request.source_type == "sql":
        schema_columns = await get_sql_table_schema(request)
        # For now we only use this for a message / debugging,
        # but soon we'll turn these into DimensionPreview objects.
        schema_info = [repr(col) for col in schema_columns]

    # Fake dims/metrics for now – unchanged from earlier
    fake_dims = [
        DimensionPreview(
            name="order_id",
            label="Order Id",
            type="numeric",
            source="orders.order_id",
            nullable=False,
            pii=False,
        ),
        DimensionPreview(
            name="created_at",
            label="Created At",
            type="time",
            source="orders.created_at",
            nullable=False,
            pii=False,
        ),
    ]

    # Build dimensions based on schema (real first step)
    dims = []
    if request.source_type == "sql":
        dims = [
            DimensionPreview(
                name=col.name,
                label=col.name.replace("_", " ").title(),     # simple label heuristic
                type=_infer_dimension_type(col.data_type),    # helper (next step)
                source=f"{request.sql_table}.{col.name}" if request.sql_table else col.name,
                nullable=col.nullable,
                pii=False,  # we don't detect PII yet
            )
            for col in schema_columns
        ]
    else:
        dims = []

    # Build a message that includes (for now) some schema info for debugging
    if schema_info:
        msg = (
            "scan_service.run_scan_for_payload is returning fake data "
            "(no real DB/LLM yet). "
            f"Stubbed SQL schema: {schema_info}"
        )
    else:
        msg = (
            "scan_service.run_scan_for_payload is returning fake data "
            "(no real DB/LLM yet). No SQL schema requested."
        )

    return RunScanResponse(
        status="simulated_service",
        message=msg,
        dimensions=fake_dims,
        metrics=fake_metrics,
    )