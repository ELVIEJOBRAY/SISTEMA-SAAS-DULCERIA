from nucleo.aplicacion.catalogo.comandos.comando_crear_marca import ComandoCrearMarca
from nucleo.aplicacion.catalogo.dto.marca_dto import MarcaDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class CrearMarca:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearMarca) -> MarcaDTO:
        return self.servicio.crear_marca(comando)
