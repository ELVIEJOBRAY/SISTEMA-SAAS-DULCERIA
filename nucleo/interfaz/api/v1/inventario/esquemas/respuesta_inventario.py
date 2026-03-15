from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaInventario(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    bodega_id: UUID
    producto_id: UUID
    presentacion_id: UUID
    cantidad_disponible: float
    cantidad_reservada: float
    cantidad_transito: float
    stock_minimo: float
    stock_maximo: float
    costo_promedio: float
    creado_en: datetime
    actualizado_en: datetime
