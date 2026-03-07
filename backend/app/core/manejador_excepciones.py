from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.excepciones import (
    ErrorDeDominio, ErrorStockInsuficiente, ErrorEntidadNoEncontrada,
    ErrorValidacionDominio, ErrorReglaDeNegocio, ErrorInquilinoNoEncontrado,
    ErrorAccesoNoAutorizado
)
import logging

logger = logging.getLogger(__name__)

# ==========================================================
# MANEJADORES DE EXCEPCIONES PARA FASTAPI
# ==========================================================
# CONVIERTEN EXCEPCIONES DE DOMINIO EN RESPUESTAS HTTP
# APROPIADAS CON CÓDIGOS DE ESTADO Y MENSAJES CLAROS.
# ==========================================================

async def manejar_error_dominio(request: Request, exc: ErrorDeDominio):
    \"\"\"MANEJA ERRORES GENERICOS DE DOMINIO (400 BAD REQUEST)\"\"\"
    logger.warning(f"Error de dominio: {exc.mensaje} - Código: {exc.codigo}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.codigo,
            "mensaje": exc.mensaje,
            "detalles": getattr(exc, "__dict__", {})
        }
    )

async def manejar_stock_insuficiente(request: Request, exc: ErrorStockInsuficiente):
    \"\"\"MANEJA ERRORES DE STOCK (400 BAD REQUEST)\"\"\"
    logger.warning(f"Stock insuficiente: Producto {exc.producto_id}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "STOCK_INSUFICIENTE",
            "mensaje": exc.mensaje,
            "producto_id": exc.producto_id,
            "solicitado": exc.solicitado,
            "disponible": exc.disponible
        }
    )

async def manejar_entidad_no_encontrada(request: Request, exc: ErrorEntidadNoEncontrada):
    \"\"\"MANEJA ERRORES DE ENTIDAD NO ENCONTRADA (404 NOT FOUND)\"\"\"
    logger.info(f"Entidad no encontrada: {exc.entidad} ID {exc.id}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "NO_ENCONTRADO",
            "mensaje": exc.mensaje,
            "entidad": exc.entidad,
            "id": exc.id
        }
    )

async def manejar_validacion_dominio(request: Request, exc: ErrorValidacionDominio):
    \"\"\"MANEJA ERRORES DE VALIDACIÓN (422 UNPROCESSABLE ENTITY)\"\"\"
    logger.warning(f"Error de validación: {exc.mensaje}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDACION_FALLIDA",
            "mensaje": exc.mensaje
        }
    )

async def manejar_regla_negocio(request: Request, exc: ErrorReglaDeNegocio):
    \"\"\"MANEJA VIOLACIONES DE REGLAS DE NEGOCIO (400 BAD REQUEST)\"\"\"
    logger.warning(f"Regla de negocio violada: {exc.mensaje}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.codigo or "REGLA_NEGOCIO",
            "mensaje": exc.mensaje
        }
    )

async def manejar_inquilino_no_encontrado(request: Request, exc: ErrorInquilinoNoEncontrado):
    \"\"\"MANEJA INQUILINO NO ENCONTRADO (404 NOT FOUND)\"\"\"
    logger.info(f"Inquilino no encontrado: {exc.identificador}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "INQUILINO_NO_ENCONTRADO",
            "mensaje": exc.mensaje,
            "identificador": exc.identificador
        }
    )

async def manejar_no_autorizado(request: Request, exc: ErrorAccesoNoAutorizado):
    \"\"\"MANEJA ACCESO NO AUTORIZADO (403 FORBIDDEN)\"\"\"
    logger.warning(f"Acceso no autorizado: {exc.mensaje}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "NO_AUTORIZADO",
            "mensaje": exc.mensaje
        }
    )

# ==========================================================
# CONFIGURACIÓN DE MANEJADORES EN FASTAPI
# ==========================================================
def configurar_manejadores_excepciones(app):
    \"\"\"REGISTRA TODOS LOS MANEJADORES DE EXCEPCIONES EN LA APP\"\"\"
    app.add_exception_handler(ErrorStockInsuficiente, manejar_stock_insuficiente)
    app.add_exception_handler(ErrorEntidadNoEncontrada, manejar_entidad_no_encontrada)
    app.add_exception_handler(ErrorValidacionDominio, manejar_validacion_dominio)
    app.add_exception_handler(ErrorReglaDeNegocio, manejar_regla_negocio)
    app.add_exception_handler(ErrorInquilinoNoEncontrado, manejar_inquilino_no_encontrado)
    app.add_exception_handler(ErrorAccesoNoAutorizado, manejar_no_autorizado)
    app.add_exception_handler(ErrorDeDominio, manejar_error_dominio)  # Último recurso
