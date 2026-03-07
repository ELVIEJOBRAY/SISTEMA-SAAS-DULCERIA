from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.nucleo.config import configuracion
from app.nucleo.base_datos import motor, Base
from app.nucleo.redis import cliente_redis
from app.middlewares.limite_peticiones import MiddlewareLimitePeticiones, MiddlewareInquilino
from app.core.manejador_excepciones import configurar_manejadores_excepciones

# IMPORTAR TODOS LOS ROUTERS
from app.api.v1 import auth
from app.api.v1 import usuarios
from app.api.v1 import productos
from app.api.v1 import clientes
from app.api.v1 import ventas
from app.api.v1 import pagos
from app.api.v1 import proveedores
from app.api.v1 import categorias
from app.api.v1 import inquilinos
from app.api.v1 import reportes

app = FastAPI(
    title=configuracion.PROJECT_NAME,
    description="Sistema de Gestión de Dulcerías SaaS",
    version=configuracion.VERSION,
    debug=configuracion.DEBUG
)

# ==========================================================
# CONFIGURACIÓN DE MIDDLEWARES
# ==========================================================

# CORS PARA FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MIDDLEWARE DE INQUILINO
app.add_middleware(MiddlewareInquilino)

# MIDDLEWARE DE LÍMITE DE PETICIONES
app.add_middleware(
    MiddlewareLimitePeticiones,
    cliente_redis=cliente_redis.cliente if cliente_redis.cliente else None,
    max_peticiones=100,
    ventana_segundos=60
)

# ==========================================================
# CONFIGURACIÓN DE MANEJADORES DE EXCEPCIONES
# ==========================================================
configurar_manejadores_excepciones(app)

# ==========================================================
# INCLUSIÓN DE TODOS LOS ROUTERS
# ==========================================================
app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(productos.router, prefix="/api/v1")
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(ventas.router, prefix="/api/v1")
app.include_router(pagos.router, prefix="/api/v1")
app.include_router(proveedores.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(inquilinos.router, prefix="/api/v1")
app.include_router(reportes.router, prefix="/api/v1")

# ==========================================================
# EVENTOS DE INICIO Y APAGADO
# ==========================================================
@app.on_event("startup")
async def iniciar():
    \"\"\"INICIALIZA CONEXIONES AL INICIAR LA APLICACIÓN\"\"\"
    print("🚀 Iniciando SGDD API...")
    
    # CONECTAR A REDIS
    await cliente_redis.conectar()
    
    # CREAR TABLAS EN BASE DE DATOS (SOLO PARA DESARROLLO)
    if configuracion.ENVIRONMENT == "development":
        Base.metadata.create_all(bind=motor)
        print("✅ Tablas de base de datos verificadas")
    
    print(f"✅ API corriendo en entorno: {configuracion.ENVIRONMENT}")

@app.on_event("shutdown")
async def apagar():
    \"\"\"CIERRA CONEXIONES AL APAGAR LA APLICACIÓN\"\"\"
    print("🛑 Apagando SGDD API...")
    
    # DESCONECTAR REDIS
    await cliente_redis.desconectar()
    
    print("✅ Conexiones cerradas correctamente")

# ==========================================================
# ENDPOINTS DE PRUEBA
# ==========================================================
@app.get("/")
def raiz():
    return {
        "message": "🚀 SGDD API funcionando correctamente",
        "entorno": configuracion.ENVIRONMENT,
        "version": configuracion.VERSION
    }

@app.get("/health")
async def salud():
    \"\"\"VERIFICA EL ESTADO DE SALUD DEL SISTEMA\"\"\"
    redis_ok = False
    try:
        await cliente_redis.cliente.ping()
        redis_ok = True
    except:
        pass
    
    return {
        "status": "ok",
        "message": "Sistema operativo",
        "entorno": configuracion.ENVIRONMENT,
        "servicios": {
            "api": "saludable",
            "redis": "conectado" if redis_ok else "desconectado",
            "base_datos": "listo"
        }
    }
