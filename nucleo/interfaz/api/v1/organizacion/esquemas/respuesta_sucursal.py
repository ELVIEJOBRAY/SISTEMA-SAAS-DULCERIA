from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaSucursal(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    correo: str | None
    telefono: str | None
    direccion: str | None
    es_principal: bool
    estado: str
    creado_en: datetime
    actualizado_en: datetime
