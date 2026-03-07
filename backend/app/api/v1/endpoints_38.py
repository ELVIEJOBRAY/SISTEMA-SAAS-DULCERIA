from fastapi import APIRouter

router = APIRouter(prefix="/api/v38", tags=["Endpoint 38"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 38 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 38}
