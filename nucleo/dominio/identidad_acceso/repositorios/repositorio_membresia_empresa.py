from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_empresa import (
    ModeloMembresiaEmpresa,
)


class RepositorioMembresiaEmpresa(ABC):
    @abstractmethod
    def crear(self, membresia: ModeloMembresiaEmpresa) -> ModeloMembresiaEmpresa:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: UUID) -> list[ModeloMembresiaEmpresa]:
        pass
