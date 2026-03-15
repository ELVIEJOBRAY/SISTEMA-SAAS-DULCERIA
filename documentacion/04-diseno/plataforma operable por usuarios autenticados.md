Claro, bro. Te dejo un **README detallado de la Fase 4** listo para guardar, por ejemplo, como:

```text
documentacion/03-arquitectura/README_FASE_4_IDENTIDAD_ACCESO.md
```

o en:

```text
documentacion/04-diseno/readme_fase_4_identidad_acceso.md
```

---

````markdown
# README — Fase 4: Módulo Identidad y Acceso

## Proyecto

**SISTEMA-SAAS-DULCERIA**

## Fase documentada

**Fase 4 — Implementación del módulo `identidad_acceso`**

## Estado

**Implementada a nivel de modelos, repositorios, aplicación, autenticación base y API FastAPI.**  
**Pendiente de validación funcional completa de extremo a extremo, si aún no ejecutas todas las pruebas del bloque final.**

---

## Propósito de la fase

El objetivo de esta fase fue construir la base de seguridad y acceso del ERP SaaS multiempresa, permitiendo que el sistema pase de una estructura organizacional operativa a una plataforma preparada para operación multiusuario.

Esta fase introduce el contexto `identidad_acceso`, encargado de gestionar:

- usuarios
- roles
- permisos
- membresías por tenant
- membresías por empresa
- autenticación base
- generación de tokens JWT

---

## Objetivo general

Implementar el módulo `identidad_acceso` siguiendo la arquitectura limpia del proyecto, integrando PostgreSQL, SQLAlchemy y FastAPI, para soportar autenticación, autorización y asignación de usuarios a contextos organizacionales.

---

## Objetivos específicos

- mapear las tablas de identidad y acceso existentes en PostgreSQL a modelos SQLAlchemy
- implementar repositorios para usuarios, roles, permisos y membresías
- construir la capa de aplicación del módulo
- introducir hash seguro de contraseñas
- implementar autenticación básica con JWT
- exponer endpoints FastAPI para gestión de identidad
- preparar al sistema para control de acceso por tenant y empresa

---

## Alcance de la fase

Durante esta fase se implementó el soporte base para:

- creación de usuarios
- obtención de usuarios
- listado de usuarios por tenant
- creación de roles
- listado de roles por tenant
- listado de permisos
- autenticación por correo o nombre de usuario
- emisión de token JWT
- vinculación de usuarios a tenant
- vinculación de usuarios a empresa

Esta fase no cubre todavía autorización avanzada por endpoint ni refresco de tokens, pero deja la base completamente preparada para eso.

---

## Contexto arquitectónico

La fase fue desarrollada bajo la arquitectura definida del proyecto:

- arquitectura limpia
- DDD
- monolito modular
- PostgreSQL
- SQLAlchemy
- FastAPI

El módulo `identidad_acceso` quedó distribuido así:

