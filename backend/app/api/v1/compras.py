from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.nucleo.base_datos import obtener_bd

router = APIRouter(prefix="/compras", tags=["Compras"])

@router.get("/")
def listar_compras(db: Session = Depends(obtener_bd)):
    return {"mensaje": "Listado de compras - Pendiente implementación"}
