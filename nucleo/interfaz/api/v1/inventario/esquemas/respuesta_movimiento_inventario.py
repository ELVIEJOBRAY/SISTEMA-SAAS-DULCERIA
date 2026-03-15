from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaMovimientoInventario(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    inventario_id: UUID | None
    producto_id: UUID
    presentacion_id: UUID
    tipo_movimiento: str
    referencia_origen: str | None
    documento_referencia: str | None
    observacion: str | None
    cantidad: float
    cantidad_anterior: float
    cantidad_nueva: float
    costo_unitario: float
    valor_total: float
    usuario_id: UUID | None
    creado_en: datetime
