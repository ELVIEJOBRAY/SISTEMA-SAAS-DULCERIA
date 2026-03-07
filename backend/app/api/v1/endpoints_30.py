from fastapi import APIRouter

router = APIRouter(prefix="/api/v30", tags=["Endpoint 30"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 30 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 30}
