from typing import Dict

class Servicio2:
    def __init__(self):
        self.nombre = f"Servicio 2"
        self.version = "1.0.0"
        self.llamadas = 0
    
    def ejecutar(self) -> str:
        self.llamadas += 1
        return f"Servicio 2 ejecutado"
    
    def info(self) -> Dict:
        return {"nombre": self.nombre, "llamadas": self.llamadas}
