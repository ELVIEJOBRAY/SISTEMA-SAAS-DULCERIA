from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.inventario.repositorios.repositorio_inventario import RepositorioInventario
from nucleo.infraestructura.db.modelos.inventario.modelo_inventario import ModeloInventario


class RepositorioInventarioSQLAlchemy(RepositorioInventario):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, inventario: ModeloInventario) -> ModeloInventario:
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def actualizar(self, inventario: ModeloInventario) -> ModeloInventario:
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def obtener_por_id(self, inventario_id: UUID) -> ModeloInventario | None:
        sentencia = select(ModeloInventario).where(ModeloInventario.id == inventario_id)
        return self.db.execute(sentencia).scalar_one_or_none()

    def obtener_por_bodega_y_presentacion(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
        presentacion_id: UUID,
    ) -> ModeloInventario | None:
        sentencia = select(ModeloInventario).where(
            ModeloInventario.tenant_id == tenant_id,
            ModeloInventario.empresa_id == empresa_id,
            ModeloInventario.bodega_id == bodega_id,
            ModeloInventario.presentacion_id == presentacion_id,
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_bodega(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[ModeloInventario]:
        sentencia = (
            select(ModeloInventario)
            .where(
                ModeloInventario.tenant_id == tenant_id,
                ModeloInventario.empresa_id == empresa_id,
                ModeloInventario.bodega_id == bodega_id,
            )
            .order_by(ModeloInventario.actualizado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())

    def listar_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[ModeloInventario]:
        sentencia = (
            select(ModeloInventario)
            .where(
                ModeloInventario.tenant_id == tenant_id,
                ModeloInventario.empresa_id == empresa_id,
                ModeloInventario.producto_id == producto_id,
            )
            .order_by(ModeloInventario.actualizado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
