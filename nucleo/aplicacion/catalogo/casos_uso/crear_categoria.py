from nucleo.aplicacion.catalogo.comandos.comando_crear_categoria import ComandoCrearCategoria
from nucleo.aplicacion.catalogo.dto.categoria_dto import CategoriaDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class CrearCategoria:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearCategoria) -> CategoriaDTO:
        return self.servicio.crear_categoria(comando)
