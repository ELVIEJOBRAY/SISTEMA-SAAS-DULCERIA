from fastapi import APIRouter
router = APIRouter(prefix="/suscripciones", tags=["Suscripciones"])

@router.get("/")
def listar_suscripciones():
    return {"mensaje": "Listado de suscripciones - Pendiente implementación"}
