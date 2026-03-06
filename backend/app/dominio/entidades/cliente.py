# ==========================================================
# ENTIDAD CLIENTE
# DOMINIO CENTRAL DEL NEGOCIO
# ==========================================================
# ESTA CLASE REPRESENTA EL CONCEPTO DE CLIENTE DENTRO DEL
# DOMINIO PRINCIPAL DEL SISTEMA.
#
# EN ARQUITECTURA LIMPIA (CLEAN ARCHITECTURE) EL DOMINIO
# ES LA CAPA MÁS IMPORTANTE DEL SOFTWARE.
#
# EN ESTA CAPA SE DEFINEN:
#
# - LAS REGLAS DE NEGOCIO
# - LAS VALIDACIONES
# - EL COMPORTAMIENTO DEL CLIENTE
# - LAS GARANTÍAS DE CONSISTENCIA
#
# ESTO SIGNIFICA QUE UN CLIENTE INVÁLIDO
# NUNCA DEBERÍA EXISTIR EN MEMORIA.
#
# ESTA CLASE PROTEGE EL SISTEMA CONTRA:
#
# - DATOS CORRUPTOS
# - DATOS INCOMPLETOS
# - ESTADOS INVÁLIDOS
#
# EN SISTEMAS EMPRESARIALES GRANDES
# ESTA CLASE REPRESENTA UNA ENTIDAD
# DEL DOMINIO (DOMAIN ENTITY).
# ==========================================================

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import re


