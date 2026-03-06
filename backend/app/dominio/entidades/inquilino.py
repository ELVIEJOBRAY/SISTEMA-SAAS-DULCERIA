# ==========================================================
# ENTIDAD INQUILINO (TENANT) - DOMINIO DEL SISTEMA
# ==========================================================
#
# ESTE ARCHIVO DEFINE LA ENTIDAD PRINCIPAL DEL MODELO SAAS:
# EL "INQUILINO" O "TENANT".
#
# EN UN SISTEMA SAAS MULTI-TENANT, CADA EMPRESA QUE USA
# EL SOFTWARE SE REPRESENTA COMO UN TENANT.
#
# EJEMPLO REAL:
#
# empresa1.sistema.com
# empresa2.sistema.com
# empresa3.sistema.com
#
# CADA UNA DE ESTAS EMPRESAS ES UN "INQUILINO".
#
# ESTA CLASE PERTENECE A LA CAPA DE DOMINIO SEGÚN
# CLEAN ARCHITECTURE Y DOMAIN DRIVEN DESIGN.
#
# ESTO SIGNIFICA QUE:
#
# ✔ NO DEPENDE DE FASTAPI
# ✔ NO DEPENDE DE BASE DE DATOS
# ✔ NO DEPENDE DE FRAMEWORKS
#
# SOLO CONTIENE:
#
# ✔ REGLAS DE NEGOCIO
# ✔ VALIDACIONES
# ✔ LÓGICA DEL DOMINIO
#
# ESTO PERMITE QUE EL DOMINIO SEA:
#
# ✔ REUTILIZABLE
# ✔ TESTEABLE
# ✔ INDEPENDIENTE
#
# ==========================================================


# ==========================================================
# IMPORTACIONES DEL SISTEMA
# ==========================================================

# Optional
# PERMITE INDICAR QUE UN VALOR PUEDE SER None
from typing import Optional

# Dict
# REPRESENTA DICCIONARIOS TIPADOS
from typing import Dict

# Any
# PERMITE VALORES DE CUALQUIER TIPO
from typing import Any

# Tuple
# REPRESENTA UNA TUPLA TIPADA (VALORES INMUTABLES)
from typing import Tuple


# datetime
# UTILIZADO PARA MANEJAR FECHAS Y HORAS
from datetime import datetime

# timezone
# PERMITE USAR HORAS EN UTC
from datetime import timezone


# Enum
# PERMITE CREAR ENUMERACIONES TIPADAS
# MUY UTIL EN DOMINIOS PARA EVITAR STRINGS MAGICOS
from enum import Enum


# re
# LIBRERIA DE EXPRESIONES REGULARES
# UTILIZADA PARA VALIDACIONES
import re


# ==========================================================
# REGEX CENTRALIZADOS
# ==========================================================
#
# SE DEFINEN AQUÍ LAS EXPRESIONES REGULARES PARA VALIDACIÓN.
#
# CENTRALIZAR REGEX TIENE VARIAS VENTAJAS:
#
# ✔ MEJOR MANTENIMIENTO
# ✔ REUTILIZACIÓN
# ✔ EVITAR DUPLICACIÓN DE CÓDIGO
#
# ESTO ES UNA BUENA PRÁCTICA EN SISTEMAS GRANDES.


# REGEX PARA VALIDAR SUBDOMINIOS
#
# REGLAS:
#
# ✔ SOLO LETRAS MINÚSCULAS
# ✔ NÚMEROS
# ✔ GUIONES
#
# ✔ NO PUEDE EMPEZAR CON GUION
# ✔ NO PUEDE TERMINAR CON GUION
#
# EJEMPLOS VALIDOS:
#
# tienda
# tienda-1
# dulceria-central
#
REGEX_SUBDOMINIO = re.compile(r"^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$")


# REGEX PARA VALIDAR EMAIL
#
# ESTA ES UNA VALIDACIÓN SIMPLE.
#
# EJEMPLOS VALIDOS:
#
# usuario@email.com
# admin@empresa.co
#
REGEX_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


# ==========================================================
# ENUM PLANES DE SUSCRIPCIÓN
# ==========================================================
#
# LOS ENUMS PERMITEN REPRESENTAR VALORES
# LIMITADOS Y CONTROLADOS.
#
# ESTO EVITA ERRORES COMO:
#
# "basico"
# "Basico"
# "BASICO"
#
# Y PERMITE USAR:
#
# PlanSuscripcion.BASICO
#
# LO QUE ES MÁS SEGURO Y PROFESIONAL.


