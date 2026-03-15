from uuid import UUID

from nucleo.aplicacion.catalogo.dto.presentacion_dto import PresentacionDTO
from nucleo.aplicacion.inventario.comandos.comando_registrar_ajuste_inventario import (
    ComandoRegistrarAjusteInventario,
)
from nucleo.aplicacion.inventario.comandos.comando_registrar_entrada_inventario import (
    ComandoRegistrarEntradaInventario,
)
from nucleo.aplicacion.inventario.comandos.comando_registrar_salida_inventario import (
    ComandoRegistrarSalidaInventario,
)
from nucleo.aplicacion.inventario.dto.inventario_dto import InventarioDTO
from nucleo.aplicacion.inventario.dto.movimiento_inventario_dto import MovimientoInventarioDTO
from nucleo.dominio.catalogo.repositorios.repositorio_presentacion import RepositorioPresentacion
from nucleo.dominio.catalogo.repositorios.repositorio_producto import RepositorioProducto
from nucleo.dominio.inventario.repositorios.repositorio_inventario import RepositorioInventario
from nucleo.dominio.inventario.repositorios.repositorio_movimiento_inventario import (
    RepositorioMovimientoInventario,
)
from nucleo.dominio.organizacion.repositorios.repositorio_bodega import RepositorioBodega
from nucleo.dominio.organizacion.repositorios.repositorio_empresa import RepositorioEmpresa
from nucleo.dominio.organizacion.repositorios.repositorio_sucursal import RepositorioSucursal
from nucleo.dominio.organizacion.repositorios.repositorio_tenant import RepositorioTenant
from nucleo.infraestructura.db.modelos.inventario.modelo_inventario import ModeloInventario
from nucleo.infraestructura.db.modelos.inventario.modelo_movimiento_inventario import (
    ModeloMovimientoInventario,
)


