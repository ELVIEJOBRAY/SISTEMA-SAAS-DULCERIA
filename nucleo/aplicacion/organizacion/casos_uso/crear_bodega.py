from nucleo.aplicacion.organizacion.comandos.comando_crear_bodega import ComandoCrearBodega
from nucleo.aplicacion.organizacion.dto.bodega_dto import BodegaDTO
from nucleo.aplicacion.organizacion.servicios.servicio_aplicacion_organizacion import (
    ServicioAplicacionOrganizacion,
)


class CrearBodega:
    def __init__(self, servicio: ServicioAplicacionOrganizacion):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearBodega) -> BodegaDTO:
        return self.servicio.crear_bodega(comando)
