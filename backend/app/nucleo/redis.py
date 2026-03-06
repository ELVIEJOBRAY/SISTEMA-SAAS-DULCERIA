# ==========================================================
# CONFIGURACIÓN DE REDIS - SISTEMA DE CACHÉ
# ==========================================================

# REDIS ES UNA BASE DE DATOS EN MEMORIA EXTREMADAMENTE RÁPIDA
# QUE FUNCIONA PRINCIPALMENTE COMO:
#
# - SISTEMA DE CACHÉ
# - ALMACENAMIENTO TEMPORAL
# - SISTEMA DE MENSAJERÍA
# - COLA DE TRABAJOS
#
# EN ARQUITECTURAS MODERNAS DE MICROSERVICIOS Y BACKENDS
# ESCALABLES, REDIS SE UTILIZA PARA REDUCIR LA CARGA
# SOBRE LA BASE DE DATOS PRINCIPAL.
#
# EJEMPLOS DE USO:
#
# - CACHEAR RESULTADOS DE CONSULTAS COSTOSAS
# - ALMACENAR TOKENS DE SESIÓN
# - CONTROLAR RATE LIMITING
# - IMPLEMENTAR COLAS DE BACKGROUND JOBS
#
# REDIS FUNCIONA COMPLETAMENTE EN MEMORIA RAM,
# POR LO QUE ES EXTREMADAMENTE RÁPIDO.

# ----------------------------------------------------------
# IMPORTACIÓN DEL CLIENTE ASÍNCRONO DE REDIS
# ----------------------------------------------------------

# SE UTILIZA LA VERSIÓN ASÍNCRONA DEL CLIENTE REDIS
# PARA TRABAJAR CORRECTAMENTE CON FASTAPI Y ASYNCIO.
#
# ESTO PERMITE QUE LAS OPERACIONES DE REDIS
# NO BLOQUEEN EL EVENT LOOP DE LA APLICACIÓN.
import redis.asyncio as redis

# OPTIONAL PERMITE INDICAR QUE UNA VARIABLE
# PUEDE SER DE UN TIPO ESPECÍFICO O NONE.
from typing import Optional

# IMPORTAMOS LA CONFIGURACIÓN CENTRAL DEL PROYECTO
# DONDE SE ENCUENTRAN VARIABLES COMO:
#
# REDIS_URL
# DATABASE_URL
# DEBUG
#
# ESTA CONFIGURACIÓN PROVIENE DEL ARCHIVO .ENV
# CARGADO MEDIANTE PYTHON-DOTENV.
from app.nucleo.config import configuracion


# ==========================================================
# CLASE CLIENTE REDIS
# ==========================================================

# ESTA CLASE ENCAPSULA TODA LA LÓGICA
# DE CONEXIÓN Y OPERACIÓN CON REDIS.
#
# UTILIZA EL PATRÓN SINGLETON PARA GARANTIZAR
# QUE TODA LA APLICACIÓN UTILICE LA MISMA
# CONEXIÓN AL SERVIDOR REDIS.
#
# BENEFICIOS:
#
# - MENOR CONSUMO DE RECURSOS
# - CONEXIONES REUTILIZADAS
# - MAYOR RENDIMIENTO
#
# ESTE PATRÓN ES MUY UTILIZADO EN
# ARQUITECTURAS PROFESIONALES DE BACKEND.

