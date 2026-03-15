from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaUsuario(BaseModel):
    id: UUID
    tenant_id: UUID
    nombres: str
    apellidos: str
    nombre_usuario: str
    correo: str
    esta_activo: bool
    es_superadministrador: bool
    ultimo_acceso: datetime | None
    creado_en: datetime
    actualizado_en: datetime
