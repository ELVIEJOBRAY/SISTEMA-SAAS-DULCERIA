from nucleo.aplicacion.inventario.servicios.servicio_movimientos_inventario import ServicioMovimientosInventario
from nucleo.infraestructura.db.conexion_postgresql import obtener_conexion


class RegistrarMovimientoInventarioCasoUso:
    def __init__(self, repositorio_movimientos, repositorio_existencias):
        self.repositorio_movimientos = repositorio_movimientos
        self.repositorio_existencias = repositorio_existencias
        self.servicio = ServicioMovimientosInventario()

    def ejecutar(self, comando):
        with obtener_conexion() as conexion:
            existencia_actual = self.repositorio_existencias.buscar_existencia(
                empresa_id=comando.empresa_id,
                producto_id=comando.producto_id,
                presentacion_id=comando.presentacion_id,
                conexion=conexion,
                bloquear=True,
            )

            stock_actual = 0.0 if existencia_actual is None else float(existencia_actual["stock_actual"])

            stock_resultante = self.servicio.calcular_stock_resultante(
                stock_actual,
                comando.tipo_movimiento,
                comando.cantidad,
            )

            movimiento = self.repositorio_movimientos.crear_desde_comando(
                comando=comando,
                stock_anterior=stock_actual,
                stock_resultante=stock_resultante,
            )

            self.repositorio_movimientos.guardar(
                movimiento=movimiento,
                conexion=conexion,
            )

            self.repositorio_existencias.actualizar_stock_actual(
                empresa_id=comando.empresa_id,
                producto_id=comando.producto_id,
                presentacion_id=comando.presentacion_id,
                stock_actual=stock_resultante,
                conexion=conexion,
            )

            return movimiento
