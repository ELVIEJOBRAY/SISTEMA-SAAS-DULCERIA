from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.identidad_acceso.repositorios.repositorio_rol import RepositorioRol
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol import ModeloRol


class RepositorioRolSQLAlchemy(RepositorioRol):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, rol: ModeloRol) -> ModeloRol:
        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def obtener_por_id(self, rol_id: UUID) -> ModeloRol | None:
        sentencia = select(ModeloRol).where(ModeloRol.id == rol_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloRol | None:
        sentencia = select(ModeloRol).where(
            ModeloRol.tenant_id == tenant_id,
            ModeloRol.codigo == codigo,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloRol]:
        sentencia = (
            select(ModeloRol)
            .where(ModeloRol.tenant_id == tenant_id)
            .order_by(ModeloRol.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
