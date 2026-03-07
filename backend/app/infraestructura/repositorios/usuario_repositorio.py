from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.usuario import Usuario
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import UsuarioModelo

class RepositorioUsuario(RepositorioBase[Usuario]):
    def __init__(self, db_session: Session): self.db = db_session
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        modelo = self.db.get(UsuarioModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    
    def obtener_todos(self) -> List[Usuario]:
        resultados = self.db.execute(select(UsuarioModelo))
        return [self._modelo_a_entidad(m) for m in resultados.scalars().all()]
    
    def guardar(self, entidad: Usuario) -> Usuario:
        from datetime import datetime
        if entidad.id is None:
            modelo = UsuarioModelo(
                nombre=entidad.nombre, email=entidad.email, rol=entidad.rol,
                activo=entidad.activo, fecha_creacion=datetime.now(timezone.utc),
                fecha_actualizacion=datetime.now(timezone.utc)
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(UsuarioModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.email = entidad.email
                modelo.rol = entidad.rol
                modelo.activo = entidad.activo
                modelo.fecha_actualizacion = datetime.now(timezone.utc)
        return entidad
    
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(UsuarioModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    
    def contar(self) -> int:
        return self.db.query(UsuarioModelo).count()
    
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        resultado = self.db.execute(select(UsuarioModelo).where(UsuarioModelo.email == email))
        modelo = resultado.scalar_one_or_none()
        return self._modelo_a_entidad(modelo) if modelo else None
    
    def _modelo_a_entidad(self, modelo: UsuarioModelo) -> Usuario:
        return Usuario(id=modelo.id, nombre=modelo.nombre, email=modelo.email, rol=modelo.rol, activo=modelo.activo)
