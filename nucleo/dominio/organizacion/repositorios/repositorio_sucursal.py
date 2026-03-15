from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.organizacion.modelo_sucursal import ModeloSucursal


class RepositorioSucursal(ABC):
    @abstractmethod
    def crear(self, sucursal: ModeloSucursal) -> ModeloSucursal:
        pass

    @abstractmethod
    def obtener_por_id(self, sucursal_id: UUID) -> ModeloSucursal | None:
        pass

    @abstractmethod
    def listar_por_empresa(self, empresa_id: UUID) -> list[ModeloSucursal]:
        pass
