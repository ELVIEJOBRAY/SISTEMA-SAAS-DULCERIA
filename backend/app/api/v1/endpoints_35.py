from fastapi import APIRouter

router = APIRouter(prefix="/api/v35", tags=["Endpoint 35"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 35 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 35}
