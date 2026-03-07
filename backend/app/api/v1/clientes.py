from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_roles
from app.aplicacion.dto.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO, ClienteResponseDTO
from app.aplicacion.servicios.cliente_servicio import ClienteServicio
from app.infraestructura.repositorios.cliente_repositorio import RepositorioCliente
from app.dominio.entidades.cliente import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteResponseDTO])
async def listar_clientes(
    db: Session = Depends(obtener_bd),
    skip: int = 0,
    limit: int = 100
):
    \"\"\"
    LISTA TODOS LOS CLIENTES
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    clientes = servicio.obtener_todos()
    return clientes[skip:skip+limit] if clientes else []

@router.get("/buscar", response_model=List[ClienteResponseDTO])
async def buscar_clientes(
    termino: str,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    BUSCA CLIENTES POR NOMBRE O EMAIL
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    # Implementar búsqueda personalizada
    todos = servicio.obtener_todos()
    return [c for c in todos if termino.lower() in c.nombre.lower() or termino.lower() in c.email.lower()]

@router.get("/{id}", response_model=ClienteResponseDTO)
async def obtener_cliente(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UN CLIENTE POR ID
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    cliente = servicio.obtener_por_id(id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return cliente

@router.post("/", response_model=ClienteResponseDTO, status_code=201)
async def crear_cliente(
    datos: ClienteCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Cliente = Depends(obtener_usuario_actual)
):
    \"\"\"
    CREA UN NUEVO CLIENTE (REQUIERE AUTENTICACIÓN)
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=ClienteResponseDTO)
async def actualizar_cliente(
    id: int,
    datos: ClienteUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Cliente = Depends(obtener_usuario_actual)
):
    \"\"\"
    ACTUALIZA UN CLIENTE EXISTENTE
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    cliente = servicio.actualizar(id, datos)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return cliente

@router.delete("/{id}")
async def eliminar_cliente(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Cliente = Depends(requerir_roles(["admin"]))
):
    \"\"\"
    ELIMINA UN CLIENTE (SOLO ADMIN)
    \"\"\"
    servicio = ClienteServicio(RepositorioCliente(db))
    if not servicio.eliminar(id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return {"mensaje": "Cliente eliminado correctamente"}
