from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.organizacion.repositorios.repositorio_empresa import RepositorioEmpresa
from nucleo.infraestructura.db.modelos.organizacion.modelo_empresa import ModeloEmpresa


class RepositorioEmpresaSQLAlchemy(RepositorioEmpresa):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, empresa: ModeloEmpresa) -> ModeloEmpresa:
        self.db.add(empresa)
        self.db.commit()
        self.db.refresh(empresa)
        return empresa

    def obtener_por_id(self, empresa_id: UUID) -> ModeloEmpresa | None:
        sentencia = select(ModeloEmpresa).where(ModeloEmpresa.id == empresa_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloEmpresa]:
        sentencia = (
            select(ModeloEmpresa)
            .where(ModeloEmpresa.tenant_id == tenant_id)
            .order_by(ModeloEmpresa.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
