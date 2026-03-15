from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.catalogo.modelo_producto import ModeloProducto


class RepositorioProducto(ABC):
    @abstractmethod
    def crear(self, producto: ModeloProducto) -> ModeloProducto:
        pass

    @abstractmethod
    def obtener_por_id(self, producto_id: UUID) -> ModeloProducto | None:
        pass

    @abstractmethod
    def obtener_por_sku(self, tenant_id: UUID, sku: str) -> ModeloProducto | None:
        pass

    @abstractmethod
    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloProducto]:
        pass
