from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_admin, requerir_roles
from app.aplicacion.dto.producto_dto import ProductoCreateDTO, ProductoUpdateDTO, ProductoResponseDTO
from app.aplicacion.servicios.producto_servicio import ProductoServicio
from app.infraestructura.repositorios.producto_repositorio import RepositorioProducto
from app.dominio.entidades.producto import Producto

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=List[ProductoResponseDTO])
async def listar_productos(
    db: Session = Depends(obtener_bd),
    skip: int = 0,
    limit: int = 100
):
    \"\"\"
    LISTA TODOS LOS PRODUCTOS (PÚBLICO)
    
    - Paginación opcional
    - No requiere autenticación
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    productos = servicio.obtener_todos()
    # Aplicar paginación básica
    return productos[skip:skip+limit] if productos else []

@router.get("/buscar", response_model=List[ProductoResponseDTO])
async def buscar_productos(
    termino: str,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    BUSCA PRODUCTOS POR NOMBRE
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    return servicio.buscar_por_nombre(termino)

@router.get("/stock-bajo", response_model=List[ProductoResponseDTO])
async def productos_stock_bajo(
    db: Session = Depends(obtener_bd),
    usuario_actual: Producto = Depends(requerir_roles(["admin", "inventario"]))
):
    \"\"\"
    LISTA PRODUCTOS CON STOCK BAJO (SOLO ADMIN/INVENTARIO)
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    return servicio.buscar_con_stock_bajo()

@router.get("/{id}", response_model=ProductoResponseDTO)
async def obtener_producto(
    id: int,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    OBTIENE UN PRODUCTO POR ID
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    producto = servicio.obtener_por_id(id)
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto

@router.post("/", response_model=ProductoResponseDTO, status_code=201)
async def crear_producto(
    datos: ProductoCreateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Producto = Depends(requerir_roles(["admin", "inventario"]))
):
    \"\"\"
    CREA UN NUEVO PRODUCTO (SOLO ADMIN/INVENTARIO)
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    return servicio.crear(datos)

@router.put("/{id}", response_model=ProductoResponseDTO)
async def actualizar_producto(
    id: int,
    datos: ProductoUpdateDTO,
    db: Session = Depends(obtener_bd),
    usuario_actual: Producto = Depends(requerir_roles(["admin", "inventario"]))
):
    \"\"\"
    ACTUALIZA UN PRODUCTO EXISTENTE (SOLO ADMIN/INVENTARIO)
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    producto = servicio.actualizar(id, datos)
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto

@router.delete("/{id}")
async def eliminar_producto(
    id: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Producto = Depends(requerir_admin)
):
    \"\"\"
    ELIMINA UN PRODUCTO (SOLO ADMIN)
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    if not servicio.eliminar(id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"mensaje": "Producto eliminado correctamente"}

@router.patch("/{id}/reducir-stock")
async def reducir_stock(
    id: int,
    cantidad: int,
    db: Session = Depends(obtener_bd),
    usuario_actual: Producto = Depends(obtener_usuario_actual)
):
    \"\"\"
    REDUCE EL STOCK DE UN PRODUCTO (VENTAS)
    \"\"\"
    servicio = ProductoServicio(RepositorioProducto(db))
    producto = servicio.reducir_stock(id, cantidad)
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o stock insuficiente")
    
    return producto
