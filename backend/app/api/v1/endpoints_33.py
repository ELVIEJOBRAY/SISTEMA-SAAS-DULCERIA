from fastapi import APIRouter

router = APIRouter(prefix="/api/v33", tags=["Endpoint 33"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 33 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 33}