class PlanSuscripcion(Enum):

    # PLAN GRATUITO
    GRATUITO = "gratuito"

    # PLAN BASICO
    BASICO = "basico"

    # PLAN PROFESIONAL
    PROFESIONAL = "profesional"

    # PLAN EMPRESARIAL
    EMPRESARIAL = "empresarial"


# ==========================================================
# ENUM ESTADOS DEL TENANT
# ==========================================================
#
# REPRESENTA EL ESTADO DEL CLIENTE EN EL SISTEMA.
#
# POSIBLES ESTADOS:
#
# ACTIVO
# SUSPENDIDO
# EN PRUEBA
# CANCELADO
#
# ESTO ES COMÚN EN SISTEMAS SAAS.


class EstadoTenant(Enum):

    ACTIVO = "activo"

    SUSPENDIDO = "suspendido"

    EN_PRUEBA = "en_prueba"

    CANCELADO = "cancelado"


# ==========================================================
# LIMITES SEGUN PLAN
# ==========================================================
#
# DEFINE LAS RESTRICCIONES DE CADA PLAN.
#
# EJEMPLO:
#
# PLAN GRATUITO:
# - MAX 5 USUARIOS
# - MAX 100 PRODUCTOS
#
# PLAN BASICO:
# - MAX 10 USUARIOS
# - MAX 500 PRODUCTOS
#
# SE USA UN DICCIONARIO DONDE:
#
# CLAVE = PLAN
# VALOR = (MAX_USUARIOS, MAX_PRODUCTOS)
#
LIMITES_PLAN: Dict[PlanSuscripcion, Tuple[int, int]] = {

    PlanSuscripcion.GRATUITO: (5, 100),

    PlanSuscripcion.BASICO: (10, 500),

    PlanSuscripcion.PROFESIONAL: (25, 2000),

    PlanSuscripcion.EMPRESARIAL: (999999, 999999),
}


# ==========================================================
# ENTIDAD INQUILINO
# ==========================================================
#
# ESTA CLASE REPRESENTA UNA EMPRESA CLIENTE
# DEL SISTEMA SAAS.
#
# CADA INSTANCIA ES UNA EMPRESA DIFERENTE.
#
# RESPONSABILIDADES:
#
# ✔ VALIDAR DATOS
# ✔ GESTIONAR PLANES
# ✔ CONTROLAR LIMITES
# ✔ ADMINISTRAR ESTADO
# ✔ GESTIONAR CONFIGURACIÓN
# ✔ ADMINISTRAR CONTACTO
#
# ESTA CLASE ES EL CORAZÓN DEL DOMINIO.


