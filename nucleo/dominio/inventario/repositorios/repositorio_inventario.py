from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.inventario.modelo_inventario import ModeloInventario


class RepositorioInventario(ABC):
    @abstractmethod
    def crear(self, inventario: ModeloInventario) -> ModeloInventario:
        pass

    @abstractmethod
    def actualizar(self, inventario: ModeloInventario) -> ModeloInventario:
        pass

    @abstractmethod
    def obtener_por_id(self, inventario_id: UUID) -> ModeloInventario | None:
        pass

    @abstractmethod
    def obtener_por_bodega_y_presentacion(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
        presentacion_id: UUID,
    ) -> ModeloInventario | None:
        pass

    @abstractmethod
    def listar_por_bodega(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[ModeloInventario]:
        pass

    @abstractmethod
    def listar_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[ModeloInventario]:
        pass
