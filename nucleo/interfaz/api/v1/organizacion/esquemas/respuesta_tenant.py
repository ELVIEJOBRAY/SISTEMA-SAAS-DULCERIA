from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaTenant(BaseModel):
    id: UUID
    nombre: str
    slug: str
    correo_contacto: str | None
    telefono_contacto: str | None
    estado: str
    creado_en: datetime
    actualizado_en: datetime