class Cliente:

    # ======================================================
    # CONSTANTES DEL SISTEMA
    # ======================================================
    # ESTAS CONSTANTES DEFINEN LOS TIPOS DE CLIENTE
    # QUE EL SISTEMA RECONOCE.
    #
    # UTILIZAR CONSTANTES ES UNA BUENA PRÁCTICA
    # PORQUE EVITA ERRORES DE ESCRITURA.
    #
    # EJEMPLO DE ERROR COMÚN:
    #
    # if cliente.tipo == "Vip"
    #
    # LA "V" MAYÚSCULA ROMPERÍA LA LÓGICA.
    #
    # UTILIZANDO CONSTANTES:
    #
    # if cliente.tipo == Cliente.TIPO_VIP
    #
    # EL SISTEMA SE VUELVE MÁS SEGURO Y MANTENIBLE.
    # ======================================================

    TIPO_REGULAR = "regular"
    TIPO_VIP = "vip"
    TIPO_EMPRESA = "empresa"

    # ======================================================
    # LISTA OFICIAL DE TIPOS DE CLIENTE
    # ======================================================
    # ESTA LISTA DEFINE TODOS LOS TIPOS DE CLIENTES
    # QUE EL SISTEMA PERMITE.
    #
    # SI SE INTENTA CREAR UN CLIENTE CON UN TIPO
    # DIFERENTE A ESTOS, EL SISTEMA GENERARÁ
    # UNA EXCEPCIÓN.
    #
    # ESTO PROTEGE LA CONSISTENCIA DEL DOMINIO.
    # ======================================================

    TIPOS_VALIDOS = [
        TIPO_REGULAR,
        TIPO_VIP,
        TIPO_EMPRESA
    ]

    # ======================================================
    # CONSTRUCTOR DEL CLIENTE
    # ======================================================
    # ESTE MÉTODO SE EJECUTA CUANDO SE CREA
    # UNA NUEVA INSTANCIA DE CLIENTE.
    #
    # SU RESPONSABILIDAD ES:
    #
    # 1 VALIDAR LOS DATOS RECIBIDOS
    # 2 ASIGNAR LOS VALORES AL OBJETO
    # 3 GARANTIZAR QUE EL OBJETO SEA VÁLIDO
    #
    # EN SISTEMAS PROFESIONALES ES CRÍTICO
    # QUE LAS ENTIDADES NUNCA EXISTAN
    # EN ESTADOS INVÁLIDOS.
    #
    # TODAS LAS VALIDACIONES SE REALIZAN
    # EN ESTE MOMENTO.
    # ======================================================

    def __init__(
        self,
        id: Optional[int],
        nombre: str,
        email: str,
        telefono: Optional[str] = None,
        tipo: str = TIPO_REGULAR,
        activo: bool = True
    ) -> None:

        # --------------------------------------------------
        # IDENTIFICADOR DEL CLIENTE
        # --------------------------------------------------
        # ESTE CAMPO REPRESENTA EL ID DEL CLIENTE
        # EN LA BASE DE DATOS.
        #
        # NORMALMENTE ES GENERADO POR LA BD
        # (AUTO INCREMENT).
        #
        # POR ESO PUEDE SER None AL CREAR
        # UN CLIENTE NUEVO.
        # --------------------------------------------------

        self.id = id

        # --------------------------------------------------
        # VALIDACIÓN DEL NOMBRE DEL CLIENTE
        # --------------------------------------------------
        # SE UTILIZA UN MÉTODO PRIVADO PARA:
        #
        # - MANTENER EL CONSTRUCTOR LIMPIO
        # - REUTILIZAR VALIDACIONES
        # - CENTRALIZAR REGLAS DE NEGOCIO
        # --------------------------------------------------

        self.nombre = self._validar_nombre(nombre)

        # --------------------------------------------------
        # VALIDACIÓN DEL EMAIL
        # --------------------------------------------------
        # EL EMAIL ES UNO DE LOS DATOS
        # MÁS IMPORTANTES DEL CLIENTE.
        #
        # POR ESO SE VALIDA FORMATO
        # Y SE NORMALIZA.
        # --------------------------------------------------

        self.email = self._validar_email(email)

        # --------------------------------------------------
        # VALIDACIÓN DEL TELÉFONO
        # --------------------------------------------------
        # EL TELÉFONO ES OPCIONAL.
        #
        # SI EXISTE, DEBE CUMPLIR
        # LAS REGLAS DE VALIDACIÓN.
        # --------------------------------------------------

        self.telefono = self._validar_telefono(telefono)

        # --------------------------------------------------
        # VALIDACIÓN DEL TIPO DE CLIENTE
        # --------------------------------------------------
        # ASEGURA QUE EL TIPO
        # SEA UNO DE LOS PERMITIDOS.
        # --------------------------------------------------

        self.tipo = self._validar_tipo(tipo)

        # --------------------------------------------------
        # ESTADO DEL CLIENTE
        # --------------------------------------------------
        # INDICA SI EL CLIENTE
        # ESTÁ ACTIVO EN EL SISTEMA.
        #
        # UN CLIENTE DESACTIVADO
        # NO DEBERÍA PODER REALIZAR
        # OPERACIONES IMPORTANTES.
        # --------------------------------------------------

        self.activo = activo

        # --------------------------------------------------
        # FECHA DE CREACIÓN
        # --------------------------------------------------
        # REGISTRA EL MOMENTO EN QUE
        # EL CLIENTE FUE CREADO.
        #
        # SE USA UTC PARA EVITAR
        # PROBLEMAS DE ZONA HORARIA.
        # --------------------------------------------------

        self.fecha_creacion: datetime = datetime.now(timezone.utc)

        # --------------------------------------------------
        # FECHA DE ACTUALIZACIÓN
        # --------------------------------------------------
        # REGISTRA CUÁNDO FUE
        # MODIFICADO EL CLIENTE
        # POR ÚLTIMA VEZ.
        # --------------------------------------------------

        self.fecha_actualizacion: datetime = datetime.now(timezone.utc)

    # ======================================================
    # VALIDACIÓN DEL NOMBRE DEL CLIENTE
    # ======================================================
    # ESTE MÉTODO GARANTIZA QUE EL NOMBRE
    # CUMPLA LAS REGLAS BÁSICAS DEL NEGOCIO.
    #
    # VALIDACIONES:
    #
    # 1 NO PUEDE SER VACÍO
    # 2 DEBE TENER AL MENOS 3 CARACTERES
    # 3 SE ELIMINAN ESPACIOS
    #
    # ESTO EVITA REGISTROS COMO:
    #
    # ""
    # " "
    # "A"
    # ======================================================

    def _validar_nombre(self, nombre: str) -> str:

        if not nombre:
            raise ValueError("EL NOMBRE DEL CLIENTE ES OBLIGATORIO")

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ValueError("EL NOMBRE DEBE TENER AL MENOS 3 CARACTERES")

        return nombre

    # ======================================================
    # VALIDACIÓN DEL EMAIL
    # ======================================================
    # ESTE MÉTODO VERIFICA QUE EL EMAIL
    # TENGA UN FORMATO CORRECTO.
    #
    # SE UTILIZA UNA EXPRESIÓN REGULAR (REGEX)
    # PARA VALIDAR EL FORMATO.
    #
    # EJEMPLOS VÁLIDOS:
    #
    # usuario@email.com
    # cliente.test@gmail.com
    #
    # EJEMPLOS INVÁLIDOS:
    #
    # cliente@
    # cliente.com
    # @gmail.com
    # ======================================================

    def _validar_email(self, email: str) -> str:

        if not email:
            raise ValueError("EL EMAIL ES OBLIGATORIO")

        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(patron, email):
            raise ValueError("FORMATO DE EMAIL INVÁLIDO")

        # NORMALIZAR EMAIL A MINÚSCULAS
        # ESTO EVITA DUPLICADOS COMO:
        #
        # CLIENTE@EMAIL.COM
        # cliente@email.com

        return email.lower()

    # ======================================================
    # VALIDACIÓN DEL TELÉFONO
    # ======================================================
    # ESTE MÉTODO VALIDA EL NÚMERO TELEFÓNICO.
    #
    # REGLAS:
    #
    # 1 ES OPCIONAL
    # 2 SI EXISTE SOLO DEBE CONTENER NÚMEROS
    # 3 DEBE TENER AL MENOS 7 DÍGITOS
    #
    # ESTO EVITA REGISTROS COMO:
    #
    # "abc123"
    # "12"
    # "telefono"
    # ======================================================

    def _validar_telefono(self, telefono: Optional[str]) -> Optional[str]:

        if telefono is None:
            return None

        telefono = telefono.strip()

        if not telefono.isdigit():
            raise ValueError("EL TELÉFONO SOLO DEBE CONTENER NÚMEROS")

        if len(telefono) < 7:
            raise ValueError("NÚMERO DE TELÉFONO INVÁLIDO")

        return telefono

    # ======================================================
    # VALIDACIÓN DEL TIPO DE CLIENTE
    # ======================================================
    # GARANTIZA QUE EL TIPO
    # SEA UNO DE LOS DEFINIDOS
    # EN TIPOS_VALIDOS.
    #
    # ESTO PROTEGE LAS REGLAS
    # DE NEGOCIO DEL SISTEMA.
    # ======================================================

    def _validar_tipo(self, tipo: str) -> str:

        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(
                f"TIPO INVÁLIDO. DEBE SER UNO DE: {self.TIPOS_VALIDOS}"
            )

        return tipo

    # ======================================================
    # MÉTODOS DE COMPORTAMIENTO
    # ======================================================
    # ESTOS MÉTODOS REPRESENTAN
    # ACCIONES QUE PUEDEN REALIZARSE
    # SOBRE UN CLIENTE.
    # ======================================================

    def activar(self) -> None:

        # SI YA ESTÁ ACTIVO
        # NO HACER NADA

        if self.activo:
            return

        self.activo = True
        self._registrar_actualizacion()

    def desactivar(self) -> None:

        if not self.activo:
            return

        self.activo = False
        self._registrar_actualizacion()

    def cambiar_tipo(self, nuevo_tipo: str) -> None:

        self.tipo = self._validar_tipo(nuevo_tipo)
        self._registrar_actualizacion()

    def actualizar_email(self, nuevo_email: str) -> None:

        self.email = self._validar_email(nuevo_email)
        self._registrar_actualizacion()

    def actualizar_telefono(self, nuevo_telefono: Optional[str]) -> None:

        self.telefono = self._validar_telefono(nuevo_telefono)
        self._registrar_actualizacion()

    def actualizar_nombre(self, nuevo_nombre: str) -> None:

        self.nombre = self._validar_nombre(nuevo_nombre)
        self._registrar_actualizacion()

    # ======================================================
    # MÉTODOS DE CONSULTA
    # ======================================================

    def es_vip(self) -> bool:
        return self.tipo == self.TIPO_VIP

    def es_empresa(self) -> bool:
        return self.tipo == self.TIPO_EMPRESA

    def esta_activo(self) -> bool:
        return self.activo

    # ======================================================
    # REGISTRO DE ACTUALIZACIÓN
    # ======================================================
    # ESTE MÉTODO ACTUALIZA LA FECHA
    # CADA VEZ QUE EL CLIENTE CAMBIA.
    # ======================================================

    def _registrar_actualizacion(self) -> None:
        self.fecha_actualizacion = datetime.now(timezone.utc)

    # ======================================================
    # SERIALIZACIÓN DEL CLIENTE
    # ======================================================
    # CONVIERTE EL OBJETO CLIENTE
    # A UN DICCIONARIO.
    #
    # ESTO ES NECESARIO PARA:
    #
    # - RESPUESTAS API
    # - SERIALIZACIÓN JSON
    # - LOGS
    # - ENVÍO DE DATOS
    # ======================================================

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "tipo": self.tipo,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat()
        }

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    # DEFINE CÓMO SE MUESTRA EL OBJETO
    # CUANDO SE IMPRIME EN CONSOLA.
    #
    # MUY ÚTIL PARA:
    #
    # - DEBUG
    # - LOGS
    # - DESARROLLO
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"<Cliente "
            f"id={self.id} "
            f"nombre='{self.nombre}' "
            f"tipo='{self.tipo}' "
            f"activo={self.activo}>"
        )