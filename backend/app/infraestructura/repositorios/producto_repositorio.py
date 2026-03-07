from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dominio.entidades.producto import Producto
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import ProductoModelo

class RepositorioProducto(RepositorioBase[Producto]):
    def __init__(self, db_session: Session): self.db = db_session
    
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        modelo = self.db.get(ProductoModelo, id)
        return self._modelo_a_entidad(modelo) if modelo else None
    
    def obtener_todos(self) -> List[Producto]:
        resultados = self.db.execute(select(ProductoModelo))
        return [self._modelo_a_entidad(m) for m in resultados.scalars().all()]
    
    def guardar(self, entidad: Producto) -> Producto:
        from datetime import datetime
        if entidad.id is None:
            modelo = ProductoModelo(
                nombre=entidad.nombre, precio=entidad.precio, stock=entidad.stock,
                activo=True, fecha_creacion=datetime.now(timezone.utc),
                fecha_actualizacion=datetime.now(timezone.utc)
            )
            self.db.add(modelo); self.db.flush()
            entidad.id = modelo.id
        else:
            modelo = self.db.get(ProductoModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.precio = entidad.precio
                modelo.stock = entidad.stock
                modelo.fecha_actualizacion = datetime.now(timezone.utc)
        return entidad
    
    def eliminar(self, id: int) -> bool:
        modelo = self.db.get(ProductoModelo, id)
        if modelo: self.db.delete(modelo); return True
        return False
    
    def contar(self) -> int:
        return self.db.query(ProductoModelo).count()
    
    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        resultados = self.db.execute(
            select(ProductoModelo).where(ProductoModelo.nombre.ilike(f"%{termino}%"))
        )
        return [self._modelo_a_entidad(m) for m in resultados.scalars().all()]
    
    def reducir_stock(self, id: int, cantidad: int) -> Optional[Producto]:
        from datetime import datetime
        modelo = self.db.get(ProductoModelo, id)
        if modelo and modelo.stock >= cantidad:
            modelo.stock -= cantidad
            modelo.fecha_actualizacion = datetime.now(timezone.utc)
            return self._modelo_a_entidad(modelo)
        return None
    
    def _modelo_a_entidad(self, modelo: ProductoModelo) -> Producto:
        return Producto(id=modelo.id, nombre=modelo.nombre, precio=modelo.precio, stock=modelo.stock, categoria="general")
