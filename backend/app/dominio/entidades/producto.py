from typing import Optional

class Producto:
    def __init__(self, id: Optional[int], nombre: str, precio: float, stock: int, categoria: str = "general"):
        if not nombre or not nombre.strip():
            raise ValueError("EL NOMBRE DEL PRODUCTO NO PUEDE ESTAR VACÍO")
        if precio <= 0:
            raise ValueError("EL PRECIO DEBE SER MAYOR A CERO")
        if stock < 0:
            raise ValueError("EL STOCK NO PUEDE SER NEGATIVO")
        
        self.id = id
        self.nombre = nombre.strip()
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.activo = True
    
    def reducir_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")
        if cantidad > self.stock:
            raise ValueError("STOCK INSUFICIENTE")
        self.stock -= cantidad
    
    def aumentar_stock(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A 0")
        self.stock += cantidad
    
    def disponible(self) -> bool:
        return self.stock > 0
    
    def __repr__(self) -> str:
        return f"<Producto id={self.id} nombre={self.nombre} stock={self.stock} precio={self.precio}>"
