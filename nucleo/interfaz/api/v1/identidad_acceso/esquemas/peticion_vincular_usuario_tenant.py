from uuid import UUID

from pydantic import BaseModel


class PeticionVincularUsuarioTenant(BaseModel):
    tenant_id: UUID
    usuario_id: UUID
    rol_id: UUID
