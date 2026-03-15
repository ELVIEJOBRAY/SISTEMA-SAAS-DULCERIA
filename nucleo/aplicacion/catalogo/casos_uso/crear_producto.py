from nucleo.aplicacion.catalogo.comandos.comando_crear_producto import ComandoCrearProducto
from nucleo.aplicacion.catalogo.dto.producto_dto import ProductoDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class CrearProducto:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoCrearProducto) -> ProductoDTO:
        return self.servicio.crear_producto(comando)
