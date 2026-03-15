from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearBodega:
    tenant_id: UUID
    empresa_id: UUID
    sucursal_id: UUID
    nombre: str
    codigo: str
    tipo: str = "general"
    permite_venta: bool = False
