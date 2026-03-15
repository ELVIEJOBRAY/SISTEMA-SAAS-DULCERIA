from abc import ABC, abstractmethod

from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_permiso import ModeloPermiso


class RepositorioPermiso(ABC):
    @abstractmethod
    def obtener_por_codigo(self, codigo: str) -> ModeloPermiso | None:
        pass

    @abstractmethod
    def listar(self) -> list[ModeloPermiso]:
        pass
