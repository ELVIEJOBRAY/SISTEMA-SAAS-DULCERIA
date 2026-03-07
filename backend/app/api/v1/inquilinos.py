from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_admin
from app.aplicacion.dto.inquilino_dto import InquilinoCreateDTO, InquilinoUpdateDTO, InquilinoResponseDTO
from app.aplicacion.servicios.inquilino_servicio import InquilinoServicio
from app.infraestructura.repositorios.inquilino_repositorio import RepositorioInquilino
from app.dominio.entidades.inquilino import Inquilino

router = APIRouter(prefix="/inquilinos", tags=["Inquilinos"])

@router.get("/", response_model=List[InquilinoResponseDTO])
async def listar_inquilinos(
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    LISTA TODOS LOS INQUILINOS (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    return servicio.obtener_todos()

@router.get("/{id}", response_model=InquilinoResponseDTO)
async def obtener_inquilino(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    OBTIENE UN INQUILINO POR ID (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    inquilino = servicio.obtener_por_id(id)
    
    if not inquilino:
        raise HTTPException(status_code=404, detail="Inquilino no encontrado")
    
    return inquilino

@router.post("/", response_model=InquilinoResponseDTO, status_code=201)
async def crear_inquilino(
    datos: InquilinoCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    CREA UN NUEVO INQUILINO (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=InquilinoResponseDTO)
async def actualizar_inquilino(
    id: int,
    datos: InquilinoUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    ACTUALIZA UN INQUILINO EXISTENTE (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    inquilino = servicio.actualizar(id, datos)
    
    if not inquilino:
        raise HTTPException(status_code=404, detail="Inquilino no encontrado")
    
    return inquilino

@router.patch("/{id}/activar", response_model=InquilinoResponseDTO)
async def activar_inquilino(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    ACTIVA UN INQUILINO (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    inquilino = servicio.activar(id)
    
    if not inquilino:
        raise HTTPException(status_code=404, detail="Inquilino no encontrado")
    
    return inquilino

@router.patch("/{id}/suspender", response_model=InquilinoResponseDTO)
async def suspender_inquilino(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    SUSPENDE UN INQUILINO (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    inquilino = servicio.suspender(id)
    
    if not inquilino:
        raise HTTPException(status_code=404, detail="Inquilino no encontrado")
    
    return inquilino

@router.patch("/{id}/cambiar-plan", response_model=InquilinoResponseDTO)
async def cambiar_plan(
    id: int,
    nuevo_plan: str,
    db: Session = Depends(obtener_bd),
    usuario_actual: Inquilino = Depends(requerir_admin)
):
    \"\"\"
    CAMBIA EL PLAN DE UN INQUILINO (SOLO ADMIN)
    \"\"\"
    servicio = InquilinoServicio(RepositorioInquilino(db))
    try:
        inquilino = servicio.cambiar_plan(id, nuevo_plan)
        if not inquilino:
            raise HTTPException(status_code=404, detail="Inquilino no encontrado")
        return inquilino
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
