from fastapi import APIRouter

router = APIRouter(prefix="/api/v32", tags=["Endpoint 32"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 32 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 32}
