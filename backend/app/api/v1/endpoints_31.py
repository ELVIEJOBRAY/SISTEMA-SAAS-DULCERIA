from fastapi import APIRouter

router = APIRouter(prefix="/api/v31", tags=["Endpoint 31"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 31 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 31}
