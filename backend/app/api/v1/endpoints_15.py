from fastapi import APIRouter

router = APIRouter(prefix="/api/v15", tags=["Endpoint 15"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 15 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 15}