class Inquilino:

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    #
    # SE EJECUTA AL CREAR EL OBJETO.
    #
    # AQUÍ SE REALIZAN TODAS LAS VALIDACIONES
    # DE DOMINIO.
    #
    def __init__(

        self,

        id: Optional[int],

        nombre: str,

        subdominio: str,

        plan: PlanSuscripcion = PlanSuscripcion.GRATUITO,

        estado: EstadoTenant = EstadoTenant.EN_PRUEBA,

        fecha_creacion: Optional[datetime] = None,

        fecha_vencimiento: Optional[datetime] = None,

        max_usuarios: Optional[int] = None,

        max_productos: Optional[int] = None,

        configuracion: Optional[Dict[str, Any]] = None,

        contacto_nombre: Optional[str] = None,

        contacto_email: Optional[str] = None,

        contacto_telefono: Optional[str] = None

    ) -> None:

        # ==================================================
        # VALIDACION DEL NOMBRE
        # ==================================================

        nombre = nombre.strip()

        if len(nombre) < 3:
            raise ValueError("EL NOMBRE DEBE TENER AL MENOS 3 CARACTERES")

        # ==================================================
        # VALIDACION DEL SUBDOMINIO
        # ==================================================

        subdominio = subdominio.strip().lower()

        if not REGEX_SUBDOMINIO.match(subdominio):
            raise ValueError("SUBDOMINIO INVALIDO")

        # ==================================================
        # VALIDACION DEL EMAIL
        # ==================================================

        if contacto_email and not REGEX_EMAIL.match(contacto_email):
            raise ValueError("EMAIL INVALIDO")

        # ==================================================
        # VALIDACION DE LIMITES
        # ==================================================

        if max_usuarios is not None and max_usuarios < 0:
            raise ValueError("LIMITE USUARIOS INVALIDO")

        if max_productos is not None and max_productos < 0:
            raise ValueError("LIMITE PRODUCTOS INVALIDO")

        # ==================================================
        # ASIGNACION DE ATRIBUTOS
        # ==================================================

        self.id = id

        self.nombre = nombre

        self.subdominio = subdominio

        self.plan = plan

        self.estado = estado

        # SI NO SE ENVIA FECHA DE CREACION
        # SE USA LA FECHA ACTUAL EN UTC
        self.fecha_creacion = fecha_creacion or datetime.now(timezone.utc)

        self.fecha_vencimiento = fecha_vencimiento

        # ==================================================
        # ASIGNACION DE LIMITES SEGUN PLAN
        # ==================================================

        if max_usuarios is None or max_productos is None:

            limites = LIMITES_PLAN[self.plan]

            self.max_usuarios = limites[0]

            self.max_productos = limites[1]

        else:

            self.max_usuarios = max_usuarios

            self.max_productos = max_productos

        # CONFIGURACION DEL TENANT
        self.configuracion = configuracion or {}

        # DATOS DE CONTACTO
        self.contacto_nombre = contacto_nombre

        self.contacto_email = contacto_email

        self.contacto_telefono = contacto_telefono


    # ======================================================
    # CAMBIAR PLAN
    # ======================================================

    def cambiar_plan(self, nuevo_plan: PlanSuscripcion) -> None:

        if self.estado == EstadoTenant.CANCELADO:
            raise ValueError("TENANT CANCELADO")

        self.plan = nuevo_plan

        limites = LIMITES_PLAN[nuevo_plan]

        self.max_usuarios = limites[0]

        self.max_productos = limites[1]

        if nuevo_plan == PlanSuscripcion.GRATUITO:
            self.fecha_vencimiento = None


    # ======================================================
    # CAMBIOS DE ESTADO
    # ======================================================

    def activar(self) -> None:

        if self.estado != EstadoTenant.CANCELADO:
            self.estado = EstadoTenant.ACTIVO

    def suspender(self) -> None:

        if self.estado != EstadoTenant.CANCELADO:
            self.estado = EstadoTenant.SUSPENDIDO

    def cancelar(self) -> None:

        self.estado = EstadoTenant.CANCELADO


    # ======================================================
    # VALIDACIONES DE ESTADO
    # ======================================================

    def esta_activo(self) -> bool:
        return self.estado == EstadoTenant.ACTIVO

    def esta_suspendido(self) -> bool:
        return self.estado == EstadoTenant.SUSPENDIDO

    def esta_en_prueba(self) -> bool:
        return self.estado == EstadoTenant.EN_PRUEBA


    # ======================================================
    # VERIFICAR SI PLAN VENCIDO
    # ======================================================

    def plan_vencido(self) -> bool:

        if not self.fecha_vencimiento:
            return False

        return datetime.now(timezone.utc) > self.fecha_vencimiento


    # ======================================================
    # ACTUALIZAR CONTACTO
    # ======================================================

    def actualizar_contacto(

        self,

        nombre: Optional[str] = None,

        email: Optional[str] = None,

        telefono: Optional[str] = None

    ) -> None:

        if nombre:
            self.contacto_nombre = nombre.strip()

        if email:

            if not REGEX_EMAIL.match(email):
                raise ValueError("EMAIL INVALIDO")

            self.contacto_email = email

        if telefono:
            self.contacto_telefono = telefono.strip()


    # ======================================================
    # ACTUALIZAR CONFIGURACION
    # ======================================================

    def actualizar_configuracion(self, nueva_config: Dict[str, Any]) -> None:

        if not nueva_config:
            return

        self.configuracion.update(nueva_config)


    # ======================================================
    # VALIDAR LIMITES
    # ======================================================

    def puede_agregar_usuario(self, usuarios_actuales: int) -> bool:
        return usuarios_actuales < self.max_usuarios

    def puede_agregar_producto(self, productos_actuales: int) -> bool:
        return productos_actuales < self.max_productos


    # ======================================================
    # REPRESENTACION DEL OBJETO
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"<Inquilino id={self.id} "
            f"nombre={self.nombre} "
            f"subdominio={self.subdominio} "
            f"plan={self.plan.value} "
            f"estado={self.estado.value}>"
        )