# ==========================================================
# SGDD API - PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN
# ==========================================================
# ESTE ARCHIVO ES EL CORAZÓN DEL BACKEND.
# AQUÍ SE CREA LA INSTANCIA PRINCIPAL DE FASTAPI QUE
# LEVANTA EL SERVIDOR Y REGISTRA TODAS LAS RUTAS DEL SISTEMA.
#
# EN ARQUITECTURAS PROFESIONALES (SAAS / MICROSERVICIOS)
# ESTE ARCHIVO ACTÚA COMO:
#
# - PUNTO DE ARRANQUE DEL SERVIDOR
# - REGISTRO DE MIDDLEWARES
# - REGISTRO DE RUTAS
# - CONFIGURACIÓN GLOBAL DEL API
# - EVENTOS DE INICIO Y CIERRE
#
# NORMALMENTE ESTE ARCHIVO ES EJECUTADO POR UVICORN:
#
# uvicorn app.main:app --reload
#
# ==========================================================

from fastapi import FastAPI

# ==========================================================
# CREACIÓN DE LA INSTANCIA PRINCIPAL DE FASTAPI
# ==========================================================
# AQUÍ SE DEFINE LA CONFIGURACIÓN GENERAL DEL API.
#
# title
# Nombre oficial de la API que aparecerá en la documentación.
#
# description
# Descripción general del sistema.
#
# version
# Versión del backend (importante para versionado de APIs).
#
# FastAPI automáticamente genera documentación interactiva en:
#
# http://localhost:8000/docs
# http://localhost:8000/redoc
#
app = FastAPI(
    title="SGDD API",
    description="Sistema de Gestión de Dulcerías SaaS",
    version="0.1.0"
)

# ==========================================================
# ENDPOINT RAÍZ
# ==========================================================
# ESTE ENDPOINT SE UTILIZA PARA:
#
# - VERIFICAR QUE LA API ESTÁ FUNCIONANDO
# - MOSTRAR UN MENSAJE DE BIENVENIDA
# - PRUEBAS RÁPIDAS DESDE EL NAVEGADOR
#
# Ejemplo:
# http://localhost:8000/
#
# Respuesta esperada:
# {
#   "message": "🚀 SGDD API funcionando correctamente"
# }
#
@app.get("/")
def root():
    return {"message": "🚀 SGDD API funcionando correctamente"}


# ==========================================================
# ENDPOINT DE SALUD DEL SISTEMA (HEALTH CHECK)
# ==========================================================
# ESTE ENDPOINT ES EXTREMADAMENTE IMPORTANTE EN
# ARQUITECTURAS MODERNAS.
#
# ES UTILIZADO POR:
#
# - DOCKER
# - KUBERNETES
# - LOAD BALANCERS
# - SISTEMAS DE MONITOREO
# - SERVICIOS CLOUD
#
# PARA VERIFICAR QUE LA API SIGUE FUNCIONANDO.
#
# Ejemplo:
# http://localhost:8000/health
#
# Respuesta esperada:
# {
#   "status": "ok",
#   "message": "Sistema operativo"
# }
#
@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Sistema operativo"
    }