class ServicioAplicacionInventario:
    def __init__(
        self,
        repositorio_inventario: RepositorioInventario,
        repositorio_movimiento_inventario: RepositorioMovimientoInventario,
        repositorio_tenant: RepositorioTenant,
        repositorio_empresa: RepositorioEmpresa,
        repositorio_sucursal: RepositorioSucursal,
        repositorio_bodega: RepositorioBodega,
        repositorio_producto: RepositorioProducto,
        repositorio_presentacion: RepositorioPresentacion,
    ):
        self.repositorio_inventario = repositorio_inventario
        self.repositorio_movimiento_inventario = repositorio_movimiento_inventario
        self.repositorio_tenant = repositorio_tenant
        self.repositorio_empresa = repositorio_empresa
        self.repositorio_sucursal = repositorio_sucursal
        self.repositorio_bodega = repositorio_bodega
        self.repositorio_producto = repositorio_producto
        self.repositorio_presentacion = repositorio_presentacion

    def _validar_contexto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        sucursal_id: UUID,
        bodega_id: UUID,
        producto_id: UUID,
        presentacion_id: UUID,
    ):
        tenant = self.repositorio_tenant.obtener_por_id(tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        empresa = self.repositorio_empresa.obtener_por_id(empresa_id)
        if not empresa:
            raise ValueError("La empresa no existe")

        sucursal = self.repositorio_sucursal.obtener_por_id(sucursal_id)
        if not sucursal:
            raise ValueError("La sucursal no existe")

        bodega = self.repositorio_bodega.obtener_por_id(bodega_id)
        if not bodega:
            raise ValueError("La bodega no existe")

        producto = self.repositorio_producto.obtener_por_id(producto_id)
        if not producto:
            raise ValueError("El producto no existe")

        presentacion = self.repositorio_presentacion.obtener_por_id(presentacion_id)
        if not presentacion:
            raise ValueError("La presentacion no existe")

        if presentacion.producto_id != producto_id:
            raise ValueError("La presentacion no pertenece al producto indicado")

        return producto, presentacion

    def _a_dto_inventario(self, inventario: ModeloInventario) -> InventarioDTO:
        return InventarioDTO(
            id=inventario.id,
            tenant_id=inventario.tenant_id,
            empresa_id=inventario.empresa_id,
            sucursal_id=inventario.sucursal_id,
            bodega_id=inventario.bodega_id,
            producto_id=inventario.producto_id,
            presentacion_id=inventario.presentacion_id,
            cantidad_disponible=float(inventario.cantidad_disponible),
            cantidad_reservada=float(inventario.cantidad_reservada),
            cantidad_transito=float(inventario.cantidad_transito),
            stock_minimo=float(inventario.stock_minimo),
            stock_maximo=float(inventario.stock_maximo),
            costo_promedio=float(inventario.costo_promedio),
            creado_en=inventario.creado_en,
            actualizado_en=inventario.actualizado_en,
        )

    def _a_dto_movimiento(self, movimiento: ModeloMovimientoInventario) -> MovimientoInventarioDTO:
        return MovimientoInventarioDTO(
            id=movimiento.id,
            tenant_id=movimiento.tenant_id,
            empresa_id=movimiento.empresa_id,
            sucursal_id=movimiento.sucursal_id,
            bodega_id=movimiento.bodega_id,
            inventario_id=movimiento.inventario_id,
            producto_id=movimiento.producto_id,
            presentacion_id=movimiento.presentacion_id,
            tipo_movimiento=movimiento.tipo_movimiento,
            referencia_origen=movimiento.referencia_origen,
            documento_referencia=movimiento.documento_referencia,
            observacion=movimiento.observacion,
            cantidad=float(movimiento.cantidad),
            cantidad_anterior=float(movimiento.cantidad_anterior),
            cantidad_nueva=float(movimiento.cantidad_nueva),
            costo_unitario=float(movimiento.costo_unitario),
            valor_total=float(movimiento.valor_total),
            usuario_id=movimiento.usuario_id,
            creado_en=movimiento.creado_en,
        )

    def _obtener_o_crear_inventario(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        sucursal_id: UUID,
        bodega_id: UUID,
        producto_id: UUID,
        presentacion_id: UUID,
    ) -> ModeloInventario:
        inventario = self.repositorio_inventario.obtener_por_bodega_y_presentacion(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            bodega_id=bodega_id,
            presentacion_id=presentacion_id,
        )

        if inventario:
            return inventario

        inventario = ModeloInventario(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            sucursal_id=sucursal_id,
            bodega_id=bodega_id,
            producto_id=producto_id,
            presentacion_id=presentacion_id,
            cantidad_disponible=0,
            cantidad_reservada=0,
            cantidad_transito=0,
            stock_minimo=0,
            stock_maximo=0,
            costo_promedio=0,
        )
        return self.repositorio_inventario.crear(inventario)

    def registrar_entrada(self, comando: ComandoRegistrarEntradaInventario) -> MovimientoInventarioDTO:
        if comando.cantidad <= 0:
            raise ValueError("La cantidad de entrada debe ser mayor que cero")

        self._validar_contexto(
            comando.tenant_id,
            comando.empresa_id,
            comando.sucursal_id,
            comando.bodega_id,
            comando.producto_id,
            comando.presentacion_id,
        )

        inventario = self._obtener_o_crear_inventario(
            comando.tenant_id,
            comando.empresa_id,
            comando.sucursal_id,
            comando.bodega_id,
            comando.producto_id,
            comando.presentacion_id,
        )

        cantidad_anterior = float(inventario.cantidad_disponible)
        cantidad_nueva = cantidad_anterior + float(comando.cantidad)

        inventario.cantidad_disponible = cantidad_nueva
        inventario.costo_promedio = float(comando.costo_unitario)
        inventario = self.repositorio_inventario.actualizar(inventario)

        movimiento = ModeloMovimientoInventario(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            sucursal_id=comando.sucursal_id,
            bodega_id=comando.bodega_id,
            inventario_id=inventario.id,
            producto_id=comando.producto_id,
            presentacion_id=comando.presentacion_id,
            tipo_movimiento="entrada",
            referencia_origen=comando.referencia_origen,
            documento_referencia=comando.documento_referencia,
            observacion=comando.observacion,
            cantidad=comando.cantidad,
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=cantidad_nueva,
            costo_unitario=comando.costo_unitario,
            valor_total=float(comando.cantidad) * float(comando.costo_unitario),
            usuario_id=comando.usuario_id,
        )
        creado = self.repositorio_movimiento_inventario.crear(movimiento)
        return self._a_dto_movimiento(creado)

    def registrar_salida(self, comando: ComandoRegistrarSalidaInventario) -> MovimientoInventarioDTO:
        if comando.cantidad <= 0:
            raise ValueError("La cantidad de salida debe ser mayor que cero")

        self._validar_contexto(
            comando.tenant_id,
            comando.empresa_id,
            comando.sucursal_id,
            comando.bodega_id,
            comando.producto_id,
            comando.presentacion_id,
        )

        inventario = self.repositorio_inventario.obtener_por_bodega_y_presentacion(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            bodega_id=comando.bodega_id,
            presentacion_id=comando.presentacion_id,
        )

        if not inventario:
            raise ValueError("No existe inventario para la presentacion en la bodega indicada")

        cantidad_anterior = float(inventario.cantidad_disponible)

        if cantidad_anterior < float(comando.cantidad):
            raise ValueError("Stock insuficiente para registrar la salida")

        cantidad_nueva = cantidad_anterior - float(comando.cantidad)

        inventario.cantidad_disponible = cantidad_nueva
        inventario = self.repositorio_inventario.actualizar(inventario)

        costo_unitario = float(comando.costo_unitario) if float(comando.costo_unitario) > 0 else float(inventario.costo_promedio)

        movimiento = ModeloMovimientoInventario(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            sucursal_id=comando.sucursal_id,
            bodega_id=comando.bodega_id,
            inventario_id=inventario.id,
            producto_id=comando.producto_id,
            presentacion_id=comando.presentacion_id,
            tipo_movimiento="salida",
            referencia_origen=comando.referencia_origen,
            documento_referencia=comando.documento_referencia,
            observacion=comando.observacion,
            cantidad=comando.cantidad,
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=cantidad_nueva,
            costo_unitario=costo_unitario,
            valor_total=float(comando.cantidad) * float(costo_unitario),
            usuario_id=comando.usuario_id,
        )
        creado = self.repositorio_movimiento_inventario.crear(movimiento)
        return self._a_dto_movimiento(creado)

    def registrar_ajuste(self, comando: ComandoRegistrarAjusteInventario) -> MovimientoInventarioDTO:
        if comando.cantidad <= 0:
            raise ValueError("La cantidad del ajuste debe ser mayor que cero")

        self._validar_contexto(
            comando.tenant_id,
            comando.empresa_id,
            comando.sucursal_id,
            comando.bodega_id,
            comando.producto_id,
            comando.presentacion_id,
        )

        inventario = self._obtener_o_crear_inventario(
            comando.tenant_id,
            comando.empresa_id,
            comando.sucursal_id,
            comando.bodega_id,
            comando.producto_id,
            comando.presentacion_id,
        )

        cantidad_anterior = float(inventario.cantidad_disponible)

        if comando.es_incremento:
            tipo_movimiento = "ajuste_positivo"
            cantidad_nueva = cantidad_anterior + float(comando.cantidad)
        else:
            tipo_movimiento = "ajuste_negativo"
            cantidad_nueva = cantidad_anterior - float(comando.cantidad)
            if cantidad_nueva < 0:
                raise ValueError("El ajuste no puede dejar stock negativo")

        inventario.cantidad_disponible = cantidad_nueva
        if float(comando.costo_unitario) > 0:
            inventario.costo_promedio = float(comando.costo_unitario)
        inventario = self.repositorio_inventario.actualizar(inventario)

        costo_unitario = float(comando.costo_unitario) if float(comando.costo_unitario) > 0 else float(inventario.costo_promedio)

        movimiento = ModeloMovimientoInventario(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            sucursal_id=comando.sucursal_id,
            bodega_id=comando.bodega_id,
            inventario_id=inventario.id,
            producto_id=comando.producto_id,
            presentacion_id=comando.presentacion_id,
            tipo_movimiento=tipo_movimiento,
            referencia_origen=comando.referencia_origen,
            documento_referencia=comando.documento_referencia,
            observacion=comando.observacion,
            cantidad=comando.cantidad,
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=cantidad_nueva,
            costo_unitario=costo_unitario,
            valor_total=float(comando.cantidad) * float(costo_unitario),
            usuario_id=comando.usuario_id,
        )
        creado = self.repositorio_movimiento_inventario.crear(movimiento)
        return self._a_dto_movimiento(creado)

    def listar_inventario_por_bodega(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        bodega_id: UUID,
    ) -> list[InventarioDTO]:
        inventarios = self.repositorio_inventario.listar_por_bodega(
            tenant_id,
            empresa_id,
            bodega_id,
        )
        return [self._a_dto_inventario(inventario) for inventario in inventarios]

    def listar_inventario_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[InventarioDTO]:
        inventarios = self.repositorio_inventario.listar_por_producto(
            tenant_id,
            empresa_id,
            producto_id,
        )
        return [self._a_dto_inventario(inventario) for inventario in inventarios]

    def listar_kardex_por_producto(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        producto_id: UUID,
    ) -> list[MovimientoInventarioDTO]:
        movimientos = self.repositorio_movimiento_inventario.listar_kardex_por_producto(
            tenant_id,
            empresa_id,
            producto_id,
        )
        return [self._a_dto_movimiento(movimiento) for movimiento in movimientos]

    def listar_kardex_por_presentacion(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        presentacion_id: UUID,
    ) -> list[MovimientoInventarioDTO]:
        movimientos = self.repositorio_movimiento_inventario.listar_kardex_por_presentacion(
            tenant_id,
            empresa_id,
            presentacion_id,
        )
        return [self._a_dto_movimiento(movimiento) for movimiento in movimientos]
