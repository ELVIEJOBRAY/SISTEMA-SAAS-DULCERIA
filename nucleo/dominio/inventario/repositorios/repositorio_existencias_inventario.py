from abc import ABC, abstractmethod

class RepositorioExistenciasInventario(ABC):
    @abstractmethod
    def obtener_stock_actual(self, empresa_id: str, producto_id: str, presentacion_id: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def actualizar_stock_actual(self, empresa_id: str, producto_id: str, presentacion_id: str | None, stock_actual: float):
        raise NotImplementedError
