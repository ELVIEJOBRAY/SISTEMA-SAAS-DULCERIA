from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol import ModeloRol


class RepositorioRol(ABC):
    @abstractmethod
    def crear(self, rol: ModeloRol) -> ModeloRol:
        pass

    @abstractmethod
    def obtener_por_id(self, rol_id: UUID) -> ModeloRol | None:
        pass

    @abstractmethod
    def obtener_por_codigo(self, tenant_id: UUID, codigo: str) -> ModeloRol | None:
        pass

    @abstractmethod
    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloRol]:
        pass
