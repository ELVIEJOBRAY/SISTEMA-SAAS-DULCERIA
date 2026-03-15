from nucleo.aplicacion.inventario.comandos.comando_registrar_ajuste_inventario import (
    ComandoRegistrarAjusteInventario,
)
from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.aplicacion.inventario.servicios.servicio_aplicacion_inventario import (
    ServicioAplicacionInventario,
)


class RegistrarAjusteInventario:
    def __init__(self, servicio: ServicioAplicacionInventario):
        self.servicio = servicio

    def ejecutar(self, comando: ComandoRegistrarAjusteInventario) -> MovimientoInventarioDTO:
        return self.servicio.registrar_ajuste(comando)
