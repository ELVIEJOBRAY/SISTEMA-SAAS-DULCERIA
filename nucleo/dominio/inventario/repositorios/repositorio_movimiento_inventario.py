from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.inventario.modelo_movimiento_inventario import (
    ModeloMovimientoInventario,
)


class RepositorioMovimientoInventario(ABC):
    @abstractmethod
    def crear(self, movimiento: ModeloMovimientoInventario) -> ModeloMovimientoInventario:
        pass

    @abstractmethod
    def obtener_por_id(self, movimiento_id: UUID) -> ModeloMovimientoInventario | None:
        pass

    @abstractmethod
    def listar_por_inventario(self, inventario_id: UUID) -> list[ModeloMovimientoInventario]:
        pass

    @abstractmethod
    def listar_kardex_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        pass

    @abstractmethod
    def listar_kardex_por_presentacion(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        presentacion_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        pass

    @abstractmethod
    def listar_por_bodega(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[ModeloMovimientoInventario]:
        pass
