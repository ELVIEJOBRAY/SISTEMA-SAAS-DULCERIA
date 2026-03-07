from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_roles
from app.aplicacion.dto.proveedor_dto import ProveedorCreateDTO, ProveedorUpdateDTO, ProveedorResponseDTO
from app.aplicacion.servicios.proveedor_servicio import ProveedorServicio
from app.infraestructura.repositorios.proveedor_repositorio import RepositorioProveedor
from app.dominio.entidades.proveedor import Proveedor

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

@router.get("/", response_model=List[ProveedorResponseDTO])
async def listar_proveedores(
    db: Session = Depends(obtener_bd),
    skip: int = 0,
    limit: int = 100
):
    \"\"\"
    LISTA TODOS LOS PROVEEDORES
    \"\"\"
    servicio = ProveedorServicio(RepositorioProveedor(db))
    proveedores = servicio.obtener_todos()
    return proveedores[skip:skip+limit] if proveedores else []

@router.get("/{id}", response_model=ProveedorResponseDTO)
async def obtener_proveedor(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UN PROVEEDOR POR ID
    \"\"\"
    servicio = ProveedorServicio(RepositorioProveedor(db))
    proveedor = servicio.obtener_por_id(id)
    
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return proveedor

@router.post("/", response_model=ProveedorResponseDTO, status_code=201)
async def crear_proveedor(
    datos: ProveedorCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Proveedor = Depends(requerir_roles(["admin", "inventario"]))
):
    \"\"\"
    CREA UN NUEVO PROVEEDOR (SOLO ADMIN/INVENTARIO)
    \"\"\"
    servicio = ProveedorServicio(RepositorioProveedor(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=ProveedorResponseDTO)
async def actualizar_proveedor(
    id: int,
    datos: ProveedorUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Proveedor = Depends(requerir_roles(["admin", "inventario"]))
):
    \"\"\"
    ACTUALIZA UN PROVEEDOR EXISTENTE
    \"\"\"
    servicio = ProveedorServicio(RepositorioProveedor(db))
    proveedor = servicio.actualizar(id, datos)
    
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return proveedor

@router.delete("/{id}")
async def eliminar_proveedor(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Proveedor = Depends(requerir_admin)
):
    \"\"\"
    ELIMINA UN PROVEEDOR (SOLO ADMIN)
    \"\"\"
    servicio = ProveedorServicio(RepositorioProveedor(db))
    if not servicio.eliminar(id):
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    return {"mensaje": "Proveedor eliminado correctamente"}
