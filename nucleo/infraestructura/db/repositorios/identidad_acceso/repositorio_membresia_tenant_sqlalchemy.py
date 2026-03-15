from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.identidad_acceso.repositorios.repositorio_membresia_tenant import (
    RepositorioMembresiaTenant,
)
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_tenant import (
    ModeloMembresiaTenant,
)


class RepositorioMembresiaTenantSQLAlchemy(RepositorioMembresiaTenant):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, membresia: ModeloMembresiaTenant) -> ModeloMembresiaTenant:
        self.db.add(membresia)
        self.db.commit()
        self.db.refresh(membresia)
        return membresia

    def listar_por_usuario(self, usuario_id: UUID) -> list[ModeloMembresiaTenant]:
        sentencia = (
            select(ModeloMembresiaTenant)
            .where(ModeloMembresiaTenant.usuario_id == usuario_id)
            .order_by(ModeloMembresiaTenant.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
