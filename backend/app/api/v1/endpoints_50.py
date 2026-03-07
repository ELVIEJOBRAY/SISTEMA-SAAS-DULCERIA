from fastapi import APIRouter

router = APIRouter(prefix="/api/v50", tags=["Endpoint 50"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 50 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 50}
