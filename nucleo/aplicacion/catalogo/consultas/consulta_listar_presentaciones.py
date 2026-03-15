from uuid import UUID

from nucleo.aplicacion.catalogo.dto.presentacion_dto import PresentacionDTO
from nucleo.aplicacion.catalogo.servicios.servicio_aplicacion_catalogo import (
    ServicioAplicacionCatalogo,
)


class ConsultaListarPresentaciones:
    def __init__(self, servicio: ServicioAplicacionCatalogo):
        self.servicio = servicio

    def ejecutar(self, producto_id: UUID) -> list[PresentacionDTO]:
        return self.servicio.listar_presentaciones(producto_id)
