from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.organizacion.modelo_tenant import ModeloTenant


class RepositorioTenant(ABC):
    @abstractmethod
    def crear(self, tenant: ModeloTenant) -> ModeloTenant:
        pass

    @abstractmethod
    def obtener_por_id(self, tenant_id: UUID) -> ModeloTenant | None:
        pass

    @abstractmethod
    def obtener_por_slug(self, slug: str) -> ModeloTenant | None:
        pass

    @abstractmethod
    def listar(self) -> list[ModeloTenant]:
        pass
