# TESIS TÉCNICA — SISTEMA-SAAS-DULCERIA
## Formato README

## 1. Título

**Diseño e implementación de una base arquitectónica limpia para un ERP SaaS multiempresa orientado al sector de dulcerías**

---

## 2. Planteamiento

El sector minorista de dulcerías suele operar con herramientas fragmentadas o de baja madurez técnica, especialmente cuando se requiere controlar catálogo, inventario, usuarios, sucursales, bodegas y crecimiento multiempresa dentro de una misma plataforma.

El problema se vuelve más complejo cuando la solución pretende operar como **software como servicio (SaaS)**, debido a la necesidad de aislar datos por tenant y, al mismo tiempo, permitir múltiples empresas y unidades operativas dentro de cada cliente.

Frente a este contexto, **SISTEMA-SAAS-DULCERIA** propone una base arquitectónica capaz de soportar:

- multi-tenancy
- multiempresa
- modularidad por dominios
- escalabilidad técnica progresiva
- separación limpia de responsabilidades

---

## 3. Hipótesis técnica

Es posible construir una base arquitectónica sólida para un ERP SaaS multiempresa orientado al sector de dulcerías mediante el uso de:

- arquitectura limpia
- diseño guiado por dominio (DDD)
- monolito modular
- separación por capas
- políticas tempranas de seguridad y contexto multi-tenant

Esta combinación permite reducir acoplamiento, mejorar mantenibilidad y preparar la solución para evolución funcional y comercial futura.

---

## 4. Objetivo general

Diseñar e implementar la base arquitectónica de un ERP SaaS multiempresa para dulcerías, con separación limpia por capas, soporte multi-tenant desde la base y módulos funcionales iniciales para organización, identidad y acceso, catálogo e inventario.

---

## 5. Objetivos específicos

- definir una arquitectura modular alineada con DDD
- estructurar el sistema en capas de dominio, aplicación, infraestructura e interfaz
- modelar el contexto organizacional multiempresa
- implementar identidad y acceso con control base de tenant
- construir el catálogo maestro de productos
- implementar operaciones básicas de inventario y trazabilidad
- endurecer la API con una política homogénea de autenticación y contexto
- dejar la plataforma preparada para evolución hacia ventas, compras y servicios SaaS comerciales

---

## 6. Marco arquitectónico

### 6.1 Estilo adoptado

El sistema adopta un **monolito modular**, decisión adecuada para una fase temprana del producto porque permite:

- menor complejidad operativa inicial
- consistencia transaccional más simple
- integración directa entre bounded contexts
- menor costo de despliegue y debugging

### 6.2 Principios aplicados

- arquitectura limpia
- DDD
- separación por capas
- orientación a casos de uso
- independencia relativa del dominio frente a infraestructura

### 6.3 Capas del sistema

#### Dominio
Contiene entidades, objetos de valor, eventos, excepciones, repositorios abstractos y servicios de dominio.

#### Aplicación
Contiene casos de uso, comandos, consultas, DTOs y servicios de aplicación.

#### Infraestructura
Contiene persistencia, modelos ORM, repositorios concretos, mapeadores, mecanismos de seguridad y servicios externos.

#### Interfaz
Contiene la API FastAPI, sus dependencias, rutas y esquemas.

---

## 7. Estructura del sistema

```text
SISTEMA-SAAS-DULCERIA/
├── base_datos/
├── cliente/
├── configuracion/
├── documentacion/
├── infraestructura/
├── nucleo/
│   ├── aplicacion/
│   ├── dominio/
│   ├── infraestructura/
│   └── interfaz/
├── plataforma/
├── pruebas/
├── scripts/
└── servicios/
```

La carpeta `nucleo` concentra la implementación principal. El resto del repositorio articula documentación, infraestructura, pruebas, clientes y expansión futura.

---

## 8. Bounded contexts modelados

### Organización
Representa la estructura operacional del tenant:

