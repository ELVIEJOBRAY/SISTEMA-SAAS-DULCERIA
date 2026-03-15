import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nucleo.interfaz.api.v1.catalogo.rutas.rutas_categorias import enrutador_categorias
from nucleo.interfaz.api.v1.catalogo.rutas.rutas_marcas import enrutador_marcas
from nucleo.interfaz.api.v1.catalogo.rutas.rutas_presentaciones import enrutador_presentaciones
from nucleo.interfaz.api.v1.catalogo.rutas.rutas_productos import enrutador_productos
from nucleo.interfaz.api.v1.identidad_acceso.rutas.rutas_autenticacion import enrutador_autenticacion
from nucleo.interfaz.api.v1.identidad_acceso.rutas.rutas_membresias import enrutador_membresias
from nucleo.interfaz.api.v1.identidad_acceso.rutas.rutas_permisos import enrutador_permisos
from nucleo.interfaz.api.v1.identidad_acceso.rutas.rutas_roles import enrutador_roles
from nucleo.interfaz.api.v1.identidad_acceso.rutas.rutas_usuarios import enrutador_usuarios
from nucleo.interfaz.api.v1.inventario.rutas.rutas_ajustes_inventario import enrutador_ajustes_inventario
from nucleo.interfaz.api.v1.inventario.rutas.rutas_consultas_inventario import enrutador_consultas_inventario
from nucleo.interfaz.api.v1.inventario.rutas.rutas_entradas_inventario import enrutador_entradas_inventario
from nucleo.interfaz.api.v1.inventario.rutas.rutas_kardex_inventario import enrutador_kardex
from nucleo.interfaz.api.v1.inventario.rutas.rutas_movimientos_inventario import enrutador as enrutador_movimientos_inventario
from nucleo.interfaz.api.v1.inventario.rutas.rutas_salidas_inventario import enrutador_salidas_inventario
from nucleo.interfaz.api.v1.organizacion.rutas.rutas_bodegas import enrutador_bodegas
from nucleo.interfaz.api.v1.organizacion.rutas.rutas_empresas import enrutador_empresas
from nucleo.interfaz.api.v1.organizacion.rutas.rutas_sucursales import enrutador_sucursales
from nucleo.interfaz.api.v1.organizacion.rutas.rutas_tenants import enrutador_tenants
from nucleo.interfaz.api.v1.ventas.rutas.rutas_ventas import enrutador_ventas


# AUDITORIA: LA CONFIGURACION DE CORS NO DEBE QUEDAR ABIERTA CON ALLOW_ORIGINS=["*"] CUANDO SE USAN CREDENCIALES.
# AUDITORIA: EN FASTAPI/STARLETTE ESA COMBINACION ES INSEGURA Y PUEDE GENERAR COMPORTAMIENTOS INCORRECTOS EN PRODUCCION.
# AUDITORIA: SE CORRIGE PARA LEER ORIGENES PERMITIDOS DESDE VARIABLE DE ENTORNO Y USAR UNA LISTA EXPLICITA.
def obtener_origenes_permitidos() -> list[str]:
    origenes = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
    return [origen.strip() for origen in origenes.split(",") if origen.strip()]


# AUDITORIA: SE DEFINE UNA SOLA INSTANCIA PRINCIPAL DE FASTAPI COMO PUNTO DE ENTRADA OFICIAL DEL SISTEMA.
app = FastAPI(
    title="Sistema SaaS Dulceria API",
    version="1.0.0",
    description="API principal del ERP SaaS multiempresa para dulcerias",
)

# AUDITORIA: SE ENDURECE CORS USANDO ORIGENES CONTROLADOS POR CONFIGURACION.
# AUDITORIA: ALLOW_METHODS Y ALLOW_HEADERS ABIERTOS PUEDEN MANTENERSE EN DESARROLLO, PERO EN PRODUCCION CONVIENE RESTRINGIRLOS SEGUN NECESIDAD REAL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=obtener_origenes_permitidos(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin"],
)

# AUDITORIA: EL ENDPOINT DE HEALTH ES CORRECTO COMO SONDA BASICA DE VIDA DEL SERVICIO.
# AUDITORIA: NO DEBE EXPONER INFORMACION INTERNA COMO VERSIONES DE LIBRERIAS, VARIABLES DE ENTORNO O ESTADO DE DEPENDENCIAS SENSIBLES.
@app.get("/health", tags=["Health"])
async def health():
    return {"estado": "ok"}

# AUDITORIA: LAS RUTAS DE AUTENTICACION Y ACCESO SE REGISTRAN EN LA APP PRINCIPAL.
# AUDITORIA: LA SEGURIDAD REAL NO SE GARANTIZA DESDE INCLUDE_ROUTER, SINO DESDE LAS DEPENDENCIAS Y VALIDACIONES DEFINIDAS DENTRO DE CADA RUTA.
app.include_router(enrutador_autenticacion)
app.include_router(enrutador_membresias)
app.include_router(enrutador_permisos)
app.include_router(enrutador_roles)
app.include_router(enrutador_usuarios)

# AUDITORIA: LAS RUTAS DE ORGANIZACION DEBEN VALIDAR SIEMPRE CONTEXTO TENANT, EMPRESA Y PERMISOS DEL USUARIO AUTENTICADO.
# AUDITORIA: SI ESTAS RUTAS PERMITEN OPERACIONES SIN AUTENTICACION, EL PROBLEMA ESTA EN LOS MODULOS DE RUTA Y NO EN ESTE REGISTRO CENTRAL.
app.include_router(enrutador_empresas)
app.include_router(enrutador_sucursales)
app.include_router(enrutador_bodegas)
app.include_router(enrutador_tenants)

# AUDITORIA: LAS RUTAS DE CATALOGO DEBEN EVITAR CONFIAR EN TENANT_ID O USUARIO_ID ENVIADOS DESDE EL CLIENTE.
# AUDITORIA: EL CONTEXTO DE SEGURIDAD DEBE DERIVARSE DEL TOKEN Y NO DEL PAYLOAD.
app.include_router(enrutador_categorias)
app.include_router(enrutador_marcas)
app.include_router(enrutador_productos)
app.include_router(enrutador_presentaciones)

# AUDITORIA: EL MODULO DE INVENTARIO ES SENSIBLE Y DEBE TENER CONTROL FUERTE DE AUTENTICACION, TENANT Y JERARQUIA ORGANIZACIONAL.
# AUDITORIA: LA COEXISTENCIA DE RUTAS DE INVENTARIO NUEVAS Y LEGACY PUEDE GENERAR INCONSISTENCIAS SI NO SE UNIFICA EL MODELO DE VALIDACION.
app.include_router(enrutador_entradas_inventario)
app.include_router(enrutador_salidas_inventario)
app.include_router(enrutador_ajustes_inventario)
app.include_router(enrutador_consultas_inventario)
app.include_router(enrutador_kardex)
app.include_router(enrutador_movimientos_inventario)

# AUDITORIA: LAS RUTAS DE VENTAS DEBEN GARANTIZAR AISLAMIENTO MULTI-TENANT Y NO CONSULTAR SOLO POR IDs GLOBALES.
app.include_router(enrutador_ventas)
