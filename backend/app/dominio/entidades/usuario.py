# ==========================================================
# ENTIDAD USUARIO - DOMINIO DEL SISTEMA
# ==========================================================

# ESTA CLASE REPRESENTA LA ENTIDAD PRINCIPAL "USUARIO"
# DENTRO DEL DOMINIO DEL SISTEMA SGDD.
#
# EN CLEAN ARCHITECTURE LAS ENTIDADES:
#
# - CONTIENEN LA LÓGICA DE NEGOCIO
# - NO DEPENDEN DE BASES DE DATOS
# - NO DEPENDEN DE FRAMEWORKS
# - SON EL NÚCLEO DEL SISTEMA
#
# ESTO PERMITE:
#
# ✔ CAMBIAR INFRAESTRUCTURA SIN ROMPER EL DOMINIO
# ✔ TESTEAR LA LÓGICA FÁCILMENTE
# ✔ MANTENER EL CÓDIGO ESCALABLE
# ==========================================================

from typing import Optional
import re


class Usuario:

    # ======================================================
    # ROLES VÁLIDOS DEL SISTEMA
    # ======================================================
    # DEFINIRLOS COMO CONSTANTE PERMITE:
    #
    # ✔ EVITAR ERRORES
    # ✔ REUTILIZAR EN TODO EL SISTEMA
    # ✔ MANTENER CONSISTENCIA
    # ======================================================
    ROLES_VALIDOS = {"admin", "gerente", "vendedor", "inventario"}

    # ======================================================
    # CONSTRUCTOR DE LA ENTIDAD
    # ======================================================
    # SE EJECUTA CUANDO SE CREA UN NUEVO USUARIO
    #
    # ATRIBUTOS
    #
    # id        → IDENTIFICADOR ÚNICO
    # nombre    → NOMBRE DEL USUARIO
    # email     → CORREO ELECTRÓNICO
    # rol       → ROL DEL SISTEMA
    # activo    → ESTADO DEL USUARIO
    # ======================================================
    def __init__(
        self,
        id: Optional[int],
        nombre: str,
        email: str,
        rol: str,
        activo: bool = True
    ):

        # ==================================================
        # VALIDACIÓN DE NOMBRE
        # ==================================================
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DEL USUARIO NO PUEDE ESTAR VACÍO")

        # ==================================================
        # VALIDACIÓN DE EMAIL
        # ==================================================
        if not self._email_valido(email):
            raise ValueError("EL EMAIL NO TIENE UN FORMATO VÁLIDO")

        # ==================================================
        # VALIDACIÓN DE ROL
        # ==================================================
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(
                f"ROL INVÁLIDO. DEBE SER UNO DE: {self.ROLES_VALIDOS}"
            )

        self.id = id
        self.nombre = nombre.strip()
        self.email = email.lower()
        self.rol = rol
        self.activo = activo

    # ======================================================
    # VALIDACIÓN DE EMAIL
    # ======================================================
    # MÉTODO INTERNO PARA VALIDAR FORMATO DE EMAIL
    # ======================================================
    def _email_valido(self, email: str) -> bool:
        patron = r"[^@]+@[^@]+\.[^@]+"
        return re.match(patron, email) is not None

    # ======================================================
    # ACTIVAR USUARIO
    # ======================================================
    # HABILITA EL ACCESO AL SISTEMA
    # ======================================================
    def activar(self) -> None:
        self.activo = True

    # ======================================================
    # DESACTIVAR USUARIO
    # ======================================================
    # PERMITE BLOQUEAR EL ACCESO SIN ELIMINAR EL REGISTRO
    #
    # ESTO ES UNA BUENA PRÁCTICA LLAMADA:
    # SOFT DISABLE
    # ======================================================
    def desactivar(self) -> None:
        self.activo = False

    # ======================================================
    # CAMBIAR ROL
    # ======================================================
    # PERMITE MODIFICAR EL ROL DEL USUARIO
    # VALIDANDO QUE SEA UN ROL PERMITIDO
    # ======================================================
    def cambiar_rol(self, nuevo_rol: str) -> None:

        if nuevo_rol not in self.ROLES_VALIDOS:
            raise ValueError(
                f"ROL INVÁLIDO. DEBE SER UNO DE: {self.ROLES_VALIDOS}"
            )

        self.rol = nuevo_rol

    # ======================================================
    # VERIFICAR SI ES ADMIN
    # ======================================================
    # ESTE MÉTODO PERMITE ESCRIBIR CÓDIGO MÁS LIMPIO
    #
    # EJEMPLO:
    #
    # if usuario.es_admin():
    #     permitir_operacion()
    # ======================================================
    def es_admin(self) -> bool:
        return self.rol == "admin"

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    # DEFINE CÓMO SE MUESTRA EL OBJETO EN LOGS O CONSOLA
    # ======================================================
    def __repr__(self) -> str:
        return f"<Usuario id={self.id} nombre={self.nombre} rol={self.rol} activo={self.activo}>"