- tenant
- empresa
- sucursal
- bodega

### Identidad y acceso
Representa el gobierno de usuarios:

- usuarios
- roles
- permisos
- membresías
- autenticación

### Catálogo
Representa el catálogo maestro:

- categorías
- marcas
- productos
- presentaciones

### Inventario
Representa el control de existencias:

- entradas
- salidas
- ajustes
- consultas
- kardex

### Plataforma SaaS
Previsto para etapas posteriores:

- cuentas
- planes
- suscripciones
- facturación SaaS

---

## 9. Implementación lograda

### 9.1 Organización
Se implementó la base de estructura multiempresa con rutas para empresas, sucursales y bodegas.

### 9.2 Identidad y acceso
Se implementaron rutas para usuarios, roles, permisos y membresías, además de soporte de seguridad mediante JWT y resolución del usuario actual.

### 9.3 Catálogo
Se implementó el núcleo de productos, incluyendo rutas para productos y soporte documental previo para categorías, marcas y presentaciones.

### 9.4 Inventario
Se implementaron rutas para entradas, salidas, ajustes y consultas, incluyendo kardex por producto y presentación.

---

## 10. Aporte principal de la fase de estabilización

Un aporte técnico central del proyecto fue la construcción de una política homogénea de seguridad de borde en la API.

### Se logró:

- dependencia compartida de seguridad
- bearer token para endpoints privados
- decodificación central de JWT
- resolución del usuario actual
- validación de usuario activo
- validación básica de tenant
- sustitución de `usuario_id` del cliente por el contexto autenticado en inventario

### Valor técnico

Esto permitió pasar de una API funcional pero heterogénea a una API con mayor coherencia de acceso y mejor preparación para aislamiento multi-tenant.

---

## 11. Hallazgos y lecciones aprendidas

### 11.1 La estructura no equivale a funcionalidad completa

El repositorio presenta una estructura rica y ambiciosa, pero el trabajo de auditoría mostró que no todos los módulos tienen la misma madurez funcional.

### 11.2 La interfaz no debe exponer lo que la aplicación no soporta

El caso de `bodegas` mostró que un router no debe inventar operaciones que aún no existen como casos de uso en la capa de aplicación.

### 11.3 La seguridad debe resolverse temprano

Endurecer la API antes de seguir agregando módulos resultó ser una decisión correcta porque reduce riesgo y mejora la gobernabilidad del sistema.

### 11.4 El multi-tenant no se resuelve solo con un campo `tenant_id`

El verdadero aislamiento requiere validar relaciones estructurales completas entre entidades, no solo comparar un valor de entrada con un claim del token.

---

## 12. Limitaciones actuales

### Técnicas

- persistencia y operaciones aún no son homogéneas en todos los módulos
- el frontend no está consolidado con el mismo nivel que el backend
- faltan pruebas automatizadas robustas
- el `tenant_id` aún llega desde el cliente en varios contratos

### Funcionales

- ventas no está cerrada
- compras no está cerrada
- clientes y proveedores no están consolidados
- reportes aún no tienen cierre funcional verificable
- plataforma SaaS comercial sigue en etapa estructural

---

## 13. Riesgos identificados

- fuga de contexto multi-tenant si no se eliminan pronto los payloads sensibles del cliente
- crecimiento desigual entre módulos
- ilusión de completitud por exceso de estructura documental o carpetas vacías
- deuda técnica si se agregan ventas y compras sin cerrar primero la consolidación del contexto

---

## 14. Valor académico y profesional del proyecto

El proyecto tiene valor académico porque demuestra:

- aplicación de arquitectura limpia
- aplicación de DDD
- modelado multiempresa y multi-tenant
- separación disciplinada de capas
- criterio técnico al alinear rutas con casos de uso reales
- documentación y auditoría del avance

Tiene también valor profesional porque representa una base viable para un ERP SaaS sectorial con potencial de evolución comercial.

---

## 15. Estado consolidado del proyecto

