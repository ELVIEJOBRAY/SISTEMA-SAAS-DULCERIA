class ErrorInventario(Exception):
    pass

class ErrorStockInsuficiente(ErrorInventario):
    pass

class ErrorMovimientoInvalido(ErrorInventario):
    pass
