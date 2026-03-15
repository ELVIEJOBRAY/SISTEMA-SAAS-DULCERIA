from nucleo.aplicacion.inventario.casos_uso.registrar_movimiento_inventario_caso_uso import RegistrarMovimientoInventarioCasoUso
from nucleo.infraestructura.db.repositorios.inventario.repositorio_existencias_inventario_postgresql import RepositorioExistenciasInventarioPostgresql
from nucleo.infraestructura.db.repositorios.inventario.repositorio_movimientos_inventario_postgresql import RepositorioMovimientosInventarioPostgresql


def obtener_caso_uso_registrar_movimiento_inventario():
    return RegistrarMovimientoInventarioCasoUso(
        repositorio_movimientos=RepositorioMovimientosInventarioPostgresql(),
        repositorio_existencias=RepositorioExistenciasInventarioPostgresql(),
    )
