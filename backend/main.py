from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.routes.run_scan import router as run_scan_router

app = FastAPI(title="SemanticLayerBuilder Backend")

# Allow frontend to call the API (for now, be permissive in dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Frontend: serve the single-page UI at "/" ---

@app.get("/")
async def serve_frontend():
    """
    Serve the frontend UI.
    This assumes frontend/index.html exists in the project root.
    """
    return FileResponse("frontend/index.html")


# --- API routes ---

app.include_router(run_scan_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}