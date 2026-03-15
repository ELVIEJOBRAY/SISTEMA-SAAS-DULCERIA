from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearPresentacion:
    tenant_id: UUID
    empresa_id: UUID
    producto_id: UUID
    nombre: str
    codigo: str
    equivalencia_base: float = 1
    precio_venta: float = 0
    costo: float = 0
    codigo_barra: str | None = None
    es_predeterminada: bool = False
