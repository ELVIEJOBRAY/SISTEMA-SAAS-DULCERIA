from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.catalogo.modelo_categoria import ModeloCategoria


class RepositorioCategoria(ABC):
    @abstractmethod
    def crear(self, categoria: ModeloCategoria) -> ModeloCategoria:
        pass

    @abstractmethod
    def obtener_por_id(self, categoria_id: UUID) -> ModeloCategoria | None:
        pass

    @abstractmethod
    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloCategoria | None:
        pass

    @abstractmethod
    def listar_por_empresa(self, tenant_id: UUID, empresa_id: UUID) -> list[ModeloCategoria]:
        pass
