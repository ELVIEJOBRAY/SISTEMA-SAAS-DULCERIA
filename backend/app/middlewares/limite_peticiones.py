from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
import redis.asyncio as redis
from typing import Dict
import hashlib

class MiddlewareLimitePeticiones(BaseHTTPMiddleware):
    \"\"\"
    MIDDLEWARE DE LÍMITE DE PETICIONES USANDO REDIS
    
    LIMITA EL NÚMERO DE PETICIONES POR IP
    PARA PREVENIR ABUSOS Y ATAQUES DOS.
    \"\"\"
    
    def __init__(self, app, cliente_redis=None, max_peticiones=100, ventana_segundos=60):
        super().__init__(app)
        self.cliente_redis = cliente_redis
        self.max_peticiones = max_peticiones
        self.ventana_segundos = ventana_segundos
        self.cache_local: Dict[str, list] = {}  # Fallback si Redis no está
    
    async def _obtener_ip_cliente(self, request: Request) -> str:
        \"\"\"OBTIENE LA IP REAL DEL CLIENTE\"\"\"
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "desconocido"
    
    async def _verificar_limite_redis(self, clave: str) -> bool:
        \"\"\"VERIFICA LÍMITE USANDO REDIS\"\"\"
        if not self.cliente_redis:
            return False
        
        try:
            # INCREMENTAR CONTADOR ATOMICO
            actual = await self.cliente_redis.incr(clave)
            if actual == 1:
                # PRIMERA PETICIÓN - EXPIRAR DESPUÉS DE LA VENTANA
                await self.cliente_redis.expire(clave, self.ventana_segundos)
            
            return actual <= self.max_peticiones
        except:
            return False
    
    def _verificar_limite_local(self, clave: str) -> bool:
        \"\"\"FALLBACK LOCAL CUANDO REDIS NO ESTÁ DISPONIBLE\"\"\"
        ahora = time.time()
        
        # LIMPIAR CACHE ANTIGUA
        if clave in self.cache_local:
            self.cache_local[clave] = [
                ts for ts in self.cache_local[clave]
                if ahora - ts < self.ventana_segundos
            ]
        else:
            self.cache_local[clave] = []
        
        # VERIFICAR LÍMITE
        if len(self.cache_local[clave]) >= self.max_peticiones:
            return False
        
        # REGISTRAR PETICIÓN
        self.cache_local[clave].append(ahora)
        return True
    
    async def dispatch(self, request: Request, call_next):
        \"\"\"PROCESA CADA PETICIÓN\"\"\"
        
        # 1. OBTENER IDENTIFICADOR (IP + RUTA)
        ip_cliente = await self._obtener_ip_cliente(request)
        ruta = request.url.path
        clave = f"limite:{ip_cliente}:{ruta}"
        
        # 2. VERIFICAR LÍMITE
        if self.cliente_redis:
            permitido = await self._verificar_limite_redis(clave)
        else:
            permitido = self._verificar_limite_local(clave)
        
        if not permitido:
            raise HTTPException(
                status_code=429,
                detail="Demasiadas peticiones. Intenta nuevamente en 60 segundos."
            )
        
        # 3. CONTINUAR CON LA PETICIÓN
        respuesta = await call_next(request)
        return respuesta

# MIDDLEWARE DE INQUILINO
class MiddlewareInquilino(BaseHTTPMiddleware):
    \"\"\"
    MIDDLEWARE PARA IDENTIFICAR EL INQUILINO ACTUAL
    Y AGREGARLO AL REQUEST STATE
    \"\"\"
    
    async def dispatch(self, request: Request, call_next):
        # IDENTIFICAR INQUILINO DESDE SUBDOMINIO O HEADER
        inquilino_id = request.headers.get("X-Inquilino-ID")
        host = request.headers.get("host", "")
        
        # ALMACENAR EN REQUEST STATE
        request.state.inquilino_id = inquilino_id
        request.state.inquilino_subdominio = host.split('.')[0] if '.' in host else None
        
        respuesta = await call_next(request)
        return respuesta
