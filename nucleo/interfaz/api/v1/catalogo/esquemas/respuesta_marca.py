from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaMarca(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None
    estado: str
    creado_en: datetime
    actualizado_en: datetime
