from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.proveedor import Proveedor
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import ProveedorModelo

class RepositorioProveedor(RepositorioBase[Proveedor]):
    def __init__(self, db_session: Session): self.db = db_session
    def obtener_por_id(self, id: int) -> Optional[Proveedor]:
        modelo = self.db.get(ProveedorModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    def obtener_todos(self) -> List[Proveedor]:
        resultados = self.db.execute(select(ProveedorModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    def guardar(self, entidad: Proveedor) -> Proveedor:
        from datetime import datetime
        if entidad.id is None:
            modelo = ProveedorModelo(
                nombre=entidad.nombre,
                nit=entidad.nit,
                contacto_nombre=entidad.contacto_nombre,
                contacto_email=entidad.contacto_email,
                contacto_telefono=entidad.contacto_telefono,
                activo=entidad.activo
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(ProveedorModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.contacto_nombre = entidad.contacto_nombre
                modelo.contacto_email = entidad.contacto_email
                modelo.contacto_telefono = entidad.contacto_telefono
                modelo.activo = entidad.activo
        return entidad
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(ProveedorModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    def contar(self) -> int: return self.db.query(ProveedorModelo).count()
    def _modelo_a_entidad(self, modelo: ProveedorModelo) -> Proveedor:
        return Proveedor(
            id=modelo.id, nombre=modelo.nombre, nit=modelo.nit,
            contacto_nombre=modelo.contacto_nombre, contacto_email=modelo.contacto_email,
            contacto_telefono=modelo.contacto_telefono, activo=modelo.activo
        )
