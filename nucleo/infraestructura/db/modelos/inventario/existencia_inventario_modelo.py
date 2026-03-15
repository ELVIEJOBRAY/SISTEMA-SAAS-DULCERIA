from dataclasses import dataclass
from typing import Optional


@dataclass
class ExistenciaInventarioModelo:
    id: str
    empresa_id: str
    producto_id: str
    presentacion_id: Optional[str]
    stock_actual: float
    updated_at: str
