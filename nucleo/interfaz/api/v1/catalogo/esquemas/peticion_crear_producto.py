from uuid import UUID

from pydantic import BaseModel, Field


class PeticionCrearProducto(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    nombre: str = Field(..., min_length=2, max_length=180)
    sku: str = Field(..., min_length=2, max_length=80)
    categoria_id: UUID | None = None
    marca_id: UUID | None = None
    codigo_barra: str | None = None
    descripcion: str | None = None
    unidad_medida_base: str = Field(default="unidad", max_length=30)
    precio_base: float = 0
    costo_base: float = 0
    permite_venta: bool = True
    controla_inventario: bool = True
