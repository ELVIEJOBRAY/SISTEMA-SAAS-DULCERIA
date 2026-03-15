from typing import Optional, Literal
from pydantic import BaseModel, Field

TipoMovimiento = Literal["entrada", "salida", "ajuste_positivo", "ajuste_negativo"]

class SolicitudRegistrarMovimientoInventario(BaseModel):
    empresa_id: str
    producto_id: str
    presentacion_id: Optional[str] = None
    tipo_movimiento: TipoMovimiento
    subtipo_movimiento: Optional[str] = None
    cantidad: float = Field(..., gt=0)
    referencia_tipo: Optional[str] = None
    referencia_id: Optional[str] = None
    descripcion: Optional[str] = None
    usuario_id: Optional[str] = None

class RespuestaMovimientoInventario(BaseModel):
    ok: bool
    mensaje: str
    data: dict
