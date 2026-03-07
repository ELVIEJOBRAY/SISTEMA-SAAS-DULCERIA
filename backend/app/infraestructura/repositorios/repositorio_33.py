from typing import Optional, List, Dict

class Repositorio33:
    def __init__(self):
        self.entidad_nombre = "Entidad 33"
        self.contador = 0
    
    def obtener(self, id: int) -> Optional[Dict]:
        self.contador += 1
        return {"id": id, "nombre": f"Entidad {id}"}
    
    def listar(self) -> List[Dict]:
        return [{"id": i, "nombre": f"Entidad {i}"} for i in range(1, 6)]
