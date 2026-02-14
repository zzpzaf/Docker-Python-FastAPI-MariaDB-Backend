# app/routers/health.py
# Testin endpoint for health checks; 
# returns simple dicts (no Pydantic models)
#
# Defines just a simple endpoint for health checks; no service layer needed



from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}