### Completado a nivel base

- arquitectura general
- bounded contexts principales
- organización base
- identidad y acceso base
- catálogo base
- inventario base
- seguridad de borde en la API

### Pendiente para madurez superior

- eliminación de `tenant_id` del cliente
- validaciones relacionales profundas
- pruebas de integración y seguridad
- integración completa de clientes front
- ventas, compras, reportes, clientes y proveedores
- operación productiva y despliegue serio

---

## 16. Propuesta de siguiente fase

La siguiente fase correcta no es abrir más módulos, sino consolidar el contexto multi-tenant.

### Propuesta

1. derivar contexto exclusivamente desde JWT
2. eliminar `tenant_id` de payloads autenticados
3. validar pertenencia entre tenant, empresa, sucursal, bodega, producto y presentación
4. automatizar pruebas de integración
5. luego pasar a ventas y compras

---

## 17. Conclusión técnica

**SISTEMA-SAAS-DULCERIA** demuestra que es posible construir una base arquitectónica consistente para un ERP SaaS multiempresa orientado al sector de dulcerías mediante una combinación de arquitectura limpia, DDD y monolito modular.

El sistema aún no está terminado, pero su base ya es suficientemente seria para sostener crecimiento funcional real.

### Conclusión final

El mayor mérito actual del proyecto no es haber cerrado todo el producto, sino haber creado una plataforma técnicamente coherente, con bounded contexts definidos, API funcional y una primera política real de seguridad multi-tenant.

Dicho de forma sintética:

> el proyecto ya es una base de ERP SaaS defendible técnica y académicamente, pero su siguiente reto crítico es consolidar el aislamiento multi-tenant y cerrar funcionalmente los módulos comerciales pendientes.

---

## 18. Cierre

Este proyecto puede presentarse como una **tesis técnica de base arquitectónica**, orientada al diseño y estabilización del núcleo de un ERP SaaS multiempresa, con potencial de continuación hacia una segunda etapa centrada en operaciones comerciales completas y explotación de producto.

# SISTEMA-SAAS-DULCERIA
## README oficial v1

ERP SaaS multiempresa para dulcerías, orientado a la gestión de organización empresarial, identidad y acceso, catálogo, inventario y futura expansión hacia ventas, compras, reportes y servicios SaaS comerciales.

---

## 1. Resumen ejecutivo

**SISTEMA-SAAS-DULCERIA** es una plataforma ERP SaaS en construcción, diseñada con enfoque **multi-tenant** y **multiempresa**, para permitir que distintos clientes operen dentro de una misma solución con aislamiento lógico de datos por tenant y segmentación operativa por empresa, sucursal y bodega.

En su estado actual, el proyecto ya cuenta con una **base arquitectónica madura**: separación por capas, bounded contexts principales, estructura documental amplia, base de infraestructura prevista y una API FastAPI con rutas funcionales para organización, identidad y acceso, catálogo e inventario.

El sistema está siendo desarrollado bajo un enfoque de **arquitectura limpia**, **DDD (Domain-Driven Design)** y **monolito modular preparado para evolución futura**.

---

## 2. Estado actual del proyecto

- **Versión actual:** v1
- **Estado:** en desarrollo
- **Madurez actual:** base arquitectónica y backend núcleo funcional
- **Enfoque actual:** consolidación del núcleo multiempresa, refuerzo de seguridad multi-tenant y estabilización de la capa HTTP

### Dictamen general

El proyecto **no está terminado** ni listo para producción, pero **sí ha superado la fase de maqueta o estructura vacía**. Actualmente dispone de una base técnica consistente para continuar con el desarrollo funcional del ERP.

---

## 3. Propósito del sistema

Este proyecto tiene como objetivo construir un **ERP SaaS multiempresa** orientado inicialmente al sector de dulcerías, permitiendo que múltiples clientes utilicen la misma plataforma con aislamiento de datos por tenant y soporte para múltiples empresas, sucursales y bodegas dentro de un mismo entorno SaaS.

