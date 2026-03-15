from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.catalogo.repositorios.repositorio_marca import RepositorioMarca
from nucleo.infraestructura.db.modelos.catalogo.modelo_marca import ModeloMarca


class RepositorioMarcaSQLAlchemy(RepositorioMarca):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, marca: ModeloMarca) -> ModeloMarca:
        self.db.add(marca)
        self.db.commit()
        self.db.refresh(marca)
        return marca

    def obtener_por_id(self, marca_id: UUID) -> ModeloMarca | None:
        sentencia = select(ModeloMarca).where(ModeloMarca.id == marca_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloMarca | None:
        sentencia = select(ModeloMarca).where(
            ModeloMarca.tenant_id == tenant_id,
            ModeloMarca.codigo == codigo,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloMarca]:
        sentencia = (
            select(ModeloMarca)
            .where(
                ModeloMarca.tenant_id == tenant_id,
                ModeloMarca.empresa_id == empresa_id,
            )
            .order_by(ModeloMarca.nombre.asc())
        )
        return list(self.db.execute(sentencia).scalars().all())
