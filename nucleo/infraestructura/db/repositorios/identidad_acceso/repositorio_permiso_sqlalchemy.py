from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.identidad_acceso.repositorios.repositorio_permiso import RepositorioPermiso
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_permiso import ModeloPermiso


class RepositorioPermisoSQLAlchemy(RepositorioPermiso):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_codigo(self, codigo: str) -> ModeloPermiso | None:
        sentencia = select(ModeloPermiso).where(ModeloPermiso.codigo == codigo)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar(self) -> list[ModeloPermiso]:
        sentencia = select(ModeloPermiso).order_by(ModeloPermiso.modulo.asc(), ModeloPermiso.codigo.asc())
        return list(self.db.execute(sentencia).scalars().all())
