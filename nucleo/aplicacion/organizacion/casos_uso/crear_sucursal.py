from nucleo.aplicacion.organizacion.comandos.comando_crear_sucursal import ComandoCrearSucursal
from nucleo.aplicacion.organizacion.dto.sucursal_dto import SucursalDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class CrearSucursal:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearSucursal) -> SucursalDTO:
        return self.servicio.crear_sucursal(comando)
