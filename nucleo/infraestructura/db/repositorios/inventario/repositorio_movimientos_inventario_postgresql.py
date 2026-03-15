from datetime import datetime
from uuid import uuid4

from nucleo.dominio.inventario.entidades.movimiento_inventario import MovimientoInventario
from nucleo.infraestructura.db.conexion_postgresql import crear_cursor, obtener_cursor


class RepositorioMovimientosInventarioPostgresql:
    def guardar(self, movimiento, conexion=None):
        sql = """
        INSERT INTO inventario_movimientos (
            id,
            empresa_id,
            producto_id,
            presentacion_id,
            tipo_movimiento,
            subtipo_movimiento,
            cantidad,
            stock_anterior,
            stock_resultante,
            referencia_tipo,
            referencia_id,
            descripcion,
            fecha_movimiento,
            usuario_id
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        if conexion is not None:
            cursor = crear_cursor(conexion)
            try:
                cursor.execute(
                    sql,
                    (
                        movimiento.id,
                        movimiento.empresa_id,
                        movimiento.producto_id,
                        movimiento.presentacion_id,
                        movimiento.tipo_movimiento,
                        movimiento.subtipo_movimiento,
                        movimiento.cantidad,
                        movimiento.stock_anterior,
                        movimiento.stock_resultante,
                        movimiento.referencia_tipo,
                        movimiento.referencia_id,
                        movimiento.descripcion,
                        movimiento.fecha_movimiento,
                        movimiento.usuario_id,
                    ),
                )
            finally:
                cursor.close()
            return movimiento

        with obtener_cursor() as cursor:
            cursor.execute(
                sql,
                (
                    movimiento.id,
                    movimiento.empresa_id,
                    movimiento.producto_id,
                    movimiento.presentacion_id,
                    movimiento.tipo_movimiento,
                    movimiento.subtipo_movimiento,
                    movimiento.cantidad,
                    movimiento.stock_anterior,
                    movimiento.stock_resultante,
                    movimiento.referencia_tipo,
                    movimiento.referencia_id,
                    movimiento.descripcion,
                    movimiento.fecha_movimiento,
                    movimiento.usuario_id,
                ),
            )

        return movimiento

    def crear_desde_comando(self, comando, stock_anterior: float, stock_resultante: float):
        return MovimientoInventario(
            id=str(uuid4()),
            empresa_id=comando.empresa_id,
            producto_id=comando.producto_id,
            presentacion_id=comando.presentacion_id,
            tipo_movimiento=comando.tipo_movimiento,
            subtipo_movimiento=comando.subtipo_movimiento,
            cantidad=float(comando.cantidad),
            stock_anterior=float(stock_anterior),
            stock_resultante=float(stock_resultante),
            referencia_tipo=comando.referencia_tipo,
            referencia_id=comando.referencia_id,
            descripcion=comando.descripcion,
            fecha_movimiento=datetime.utcnow().isoformat(),
            usuario_id=comando.usuario_id,
        )

    def listar_por_producto(self, empresa_id: str, producto_id: str):
        sql = """
        SELECT
            id,
            empresa_id,
            producto_id,
            presentacion_id,
            tipo_movimiento,
            subtipo_movimiento,
            cantidad,
            stock_anterior,
            stock_resultante,
            referencia_tipo,
            referencia_id,
            descripcion,
            fecha_movimiento,
            usuario_id
        FROM inventario_movimientos
        WHERE empresa_id = %s
          AND producto_id = %s
        ORDER BY fecha_movimiento ASC, id ASC
        """

        with obtener_cursor(diccionario=True) as cursor:
            cursor.execute(sql, (empresa_id, producto_id))
            return [self._normalizar_fila(dict(fila)) for fila in cursor.fetchall()]

    def listar_por_presentacion(self, empresa_id: str, presentacion_id: str):
        sql = """
        SELECT
            id,
            empresa_id,
            producto_id,
            presentacion_id,
            tipo_movimiento,
            subtipo_movimiento,
            cantidad,
            stock_anterior,
            stock_resultante,
            referencia_tipo,
            referencia_id,
            descripcion,
            fecha_movimiento,
            usuario_id
        FROM inventario_movimientos
        WHERE empresa_id = %s
          AND presentacion_id = %s
        ORDER BY fecha_movimiento ASC, id ASC
        """

        with obtener_cursor(diccionario=True) as cursor:
            cursor.execute(sql, (empresa_id, presentacion_id))
            return [self._normalizar_fila(dict(fila)) for fila in cursor.fetchall()]

    def _normalizar_fila(self, fila: dict) -> dict:
        fila["cantidad"] = float(fila["cantidad"])
        fila["stock_anterior"] = float(fila["stock_anterior"])
        fila["stock_resultante"] = float(fila["stock_resultante"])
        fila["fecha_movimiento"] = str(fila["fecha_movimiento"])
        return fila
