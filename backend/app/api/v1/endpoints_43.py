from fastapi import APIRouter

router = APIRouter(prefix="/api/v43", tags=["Endpoint 43"])

@router.get("/")
async def raiz():
    return {"mensaje": f"Endpoint 43 funcionando"}

@router.get("/info")
async def info():
    return {"version": "1.0.0", "endpoint": 43}
