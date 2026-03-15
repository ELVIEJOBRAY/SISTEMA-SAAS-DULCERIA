from dataclasses import dataclass


@dataclass
class ComandoCrearTenant:
    nombre: str
    slug: str
    correo_contacto: str | None = None
    telefono_contacto: str | None = None
