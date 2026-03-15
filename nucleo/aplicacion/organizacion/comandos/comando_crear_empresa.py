from dataclasses import dataclass
from uuid import UUID


@dataclass
class ComandoCrearEmpresa:
    tenant_id: UUID
    nombre: str
    nit: str
    nombre_comercial: str | None = None
    correo: str | None = None
    telefono: str | None = None
    direccion: str | None = None
