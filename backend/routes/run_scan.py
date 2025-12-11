from fastapi import APIRouter

from backend.models.run_scan_models import RunScanRequest, RunScanResponse
from backend.services.scan_service import run_scan_for_payload

router = APIRouter()


@router.post("/run_scan", response_model=RunScanResponse)
async def run_scan(request: RunScanRequest) -> RunScanResponse:
    """
    Endpoint for kicking off a semantic scan.

    Currently delegates to a fake implementation in scan_service
    that returns hard-coded dimensions/metrics so we can verify
    the end-to-end wiring (frontend → backend → service → frontend).
    """
    result = await run_scan_for_payload(request)
    return result