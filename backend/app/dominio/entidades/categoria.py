# ==========================================================
# ENTIDAD CATEGORÍA - DOMINIO DEL SISTEMA
# ==========================================================
#
# REPRESENTA UNA CATEGORÍA DE PRODUCTOS DENTRO DEL SISTEMA SGDD.
# LAS CATEGORÍAS PERMITEN ORGANIZAR Y CLASIFICAR LOS PRODUCTOS
# PARA UNA MEJOR GESTIÓN DEL INVENTARIO.
#
# EN CLEAN ARCHITECTURE LAS ENTIDADES:
#
# - CONTIENEN LA LÓGICA DE NEGOCIO
# - NO DEPENDEN DE BASE DE DATOS
# - NO DEPENDEN DE FRAMEWORKS
# - SON EL NÚCLEO DEL SISTEMA
#
# ==========================================================

from typing import Optional
from datetime import datetime, timezone


class Categoria:

    # ======================================================
    # CONSTRUCTOR DE LA ENTIDAD CATEGORÍA
    # ======================================================
    #
    # ATRIBUTOS
    #
    # id              → IDENTIFICADOR ÚNICO
    # nombre          → NOMBRE DE LA CATEGORÍA
    # descripcion     → DESCRIPCIÓN DETALLADA (OPCIONAL)
    # activo          → ESTADO DE LA CATEGORÍA
    # fecha_creacion  → FECHA DE CREACIÓN
    # productos_count → CONTADOR DE PRODUCTOS
    #
    # ======================================================

    def __init__(
        self,
        id: Optional[int],
        nombre: str,
        descripcion: Optional[str] = None,
        activo: bool = True,
        fecha_creacion: Optional[datetime] = None,
        productos_count: int = 0
    ):

        # ==================================================
        # VALIDACIÓN DE NOMBRE
        # ==================================================
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DE LA CATEGORÍA NO PUEDE ESTAR VACÍO")

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ValueError("EL NOMBRE DE LA CATEGORÍA DEBE TENER AL MENOS 3 CARACTERES")

        # ==================================================
        # VALIDACIÓN DE DESCRIPCIÓN
        # ==================================================
        if descripcion:
            descripcion = descripcion.strip()

            if len(descripcion) < 5:
                raise ValueError("LA DESCRIPCIÓN DEBE TENER AL MENOS 5 CARACTERES")

        # ==================================================
        # VALIDACIÓN DE CONTADOR
        # ==================================================
        if productos_count < 0:
            raise ValueError("EL CONTADOR DE PRODUCTOS NO PUEDE SER NEGATIVO")

        self.id = id
        self.nombre = nombre.upper()
        self.descripcion = descripcion
        self.activo = activo
        self.fecha_creacion = fecha_creacion or datetime.now(timezone.utc)
        self.productos_count = productos_count

    # ======================================================
    # ACTIVAR CATEGORÍA
    # ======================================================

    def activar(self) -> None:
        # Activa la categoria
        self.activo = True

    # ======================================================
    # DESACTIVAR CATEGORÍA
    # ======================================================

    def desactivar(self) -> None:
        # Desactiva la categoria
        self.activo = False

    # ======================================================
    # ACTUALIZAR NOMBRE
    # ======================================================

    def actualizar_nombre(self, nuevo_nombre: str) -> None:

        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("EL NOMBRE DE LA CATEGORÍA NO PUEDE ESTAR VACÍO")

        nuevo_nombre = nuevo_nombre.strip()

        if len(nuevo_nombre) < 3:
            raise ValueError("EL NOMBRE DEBE TENER AL MENOS 3 CARACTERES")

        self.nombre = nuevo_nombre.upper()

    # ======================================================
    # ACTUALIZAR DESCRIPCIÓN
    # ======================================================

    def actualizar_descripcion(self, nueva_descripcion: Optional[str]) -> None:

        if nueva_descripcion:

            nueva_descripcion = nueva_descripcion.strip()

            if len(nueva_descripcion) < 5:
                raise ValueError("LA DESCRIPCIÓN DEBE TENER AL MENOS 5 CARACTERES")

        self.descripcion = nueva_descripcion

    # ======================================================
    # INCREMENTAR PRODUCTOS
    # ======================================================

    def incrementar_productos(self, cantidad: int = 1) -> None:

        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")

        self.productos_count += cantidad

    # ======================================================
    # DECREMENTAR PRODUCTOS
    # ======================================================

    def decrementar_productos(self, cantidad: int = 1) -> None:

        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")

        if self.productos_count - cantidad < 0:
            raise ValueError("NO PUEDE HABER PRODUCTOS NEGATIVOS")

        self.productos_count -= cantidad

    # ======================================================
    # VERIFICAR SI TIENE PRODUCTOS
    # ======================================================

    def tiene_productos(self) -> bool:
        return self.productos_count > 0

    # ======================================================
    # VERIFICAR SI ESTÁ ACTIVA
    # ======================================================

    def esta_activa(self) -> bool:
        return self.activo

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================

    def __repr__(self) -> str:

        estado = "ACTIVA" if self.activo else "INACTIVA"

        return (
            f"<Categoria id={self.id} "
            f"nombre={self.nombre} "
            f"estado={estado} "
            f"productos={self.productos_count}>"
        )
