from pydantic import BaseModel
from typing import Optional

class FacturaCreateDTO(BaseModel):
    venta_id: int
    numero_factura: str
    cliente_nombre: str
    cliente_identificacion: str
    tipo: Optional[str] = "factura"
    cliente_direccion: Optional[str] = None

class FacturaUpdateDTO(BaseModel):
    estado: Optional[str] = None

class FacturaResponseDTO(BaseModel):
    id: int
    venta_id: int
    numero_factura: str
    tipo: str
    estado: str
    subtotal: float
    total: float
    class Config: from_attributes = True
