from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from app.nucleo.base_datos import obtener_bd
from app.aplicacion.dto.usuario_dto import UsuarioCreateDTO, UsuarioResponseDTO
from app.aplicacion.servicios.auth_servicio import AuthServicio
from app.infraestructura.repositorios.usuario_repositorio import RepositorioUsuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioResponseDTO)
async def registro(
    datos: UsuarioCreateDTO,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    REGISTRA UN NUEVO USUARIO EN EL SISTEMA
    
    - Validación de email único
    - Hash de contraseña
    - Asignación de rol por defecto
    \"\"\"
    repo = RepositorioUsuario(db)
    auth = AuthServicio(repo)
    
    try:
        usuario = auth.registrar(
            nombre=datos.nombre,
            email=datos.email,
            password=datos.password,
            rol=datos.rol
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    email: str,
    password: str,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    INICIA SESIÓN Y DEVUELVE TOKEN JWT
    
    - Verifica credenciales
    - Genera token con expiración
    - Retorna token y datos del usuario
    \"\"\"
    repo = RepositorioUsuario(db)
    auth = AuthServicio(repo)
    
    resultado = auth.login(email, password)
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return resultado

@router.post("/refrescar")
async def refrescar_token(
    token: str,
    db: Session = Depends(obtener_bd)
):
    \"\"\"
    REFRESCA UN TOKEN JWT EXPIRADO
    
    - Valida token anterior
    - Genera nuevo token
    \"\"\"
    repo = RepositorioUsuario(db)
    auth = AuthServicio(repo)
    
    nuevo_token = auth.refresh_token(token)
    if not nuevo_token:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"access_token": nuevo_token, "token_type": "bearer"}
