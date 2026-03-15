from uuid import UUID

from pydantic import BaseModel


class RespuestaToken(BaseModel):
    access_token: str
    token_type: str
    expira_en_segundos: int
    usuario_id: UUID
    tenant_id: UUID
    nombre_usuario: str
