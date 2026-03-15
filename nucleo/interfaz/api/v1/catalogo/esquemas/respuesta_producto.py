from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaProducto(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    categoria_id: UUID | None
    marca_id: UUID | None
    nombre: str
    sku: str
    codigo_barra: str | None
    descripcion: str | None
    unidad_medida_base: str
    precio_base: float
    costo_base: float
    permite_venta: bool
    controla_inventario: bool
    estado: str
    creado_en: datetime
    actualizado_en: datetime
