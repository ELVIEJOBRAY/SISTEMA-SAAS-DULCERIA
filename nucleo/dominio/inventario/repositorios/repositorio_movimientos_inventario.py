from abc import ABC, abstractmethod

class RepositorioMovimientosInventario(ABC):
    @abstractmethod
    def guardar(self, movimiento):
        raise NotImplementedError

    @abstractmethod
    def crear_desde_comando(self, comando, stock_anterior: float, stock_resultante: float):
        raise NotImplementedError
