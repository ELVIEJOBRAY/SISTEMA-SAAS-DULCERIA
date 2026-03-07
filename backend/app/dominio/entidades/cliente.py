from typing import Optional
import re

class Cliente:
    TIPO_REGULAR = "regular"
    TIPO_VIP = "vip"
    TIPO_EMPRESA = "empresa"
    TIPOS_VALIDOS = [TIPO_REGULAR, TIPO_VIP, TIPO_EMPRESA]
    
    def __init__(self, id: Optional[int], nombre: str, email: str, telefono: Optional[str] = None, tipo: str = TIPO_REGULAR, activo: bool = True):
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DEL CLIENTE ES OBLIGATORIO")
        if len(nombre.strip()) < 3:
            raise ValueError("EL NOMBRE DEBE TENER AL MENOS 3 CARACTERES")
        if not self._email_valido(email):
            raise ValueError("FORMATO DE EMAIL INVÁLIDO")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"TIPO INVÁLIDO. DEBE SER: {self.TIPOS_VALIDOS}")
        
        self.id = id
        self.nombre = nombre.strip()
        self.email = email.lower()
        self.telefono = telefono
        self.tipo = tipo
        self.activo = activo
        self.fecha_registro = None
    
    def _email_valido(self, email: str) -> bool:
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None
    
    def activar(self) -> None: self.activo = True
    def desactivar(self) -> None: self.activo = False
    def es_vip(self) -> bool: return self.tipo == self.TIPO_VIP
    def es_empresa(self) -> bool: return self.tipo == self.TIPO_EMPRESA
    
    def __repr__(self) -> str:
        return f"<Cliente id={self.id} nombre={self.nombre} tipo={self.tipo} activo={self.activo}>"
