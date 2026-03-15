from nucleo.aplicacion.inventario.comandos.comando_registrar_entrada_inventario import (
    ComandoRegistrarEntradaInventario,
)
from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class RegistrarEntradaInventario:
    def __init__(self, servicio: ServicioAplicacionInventario):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoRegistrarEntradaInventario) -> MovimientoInventarioDTO:
        return self.servicio.registrar_entrada(comando)
