from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RespuestaMembresiaEmpresa(BaseModel):
    id: UUID
    tenant_id: UUID
    empresa_id: UUID
    usuario_id: UUID
    rol_id: UUID
    estado: str
    creado_en: datetime
