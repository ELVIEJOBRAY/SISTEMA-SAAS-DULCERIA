from fastapi import Depends
from sqlalchemy.orm import Session

from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.identidad_acceso import (
    RepositorioMembresiaEmpresaSQLAlchemy,
    RepositorioMembresiaTenantSQLAlchemy,
    RepositorioPermisoSQLAlchemy,
    RepositorioRolSQLAlchemy,
    RepositorioUsuarioSQLAlchemy,
)
from nucleo.infraestructura.db.repositorios.organizacion import (
    RepositorioEmpresaSQLAlchemy,
    RepositorioTenantSQLAlchemy,
)


def obtener_servicio_identidad(
    db: Session = Depends(obtener_db),
) -> ServicioAplicacionIdentidad:
    return ServicioAplicacionIdentidad(
        repositorio_usuario=RepositorioUsuarioSQLAlchemy(db),
        repositorio_rol=RepositorioRolSQLAlchemy(db),
        repositorio_permiso=RepositorioPermisoSQLAlchemy(db),
        repositorio_membresia_tenant=RepositorioMembresiaTenantSQLAlchemy(db),
        repositorio_membresia_empresa=RepositorioMembresiaEmpresaSQLAlchemy(db),
        repositorio_tenant=RepositorioTenantSQLAlchemy(db),
        repositorio_empresa=RepositorioEmpresaSQLAlchemy(db),
    )
