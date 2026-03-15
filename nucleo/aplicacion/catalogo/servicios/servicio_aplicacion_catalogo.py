from uuid import UUID

from nucleo.aplicacion.catalogo.comandos.comando_crear_categoria import ComandoCrearCategoria
from nucleo.aplicacion.catalogo.comandos.comando_crear_marca import ComandoCrearMarca
from nucleo.aplicacion.catalogo.comandos.comando_crear_presentacion import ComandoCrearPresentacion
from nucleo.aplicacion.catalogo.comandos.comando_crear_producto import ComandoCrearProducto
from nucleo.aplicacion.catalogo.dto.categoria_dto import CategoriaDTO
from nucleo.aplicacion.catalogo.dto.marca_dto import MarcaDTO
from nucleo.aplicacion.catalogo.dto.presentacion_dto import PresentacionDTO
from nucleo.aplicacion.catalogo.dto.producto_dto import ProductoDTO
from nucleo.dominio.catalogo.repositorios.repositorio_categoria import RepositorioCategoria
from nucleo.dominio.catalogo.repositorios.repositorio_marca import RepositorioMarca
from nucleo.dominio.catalogo.repositorios.repositorio_presentacion import RepositorioPresentacion
from nucleo.dominio.catalogo.repositorios.repositorio_producto import RepositorioProducto
from nucleo.dominio.organizacion.repositorios.repositorio_empresa import RepositorioEmpresa
from nucleo.dominio.organizacion.repositorios.repositorio_tenant import RepositorioTenant
from nucleo.infraestructura.db.modelos.catalogo.modelo_categoria import ModeloCategoria
from nucleo.infraestructura.db.modelos.catalogo.modelo_marca import ModeloMarca
from nucleo.infraestructura.db.modelos.catalogo.modelo_presentacion import ModeloPresentacion
from nucleo.infraestructura.db.modelos.catalogo.modelo_producto import ModeloProducto


