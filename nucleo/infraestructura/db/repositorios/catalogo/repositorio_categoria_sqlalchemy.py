from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.catalogo.repositorios.repositorio_categoria import RepositorioCategoria
from nucleo.infraestructura.db.modelos.catalogo.modelo_categoria import ModeloCategoria


class RepositorioCategoriaSQLAlchemy(RepositorioCategoria):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, categoria: ModeloCategoria) -> ModeloCategoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_por_id(self, categoria_id: UUID) -> ModeloCategoria | None:
        sentencia = select(ModeloCategoria).where(ModeloCategoria.id == categoria_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloCategoria | None:
        sentencia = select(ModeloCategoria).where(
            ModeloCategoria.tenant_id == tenant_id,
            ModeloCategoria.codigo == codigo,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloCategoria]:
        sentencia = (
            select(ModeloCategoria)
            .where(
                ModeloCategoria.tenant_id == tenant_id,
                ModeloCategoria.empresa_id == empresa_id,
            )
            .order_by(ModeloCategoria.nombre.asc())
        )
        return list(self.db.execute(sentencia).scalars().all())
