from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_usuario import ModeloUsuario


class RepositorioUsuario(ABC):
    @abstractmethod
    def crear(self, usuario: ModeloUsuario) -> ModeloUsuario:
        pass

    @abstractmethod
    def obtener_por_id(self, usuario_id: UUID) -> ModeloUsuario | None:
        pass

    @abstractmethod
    def obtener_por_correo(self, tenant_id: UUID, correo: str) -> ModeloUsuario | None:
        pass

    @abstractmethod
    def obtener_por_nombre_usuario(self, tenant_id: UUID, nombre_usuario: str) -> ModeloUsuario | None:
        pass

    @abstractmethod
    def listar_por_tenant(self, tenant_id: UUID) -> list[ModeloUsuario]:
        pass
