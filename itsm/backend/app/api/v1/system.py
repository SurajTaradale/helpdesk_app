from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import get_logger, log_stream

router = APIRouter()
logger = get_logger(__name__)

@router.get("/logs/")
async def get_logs():
    # Retrieve logs from the in-memory log stream
    log_contents = log_stream.getvalue()

    if log_contents:
        return JSONResponse(content={"logs": log_contents})
    else:
        raise HTTPException(status_code=404, detail="No logs found.")

