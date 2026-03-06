# ==========================================================
# ENTIDAD DETALLE VENTA (LÍNEA DE VENTA)
# SISTEMA DE TRANSACCIONES DEL NEGOCIO
# ==========================================================
#
# ESTA CLASE REPRESENTA UNA LÍNEA DE VENTA, ES DECIR,
# UN PRODUCTO INDIVIDUAL DENTRO DE UNA VENTA.
#
# UNA VENTA PUEDE TENER MÚLTIPLES DETALLES.
# CADA DETALLE CORRESPONDE A UN PRODUCTO ESPECÍFICO
# CON SU CANTIDAD, PRECIO Y DESCUENTO.
#
# RELACIÓN:
#
# VENTA (1) ──── TIENE ──── (N) DETALLES
#
# EN EL DOMINIO DEL NEGOCIO, LOS DETALLES SON IMPORTANTES PORQUE:
#
# • REGISTRAN QUÉ PRODUCTOS SE VENDIERON
# • PERMITEN CONTROLAR EL INVENTARIO POR PRODUCTO
# • GUARDAN EL PRECIO HISTÓRICO EN EL MOMENTO DE LA VENTA
# • FACILITAN DEVOLUCIONES PARCIALES
# • PERMITEN REPORTES DE VENTAS POR PRODUCTO
#
# ==========================================================

from typing import Optional, Dict, Any


