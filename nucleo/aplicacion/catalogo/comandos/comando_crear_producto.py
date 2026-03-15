from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearProducto:
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    sku: str
    categoria_id: UUID | None = None
    marca_id: UUID | None = None
    codigo_barra: str | None = None
    descripcion: str | None = None
    unidad_medida_base: str = "unidad"
    precio_base: float = 0
    costo_base: float = 0
    permite_venta: bool = True
    controla_inventario: bool = True
