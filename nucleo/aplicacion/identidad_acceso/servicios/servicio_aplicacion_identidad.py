from uuid import UUID

from nucleo.aplicacion.identidad_acceso.comandos.comando_asignar_rol import ComandoAsignarRol
from nucleo.aplicacion.identidad_acceso.comandos.comando_crear_usuario import ComandoCrearUsuario
from nucleo.aplicacion.identidad_acceso.comandos.comando_iniciar_sesion import ComandoIniciarSesion
from nucleo.aplicacion.identidad_acceso.dto.membresia_empresa_dto import MembresiaEmpresaDTO
from nucleo.aplicacion.identidad_acceso.dto.membresia_tenant_dto import MembresiaTenantDTO
from nucleo.aplicacion.identidad_acceso.dto.permiso_dto import PermisoDTO
from nucleo.aplicacion.identidad_acceso.dto.respuesta_token import RespuestaTokenDTO
from nucleo.aplicacion.identidad_acceso.dto.rol_dto import RolDTO
from nucleo.aplicacion.identidad_acceso.dto.usuario_dto import UsuarioDTO
from nucleo.dominio.identidad_acceso.repositorios.repositorio_membresia_empresa import (
    RepositorioMembresiaEmpresa,
)
from nucleo.dominio.identidad_acceso.repositorios.repositorio_membresia_tenant import (
    RepositorioMembresiaTenant,
)
from nucleo.dominio.identidad_acceso.repositorios.repositorio_permiso import RepositorioPermiso
from nucleo.dominio.identidad_acceso.repositorios.repositorio_rol import RepositorioRol
from nucleo.dominio.identidad_acceso.repositorios.repositorio_usuario import RepositorioUsuario
from nucleo.dominio.organizacion.repositorios.repositorio_empresa import RepositorioEmpresa
from nucleo.dominio.organizacion.repositorios.repositorio_tenant import RepositorioTenant
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_empresa import (
    ModeloMembresiaEmpresa,
)
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_membresia_tenant import (
    ModeloMembresiaTenant,
)
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_rol import ModeloRol
from nucleo.infraestructura.db.modelos.identidad_acceso.modelo_usuario import ModeloUsuario
from nucleo.infraestructura.seguridad.autenticacion.gestor_contrasenas import GestorContrasenas
from nucleo.infraestructura.seguridad.autenticacion.gestor_jwt import GestorJWT


