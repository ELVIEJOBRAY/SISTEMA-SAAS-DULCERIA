from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoIniciarSesion:
    tenant_id: UUID
    identificador: str
    contrasena_plana: str
