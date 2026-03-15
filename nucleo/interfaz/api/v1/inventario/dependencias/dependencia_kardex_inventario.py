from nucleo.aplicacion.inventario.consultas.obtener_kardex_inventario_consulta import ObtenerKardexInventarioConsulta
from nucleo.infraestructura.db.repositorios.inventario.repositorio_movimientos_inventario_postgresql import RepositorioMovimientosInventarioPostgresql


def obtener_consulta_kardex_inventario():
    return ObtenerKardexInventarioConsulta(
        repositorio_movimientos=RepositorioMovimientosInventarioPostgresql(),
    )
