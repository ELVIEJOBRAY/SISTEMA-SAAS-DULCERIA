from fastapi import Depends
from sqlalchemy.orm import Session

from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)
from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.catalogo import (
    RepositorioCategoriaSQLAlchemy,
    RepositorioMarcaSQLAlchemy,
    RepositorioPresentacionSQLAlchemy,
    RepositorioProductoSQLAlchemy,
)
from nucleo.infraestructura.db.repositorios.organizacion import (
    RepositorioEmpresaSQLAlchemy,
    RepositorioTenantSQLAlchemy,
)


def obtener_servicio_catalogo(
    db: Session = Depends(obtener_db),
) -> ServicioAplicacionCatalogo:
    return ServicioAplicacionCatalogo(
        repositorio_categoria=RepositorioCategoriaSQLAlchemy(db),
        repositorio_marca=RepositorioMarcaSQLAlchemy(db),
        repositorio_producto=RepositorioProductoSQLAlchemy(db),
        repositorio_presentacion=RepositorioPresentacionSQLAlchemy(db),
        repositorio_tenant=RepositorioTenantSQLAlchemy(db),
        repositorio_empresa=RepositorioEmpresaSQLAlchemy(db),
    )
