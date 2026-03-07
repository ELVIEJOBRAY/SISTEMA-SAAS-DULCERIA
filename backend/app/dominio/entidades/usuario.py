from typing import Optional
import re

class Usuario:
    ROLES_VALIDOS = {"admin", "gerente", "vendedor", "inventario"}
    
    def __init__(self, id: Optional[int], nombre: str, email: str, rol: str, activo: bool = True):
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DEL USUARIO NO PUEDE ESTAR VACÍO")
        if not self._email_valido(email):
            raise ValueError("EL EMAIL NO TIENE UN FORMATO VÁLIDO")
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(f"ROL INVÁLIDO. DEBE SER UNO DE: {self.ROLES_VALIDOS}")
        
        self.id = id
        self.nombre = nombre.strip()
        self.email = email.lower()
        self.rol = rol
        self.activo = activo
    
    def _email_valido(self, email: str) -> bool:
        patron = r"[^@]+@[^@]+\.[^@]+"
        return re.match(patron, email) is not None
    
    def activar(self) -> None: self.activo = True
    def desactivar(self) -> None: self.activo = False
    def es_admin(self) -> bool: return self.rol == "admin"
    
    def cambiar_rol(self, nuevo_rol: str) -> None:
        if nuevo_rol not in self.ROLES_VALIDOS:
            raise ValueError(f"ROL INVÁLIDO. DEBE SER UNO DE: {self.ROLES_VALIDOS}")
        self.rol = nuevo_rol
    
    def __repr__(self) -> str:
        return f"<Usuario id={self.id} nombre={self.nombre} rol={self.rol} activo={self.activo}>"
