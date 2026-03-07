from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.nucleo.base_datos import obtener_bd

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/")
def listar_inventario(db: Session = Depends(obtener_bd)):
    return {"mensaje": "Listado de inventario - Pendiente implementación"}