La solución está planteada para evolucionar desde un núcleo modular limpio hacia una plataforma empresarial escalable, mantenible y comercializable.

---

## 4. Objetivos principales

- soportar múltiples tenants dentro del mismo sistema SaaS
- permitir múltiples empresas por tenant
- gestionar sucursales y bodegas
- controlar usuarios, roles, permisos y membresías por contexto
- administrar catálogo de productos y presentaciones
- controlar inventario y trazabilidad operativa
- preparar el sistema para ventas, compras, reportes y POS
- dejar lista la base para planes, suscripciones y facturación SaaS

---

## 5. Principios arquitectónicos

La solución se construye bajo los siguientes principios:

- arquitectura limpia
- diseño guiado por dominio (DDD)
- monolito modular preparado para evolución futura
- separación clara entre dominio, aplicación, infraestructura e interfaz
- soporte multiempresa y multi-tenant desde la base
- orientación a crecimiento controlado antes de fragmentación en microservicios

---

## 6. Estructura general del repositorio

```text
SISTEMA-SAAS-DULCERIA/
├── .github/
├── base_datos/
├── cliente/
│   ├── movil/
│   ├── pos/
│   └── web/
├── configuracion/
├── documentacion/
├── infraestructura/
├── nucleo/
│   ├── aplicacion/
│   ├── dominio/
│   ├── infraestructura/
│   └── interfaz/
├── plataforma/
├── pruebas/
├── scripts/
└── servicios/
```

### Lectura de alto nivel

- `nucleo/`: núcleo del sistema con la implementación por capas
- `cliente/`: canales cliente web, móvil y POS
- `infraestructura/`: activos de despliegue, monitoreo, red, seguridad y cloud
- `base_datos/`: esquemas, migraciones, semillas y respaldos
- `plataforma/`: proyección de servicios administrativos y SaaS comercial
- `servicios/`: dominios previstos para evolución o separación futura
- `documentacion/`: soporte técnico, requisitos, arquitectura, operación y auditoría
- `pruebas/`: pruebas unitarias, integración y e2e

---

## 7. Arquitectura interna del núcleo

La carpeta `nucleo` representa el corazón del sistema y sigue una separación por capas alineada con arquitectura limpia.

### 7.1 Dominio

Ubicado en `nucleo/dominio`, contiene elementos del modelo de negocio:

- entidades
- eventos
- excepciones
- objetos de valor
- repositorios abstractos
- servicios de dominio

### 7.2 Aplicación

Ubicado en `nucleo/aplicacion`, contiene:

- casos de uso
- comandos
- consultas
- DTOs
- servicios de aplicación

### 7.3 Infraestructura

Ubicado en `nucleo/infraestructura`, contiene:

- conexión y persistencia de base de datos
- modelos ORM
- mapeadores
- repositorios SQLAlchemy
- seguridad (autenticación/autorización)
- servicios externos

### 7.4 Interfaz

Ubicado en `nucleo/interfaz/api`, expone la API pública del sistema:

- dependencias comunes
- rutas por módulo
- esquemas de petición y respuesta
- ensamblaje principal de FastAPI

---

## 8. Módulos funcionales actualmente identificados

El sistema está organizado por bounded contexts principales:

### 8.1 Organización

Responsable de:

- tenants
- empresas
- sucursales
- bodegas

### 8.2 Identidad y acceso

Responsable de:

- usuarios
- roles
- permisos
- membresías por tenant y empresa
- autenticación JWT

### 8.3 Catálogo

Responsable de:

- categorías
- marcas
- productos
- presentaciones

### 8.4 Inventario

Responsable de:

- entradas
- salidas
- ajustes
- inventario por bodega
- kardex por producto y presentación

### 8.5 Plataforma SaaS

Definido a nivel estructural para futura evolución:

- cuentas
- planes
- suscripciones
- facturación SaaS

### 8.6 Servicios previstos

