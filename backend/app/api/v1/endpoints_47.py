from fastapi import APIRouter

router = APIRouter(prefix="/api/v47", tags=["Endpoint 47"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 47 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 47}
