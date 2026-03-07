from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_roles
from app.aplicacion.dto.categoria_dto import CategoriaCreateDTO, CategoriaUpdateDTO, CategoriaResponseDTO
from app.aplicacion.servicios.categoria_servicio import CategoriaServicio
from app.infraestructura.repositorios.categoria_repositorio import RepositorioCategoria
from app.dominio.entidades.categoria import Categoria

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=List[CategoriaResponseDTO])
async def listar_categorias(
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    LISTA TODAS LAS CATEGORÍAS
    \"\"\"
    servicio = CategoriaServicio(RepositorioCategoria(db))
    return servicio.obtener_todos()

@router.get("/{id}", response_model=CategoriaResponseDTO)
async def obtener_categoria(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UNA CATEGORÍA POR ID
    \"\"\"
    servicio = CategoriaServicio(RepositorioCategoria(db))
    categoria = servicio.obtener_por_id(id)
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return categoria

@router.post("/", response_model=CategoriaResponseDTO, status_code=201)
async def crear_categoria(
    datos: CategoriaCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Categoria = Depends(requerir_roles(["admin"]))
):
    \"\"\"
    CREA UNA NUEVA CATEGORÍA (SOLO ADMIN)
    \"\"\"
    servicio = CategoriaServicio(RepositorioCategoria(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=CategoriaResponseDTO)
async def actualizar_categoria(
    id: int,
    datos: CategoriaUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Categoria = Depends(requerir_roles(["admin"]))
):
    \"\"\"
    ACTUALIZA UNA CATEGORÍA EXISTENTE (SOLO ADMIN)
    \"\"\"
    servicio = CategoriaServicio(RepositorioCategoria(db))
    categoria = servicio.actualizar(id, datos)
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return categoria

@router.delete("/{id}")
async def eliminar_categoria(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Categoria = Depends(requerir_admin)
):
    \"\"\"
    ELIMINA UNA CATEGORÍA (SOLO ADMIN)
    \"\"\"
    servicio = CategoriaServicio(RepositorioCategoria(db))
    if not servicio.eliminar(id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return {"mensaje": "Categoría eliminada correctamente"}
