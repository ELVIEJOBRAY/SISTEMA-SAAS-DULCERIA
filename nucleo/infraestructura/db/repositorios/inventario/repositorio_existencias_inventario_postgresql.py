from uuid import uuid4

from nucleo.infraestructura.db.conexion_postgresql import crear_cursor, obtener_cursor


class RepositorioExistenciasInventarioPostgresql:
    def obtener_stock_actual(self, empresa_id: str, producto_id: str, presentacion_id: str | None = None, conexion=None):
        existente = self.buscar_existencia(
            empresa_id=empresa_id,
            producto_id=producto_id,
            presentacion_id=presentacion_id,
            conexion=conexion,
            bloquear=False,
        )
        if existente is None:
            return 0.0
        return float(existente["stock_actual"])

    def buscar_existencia(self, empresa_id: str, producto_id: str, presentacion_id: str | None, conexion=None, bloquear: bool = False):
        clausula_bloqueo = " FOR UPDATE" if bloquear else ""

        if presentacion_id is None:
            sql = f"""
            SELECT id, empresa_id, producto_id, presentacion_id, stock_actual, updated_at
            FROM inventario_existencias
            WHERE empresa_id = %s
              AND producto_id = %s
              AND presentacion_id IS NULL
            LIMIT 1{clausula_bloqueo}
            """
            parametros = (empresa_id, producto_id)
        else:
            sql = f"""
            SELECT id, empresa_id, producto_id, presentacion_id, stock_actual, updated_at
            FROM inventario_existencias
            WHERE empresa_id = %s
              AND producto_id = %s
              AND presentacion_id = %s
            LIMIT 1{clausula_bloqueo}
            """
            parametros = (empresa_id, producto_id, presentacion_id)

        if conexion is not None:
            cursor = crear_cursor(conexion, diccionario=True)
            try:
                cursor.execute(sql, parametros)
                fila = cursor.fetchone()
                return dict(fila) if fila else None
            finally:
                cursor.close()

        with obtener_cursor(diccionario=True) as cursor:
            cursor.execute(sql, parametros)
            fila = cursor.fetchone()
            return dict(fila) if fila else None

    def actualizar_stock_actual(self, empresa_id: str, producto_id: str, presentacion_id: str | None, stock_actual: float, conexion=None):
        existente = self.buscar_existencia(
            empresa_id=empresa_id,
            producto_id=producto_id,
            presentacion_id=presentacion_id,
            conexion=conexion,
            bloquear=True if conexion is not None else False,
        )

        if existente is None:
            return self._crear_existencia(
                empresa_id=empresa_id,
                producto_id=producto_id,
                presentacion_id=presentacion_id,
                stock_actual=stock_actual,
                conexion=conexion,
            )

        return self._actualizar_existencia(
            id_existencia=existente["id"],
            stock_actual=stock_actual,
            conexion=conexion,
        )

    def _crear_existencia(self, empresa_id: str, producto_id: str, presentacion_id: str | None, stock_actual: float, conexion=None):
        id_existencia = str(uuid4())

        sql = """
        INSERT INTO inventario_existencias (
            id,
            empresa_id,
            producto_id,
            presentacion_id,
            stock_actual,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """

        if conexion is not None:
            cursor = crear_cursor(conexion)
            try:
                cursor.execute(
                    sql,
                    (
                        id_existencia,
                        empresa_id,
                        producto_id,
                        presentacion_id,
                        float(stock_actual),
                    ),
                )
            finally:
                cursor.close()
        else:
            with obtener_cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        id_existencia,
                        empresa_id,
                        producto_id,
                        presentacion_id,
                        float(stock_actual),
                    ),
                )

        return {
            "id": id_existencia,
            "empresa_id": empresa_id,
            "producto_id": producto_id,
            "presentacion_id": presentacion_id,
            "stock_actual": float(stock_actual),
        }

    def _actualizar_existencia(self, id_existencia: str, stock_actual: float, conexion=None):
        sql = """
        UPDATE inventario_existencias
        SET stock_actual = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """

        if conexion is not None:
            cursor = crear_cursor(conexion)
            try:
                cursor.execute(sql, (float(stock_actual), id_existencia))
            finally:
                cursor.close()
        else:
            with obtener_cursor() as cursor:
                cursor.execute(sql, (float(stock_actual), id_existencia))

        return {
            "id": id_existencia,
            "stock_actual": float(stock_actual),
        }
