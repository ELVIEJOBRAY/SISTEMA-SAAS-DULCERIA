from dataclasses import dataclass
from uuid import UUID


@dataclass
class RespuestaTokenDTO:
    access_token: str
    token_type: str
    expira_en_segundos: int
    usuario_id: UUID
    tenant_id: UUID
    nombre_usuario: str
