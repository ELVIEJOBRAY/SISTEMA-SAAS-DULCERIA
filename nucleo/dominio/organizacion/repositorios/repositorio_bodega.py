from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.organizacion.modelo_bodega import ModeloBodega


class RepositorioBodega(ABC):
    @abstractmethod
    def crear(self, bodega: ModeloBodega) -> ModeloBodega:
        pass

    @abstractmethod
    def obtener_por_id(self, bodega_id: UUID) -> ModeloBodega | None:
        pass

    @abstractmethod
    def listar_por_sucursal(self, sucursal_id: UUID) -> list[ModeloBodega]:
        pass
