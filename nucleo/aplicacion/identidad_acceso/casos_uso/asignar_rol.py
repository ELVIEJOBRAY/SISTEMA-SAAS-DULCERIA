from nucleo.aplicacion.identidad_acceso.comandos.comando_asignar_rol import ComandoAsignarRol
from nucleo.aplicacion.identidad_acceso.dto.rol_dto import RolDTO
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)


class AsignarRol:
    def __init__(self, servicio: ServicioAplicacionIdentidad):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoAsignarRol) -> RolDTO:
        return self.servicio.crear_rol(comando)