Se observan estructuras preparadas para:

- analítica
- autenticación
- clientes
- compras
- empleados
- facturación
- inventario
- productos
- proveedores
- reportes
- ventas

Estas carpetas representan una intención clara de escalamiento funcional, pero no implican por sí mismas madurez equivalente en todos los módulos.

---

## 9. Estado funcional confirmado del backend

La aplicación FastAPI ya integra rutas funcionales para los siguientes módulos:

- organización
- identidad y acceso
- catálogo
- inventario

Además, en la fase más reciente se consolidó una política de seguridad de borde basada en:

- dependencia compartida para autenticación
- resolución del usuario actual
- validación básica de tenant en el entrypoint
- sustitución del `usuario_id` enviado por cliente por el del contexto autenticado en operaciones sensibles

### Componentes de seguridad reforzados

Se consolidó el archivo:

```text
nucleo/interfaz/api/dependencias/seguridad.py
```

Y se endurecieron rutas de:

- `rutas_productos.py`
- `rutas_usuarios.py`
- `rutas_roles.py`
- `rutas_permisos.py`
- `rutas_membresias.py`
- `rutas_entradas_inventario.py`
- `rutas_salidas_inventario.py`
- `rutas_ajustes_inventario.py`
- `rutas_consultas_inventario.py`
- `rutas_empresas.py`
- `rutas_sucursales.py`
- `rutas_bodegas.py`

---

## 10. Seguridad actual de la API

### Lo que ya se logró

- autenticación centralizada con bearer token
- resolución del usuario autenticado actual desde JWT
- validación de usuario activo
- validación básica de coherencia entre `tenant_id` del token y del usuario
- validación de `tenant_id` en múltiples endpoints privados
- mejor trazabilidad de usuario en movimientos de inventario

### Lo que aún falta

- eliminar `tenant_id` del body y query en endpoints autenticados
- derivar el contexto siempre desde `usuario_actual`
- validar pertenencia estructural entre tenant, empresa, sucursal, bodega, producto y presentación
- autorización basada en permisos/roles más fina

---

## 11. Estado del frontend

La estructura del cliente está prevista en tres canales:

- `cliente/web`
- `cliente/pos`
- `cliente/movil`

Sin embargo, el estado más maduro confirmado sigue estando en el backend. La presencia de estructura en cliente indica intención clara de producto multicanal, pero no equivale por sí sola a una integración funcional completa de todos los canales.

---

## 12. Infraestructura y operación

El repositorio contiene una base amplia para operación futura:

### Infraestructura prevista

- PostgreSQL
- Redis
- RabbitMQ
- Nginx
- Grafana
- Prometheus
- Loki
- Promtail
- Terraform para AWS
- políticas y secretos de seguridad
- pasarela API

### Lectura arquitectónica

El sistema no solo fue pensado como una aplicación monolítica simple, sino como una plataforma preparada para despliegue serio, observabilidad y evolución operativa.

---

## 13. Documentación del proyecto

La carpeta `documentacion` presenta una madurez documental poco común para un proyecto en desarrollo, con secciones para:

- investigación
- requisitos
- arquitectura
- diseño
- módulo catálogo
- operación
- auditoría

Esto fortalece la trazabilidad técnica y el potencial del proyecto como trabajo de grado, producto demostrable o base de portafolio profesional.

---

## 14. Fases consolidadas del proyecto

### Fases completadas o consolidadas en base arquitectónica

1. **Fundación arquitectónica**
   - estructura por capas
   - separación modular
   - lineamientos de arquitectura limpia y DDD

2. **Modelo organizacional base**
   - tenants
   - empresas
   - sucursales
   - bodegas

3. **Modelo de identidad y acceso base**
   - usuarios
   - roles
   - permisos
   - membresías

4. **Módulo catálogo base**
   - categorías
   - marcas
   - productos
   - presentaciones

5. **Módulo inventario base**
   - entradas
   - salidas
   - ajustes
   - consultas y kardex

