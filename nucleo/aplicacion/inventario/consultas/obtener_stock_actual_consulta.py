class ObtenerStockActualConsulta:
    def __init__(self, repositorio_existencias):
        self.repositorio_existencias = repositorio_existencias

    def ejecutar(self, empresa_id: str, producto_id: str, presentacion_id: str | None = None):
        return self.repositorio_existencias.obtener_stock_actual(
            empresa_id,
            producto_id,
            presentacion_id,
        )
