from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PresentacionDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    producto_id: UUID
    nombre: str
    codigo: str
    equivalencia_base: float
    precio_venta: float
    costo: float
    codigo_barra: str | None
    es_predeterminada: bool
    estado: str
    creado_en: datetime
    actualizado_en: datetime
