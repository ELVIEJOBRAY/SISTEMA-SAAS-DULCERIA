from dataclasses import dataclass
from typing import Optional

@dataclass
class RegistrarMovimientoInventario:
    empresa_id: str
    producto_id: str
    presentacion_id: Optional[str]
    tipo_movimiento: str
    subtipo_movimiento: Optional[str]
    cantidad: float
    referencia_tipo: Optional[str]
    referencia_id: Optional[str]
    descripcion: Optional[str]
    usuario_id: Optional[str]
