from fastapi import APIRouter

router = APIRouter(prefix="/api/v39", tags=["Endpoint 39"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 39 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 39}
