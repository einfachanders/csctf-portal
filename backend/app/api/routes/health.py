from datetime import datetime
# 3rd party imports
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get(f"", status_code=200, response_model=None)
async def health():
    return None