class ServicioAplicacionCatalogo:
    def __init__(
        self,
        repositorio_categoria: RepositorioCategoria,
        repositorio_marca: RepositorioMarca,
        repositorio_producto: RepositorioProducto,
        repositorio_presentacion: RepositorioPresentacion,
        repositorio_tenant: RepositorioTenant,
        repositorio_empresa: RepositorioEmpresa,
    ):
        self.repositorio_categoria = repositorio_categoria
        self.repositorio_marca = repositorio_marca
        self.repositorio_producto = repositorio_producto
        self.repositorio_presentacion = repositorio_presentacion
        self.repositorio_tenant = repositorio_tenant
        self.repositorio_empresa = repositorio_empresa

    def _validar_tenant_empresa(self, tenant_id: UUID, empresa_id: UUID) -> None:
        tenant = self.repositorio_tenant.obtener_por_id(tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        empresa = self.repositorio_empresa.obtener_por_id(empresa_id)
        if not empresa:
            raise ValueError("La empresa no existe")

    def crear_categoria(self, comando: ComandoCrearCategoria) -> CategoriaDTO:
        self._validar_tenant_empresa(comando.tenant_id, comando.empresa_id)

        existente = self.repositorio_categoria.obtener_por_codigo(comando.tenant_id, comando.codigo)
        if existente:
            raise ValueError("Ya existe una categoria con ese codigo en el tenant")

        categoria = ModeloCategoria(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            descripcion=comando.descripcion,
        )
        creada = self.repositorio_categoria.crear(categoria)

        return CategoriaDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            nombre=creada.nombre,
            codigo=creada.codigo,
            descripcion=creada.descripcion,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def crear_marca(self, comando: ComandoCrearMarca) -> MarcaDTO:
        self._validar_tenant_empresa(comando.tenant_id, comando.empresa_id)

        existente = self.repositorio_marca.obtener_por_codigo(comando.tenant_id, comando.codigo)
        if existente:
            raise ValueError("Ya existe una marca con ese codigo en el tenant")

        marca = ModeloMarca(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            descripcion=comando.descripcion,
        )
        creada = self.repositorio_marca.crear(marca)

        return MarcaDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            nombre=creada.nombre,
            codigo=creada.codigo,
            descripcion=creada.descripcion,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def crear_producto(self, comando: ComandoCrearProducto) -> ProductoDTO:
        self._validar_tenant_empresa(comando.tenant_id, comando.empresa_id)

        existente = self.repositorio_producto.obtener_por_sku(comando.tenant_id, comando.sku)
        if existente:
            raise ValueError("Ya existe un producto con ese SKU en el tenant")

        if comando.categoria_id:
            categoria = self.repositorio_categoria.obtener_por_id(comando.categoria_id)
            if not categoria:
                raise ValueError("La categoria no existe")

        if comando.marca_id:
            marca = self.repositorio_marca.obtener_por_id(comando.marca_id)
            if not marca:
                raise ValueError("La marca no existe")

        producto = ModeloProducto(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            categoria_id=comando.categoria_id,
            marca_id=comando.marca_id,
            nombre=comando.nombre,
            sku=comando.sku,
            codigo_barra=comando.codigo_barra,
            descripcion=comando.descripcion,
            unidad_medida_base=comando.unidad_medida_base,
            precio_base=comando.precio_base,
            costo_base=comando.costo_base,
            permite_venta=comando.permite_venta,
            controla_inventario=comando.controla_inventario,
        )
        creado = self.repositorio_producto.crear(producto)

        return ProductoDTO(
            id=creado.id,
            tenant_id=creado.tenant_id,
            empresa_id=creado.empresa_id,
            categoria_id=creado.categoria_id,
            marca_id=creado.marca_id,
            nombre=creado.nombre,
            sku=creado.sku,
            codigo_barra=creado.codigo_barra,
            descripcion=creado.descripcion,
            unidad_medida_base=creado.unidad_medida_base,
            precio_base=float(creado.precio_base),
            costo_base=float(creado.costo_base),
            permite_venta=creado.permite_venta,
            controla_inventario=creado.controla_inventario,
            estado=creado.estado,
            creado_en=creado.creado_en,
            actualizado_en=creado.actualizado_en,
        )

    def crear_presentacion(self, comando: ComandoCrearPresentacion) -> PresentacionDTO:
        self._validar_tenant_empresa(comando.tenant_id, comando.empresa_id)

        producto = self.repositorio_producto.obtener_por_id(comando.producto_id)
        if not producto:
            raise ValueError("El producto no existe")

        presentacion = ModeloPresentacion(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            producto_id=comando.producto_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            equivalencia_base=comando.equivalencia_base,
            precio_venta=comando.precio_venta,
            costo=comando.costo,
            codigo_barra=comando.codigo_barra,
            es_predeterminada=comando.es_predeterminada,
        )
        creada = self.repositorio_presentacion.crear(presentacion)

        return PresentacionDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            producto_id=creada.producto_id,
            nombre=creada.nombre,
            codigo=creada.codigo,
            equivalencia_base=float(creada.equivalencia_base),
            precio_venta=float(creada.precio_venta),
            costo=float(creada.costo),
            codigo_barra=creada.codigo_barra,
            es_predeterminada=creada.es_predeterminada,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def listar_categorias(self, tenant_id: UUID, empresa_id: UUID) -> list[CategoriaDTO]:
        categorias = self.repositorio_categoria.listar_por_empresa(tenant_id, empresa_id)
        return [
            CategoriaDTO(
                id=categoria.id,
                tenant_id=categoria.tenant_id,
                empresa_id=categoria.empresa_id,
                nombre=categoria.nombre,
                codigo=categoria.codigo,
                descripcion=categoria.descripcion,
                estado=categoria.estado,
                creado_en=categoria.creado_en,
                actualizado_en=categoria.actualizado_en,
            )
            for categoria in categorias
        ]

    def listar_marcas(self, tenant_id: UUID, empresa_id: UUID) -> list[MarcaDTO]:
        marcas = self.repositorio_marca.listar_por_empresa(tenant_id, empresa_id)
        return [
            MarcaDTO(
                id=marca.id,
                tenant_id=marca.tenant_id,
                empresa_id=marca.empresa_id,
                nombre=marca.nombre,
                codigo=marca.codigo,
                descripcion=marca.descripcion,
                estado=marca.estado,
                creado_en=marca.creado_en,
                actualizado_en=marca.actualizado_en,
            )
            for marca in marcas
        ]

    def listar_productos(self, tenant_id: UUID, empresa_id: UUID) -> list[ProductoDTO]:
        productos = self.repositorio_producto.listar_por_empresa(tenant_id, empresa_id)
        return [
            ProductoDTO(
                id=producto.id,
                tenant_id=producto.tenant_id,
                empresa_id=producto.empresa_id,
                categoria_id=producto.categoria_id,
                marca_id=producto.marca_id,
                nombre=producto.nombre,
                sku=producto.sku,
                codigo_barra=producto.codigo_barra,
                descripcion=producto.descripcion,
                unidad_medida_base=producto.unidad_medida_base,
                precio_base=float(producto.precio_base),
                costo_base=float(producto.costo_base),
                permite_venta=producto.permite_venta,
                controla_inventario=producto.controla_inventario,
                estado=producto.estado,
                creado_en=producto.creado_en,
                actualizado_en=producto.actualizado_en,
            )
            for producto in productos
        ]

    def listar_presentaciones(self, producto_id: UUID) -> list[PresentacionDTO]:
        presentaciones = self.repositorio_presentacion.listar_por_producto(producto_id)
        return [
            PresentacionDTO(
                id=presentacion.id,
                tenant_id=presentacion.tenant_id,
                empresa_id=presentacion.empresa_id,
                producto_id=presentacion.producto_id,
                nombre=presentacion.nombre,
                codigo=presentacion.codigo,
                equivalencia_base=float(presentacion.equivalencia_base),
                precio_venta=float(presentacion.precio_venta),
                costo=float(presentacion.costo),
                codigo_barra=presentacion.codigo_barra,
                es_predeterminada=presentacion.es_predeterminada,
                estado=presentacion.estado,
                creado_en=presentacion.creado_en,
                actualizado_en=presentacion.actualizado_en,
            )
            for presentacion in presentaciones
        ]
