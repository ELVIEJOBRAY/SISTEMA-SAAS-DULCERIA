from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.aplicacion.ventas.servicios.servicio_aplicacion_ventas import (
    ServicioAplicacionVentas,
)
from nucleo.dominio.ventas.repositorios.repositorio_venta import RepositorioVenta
from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.ventas.repositorio_venta_sqlalchemy import (
    RepositorioVentaSQLAlchemy,
)
from nucleo.interfaz.api.v1.inventario.dependencias.dependencias_inventario import (
    obtener_servicio_inventario,
)


def obtener_servicio_aplicacion_ventas() -> ServicioAplicacionVentas:
    return ServicioAplicacionVentas()


def obtener_repositorio_venta(
    db: Session = Depends(obtener_db),
) -> RepositorioVenta:
    return RepositorioVentaSQLAlchemy(db)


def obtener_db_ventas(
    db: Session = Depends(obtener_db),
) -> Session:
    return db


def obtener_servicio_inventario_para_ventas(
    servicio: ServicioAplicacionInventario = Depends(obtener_servicio_inventario),
) -> ServicioAplicacionInventario:
    return servicio
