from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from nucleo.dominio.inventario.repositorios.repositorio_movimiento_inventario import (
    RepositorioMovimientoInventario,
)
from nucleo.infraestructura.db.modelos.inventario.modelo_movimiento_inventario import (
    ModeloMovimientoInventario,
)


class RepositorioMovimientoInventarioSQLAlchemy(RepositorioMovimientoInventario):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, movimiento: ModeloMovimientoInventario) -> ModeloMovimientoInventario:
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def obtener_por_id(self, movimiento_id: UUID) -> ModeloMovimientoInventario | None:
        sentencia = select(ModeloMovimientoInventario).where(
            ModeloMovimientoInventario.id == movimiento_id
        )
        return self.db.execute(sentencia).scalar_one_or_none()

    def listar_por_inventario(self, inventario_id: UUID) -> list[ModeloMovimientoInventario]:
        sentencia = (
            select(ModeloMovimientoInventario)
            .where(ModeloMovimientoInventario.inventario_id == inventario_id)
            .order_by(ModeloMovimientoInventario.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())

    def listar_kardex_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        sentencia = (
            select(ModeloMovimientoInventario)
            .where(
                ModeloMovimientoInventario.tenant_id == tenant_id,
                ModeloMovimientoInventario.empresa_id == empresa_id,
                ModeloMovimientoInventario.producto_id == producto_id,
            )
            .order_by(ModeloMovimientoInventario.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())

    def listar_kardex_por_presentacion(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        presentacion_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        sentencia = (
            select(ModeloMovimientoInventario)
            .where(
                ModeloMovimientoInventario.tenant_id == tenant_id,
                ModeloMovimientoInventario.empresa_id == empresa_id,
                ModeloMovimientoInventario.presentacion_id == presentacion_id,
            )
            .order_by(ModeloMovimientoInventario.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())

    def listar_por_bodega(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        sentencia = (
            select(ModeloMovimientoInventario)
            .where(
                ModeloMovimientoInventario.tenant_id == tenant_id,
                ModeloMovimientoInventario.empresa_id == empresa_id,
                ModeloMovimientoInventario.bodega_id == bodega_id,
            )
            .order_by(ModeloMovimientoInventario.creado_en.desc())
        )
        return list(self.db.execute(sentencia).scalars().all())
