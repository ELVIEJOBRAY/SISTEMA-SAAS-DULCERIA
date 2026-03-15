from abc import ABC, abstractmethod
from uuid import UUID

from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_tenant import (
    ModeloMembresiaTenant,
)


class RepositorioMembresiaTenant(ABC):
    @abstractmethod
    def crear(self, membresia: ModeloMembresiaTenant) -> ModeloMembresiaTenant:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: UUID) -> list[ModeloMembresiaTenant]:
        pass
