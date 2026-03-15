from uuid import UUID

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from nucleo.infraestructura.db.conexion import obtener_db
from nucleo.infraestructura.db.repositorios.identidad_acceso import (
    RepositorioUsuarioSQLAlchemy,
)
from nucleo.infraestructura.seguridad.autenticacion.gestor_jwt import GestorJWT

esquema_bearer = HTTPBearer(auto_error=False)


def obtener_claims_token(
    credenciales: HTTPAuthorizationCredentials = Security(esquema_bearer),
) -> dict:
    if not credenciales:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

    try:
        return GestorJWT().decodificar_token(credenciales.credentials)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error


def obtener_usuario_actual(
    claims: dict = Depends(obtener_claims_token),
    db: Session = Depends(obtener_db),
):
    usuario_id = claims.get("sub")
    tenant_id = claims.get("tenant_id")

    if not usuario_id or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    repo = RepositorioUsuarioSQLAlchemy(db)
    usuario = repo.obtener_por_id(UUID(usuario_id))

    if not usuario or not usuario.esta_activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inválido o inactivo",
        )

    if str(usuario.tenant_id) != str(tenant_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contexto de tenant inválido",
        )

    return usuario
