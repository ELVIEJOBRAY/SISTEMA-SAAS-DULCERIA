from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.nucleo.base_datos import obtener_bd

router = APIRouter(prefix="/facturacion", tags=["Facturación"])

@router.get("/")
def listar_facturas(db: Session = Depends(obtener_bd)):
    return {"mensaje": "Listado de facturas - Pendiente implementación"}
