from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.nucleo.base_datos import Base

# USUARIO
class UsuarioModelo(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    rol = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# PRODUCTO
class ProductoModelo(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# CATEGORIA
class CategoriaModelo(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(500), nullable=True)
    productos = relationship("ProductoModelo", backref="categoria")

# CLIENTE
class ClienteModelo(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    tipo = Column(String(20), default="regular")
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

# VENTA
class VentaModelo(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    total = Column(Float, nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_venta = Column(DateTime, default=datetime.utcnow)
    cliente = relationship("ClienteModelo", backref="ventas")

# DETALLE VENTA
class DetalleVentaModelo(Base):
    __tablename__ = "detalles_venta"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    venta = relationship("VentaModelo", backref="detalles")
    producto = relationship("ProductoModelo", backref="detalles_venta")

# PAGO
class PagoModelo(Base):
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    monto = Column(Float, nullable=False)
    metodo = Column(String(30), nullable=False)
    estado = Column(String(20), default="pendiente")
    referencia = Column(String(100), nullable=True)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    venta = relationship("VentaModelo", backref="pagos")

# FACTURA
class FacturaModelo(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), unique=True)
    numero_factura = Column(String(50), unique=True, nullable=False)
    tipo = Column(String(30), default="factura")
    estado = Column(String(20), default="emitida")
    subtotal = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    venta = relationship("VentaModelo", backref="factura")

# PROVEEDOR
class ProveedorModelo(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    nit = Column(String(20), unique=True, nullable=False)
    contacto_nombre = Column(String(100), nullable=True)
    contacto_email = Column(String(100), nullable=True)
    contacto_telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)

# INQUILINO (TENANT)
class InquilinoModelo(Base):
    __tablename__ = "inquilinos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    subdominio = Column(String(50), unique=True, nullable=False)
    plan = Column(String(30), default="gratuito")
    estado = Column(String(20), default="activo")
    max_usuarios = Column(Integer, default=5)
    max_productos = Column(Integer, default=100)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
