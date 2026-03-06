# ==========================================================
# ENTIDAD PRODUCTO - DOMINIO DEL SISTEMA
# ==========================================================
#
# ESTA CLASE REPRESENTA UN PRODUCTO DENTRO DEL SISTEMA SGDD.
#
# EN CLEAN ARCHITECTURE LAS ENTIDADES:
#
# - CONTIENEN LA LÓGICA DE NEGOCIO
# - NO DEPENDEN DE BASE DE DATOS
# - NO DEPENDEN DE FRAMEWORKS
# - SON EL NÚCLEO DEL SISTEMA
#
# ESTO PERMITE:
#
# ✔ MANTENER EL SISTEMA ESCALABLE
# ✔ TESTEAR FÁCILMENTE
# ✔ CAMBIAR INFRAESTRUCTURA SIN AFECTAR EL DOMINIO
#
# ==========================================================

from typing import Optional


class Producto:

    # ======================================================
    # CONSTRUCTOR DE LA ENTIDAD PRODUCTO
    # ======================================================
    #
    # ATRIBUTOS
    #
    # id        → IDENTIFICADOR ÚNICO
    # nombre    → NOMBRE DEL PRODUCTO
    # precio    → PRECIO DE VENTA
    # stock     → CANTIDAD DISPONIBLE
    # categoria → CATEGORÍA DEL PRODUCTO
    #
    # ======================================================
    def __init__(
        self,
        id: Optional[int],
        nombre: str,
        precio: float,
        stock: int,
        categoria: str
    ):

        # ==================================================
        # VALIDACIÓN DE NOMBRE
        # ==================================================
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DEL PRODUCTO NO PUEDE ESTAR VACÍO")

        # ==================================================
        # VALIDACIÓN DE PRECIO
        # ==================================================
        if precio < 0:
            raise ValueError("EL PRECIO NO PUEDE SER NEGATIVO")

        # ==================================================
        # VALIDACIÓN DE STOCK
        # ==================================================
        if stock < 0:
            raise ValueError("EL STOCK NO PUEDE SER NEGATIVO")

        # ==================================================
        # VALIDACIÓN DE CATEGORÍA
        # ==================================================
        if not categoria or not categoria.strip():
            raise ValueError("LA CATEGORÍA NO PUEDE ESTAR VACÍA")

        self.id = id
        self.nombre = nombre.strip()
        self.precio = precio
        self.stock = stock
        self.categoria = categoria.strip()

    # ======================================================
    # REDUCIR STOCK
    # ======================================================
    #
    # SE UTILIZA CUANDO SE REALIZA UNA VENTA
    #
    # VALIDA:
    # - QUE LA CANTIDAD SEA POSITIVA
    # - QUE HAYA SUFICIENTE STOCK
    #
    # ======================================================
    def reducir_stock(self, cantidad: int) -> None:

        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")

        if cantidad > self.stock:
            raise ValueError("STOCK INSUFICIENTE")

        self.stock -= cantidad

    # ======================================================
    # AUMENTAR STOCK
    # ======================================================
    #
    # SE UTILIZA CUANDO:
    #
    # - LLEGA INVENTARIO
    # - SE REPONE PRODUCTO
    #
    # ======================================================
    def aumentar_stock(self, cantidad: int) -> None:

        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")

        self.stock += cantidad

    # ======================================================
    # CAMBIAR PRECIO
    # ======================================================
    #
    # PERMITE MODIFICAR EL PRECIO DEL PRODUCTO
    # VALIDANDO QUE NO SEA NEGATIVO
    #
    # ======================================================
    def cambiar_precio(self, nuevo_precio: float) -> None:

        if nuevo_precio < 0:
            raise ValueError("EL PRECIO NO PUEDE SER NEGATIVO")

        self.precio = nuevo_precio

    # ======================================================
    # VERIFICAR DISPONIBILIDAD
    # ======================================================
    #
    # PERMITE SABER SI HAY STOCK DISPONIBLE
    #
    # EJEMPLO:
    #
    # if producto.disponible():
    #     vender()
    #
    # ======================================================
    def disponible(self) -> bool:
        return self.stock > 0

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    #
    # DEFINE CÓMO SE MUESTRA EL OBJETO EN LOGS O CONSOLA
    #
    # ======================================================
    def __repr__(self) -> str:
        return (
            f"<Producto id={self.id} "
            f"nombre={self.nombre} "
            f"precio={self.precio} "
            f"stock={self.stock} "
            f"categoria={self.categoria}>"
        )
