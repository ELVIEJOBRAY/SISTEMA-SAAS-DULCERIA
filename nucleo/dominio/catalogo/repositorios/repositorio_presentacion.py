from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.catalogo.modelo_presentacion import ModeloPresentacion


class RepositorioPresentacion(ABC):
    @abstractmethod
    def crear(self, presentacion: ModeloPresentacion) -> ModeloPresentacion:
        pass

    @abstractmethod
    def obtener_por_id(self, presentacion_id: UUID) -> ModeloPresentacion | None:
        pass

    @abstractmethod
    def listar_por_producto(self, producto_id: UUID) -> list[ModeloPresentacion]:
        pass
