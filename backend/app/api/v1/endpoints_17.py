from fastapi import APIRouter

router = APIRouter(prefix="/api/v17", tags=["Endpoint 17"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 17 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 17}
