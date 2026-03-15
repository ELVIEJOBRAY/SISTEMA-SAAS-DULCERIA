from nucleo.aplicacion.catalogo.comandos.comando_crear_presentacion import ComandoCrearPresentacion
from nucleo.aplicacion.catalogo.dto.presentacion_dto import PresentacionDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class CrearPresentacion:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearPresentacion) -> PresentacionDTO:
        return self.servicio.crear_presentacion(comando)
