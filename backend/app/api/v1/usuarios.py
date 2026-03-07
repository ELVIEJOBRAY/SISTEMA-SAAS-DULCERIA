from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, obtener_inquilino_actual, requerir_admin
from app.aplicacion.dto.usuario_dto import UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO
from app.aplicacion.servicios.usuario_servicio import UsuarioServicio
from app.infraestructura.repositorios.usuario_repositorio import RepositorioUsuario
from app.dominio.entidades.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioResponseDTO])
async def listar_usuarios(
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(requerir_admin)
):
    \"\"\"
    LISTA TODOS LOS USUARIOS (SOLO ADMIN)
    
    - Requiere autenticación
    - Solo usuarios con rol admin pueden acceder
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    return servicio.obtener_todos()

@router.get("/{id}", response_model=UsuarioResponseDTO)
async def obtener_usuario(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    \"\"\"
    OBTIENE UN USUARIO POR ID
    
    - Usuarios solo pueden ver su propio perfil
    - Admins pueden ver cualquier perfil
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    usuario = servicio.obtener_por_id(id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not usuario_actual.es_admin() and usuario_actual.id != id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    return usuario

@router.post("/", response_model=UsuarioResponseDTO, status_code=201)
async def crear_usuario(
    datos: UsuarioCreateDTO,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    CREA UN NUEVO USUARIO (REGISTRO PÚBLICO)
    
    - No requiere autenticación
    - Validación de email único
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=UsuarioResponseDTO)
async def actualizar_usuario(
    id: int,
    datos: UsuarioUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    \"\"\"
    ACTUALIZA UN USUARIO
    
    - Usuarios solo pueden actualizar su propio perfil
    - Admins pueden actualizar cualquier perfil
    \"\"\"
    if not usuario_actual.es_admin() and usuario_actual.id != id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    servicio = UsuarioServicio(RepositorioUsuario(db))
    usuario = servicio.actualizar(id, datos)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(requerir_admin)
):
    \"\"\"
    ELIMINA UN USUARIO (SOLO ADMIN)
    
    - Soft delete o eliminación física
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    if not servicio.eliminar(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"mensaje": "Usuario eliminado correctamente"}

@router.patch("/{id}/activar", response_model=UsuarioResponseDTO)
async def activar_usuario(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(requerir_admin)
):
    \"\"\"
    ACTIVA UN USUARIO (SOLO ADMIN)
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    usuario = servicio.activar(id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

@router.patch("/{id}/desactivar", response_model=UsuarioResponseDTO)
async def desactivar_usuario(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Usuario = Depends(requerir_admin)
):
    \"\"\"
    DESACTIVA UN USUARIO (SOLO ADMIN)
    \"\"\"
    servicio = UsuarioServicio(RepositorioUsuario(db))
    usuario = servicio.desactivar(id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario
