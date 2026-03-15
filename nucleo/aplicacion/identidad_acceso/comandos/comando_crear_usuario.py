from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearUsuario:
    tenant_id: UUID
    nombres: str
    apellidos: str
    nombre_usuario: str
    correo: str
    contrasena_hash: str
    esta_activo: bool = True
    es_superadministrador: bool = False
