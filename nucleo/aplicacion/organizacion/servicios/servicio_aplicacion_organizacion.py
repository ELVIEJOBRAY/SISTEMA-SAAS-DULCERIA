from uuid import UUID

from nucleo.aplicacion.organizacion.comandos.comando_crear_bodega import ComandoCrearBodega
from nucleo.aplicacion.organizacion.comandos.comando_crear_empresa import ComandoCrearEmpresa
from nucleo.aplicacion.organizacion.comandos.comando_crear_sucursal import ComandoCrearSucursal
from nucleo.aplicacion.organizacion.comandos.comando_crear_tenant import ComandoCrearTenant
from nucleo.aplicacion.organizacion.dto.bodega_dto import BodegaDTO
from nucleo.aplicacion.organizacion.dto.empresa_dto import EmpresaDTO
from nucleo.aplicacion.organizacion.dto.sucursal_dto import SucursalDTO
from nucleo.aplicacion.organizacion.dto.tenant_dto import TenantDTO
from nucleo.dominio.organizacion.repositorios.repositorio_bodega import RepositorioBodega
from nucleo.dominio.organizacion.repositorios.repositorio_empresa import RepositorioEmpresa
from nucleo.dominio.organizacion.repositorios.repositorio_sucursal import RepositorioSucursal
from nucleo.dominio.organizacion.repositorios.repositorio_tenant import RepositorioTenant
from nucleo.infraestructura.db.modelos.organizacion.modelo_bodega import ModeloBodega
from nucleo.infraestructura.db.modelos.organizacion.modelo_empresa import ModeloEmpresa
from nucleo.infraestructura.db.modelos.organizacion.modelo_sucursal import ModeloSucursal
from nucleo.infraestructura.db.modelos.organizacion.modelo_tenant import ModeloTenant


class ServicioAplicacionOrganizacion:
    def __init__(
        self,
        repositorio_tenant: RepositorioTenant,
        repositorio_empresa: RepositorioEmpresa,
        repositorio_sucursal: RepositorioSucursal,
        repositorio_bodega: RepositorioBodega,
    ):
        self.repositorio_tenant = repositorio_tenant
        self.repositorio_empresa = repositorio_empresa
        self.repositorio_sucursal = repositorio_sucursal
        self.repositorio_bodega = repositorio_bodega

    def crear_tenant(self, comando: ComandoCrearTenant) -> TenantDTO:
        existente = self.repositorio_tenant.obtener_por_slug(comando.slug)
        if existente:
            raise ValueError("Ya existe un tenant con ese slug")

        tenant = ModeloTenant(
            nombre=comando.nombre,
            slug=comando.slug,
            correo_contacto=comando.correo_contacto,
            telefono_contacto=comando.telefono_contacto,
        )
        creado = self.repositorio_tenant.crear(tenant)

        return TenantDTO(
            id=creado.id,
            nombre=creado.nombre,
            slug=creado.slug,
            correo_contacto=creado.correo_contacto,
            telefono_contacto=creado.telefono_contacto,
            estado=creado.estado,
            creado_en=creado.creado_en,
            actualizado_en=creado.actualizado_en,
        )

    def crear_empresa(self, comando: ComandoCrearEmpresa) -> EmpresaDTO:
        tenant = self.repositorio_tenant.obtener_por_id(comando.tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        empresa = ModeloEmpresa(
            tenant_id=comando.tenant_id,
            nombre=comando.nombre,
            nombre_comercial=comando.nombre_comercial,
            nit=comando.nit,
            correo=comando.correo,
            telefono=comando.telefono,
            direccion=comando.direccion,
        )
        creada = self.repositorio_empresa.crear(empresa)

        return EmpresaDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            nombre=creada.nombre,
            nombre_comercial=creada.nombre_comercial,
            nit=creada.nit,
            correo=creada.correo,
            telefono=creada.telefono,
            direccion=creada.direccion,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def crear_sucursal(self, comando: ComandoCrearSucursal) -> SucursalDTO:
        empresa = self.repositorio_empresa.obtener_por_id(comando.empresa_id)
        if not empresa:
            raise ValueError("La empresa no existe")

        sucursal = ModeloSucursal(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            correo=comando.correo,
            telefono=comando.telefono,
            direccion=comando.direccion,
            es_principal=comando.es_principal,
        )
        creada = self.repositorio_sucursal.crear(sucursal)

        return SucursalDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            nombre=creada.nombre,
            codigo=creada.codigo,
            correo=creada.correo,
            telefono=creada.telefono,
            direccion=creada.direccion,
            es_principal=creada.es_principal,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def crear_bodega(self, comando: ComandoCrearBodega) -> BodegaDTO:
        sucursal = self.repositorio_sucursal.obtener_por_id(comando.sucursal_id)
        if not sucursal:
            raise ValueError("La sucursal no existe")

        bodega = ModeloBodega(
            tenant_id=comando.tenant_id,
            empresa_id=comando.empresa_id,
            sucursal_id=comando.sucursal_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            tipo=comando.tipo,
            permite_venta=comando.permite_venta,
        )
        creada = self.repositorio_bodega.crear(bodega)

        return BodegaDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            sucursal_id=creada.sucursal_id,
            nombre=creada.nombre,
            codigo=creada.codigo,
            tipo=creada.tipo,
            permite_venta=creada.permite_venta,
            estado=creada.estado,
            creado_en=creada.creado_en,
            actualizado_en=creada.actualizado_en,
        )

    def listar_empresas(self, tenant_id: UUID) -> list[EmpresaDTO]:
        empresas = self.repositorio_empresa.listar_por_tenant(tenant_id)
        return [
            EmpresaDTO(
                id=empresa.id,
                tenant_id=empresa.tenant_id,
                nombre=empresa.nombre,
                nombre_comercial=empresa.nombre_comercial,
                nit=empresa.nit,
                correo=empresa.correo,
                telefono=empresa.telefono,
                direccion=empresa.direccion,
                estado=empresa.estado,
                creado_en=empresa.creado_en,
                actualizado_en=empresa.actualizado_en,
            )
            for empresa in empresas
        ]

    def listar_sucursales(self, empresa_id: UUID) -> list[SucursalDTO]:
        sucursales = self.repositorio_sucursal.listar_por_empresa(empresa_id)
        return [
            SucursalDTO(
                id=sucursal.id,
                tenant_id=sucursal.tenant_id,
                empresa_id=sucursal.empresa_id,
                nombre=sucursal.nombre,
                codigo=sucursal.codigo,
                correo=sucursal.correo,
                telefono=sucursal.telefono,
                direccion=sucursal.direccion,
                es_principal=sucursal.es_principal,
                estado=sucursal.estado,
                creado_en=sucursal.creado_en,
                actualizado_en=sucursal.actualizado_en,
            )
            for sucursal in sucursales
        ]
