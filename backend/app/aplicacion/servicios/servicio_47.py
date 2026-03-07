from typing import Dict

class Servicio47:
    def __init__(self):
        self.nombre = f"Servicio 47"
        self.version = "1.0.0"
        self.llamadas = 0
    
    def ejecutar(self) -> str:
        self.llamadas += 1
        return f"Servicio 47 ejecutado"
    
    def info(self) -> Dict:
        return {"nombre": self.nombre, "llamadas": self.llamadas}
