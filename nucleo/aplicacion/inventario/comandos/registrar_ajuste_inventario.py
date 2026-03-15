from dataclasses import dataclass
from typing import Optional

@dataclass
class RegistrarAjusteInventario:
    empresa_id: str
    producto_id: str
    presentacion_id: Optional[str]
    tipo_ajuste: str
    cantidad: float
    motivo: str
    usuario_id: Optional[str]
