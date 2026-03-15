from nucleo.aplicacion.inventario.comandos.comando_registrar_salida_inventario import (
    ComandoRegistrarSalidaInventario,
)
from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class RegistrarSalidaInventario:
    def __init__(self, servicio: ServicioAplicacionInventario):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoRegistrarSalidaInventario) -> MovimientoInventarioDTO:
        return self.servicio.registrar_salida(comando)
