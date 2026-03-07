from typing import Optional, List
from app.aplicacion.dto.usuario_dto import UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO
from app.aplicacion.servicios.base_servicio import ServicioBase
from app.dominio.entidades.usuario import Usuario
from app.infraestructura.repositorios.usuario_repositorio import RepositorioUsuario

class UsuarioServicio(ServicioBase[Usuario, UsuarioCreateDTO, UsuarioUpdateDTO, UsuarioResponseDTO]):
    def __init__(self, repositorio: RepositorioUsuario):
        super().__init__(repositorio)
        self.repo_usuario = repositorio
    
    def _dto_a_entidad(self, dto: UsuarioCreateDTO) -> Usuario:
        return Usuario(id=None, nombre=dto.nombre, email=dto.email, rol=dto.rol, activo=True)
    
    def _entidad_a_dto(self, entidad: Usuario) -> UsuarioResponseDTO:
        return UsuarioResponseDTO(id=entidad.id, nombre=entidad.nombre, email=entidad.email, rol=entidad.rol, activo=entidad.activo)
    
    def _actualizar_entidad(self, entidad: Usuario, dto: UsuarioUpdateDTO) -> Usuario:
        if dto.nombre: entidad.nombre = dto.nombre
        if dto.email: entidad.email = dto.email
        if dto.rol: entidad.rol = dto.rol
        if dto.activo is not None: entidad.activo = dto.activo
        return entidad
    
    def buscar_por_email(self, email: str) -> Optional[UsuarioResponseDTO]:
        usuario = self.repo_usuario.buscar_por_email(email)
        return self._entidad_a_dto(usuario) if usuario else None
    
    def activar(self, id: int) -> Optional[UsuarioResponseDTO]:
        usuario = self.obtener_por_id(id)
        if not usuario: return None
        return self.actualizar(id, UsuarioUpdateDTO(activo=True))
    
    def desactivar(self, id: int) -> Optional[UsuarioResponseDTO]:
        usuario = self.obtener_por_id(id)
        if not usuario: return None
        return self.actualizar(id, UsuarioUpdateDTO(activo=False))
