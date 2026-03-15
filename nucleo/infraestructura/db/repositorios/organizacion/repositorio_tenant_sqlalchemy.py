from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.organizacion.repositorios.repositorio_tenant import RepositorioTenant
from nucleo.infraestructura.db.modelos.organizacion.modelo_tenant import ModeloTenant


class RepositorioTenantSQLAlchemy(RepositorioTenant):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, tenant: ModeloTenant) -> ModeloTenant:
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant

    def obtener_por_id(self, tenant_id: UUID) -> ModeloTenant | None:
        sentencia = select(ModeloTenant).where(ModeloTenant.id == tenant_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_slug(self, slug: str) -> ModeloTenant | None:
        sentencia = select(ModeloTenant).where(ModeloTenant.slug == slug)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar(self) -> list[ModeloTenant]:
        sentencia = select(ModeloTenant).order_by(ModeloTenant.creado_en.desc())
        return list(self.db.execute(sentencia).scalars().all())
