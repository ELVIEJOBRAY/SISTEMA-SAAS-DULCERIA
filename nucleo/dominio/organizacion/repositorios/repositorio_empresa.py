from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.organizacion.modelo_empresa import ModeloEmpresa


class RepositorioEmpresa(ABC):
    @abstractmethod
    def crear(self, empresa: ModeloEmpresa) -> ModeloEmpresa:
        pass

    @abstractmethod
    def obtener_por_id(self, empresa_id: UUID) -> ModeloEmpresa | None:
        pass

    @abstractmethod
    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloEmpresa]:
        pass
