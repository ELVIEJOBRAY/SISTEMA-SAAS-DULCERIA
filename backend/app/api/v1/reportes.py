from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.nucleo.base_datos import obtener_bd
from app.api.v1.dependencias import obtener_usuario_actual, requerir_roles
from app.infraestructura.repositorios.venta_repositorio import RepositorioVenta
from app.infraestructura.repositorios.producto_repositorio import RepositorioProducto
from app.infraestructura.repositorios.cliente_repositorio import RepositorioCliente
from app.infraestructura.repositorios.usuario_repositorio import RepositorioUsuario

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/dashboard")
async def dashboard(
    db: Session = Depends(obtener_bd),
    usuario_actual = Depends(obtener_usuario_actual)
):
    \"\"\"
    REPORTE DE DASHBOARD PRINCIPAL
    
    Muestra métricas clave del sistema
    \"\"\"
    repo_ventas = RepositorioVenta(db)
    repo_productos = RepositorioProducto(db)
    repo_clientes = RepositorioCliente(db)
    repo_usuarios = RepositorioUsuario(db)
    
    # Obtener ventas del día
    hoy = datetime.now().date()
    todas_ventas = repo_ventas.obtener_todos()
    ventas_hoy = [v for v in todas_ventas if hasattr(v, 'fecha_venta') and v.fecha_venta.date() == hoy]
    
    return {
        "fecha": hoy.isoformat(),
        "total_ventas": repo_ventas.contar(),
        "total_productos": repo_productos.contar(),
        "total_clientes": repo_clientes.contar(),
        "total_usuarios": repo_usuarios.contar(),
        "ventas_hoy": len(ventas_hoy),
        "productos_stock_bajo": len(repo_productos.buscar_con_stock_bajo())
    }

@router.get("/ventas")
async def reporte_ventas(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    db: Session = Depends(obtener_bd),
    usuario_actual = Depends(requerir_roles(["admin", "gerente"]))
):
    \"\"\"
    REPORTE DE VENTAS POR RANGO DE FECHAS
    \"\"\"
    repo = RepositorioVenta(db)
    todas = repo.obtener_todos()
    
    # Convertir fechas
    try:
        inicio = datetime.fromisoformat(fecha_inicio) if fecha_inicio else datetime.now() - timedelta(days=30)
        fin = datetime.fromisoformat(fecha_fin) if fecha_fin else datetime.now()
    except:
        inicio = datetime.now() - timedelta(days=30)
        fin = datetime.now()
    
    ventas_filtradas = [
        v for v in todas 
        if hasattr(v, 'fecha_venta') and inicio <= v.fecha_venta <= fin
    ]
    
    total = sum(v.total for v in ventas_filtradas if hasattr(v, 'total'))
    
    return {
        "fecha_inicio": inicio.isoformat(),
        "fecha_fin": fin.isoformat(),
        "total_ventas": len(ventas_filtradas),
        "monto_total": total,
        "promedio_por_venta": total / len(ventas_filtradas) if ventas_filtradas else 0
    }

@router.get("/productos/mas-vendidos")
async def productos_mas_vendidos(
    limite: int = 10,
    db: Session = Depends(obtener_bd),
    usuario_actual = Depends(obtener_usuario_actual)
):
    \"\"\"
    REPORTE DE PRODUCTOS MÁS VENDIDOS
    \"\"\"
    # Implementación simplificada
    return {
        "mensaje": "Reporte de productos más vendidos",
        "limite": limite,
        "productos": []
    }

@router.get("/clientes/frecuentes")
async def clientes_frecuentes(
    limite: int = 10,
    db: Session = Depends(obtener_bd),
    usuario_actual = Depends(obtener_usuario_actual)
):
    \"\"\"
    REPORTE DE CLIENTES FRECUENTES
    \"\"\"
    repo_clientes = RepositorioCliente(db)
    clientes = repo_clientes.obtener_todos()
    
    # Ordenar por total_compras (simulado)
    clientes_ordenados = sorted(clientes, key=lambda c: c.total_compras if hasattr(c, 'total_compras') else 0, reverse=True)
    
    return {
        "total_clientes": len(clientes_ordenados),
        "clientes_frecuentes": clientes_ordenados[:limite]
    }
