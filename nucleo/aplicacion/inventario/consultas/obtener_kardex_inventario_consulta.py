class ObtenerKardexInventarioConsulta:
    def __init__(self, repositorio_movimientos):
        self.repositorio_movimientos = repositorio_movimientos

    def por_producto(self, empresa_id: str, producto_id: str):
        return self.repositorio_movimientos.listar_por_producto(
            empresa_id=empresa_id,
            producto_id=producto_id,
        )

    def por_presentacion(self, empresa_id: str, presentacion_id: str):
        return self.repositorio_movimientos.listar_por_presentacion(
            empresa_id=empresa_id,
            presentacion_id=presentacion_id,
        )
