class ServicioMovimientosInventario:
    def validar_cantidad(self, cantidad: float) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

    def calcular_stock_resultante(self, stock_actual: float, tipo_movimiento: str, cantidad: float) -> float:
        self.validar_cantidad(cantidad)

        if tipo_movimiento in ("entrada", "ajuste_positivo"):
            return stock_actual + cantidad

        if tipo_movimiento in ("salida", "ajuste_negativo"):
            nuevo_stock = stock_actual - cantidad
            if nuevo_stock < 0:
                raise ValueError("Stock insuficiente para realizar el movimiento")
            return nuevo_stock

        raise ValueError("Tipo de movimiento no valido")
