from uuid import UUID

from pydantic import BaseModel


class PeticionVincularUsuarioEmpresa(BaseModel):
    tenant_id: UUID
    empresa_id: UUID
    usuario_id: UUID
    rol_id: UUID