class DetalleVenta:

    # ======================================================
    # CONSTRUCTOR DEL DETALLE DE VENTA
    # ======================================================
    # ESTE MÉTODO SE EJECUTA CUANDO SE AGREGA UN PRODUCTO
    # A UNA VENTA.
    #
    # SU RESPONSABILIDAD ES:
    #
    # 1 VALIDAR LOS DATOS RECIBIDOS
    # 2 ASIGNAR ATRIBUTOS INICIALES
    # 3 GARANTIZAR QUE EL DETALLE SEA VÁLIDO
    # ======================================================

    def __init__(
        self,
        id: Optional[int],
        venta_id: int,
        producto_id: int,
        nombre_producto: str,
        cantidad: int,
        precio_unitario: float,
        descuento: float = 0.0
    ) -> None:

        # ==================================================
        # VALIDACIONES DE ENTRADA
        # ==================================================
        # CADA ATRIBUTO ES VALIDADO INDIVIDUALMENTE
        # PARA GARANTIZAR LA INTEGRIDAD DEL OBJETO

        # VALIDAR QUE EL ID DE LA VENTA SEA CORRECTO
        self.venta_id = self._validar_venta_id(venta_id)

        # VALIDAR QUE EL ID DEL PRODUCTO SEA CORRECTO
        self.producto_id = self._validar_producto_id(producto_id)

        # VALIDAR QUE EL NOMBRE DEL PRODUCTO NO ESTÉ VACÍO
        self.nombre_producto = self._validar_nombre_producto(nombre_producto)

        # VALIDAR QUE LA CANTIDAD SEA POSITIVA
        self.cantidad = self._validar_cantidad(cantidad)

        # VALIDAR QUE EL PRECIO UNITARIO SEA POSITIVO
        self.precio_unitario = self._validar_precio(precio_unitario)

        # VALIDAR QUE EL DESCUENTO ESTÉ EN RANGO 0-100%
        self.descuento = self._validar_descuento(descuento)

        # ==================================================
        # ASIGNACIÓN DE ATRIBUTOS
        # ==================================================
        # LOS ATRIBUTOS SE GUARDAN EN EL OBJETO
        # Y SE CALCULA EL SUBTOTAL AUTOMÁTICAMENTE

        self.id = id  # ID del detalle, normalmente asignado por BD

        # CÁLCULO DEL SUBTOTAL: PRECIO * CANTIDAD - DESCUENTO
        self.subtotal = self._calcular_subtotal()

    # ======================================================
    # VALIDACIONES INTERNAS
    # ======================================================
    # MÉTODOS PRIVADOS PARA GARANTIZAR QUE CADA CAMPO
    # CUMPLA CON LAS REGLAS DE NEGOCIO
    # ======================================================

    def _validar_venta_id(self, venta_id: int) -> int:
        """
        VALIDA QUE EL ID DE LA VENTA SEA VÁLIDO.
        """

        if venta_id <= 0:
            raise ValueError("ID DE VENTA INVÁLIDO")

        return venta_id

    def _validar_producto_id(self, producto_id: int) -> int:
        """
        VALIDA QUE EL ID DEL PRODUCTO SEA VÁLIDO.
        """

        if producto_id <= 0:
            raise ValueError("ID DE PRODUCTO INVÁLIDO")

        return producto_id

    def _validar_nombre_producto(self, nombre_producto: str) -> str:
        """
        VALIDA QUE EL NOMBRE DEL PRODUCTO NO ESTÉ VACÍO.
        """

        if not nombre_producto or not nombre_producto.strip():
            raise ValueError("EL NOMBRE DEL PRODUCTO ES OBLIGATORIO")

        return nombre_producto.strip()

    def _validar_cantidad(self, cantidad: int) -> int:
        """
        VALIDA QUE LA CANTIDAD SEA MAYOR A CERO.
        """

        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A CERO")

        return cantidad

    def _validar_precio(self, precio: float) -> float:
        """
        VALIDA QUE EL PRECIO SEA MAYOR A CERO.
        """

        if precio <= 0:
            raise ValueError("EL PRECIO DEBE SER MAYOR A CERO")

        return precio

    def _validar_descuento(self, descuento: float) -> float:
        """
        VALIDA QUE EL DESCUENTO ESTÉ ENTRE 0 Y 100.
        """

        if descuento < 0 or descuento > 100:
            raise ValueError("EL DESCUENTO DEBE ESTAR ENTRE 0 Y 100")

        return descuento

    # ======================================================
    # CÁLCULO DE SUBTOTAL
    # ======================================================
    # CALCULA EL SUBTOTAL DE LA LÍNEA CONSIDERANDO:
    #
    # subtotal = (precio_unitario * cantidad) * (1 - descuento/100)
    # ======================================================

    def _calcular_subtotal(self) -> float:

        subtotal_sin_descuento = self.precio_unitario * self.cantidad
        subtotal_con_descuento = subtotal_sin_descuento * (1 - self.descuento / 100)

        return round(subtotal_con_descuento, 2)

    # ======================================================
    # ACTUALIZAR CANTIDAD
    # ======================================================
    # PERMITE CAMBIAR LA CANTIDAD DE UN PRODUCTO
    # EN LA VENTA. ACTUALIZA AUTOMÁTICAMENTE EL SUBTOTAL.
    # ======================================================

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:

        self.cantidad = self._validar_cantidad(nueva_cantidad)
        self.subtotal = self._calcular_subtotal()

    # ======================================================
    # ACTUALIZAR DESCUENTO
    # ======================================================
    # PERMITE CAMBIAR EL DESCUENTO APLICADO AL PRODUCTO.
    # ACTUALIZA AUTOMÁTICAMENTE EL SUBTOTAL.
    # ======================================================

    def actualizar_descuento(self, nuevo_descuento: float) -> None:

        self.descuento = self._validar_descuento(nuevo_descuento)
        self.subtotal = self._calcular_subtotal()

    # ======================================================
    # SERIALIZACIÓN
    # ======================================================
    # CONVIERTE EL DETALLE A DICCIONARIO
    # PARA RESPUESTAS API O JSON.
    # ======================================================

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "venta_id": self.venta_id,
            "producto_id": self.producto_id,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "descuento": self.descuento,
            "subtotal": self.subtotal
        }

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    # DEFINE CÓMO SE IMPRIME EL OBJETO EN CONSOLA,
    # MUY ÚTIL PARA DEPURACIÓN.
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"<DetalleVenta "
            f"id={self.id} "
            f"producto={self.nombre_producto} "
            f"cantidad={self.cantidad} "
            f"subtotal={self.subtotal}>"
        )