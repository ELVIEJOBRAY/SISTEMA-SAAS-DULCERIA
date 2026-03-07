from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import jwt
from datetime import datetime, timezone

from app.nucleo.base_datos import obtener_bd
from app.dominio.entidades.usuario import Usuario
from app.dominio.entidades.inquilino import Inquilino
from app.infraestructura.repositorios.usuario_repositorio import RepositorioUsuario
from app.infraestructura.repositorios.inquilino_repositorio import RepositorioInquilino
from app.nucleo.config import configuracion

seguridad = HTTPBearer()

# ==========================================================
# DEPENDENCIA: OBTENER USUARIO ACTUAL DESDE TOKEN JWT
# ==========================================================
async def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad),
    db: Session = Depends(obtener_bd)
) -> Usuario:
    \"\"\"
    EXTRAE Y VALIDA EL TOKEN JWT PARA OBTENER EL USUARIO ACTUAL
    
    - Decodifica el token
    - Verifica expiración
    - Obtiene usuario de la BD
    - Lanza 401 si no es válido
    \"\"\"
    token = credenciales.credentials
    
    try:
        # DECODIFICAR TOKEN
        payload = jwt.decode(
            token,
            configuracion.JWT_SECRET,
            algorithms=[configuracion.JWT_ALGORITHM]
        )
        usuario_id = payload.get("sub")
        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # OBTENER USUARIO DE BD
        repo = RepositorioUsuario(db)
        usuario = repo.obtener_por_id(int(usuario_id))
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )
        
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo"
            )
        
        return usuario
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# ==========================================================
# DEPENDENCIA: OBTENER USUARIO OPCIONAL (PARA ENDPOINTS PÚBLICOS)
# ==========================================================
async def obtener_usuario_opcional(
    credenciales: Optional[HTTPAuthorizationCredentials] = Depends(seguridad),
    db: Session = Depends(obtener_bd)
) -> Optional[Usuario]:
    \"\"\"
    VERSIÓN OPCIONAL - NO LANZA ERROR SI NO HAY TOKEN
    
    Útil para endpoints que tienen comportamiento diferente
    para usuarios autenticados vs anónimos.
    \"\"\"
    if not credenciales:
        return None
    
    try:
        return await obtener_usuario_actual(credenciales, db)
    except HTTPException:
        return None

# ==========================================================
# DEPENDENCIA: OBTENER INQUILINO ACTUAL
# ==========================================================
async def obtener_inquilino_actual(
    request: Request,
    db: Session = Depends(obtener_bd)
) -> Optional[Inquilino]:
    \"\"\"
    IDENTIFICA EL INQUILINO ACTUAL DESDE EL SUBDOMINIO O HEADER
    
    Estrategias:
    1. Header X-Inquilino-ID
    2. Subdominio (inquilino.sgdd.com)
    3. Default tenant para desarrollo
    \"\"\"
    # 1. PROBAR HEADER
    inquilino_id = request.headers.get("X-Inquilino-ID")
    if inquilino_id:
        try:
            repo = RepositorioInquilino(db)
            inquilino = repo.obtener_por_id(int(inquilino_id))
            if inquilino:
                return inquilino
        except:
            pass
    
    # 2. PROBAR SUBDOMINIO
    host = request.headers.get("host", "")
    if '.' in host:
        subdominio = host.split('.')[0]
        repo = RepositorioInquilino(db)
        inquilino = repo.buscar_por_subdominio(subdominio)
        if inquilino:
            return inquilino
    
    # 3. INQUILINO POR DEFECTO (DESARROLLO)
    if configuracion.ENVIRONMENT == "development":
        repo = RepositorioInquilino(db)
        inquilinos = repo.obtener_todos()
        if inquilinos:
            return inquilinos[0]
    
    return None

# ==========================================================
# DEPENDENCIA: VERIFICAR QUE EL USUARIO SEA ADMIN
# ==========================================================
def requerir_admin(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    \"\"\"
    VERIFICA QUE EL USUARIO ACTUAL SEA ADMINISTRADOR
    \"\"\"
    if not usuario_actual.es_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return usuario_actual

# ==========================================================
# DEPENDENCIA: VERIFICAR PERMISOS POR ROL
# ==========================================================
def requerir_roles(roles: list):
    \"\"\"
    FACTORÍA DE DEPENDENCIAS PARA VERIFICAR ROLES
    
    Uso:
    @router.get("/solo-admin")
    def ruta(user: Usuario = Depends(requerir_roles(["admin"]))):
        ...
    \"\"\"
    def verificador_rol(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
        if usuario_actual.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de estos roles: {roles}"
            )
        return usuario_actual
    return verificador_rol
