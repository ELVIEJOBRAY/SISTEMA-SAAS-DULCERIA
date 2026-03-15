from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.catalogo.modelo_marca import ModeloMarca


class RepositorioMarca(ABC):
    @abstractmethod
    def crear(self, marca: ModeloMarca) -> ModeloMarca:
        pass

    @abstractmethod
    def obtener_por_id(self, marca_id: UUID) -> ModeloMarca | None:
        pass

    @abstractmethod
    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloMarca | None:
        pass

    @abstractmethod
    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloMarca]:
        pass
