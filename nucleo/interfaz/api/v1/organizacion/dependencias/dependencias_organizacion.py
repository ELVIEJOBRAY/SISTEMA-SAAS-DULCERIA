from fastapi import Depends
from sqlalchemy.orm import Session

from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)
from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.organizacion import (
    RepositorioBodegaSQLAlchemy,
    RepositorioEmpresaSQLAlchemy,
    RepositorioSucursalSQLAlchemy,
    RepositorioTenantSQLAlchemy,
)


def obtener_servicio_organizacion(
    db: Session = Depends(obtener_db),
) -> ServicioAplicacionOrganizacion:
    return ServicioAplicacionOrganizacion(
        repositorio_tenant=RepositorioTenantSQLAlchemy(db),
        repositorio_empresa=RepositorioEmpresaSQLAlchemy(db),
        repositorio_sucursal=RepositorioSucursalSQLAlchemy(db),
        repositorio_bodega=RepositorioBodegaSQLAlchemy(db),
    )