class ServicioAplicacionIdentidad:
    def __init__(
        self,
        repositorio_usuario: RepositorioUsuario,
        repositorio_rol: RepositorioRol,
        repositorio_permiso: RepositorioPermiso,
        repositorio_membresia_tenant: RepositorioMembresiaTenant,
        repositorio_membresia_empresa: RepositorioMembresiaEmpresa,
        repositorio_tenant: RepositorioTenant,
        repositorio_empresa: RepositorioEmpresa,
        gestor_contrasenas: GestorContrasenas | None = None,
        gestor_jwt: GestorJWT | None = None,
    ):
        self.repositorio_usuario = repositorio_usuario
        self.repositorio_rol = repositorio_rol
        self.repositorio_permiso = repositorio_permiso
        self.repositorio_membresia_tenant = repositorio_membresia_tenant
        self.repositorio_membresia_empresa = repositorio_membresia_empresa
        self.repositorio_tenant = repositorio_tenant
        self.repositorio_empresa = repositorio_empresa
        self.gestor_contrasenas = gestor_contrasenas or GestorContrasenas()
        self.gestor_jwt = gestor_jwt or GestorJWT()

    def crear_usuario(self, comando: ComandoCrearUsuario) -> UsuarioDTO:
        tenant = self.repositorio_tenant.obtener_por_id(comando.tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        usuario_por_correo = self.repositorio_usuario.obtener_por_correo(
            comando.tenant_id,
            comando.correo,
        )
        if usuario_por_correo:
            raise ValueError("Ya existe un usuario con ese correo en el tenant")

        usuario_por_nombre = self.repositorio_usuario.obtener_por_nombre_usuario(
            comando.tenant_id,
            comando.nombre_usuario,
        )
        if usuario_por_nombre:
            raise ValueError("Ya existe un usuario con ese nombre de usuario en el tenant")

        usuario = ModeloUsuario(
            tenant_id=comando.tenant_id,
            nombres=comando.nombres,
            apellidos=comando.apellidos,
            nombre_usuario=comando.nombre_usuario,
            correo=comando.correo,
            contrasena_hash=comando.contrasena_hash,
            esta_activo=comando.esta_activo,
            es_superadministrador=comando.es_superadministrador,
        )
        creado = self.repositorio_usuario.crear(usuario)

        return UsuarioDTO(
            id=creado.id,
            tenant_id=creado.tenant_id,
            nombres=creado.nombres,
            apellidos=creado.apellidos,
            nombre_usuario=creado.nombre_usuario,
            correo=creado.correo,
            esta_activo=creado.esta_activo,
            es_superadministrador=creado.es_superadministrador,
            ultimo_acceso=creado.ultimo_acceso,
            creado_en=creado.creado_en,
            actualizado_en=creado.actualizado_en,
        )

    def crear_usuario_con_contrasena(self, comando: ComandoCrearUsuario, contrasena_plana: str) -> UsuarioDTO:
        comando.contrasena_hash = self.gestor_contrasenas.generar_hash(contrasena_plana)
        return self.crear_usuario(comando)

    def autenticar_usuario(self, comando: ComandoIniciarSesion) -> RespuestaTokenDTO:
        tenant = self.repositorio_tenant.obtener_por_id(comando.tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        usuario = self.repositorio_usuario.obtener_por_correo(
            comando.tenant_id,
            comando.identificador,
        )
        if not usuario:
            usuario = self.repositorio_usuario.obtener_por_nombre_usuario(
                comando.tenant_id,
                comando.identificador,
            )

        if not usuario:
            raise ValueError("Credenciales invalidas")

        if not usuario.esta_activo:
            raise ValueError("El usuario esta inactivo")

        if not self.gestor_contrasenas.verificar_contrasena(
            comando.contrasena_plana,
            usuario.contrasena_hash,
        ):
            raise ValueError("Credenciales invalidas")

        token, expira_en_segundos = self.gestor_jwt.crear_token_acceso(
            usuario_id=usuario.id,
            tenant_id=usuario.tenant_id,
            nombre_usuario=usuario.nombre_usuario,
        )

        return RespuestaTokenDTO(
            access_token=token,
            token_type="bearer",
            expira_en_segundos=expira_en_segundos,
            usuario_id=usuario.id,
            tenant_id=usuario.tenant_id,
            nombre_usuario=usuario.nombre_usuario,
        )

    def obtener_usuario(self, usuario_id: UUID) -> UsuarioDTO:
        usuario = self.repositorio_usuario.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe")

        return UsuarioDTO(
            id=usuario.id,
            tenant_id=usuario.tenant_id,
            nombres=usuario.nombres,
            apellidos=usuario.apellidos,
            nombre_usuario=usuario.nombre_usuario,
            correo=usuario.correo,
            esta_activo=usuario.esta_activo,
            es_superadministrador=usuario.es_superadministrador,
            ultimo_acceso=usuario.ultimo_acceso,
            creado_en=usuario.creado_en,
            actualizado_en=usuario.actualizado_en,
        )

    def listar_usuarios(self, tenant_id: UUID) -> list[UsuarioDTO]:
        usuarios = self.repositorio_usuario.listar_por_tenant(tenant_id)
        return [
            UsuarioDTO(
                id=usuario.id,
                tenant_id=usuario.tenant_id,
                nombres=usuario.nombres,
                apellidos=usuario.apellidos,
                nombre_usuario=usuario.nombre_usuario,
                correo=usuario.correo,
                esta_activo=usuario.esta_activo,
                es_superadministrador=usuario.es_superadministrador,
                ultimo_acceso=usuario.ultimo_acceso,
                creado_en=usuario.creado_en,
                actualizado_en=usuario.actualizado_en,
            )
            for usuario in usuarios
        ]

    def crear_rol(self, comando: ComandoAsignarRol) -> RolDTO:
        tenant = self.repositorio_tenant.obtener_por_id(comando.tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        rol_existente = self.repositorio_rol.obtener_por_codigo(
            comando.tenant_id,
            comando.codigo,
        )
        if rol_existente:
            raise ValueError("Ya existe un rol con ese codigo en el tenant")

        rol = ModeloRol(
            tenant_id=comando.tenant_id,
            nombre=comando.nombre,
            codigo=comando.codigo,
            descripcion=comando.descripcion,
            es_sistema=comando.es_sistema,
        )
        creado = self.repositorio_rol.crear(rol)

        return RolDTO(
            id=creado.id,
            tenant_id=creado.tenant_id,
            nombre=creado.nombre,
            codigo=creado.codigo,
            descripcion=creado.descripcion,
            es_sistema=creado.es_sistema,
            creado_en=creado.creado_en,
            actualizado_en=creado.actualizado_en,
        )

    def listar_roles(self, tenant_id: UUID) -> list[RolDTO]:
        roles = self.repositorio_rol.listar_por_tenant(tenant_id)
        return [
            RolDTO(
                id=rol.id,
                tenant_id=rol.tenant_id,
                nombre=rol.nombre,
                codigo=rol.codigo,
                descripcion=rol.descripcion,
                es_sistema=rol.es_sistema,
                creado_en=rol.creado_en,
                actualizado_en=rol.actualizado_en,
            )
            for rol in roles
        ]

    def listar_permisos(self) -> list[PermisoDTO]:
        permisos = self.repositorio_permiso.listar()
        return [
            PermisoDTO(
                id=permiso.id,
                codigo=permiso.codigo,
                nombre=permiso.nombre,
                descripcion=permiso.descripcion,
                modulo=permiso.modulo,
                creado_en=permiso.creado_en,
            )
            for permiso in permisos
        ]

    def vincular_usuario_tenant(
        self,
        tenant_id: UUID,
        usuario_id: UUID,
        rol_id: UUID,
    ) -> MembresiaTenantDTO:
        tenant = self.repositorio_tenant.obtener_por_id(tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        usuario = self.repositorio_usuario.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe")

        rol = self.repositorio_rol.obtener_por_id(rol_id)
        if not rol:
            raise ValueError("El rol no existe")

        membresia = ModeloMembresiaTenant(
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            rol_id=rol_id,
        )
        creada = self.repositorio_membresia_tenant.crear(membresia)

        return MembresiaTenantDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            usuario_id=creada.usuario_id,
            rol_id=creada.rol_id,
            estado=creada.estado,
            creado_en=creada.creado_en,
        )

    def vincular_usuario_empresa(
        self,
        tenant_id: UUID,
        empresa_id: UUID,
        usuario_id: UUID,
        rol_id: UUID,
    ) -> MembresiaEmpresaDTO:
        tenant = self.repositorio_tenant.obtener_por_id(tenant_id)
        if not tenant:
            raise ValueError("El tenant no existe")

        empresa = self.repositorio_empresa.obtener_por_id(empresa_id)
        if not empresa:
            raise ValueError("La empresa no existe")

        usuario = self.repositorio_usuario.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe")

        rol = self.repositorio_rol.obtener_por_id(rol_id)
        if not rol:
            raise ValueError("El rol no existe")

        membresia = ModeloMembresiaEmpresa(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            rol_id=rol_id,
        )
        creada = self.repositorio_membresia_empresa.crear(membresia)

        return MembresiaEmpresaDTO(
            id=creada.id,
            tenant_id=creada.tenant_id,
            empresa_id=creada.empresa_id,
            usuario_id=creada.usuario_id,
            rol_id=creada.rol_id,
            estado=creada.estado,
            creado_en=creada.creado_en,
        )
