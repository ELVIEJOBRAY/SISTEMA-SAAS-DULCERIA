from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaRol(BaseModel):
    id: UUID
    tenant_id: UUID
    nombre: str
    codigo: str
    descripcion: str | None
    es_sistema: bool
    creado_en: datetime
    actualizado_en: datetime
