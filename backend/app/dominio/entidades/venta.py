from typing import Optional
from enum import Enum

class EstadoVenta(Enum):
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class Venta:
    def __init__(self, id: Optional[int], cliente_id: int, total: float, estado: str = "pendiente"):
        if cliente_id <= 0:
            raise ValueError("ID DE CLIENTE INVÁLIDO")
        if total < 0:
            raise ValueError("EL TOTAL NO PUEDE SER NEGATIVO")
        if estado not in [e.value for e in EstadoVenta]:
            raise ValueError(f"ESTADO INVÁLIDO. VALORES: pendiente, completada, cancelada")
        
        self.id = id
        self.cliente_id = cliente_id
        self.total = total
        self.estado = estado
    
    def completar(self) -> None:
        if self.estado != "pendiente":
            raise ValueError(f"NO SE PUEDE COMPLETAR UNA VENTA EN ESTADO {self.estado}")
        self.estado = "completada"
    
    def cancelar(self) -> None:
        if self.estado == "completada":
            raise ValueError("NO SE PUEDE CANCELAR UNA VENTA COMPLETADA")
        self.estado = "cancelada"
    
    def esta_completada(self) -> bool: return self.estado == "completada"
    def esta_cancelada(self) -> bool: return self.estado == "cancelada"
    
    def __repr__(self) -> str:
        return f"<Venta id={self.id} cliente={self.cliente_id} total={self.total} estado={self.estado}>"
