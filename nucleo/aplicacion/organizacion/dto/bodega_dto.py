from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class BodegaDTO:
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    nombre: str
    codigo: str
    tipo: str
    permite_venta: bool
    estado: str
    creado_en: datetime
    actualizado_en: datetime
