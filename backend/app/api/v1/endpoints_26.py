from fastapi import APIRouter

router = APIRouter(prefix="/api/v26", tags=["Endpoint 26"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 26 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 26}
