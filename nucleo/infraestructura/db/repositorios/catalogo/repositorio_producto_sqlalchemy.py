from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.catalogo.repositorios.repositorio_producto import RepositorioProducto
from nucleo.infraestructura.db.modelos.catalogo.modelo_producto import ModeloProducto


class RepositorioProductoSQLAlchemy(RepositorioProducto):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, producto: ModeloProducto) -> ModeloProducto:
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_por_id(self, producto_id: UUID) -> ModeloProducto | None:
        sentencia = select(ModeloProducto).where(ModeloProducto.id == producto_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_sku(self, tenant_id: UUID, sku: str) -> ModeloProducto | None:
        sentencia = select(ModeloProducto).where(
            ModeloProducto.tenant_id == tenant_id,
            ModeloProducto.sku == sku,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloProducto]:
        sentencia = (
            select(ModeloProducto)
            .where(
                ModeloProducto.tenant_id == tenant_id,
                ModeloProducto.empresa_id == empresa_id,
            )
            .order_by(ModeloProducto.nombre.asc())
        )
        return list(self.db.execute(sentencia).scalars().all())