```text
nucleo
├── dominio
│   └── identidad_acceso
├── aplicacion
│   └── identidad_acceso
├── infraestructura
│   ├── db
│   │   └── modelos / repositorios
│   └── seguridad
│       └── autenticacion
└── interfaz
    └── api
        └── v1
            └── identidad_acceso
````

---

## Entidades cubiertas en esta fase

### Usuario

Representa a una persona con acceso al sistema dentro de un tenant.

### Rol

Representa un conjunto de capacidades operativas dentro del tenant.

### Permiso

Representa una capacidad específica del sistema, asociada a un módulo.

### RolPermiso

Relaciona roles con permisos.

### MembresiaTenant

Relaciona un usuario con un tenant bajo un rol determinado.

### MembresiaEmpresa

Relaciona un usuario con una empresa específica bajo un rol determinado.

---

## Base de datos involucrada

### Motor

* PostgreSQL

### Base utilizada

* `sistema_saas_dulceria`

### Tablas trabajadas

* `usuarios`
* `roles`
* `permisos`
* `roles_permisos`
* `membresias_tenant`
* `membresias_empresa`

---

## Subfases implementadas

# Fase 4.1 — Modelos SQLAlchemy

Se implementaron los modelos ORM para las tablas de identidad y acceso:

* `ModeloUsuario`
* `ModeloRol`
* `ModeloPermiso`
* `ModeloRolPermiso`
* `ModeloMembresiaTenant`
* `ModeloMembresiaEmpresa`

### Ubicación

```text
nucleo/infraestructura/db/modelos/identidad_acceso/
```

### Propósito

* mapear tablas reales de PostgreSQL
* definir tipos, relaciones y restricciones
* servir como base de los repositorios

---

# Fase 4.2 — Repositorios SQLAlchemy

Se implementaron interfaces abstractas en dominio y repositorios concretos en infraestructura para:

* usuarios
* roles
* permisos
* membresías tenant
* membresías empresa

### Interfaces de dominio

```text
nucleo/dominio/identidad_acceso/repositorios/
```

### Implementaciones SQLAlchemy

```text
nucleo/infraestructura/db/repositorios/identidad_acceso/
```

### Operaciones cubiertas

#### Usuario

* crear
* obtener por id
* obtener por correo
* obtener por nombre de usuario
* listar por tenant

#### Rol

* crear
* obtener por id
* obtener por código
* listar por tenant

#### Permiso

* obtener por código
* listar

#### Membresía tenant

* crear
* listar por usuario

#### Membresía empresa

* crear
* listar por usuario

---

# Fase 4.3 — Capa de aplicación

Se implementaron:

## DTO

* `UsuarioDTO`
* `RolDTO`
* `PermisoDTO`
* `MembresiaTenantDTO`
* `MembresiaEmpresaDTO`

## Comandos

* `ComandoCrearUsuario`
* `ComandoAsignarRol`
* `ComandoAsignarPermiso`

## Servicio de aplicación

* `ServicioAplicacionIdentidad`

## Casos de uso / consultas

* `CrearUsuario`
* `AutenticarUsuario` inicial
* `AsignarRol`
* `AsignarPermiso`
* `VincularUsuarioTenant`
* `VincularUsuarioEmpresa`
* `ConsultaObtenerUsuario`
* `ConsultaListarRoles`
* `ConsultaListarPermisos`
* `ConsultaListarUsuarios`

### Responsabilidades del servicio de aplicación

* validar existencia de tenant y empresa
* validar unicidad de correo y nombre de usuario por tenant
* coordinar repositorios
* transformar resultados a DTO
* centralizar la lógica de aplicación del módulo

---

# Fase 4.4 — Autenticación base

Se implementó la base de autenticación del sistema.

## Componentes

### Gestor de contraseñas

Archivo:

```text
nucleo/infraestructura/seguridad/autenticacion/gestor_contrasenas.py
```

### Funciones principales

* generar hash seguro con PBKDF2-SHA256
* verificar contraseñas contra hash almacenado

### Gestor JWT

Archivo:

```text
nucleo/infraestructura/seguridad/autenticacion/gestor_jwt.py
```

### Funciones principales

* crear token de acceso
* validar firma del token
* validar expiración
* decodificar payload

### Comando adicional

* `ComandoIniciarSesion`

### DTO adicional

* `RespuestaTokenDTO`

### Resultado de esta subfase

El módulo quedó preparado para autenticar usuarios y emitir JWT funcionales.

---

# Fase 4.5 — API FastAPI de identidad_acceso

Se implementaron dependencias, esquemas y rutas HTTP del módulo.

## Dependencias

Archivo:

```text
nucleo/interfaz/api/v1/identidad_acceso/dependencias/dependencias_identidad.py
```

Responsabilidad:

* construir `ServicioAplicacionIdentidad`
* inyectar repositorios y dependencias de seguridad

## Esquemas de petición

* `PeticionCrearUsuario`
* `PeticionAsignarRol`
* `PeticionIniciarSesion`
* `PeticionVincularUsuarioTenant`
* `PeticionVincularUsuarioEmpresa`

## Esquemas de respuesta

* `RespuestaUsuario`
* `RespuestaRol`
* `RespuestaPermiso`
* `RespuestaToken`
* `RespuestaMembresiaTenant`
* `RespuestaMembresiaEmpresa`

## Rutas implementadas

### Usuarios

* `POST /identidad-acceso/usuarios`
* `GET /identidad-acceso/usuarios/{usuario_id}`
* `GET /identidad-acceso/usuarios?tenant_id=...`

### Roles

* `POST /identidad-acceso/roles`
* `GET /identidad-acceso/roles?tenant_id=...`

### Permisos

* `GET /identidad-acceso/permisos`

### Autenticación

* `POST /identidad-acceso/autenticacion/iniciar-sesion`

### Membresías

* `POST /identidad-acceso/membresias/tenant`
* `POST /identidad-acceso/membresias/empresa`

---

## Integración con `app.py`

Se actualizó la aplicación principal para incluir los routers de `identidad_acceso` junto con los de `organizacion`.

### Archivo

```text
nucleo/interfaz/api/app.py
```

### Routers agregados

* `enrutador_usuarios`
* `enrutador_roles`
* `enrutador_permisos`
* `enrutador_autenticacion`
* `enrutador_membresias`

---

## Flujo funcional esperado de la fase

La fase 4 deja preparado este flujo:

```text
crear rol
crear usuario
iniciar sesión
obtener token JWT
vincular usuario al tenant
vincular usuario a la empresa
consultar roles, usuarios y permisos
```

---

## Validaciones técnicas realizadas

Hasta el cierre de esta fase, se validó repetidamente:

### 1. Salud de la API

Se confirmó que el endpoint:

```text
GET /test-db
```

sigue respondiendo correctamente con conexión viva a PostgreSQL.

### 2. Integridad de imports

Cada subfase fue validada comprobando que la aplicación siguiera levantando sin errores.

### 3. Integración con organización

El módulo `identidad_acceso` fue construido usando:

* `RepositorioTenant`
* `RepositorioEmpresa`

Esto asegura coherencia entre organización e identidad.

---

## Resultado técnico de la fase

Con la Fase 4 implementada, el ERP SaaS ya cuenta con:

* base de usuarios multiempresa
* base de roles por tenant
* catálogo de permisos consultable
* membresías tenant y empresa
* hash seguro de contraseñas
* login con JWT
* API HTTP para identidad y acceso

Esto convierte al proyecto en un sistema ya preparado para operación autenticada.

---

## Archivos principales tocados

### Dominio

```text
nucleo/dominio/identidad_acceso/repositorios/repositorio_usuario.py
nucleo/dominio/identidad_acceso/repositorios/repositorio_rol.py
nucleo/dominio/identidad_acceso/repositorios/repositorio_permiso.py
nucleo/dominio/identidad_acceso/repositorios/repositorio_membresia_tenant.py
nucleo/dominio/identidad_acceso/repositorios/repositorio_membresia_empresa.py
```

### Aplicación

```text
nucleo/aplicacion/identidad_acceso/dto/usuario_dto.py
nucleo/aplicacion/identidad_acceso/dto/rol_dto.py
nucleo/aplicacion/identidad_acceso/dto/permiso_dto.py
nucleo/aplicacion/identidad_acceso/dto/membresia_tenant_dto.py
nucleo/aplicacion/identidad_acceso/dto/membresia_empresa_dto.py
nucleo/aplicacion/identidad_acceso/dto/respuesta_token.py
nucleo/aplicacion/identidad_acceso/comandos/comando_crear_usuario.py
nucleo/aplicacion/identidad_acceso/comandos/comando_asignar_rol.py
nucleo/aplicacion/identidad_acceso/comandos/comando_asignar_permiso.py
nucleo/aplicacion/identidad_acceso/comandos/comando_iniciar_sesion.py
nucleo/aplicacion/identidad_acceso/servicios/servicio_aplicacion_identidad.py
nucleo/aplicacion/identidad_acceso/casos_uso/crear_usuario.py
nucleo/aplicacion/identidad_acceso/casos_uso/autenticar_usuario.py
nucleo/aplicacion/identidad_acceso/casos_uso/asignar_rol.py
nucleo/aplicacion/identidad_acceso/casos_uso/asignar_permiso.py
nucleo/aplicacion/identidad_acceso/casos_uso/vincular_usuario_tenant.py
nucleo/aplicacion/identidad_acceso/casos_uso/vincular_usuario_empresa.py
nucleo/aplicacion/identidad_acceso/consultas/consulta_obtener_usuario.py
nucleo/aplicacion/identidad_acceso/consultas/consulta_listar_roles.py
nucleo/aplicacion/identidad_acceso/consultas/consulta_listar_permisos.py
nucleo/aplicacion/identidad_acceso/consultas/consulta_listar_usuarios.py
```

### Infraestructura

```text
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_usuario.py
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_rol.py
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_permiso.py
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_rol_permiso.py
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_membresia_tenant.py
nucleo/infraestructura/db/modelos/identidad_acceso/modelo_membresia_empresa.py
nucleo/infraestructura/db/repositorios/identidad_acceso/repositorio_usuario_sqlalchemy.py
nucleo/infraestructura/db/repositorios/identidad_acceso/repositorio_rol_sqlalchemy.py
nucleo/infraestructura/db/repositorios/identidad_acceso/repositorio_permiso_sqlalchemy.py
nucleo/infraestructura/db/repositorios/identidad_acceso/repositorio_membresia_tenant_sqlalchemy.py
nucleo/infraestructura/db/repositorios/identidad_acceso/repositorio_membresia_empresa_sqlalchemy.py
nucleo/infraestructura/seguridad/autenticacion/gestor_contrasenas.py
nucleo/infraestructura/seguridad/autenticacion/gestor_jwt.py
```

### Interfaz

```text
nucleo/interfaz/api/v1/identidad_acceso/dependencias/dependencias_identidad.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/peticion_crear_usuario.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/peticion_asignar_rol.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/peticion_iniciar_sesion.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/peticion_vincular_usuario_tenant.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/peticion_vincular_usuario_empresa.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_usuario.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_rol.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_permiso.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_token.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_membresia_tenant.py
nucleo/interfaz/api/v1/identidad_acceso/esquemas/respuesta_membresia_empresa.py
nucleo/interfaz/api/v1/identidad_acceso/rutas/rutas_usuarios.py
nucleo/interfaz/api/v1/identidad_acceso/rutas/rutas_roles.py
nucleo/interfaz/api/v1/identidad_acceso/rutas/rutas_permisos.py
nucleo/interfaz/api/v1/identidad_acceso/rutas/rutas_autenticacion.py
nucleo/interfaz/api/v1/identidad_acceso/rutas/rutas_membresias.py
nucleo/interfaz/api/app.py
```

---

## Problemas encontrados durante la fase

### Integración incremental

El módulo fue creciendo por capas, por lo que fue necesario validar continuamente que `/test-db` siguiera funcionando tras cada cambio.

### Riesgo de inconsistencias entre organización e identidad

Se resolvió integrando repositorios de `tenant` y `empresa` dentro del servicio de identidad, para validar referencias antes de crear usuarios o membresías.

### Complejidad de la autenticación

Se decidió implementar primero una autenticación base con:

* hash PBKDF2-SHA256
* JWT firmado con HMAC SHA256

Esto deja una base sólida sin introducir todavía complejidades como refresh tokens o revocación centralizada.

---

## Lecciones técnicas de la fase

* la arquitectura soporta bien módulos transversales como identidad
* la separación entre aplicación y seguridad ayuda a mantener el diseño limpio
* el uso de DTO evita acoplamiento innecesario con modelos ORM
* JWT ya permite comenzar pruebas reales de login
* el sistema ya tiene base para autorización futura por endpoint y por contexto

---

## Criterio de cierre de la fase

La Fase 4 se considera cerrada cuando se valida exitosamente el siguiente flujo:

1. crear un rol
2. crear un usuario
3. iniciar sesión
4. obtener token JWT
5. listar permisos
6. vincular el usuario al tenant
7. vincular el usuario a la empresa
8. consultar el usuario y sus listados

Si el código ya está escrito pero esa prueba no se ha ejecutado todavía, la fase está **implementada pero pendiente de validación funcional final**.

---

## Qué sigue después de esta fase

La siguiente fase natural del proyecto es:

# Fase 5 — Módulo `catalogo`

## Objetivo

Construir el catálogo maestro del ERP, incluyendo:

* categorías
* marcas
* productos
* presentaciones
* precios base
* estados del producto

## Razón

No conviene saltar directamente a inventario o ventas sin tener primero definido el catálogo de productos.

---

## Recomendación de cierre operativo

Cuando termines la validación funcional completa de esta fase:

```bash
git add .
git commit -m "implementa y valida modulo identidad_acceso"
git push
```

---

## Resumen ejecutivo

La Fase 4 agregó la base de seguridad del ERP SaaS:

* usuarios
* roles
* permisos
* membresías
* autenticación
* JWT
* API de identidad y acceso

Con esta fase, el sistema deja de ser solo estructural y comienza a convertirse en una plataforma operable por usuarios autenticados dentro de un tenant y una empresa.

````

---

## Comando PowerShell para crear el archivo

```powershell
@'
[PEGA AQUI EL CONTENIDO DEL README]
'@ | Set-Content -Path .\documentacion\03-arquitectura\README_FASE_4_IDENTIDAD_ACCESO.md -Encoding UTF8
````

## Comando para crear solo el archivo vacío

```powershell
New-Item -ItemType File -Path .\documentacion\03-arquitectura\README_FASE_4_IDENTIDAD_ACCESO.md -Force
```

Si quieres, el siguiente te lo dejo como **README de Fase 5 — catálogo** antes de empezar a construirla.
