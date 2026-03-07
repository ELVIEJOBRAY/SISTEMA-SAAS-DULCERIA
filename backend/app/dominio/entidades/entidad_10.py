from typing import Optional, Dict
from datetime import datetime

class Entidad10:
    def __init__(self, id: Optional[int] = None, nombre: str = "Entidad 10", activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.activo = activo
        self.fecha_creacion = datetime.now()
        self.version = 1
    
    def metodo_1(self) -> str: return f"Método 1 de {self.nombre}"
    def metodo_2(self) -> int: return self.version
    def metodo_3(self) -> None: self.version += 1
    def metodo_4(self) -> Dict: return {"id": self.id, "nombre": self.nombre}
