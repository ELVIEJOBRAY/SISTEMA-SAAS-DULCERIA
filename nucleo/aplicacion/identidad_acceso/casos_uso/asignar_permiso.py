from nucleo.aplicacion.identidad_acceso.dto.permiso_dto import PermisoDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class AsignarPermiso:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self) -> list[PermisoDTO]:
        return self.servicio.listar_permisos()
