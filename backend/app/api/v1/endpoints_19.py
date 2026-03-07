from fastapi import APIRouter

router = APIRouter(prefix="/api/v19", tags=["Endpoint 19"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 19 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 19}