class ClienteRedis:

    # ------------------------------------------------------
    # CONSTRUCTOR DE LA CLASE
    # ------------------------------------------------------
    # INICIALIZA LA VARIABLE CLIENTE COMO NONE.
    #
    # POSTERIORMENTE SE ASIGNARÁ LA CONEXIÓN REAL
    # CUANDO SE EJECUTE EL MÉTODO "conectar".
    def __init__(self):
        self.cliente: Optional[redis.Redis] = None
    

    # ======================================================
    # CONEXIÓN AL SERVIDOR REDIS
    # ======================================================

    # ESTE MÉTODO CREA LA CONEXIÓN HACIA
    # EL SERVIDOR REDIS UTILIZANDO LA URL
    # DEFINIDA EN EL ARCHIVO .ENV.
    async def conectar(self):

        \"\"\"Establece conexión con el servidor Redis\"\"\"

        self.cliente = await redis.from_url(
            configuracion.REDIS_URL,

            # DEFINE LA CODIFICACIÓN UTILIZADA
            # PARA LOS DATOS DEVUELTOS POR REDIS.
            encoding="utf-8",

            # CONVIERTE AUTOMÁTICAMENTE LOS BYTES
            # DEVUELTOS POR REDIS EN STRINGS.
            decode_responses=True
        )

        print("✅ Conectado a Redis")


    # ======================================================
    # DESCONEXIÓN DEL SERVIDOR REDIS
    # ======================================================

    # ESTE MÉTODO CIERRA LA CONEXIÓN
    # CUANDO LA APLICACIÓN SE DETIENE.
    #
    # ESTO EVITA:
    #
    # - CONEXIONES COLGADAS
    # - FUGAS DE RECURSOS
    # - PROBLEMAS EN REINICIOS DEL SERVIDOR
    async def desconectar(self):

        \"\"\"Cierra la conexión con Redis\"\"\"

        if self.cliente:
            await self.cliente.close()
            print("✅ Desconectado de Redis")
    

    # ======================================================
    # OPERACIONES BÁSICAS DE CACHÉ
    # ======================================================

    # ------------------------------------------------------
    # OBTENER VALOR DEL CACHÉ
    # ------------------------------------------------------
    # RECUPERA UN VALOR ALMACENADO
    # UTILIZANDO SU CLAVE.
    async def obtener(self, clave: str):

        \"\"\"Obtiene un valor del caché por su clave\"\"\"

        return await self.cliente.get(clave)


    # ------------------------------------------------------
    # GUARDAR VALOR EN CACHÉ
    # ------------------------------------------------------
    # ALMACENA UN VALOR EN REDIS
    # CON UN TIEMPO DE EXPIRACIÓN.
    #
    # LA EXPIRACIÓN ES IMPORTANTE
    # PARA EVITAR QUE EL CACHÉ
    # CREZCA INDEFINIDAMENTE.
    async def guardar(self, clave: str, valor: str, expiracion: int = 3600):

        \"\"\"
        Guarda un valor en caché con tiempo de expiración
        
        Args:
            clave: Identificador único
            valor: Datos a almacenar
            expiracion: Tiempo en segundos (default: 1 hora)
        \"\"\"

        await self.cliente.set(clave, valor, ex=expiracion)


    # ------------------------------------------------------
    # ELIMINAR CLAVE DEL CACHÉ
    # ------------------------------------------------------
    # BORRA UN REGISTRO ESPECÍFICO
    # DEL SISTEMA DE CACHÉ.
    async def eliminar(self, clave: str):

        \"\"\"Elimina una clave del caché\"\"\"

        await self.cliente.delete(clave)


    # ------------------------------------------------------
    # VERIFICAR EXISTENCIA DE CLAVE
    # ------------------------------------------------------
    # PERMITE SABER SI UNA CLAVE
    # EXISTE EN REDIS.
    #
    # REDIS DEVUELVE UN NÚMERO:
    # 0 = NO EXISTE
    # 1 = EXISTE
    #
    # POR ESO SE COMPARA CON > 0
    # PARA DEVOLVER TRUE O FALSE.
    async def existe(self, clave: str) -> bool:

        \"\"\"Verifica si una clave existe en caché\"\"\"

        return await self.cliente.exists(clave) > 0


# ==========================================================
# INSTANCIA GLOBAL DEL CLIENTE REDIS
# ==========================================================

# SE CREA UNA INSTANCIA GLOBAL
# PARA QUE TODA LA APLICACIÓN
# UTILICE EL MISMO CLIENTE REDIS.
#
# ESTO EVITA CREAR CONEXIONES
# NUEVAS EN CADA PETICIÓN.
cliente_redis = ClienteRedis()


# ==========================================================
# DEPENDENCIA PARA ENDPOINTS FASTAPI
# ==========================================================

# ESTA FUNCIÓN PERMITE QUE FASTAPI
# INYECTE AUTOMÁTICAMENTE EL CLIENTE REDIS
# EN LOS ENDPOINTS UTILIZANDO DEPENDENCY INJECTION.
#
# EJEMPLO DE USO EN UN ENDPOINT:
#
# @app.get("/datos")
# async def obtener_datos(redis: ClienteRedis = Depends(obtener_redis)):
#     valor = await redis.obtener("mi_clave")
#     return {"dato": valor}

async def obtener_redis():

    \"\"\"
    Dependencia de FastAPI para inyectar el cliente Redis
    \"\"\"

    return cliente_redis
