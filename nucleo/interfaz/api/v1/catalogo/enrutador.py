# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from aplicacion.dto.producto_dto import ProductoCrear, ProductoActualizar, ProductoRespuesta
from aplicacion.casos_uso.gestionar_productos import GestionarProductos

enrutador = APIRouter(prefix="/productos", tags=["productos"])

@enrutador.post("/", response_model=ProductoRespuesta)
async def crear_producto(producto: ProductoCrear):
    """Crea un nuevo producto"""
    return {"mensaje": "Producto creado", "producto": producto}

@enrutador.get("/", response_model=List[ProductoRespuesta])
async def listar_productos(activos: bool = True):
    """Lista todos los productos"""
    return []

@enrutador.get("/{producto_id}", response_model=ProductoRespuesta)
async def obtener_producto(producto_id: int):
    """Obtiene un producto por ID"""
    return {"id": producto_id, "nombre": "Ejemplo", "precio": 1000, "stock": 10, "stock_minimo": 5, "categoria": "dulces", "activo": True, "fecha_creacion": "2024-01-01"}

@enrutador.put("/{producto_id}", response_model=ProductoRespuesta)
async def actualizar_producto(producto_id: int, producto: ProductoActualizar):
    """Actualiza un producto"""
    return {"id": producto_id, "nombre": "Actualizado", "precio": 1200, "stock": 15, "stock_minimo": 5, "categoria": "dulces", "activo": True, "fecha_creacion": "2024-01-01"}

@enrutador.delete("/{producto_id}")
async def eliminar_producto(producto_id: int):
    """Elimina lógicamente un producto"""
    return {"mensaje": f"Producto {producto_id} eliminado"}
