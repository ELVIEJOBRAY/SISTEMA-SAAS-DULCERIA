from typing import Optional, List
from app.aplicacion.dto.producto_dto import ProductoCreateDTO, ProductoUpdateDTO, ProductoResponseDTO
from app.aplicacion.servicios.base_servicio import ServicioBase
from app.dominio.entidades.producto import Producto
from app.infraestructura.repositorios.producto_repositorio import RepositorioProducto

class ProductoServicio(ServicioBase[Producto, ProductoCreateDTO, ProductoUpdateDTO, ProductoResponseDTO]):
    def __init__(self, repositorio: RepositorioProducto):
        super().__init__(repositorio)
        self.repo_producto = repositorio
    
    def _dto_a_entidad(self, dto: ProductoCreateDTO) -> Producto:
        return Producto(id=None, nombre=dto.nombre, precio=dto.precio, stock=dto.stock)
    
    def _entidad_a_dto(self, entidad: Producto) -> ProductoResponseDTO:
        return ProductoResponseDTO(id=entidad.id, nombre=entidad.nombre, precio=entidad.precio, stock=entidad.stock, activo=True)
    
    def _actualizar_entidad(self, entidad: Producto, dto: ProductoUpdateDTO) -> Producto:
        if dto.nombre: entidad.nombre = dto.nombre
        if dto.precio: entidad.precio = dto.precio
        if dto.stock is not None: entidad.stock = dto.stock
        return entidad
    
    def buscar_por_nombre(self, termino: str) -> List[ProductoResponseDTO]:
        productos = self.repo_producto.buscar_por_nombre(termino)
        return [self._entidad_a_dto(p) for p in productos]
    
    def reducir_stock(self, id: int, cantidad: int) -> Optional[ProductoResponseDTO]:
        producto = self.repo_producto.reducir_stock(id, cantidad)
        return self._entidad_a_dto(producto) if producto else None