6. **Fase de seguridad y estabilización de API**
   - dependencia transversal de seguridad
   - rutas privadas protegidas
   - refuerzo multi-tenant básico

### Fases en progreso

7. **Consolidación multi-tenant profunda**
   - eliminación de `tenant_id` del cliente
   - validaciones estructurales de pertenencia

8. **Maduración del frontend y canales cliente**
   - web
   - POS
   - móvil

9. **Pruebas automatizadas serias**
   - unitarias
   - integración
   - end to end

### Fases pendientes

10. **Ventas**
11. **Compras**
12. **Clientes**
13. **Proveedores**
14. **Reportes operativos y gerenciales**
15. **Plataforma SaaS comercial**
16. **Operación productiva y despliegue real**

---

## 15. Qué funciona hoy

### Confirmado

- el backend FastAPI arranca correctamente
- la documentación Swagger/OpenAPI está disponible
- el ensamblaje principal de la app integra módulos clave
- existe una primera capa de seguridad multi-tenant en rutas sensibles
- catálogo, identidad, organización e inventario tienen estructura operativa real

### No debe afirmarse todavía sin más evidencia

- que el sistema esté listo para producción
- que todas las rutas del frontend estén integradas realmente con backend
- que ventas, compras, reportes y POS estén cerrados funcionalmente
- que exista endurecimiento completo de aislamiento multi-tenant

---

## 16. Deuda técnica principal

### 16.1 Deuda de seguridad

- `tenant_id` aún llega desde el cliente en varios contratos
- falta validación de pertenencia entre agregados
- autorización fina por rol/permiso aún no está cerrada

### 16.2 Deuda de consistencia funcional

- algunos módulos tienen estructura más madura que otros
- hay carpetas de proyección futura sin el mismo nivel de implementación real

### 16.3 Deuda de pruebas

- faltan pruebas de autenticación y autorización
- faltan pruebas de integración multi-tenant
- faltan pruebas de inventario con trazabilidad

### 16.4 Deuda de producto

- ventas, compras, clientes, proveedores y reportes aún requieren consolidación

---

## 17. Recomendación de evolución

La siguiente fase técnicamente más rentable no es abrir nuevos módulos a ciegas, sino **consolidar el contexto multi-tenant**.

### Prioridades recomendadas

1. eliminar `tenant_id` del cliente en endpoints autenticados
2. derivar contexto exclusivamente desde JWT
3. reforzar validaciones estructurales de pertenencia
4. escribir pruebas de integración para rutas críticas
5. cerrar catálogo restante y endurecer organización
6. luego pasar a ventas y compras

---

## 18. Requisitos para ejecutar y trabajar el proyecto

### Backend

- Python 3.x
- FastAPI / Uvicorn
- SQLAlchemy
- base de datos PostgreSQL

### Infraestructura prevista

- Docker / contenedores
- Redis
- RabbitMQ
- Grafana / Prometheus
- Nginx

### Cliente

- stack web moderno con JavaScript
- estructura separada para web, POS y móvil

---

## 19. Conclusión oficial de la versión v1

**SISTEMA-SAAS-DULCERIA v1** representa una **base arquitectónica seria y funcional**, orientada a construir un ERP SaaS multiempresa para dulcerías.

En esta versión, el valor principal del proyecto no está en haber cerrado ya todo el producto, sino en haber establecido una plataforma técnicamente coherente para crecer de forma controlada.

### Conclusión ejecutiva

- sí existe una base funcional real
- sí existe una arquitectura defendible profesionalmente
- sí existe una orientación clara a producto empresarial
- todavía falta consolidación funcional y operativa antes de hablar de producción

En síntesis, la versión v1 debe entenderse como:

> una plataforma ERP SaaS multiempresa en construcción, con núcleo modular funcional, seguridad de borde en consolidación y base sólida para continuar hacia inventario maduro, ventas, compras y explotación comercial.



