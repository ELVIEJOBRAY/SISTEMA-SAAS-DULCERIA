import pytest

from nucleo.aplicacion.inventario.servicios.servicio_movimientos_inventario import ServicioMovimientosInventario


def test_entrada_incrementa_stock():
    servicio = ServicioMovimientosInventario()
    assert servicio.calcular_stock_resultante(10, "entrada", 5) == 15


def test_salida_reduce_stock():
    servicio = ServicioMovimientosInventario()
    assert servicio.calcular_stock_resultante(10, "salida", 3) == 7


def test_salida_con_stock_insuficiente_lanza_error():
    servicio = ServicioMovimientosInventario()
    with pytest.raises(ValueError):
        servicio.calcular_stock_resultante(2, "salida", 5)
