from fastapi import Depends
from sqlalchemy.orm import Session

from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)
from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.catalogo import (
    RepositorioPresentacionSQLAlchemy,
    RepositorioProductoSQLAlchemy,
)
from nucleo.infraestructura.db.repositorios.inventario import (
    RepositorioInventarioSQLAlchemy,
    RepositorioMovimientoInventarioSQLAlchemy,
)
from nucleo.infraestructura.db.repositorios.organizacion import (
    RepositorioBodegaSQLAlchemy,
    RepositorioEmpresaSQLAlchemy,
    RepositorioSucursalSQLAlchemy,
    RepositorioTenantSQLAlchemy,
)


def obtener_servicio_inventario(
    db: Session = Depends(obtener_db),
) -> ServicioAplicacionInventario:
    return ServicioAplicacionInventario(
        repositorio_inventario=RepositorioInventarioSQLAlchemy(db),
        repositorio_movimiento_inventario=RepositorioMovimientoInventarioSQLAlchemy(db),
        repositorio_tenant=RepositorioTenantSQLAlchemy(db),
        repositorio_empresa=RepositorioEmpresaSQLAlchemy(db),
        repositorio_sucursal=RepositorioSucursalSQLAlchemy(db),
        repositorio_bodega=RepositorioBodegaSQLAlchemy(db),
        repositorio_producto=RepositorioProductoSQLAlchemy(db),
        repositorio_presentacion=RepositorioPresentacionSQLAlchemy(db),
    )
