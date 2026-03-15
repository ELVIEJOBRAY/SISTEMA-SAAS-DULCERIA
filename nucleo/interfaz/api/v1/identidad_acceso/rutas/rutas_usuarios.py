from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from nucleo.aplicacion.identidad_acceso.casos_uso.crear_usuario import CrearUsuario
from nucleo.aplicacion.identidad_acceso.comandos.comando_crear_usuario import ComandoCrearUsuario
from nucleo.aplicacion.identidad_acceso.consultas.consulta_listar_usuarios import ConsultaListarUsuarios
from nucleo.aplicacion.identidad_acceso.consultas.consulta_obtener_usuario import (
    ConsultaObtenerUsuario,
)
from nucleo.aplicacion.identidad_acceso.servicios.servicio_aplicacion_identidad import (
    ServicioAplicacionIdentidad,
)
from nucleo.interfaz.api.dependencias.seguridad import obtener_usuario_actual
from nucleo.interfaz.api.v1.identidad_acceso.dependencias.dependencias_identidad import (
    obtener_servicio_identidad,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.peticion_crear_usuario import (
    PeticionCrearUsuario,
)
from nucleo.interfaz.api.v1.identidad_acceso.esquemas.respuesta_usuario import RespuestaUsuario

enrutador_usuarios = APIRouter(prefix="/identidad-acceso/usuarios", tags=["Identidad - Usuarios"])


@enrutador_usuarios.post("", response_model=RespuestaUsuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    peticion: PeticionCrearUsuario,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(peticion.tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    caso_uso = CrearUsuario(servicio)
    comando = ComandoCrearUsuario(
        tenant_id=peticion.tenant_id,
        nombres=peticion.nombres,
        apellidos=peticion.apellidos,
        nombre_usuario=peticion.nombre_usuario,
        correo=peticion.correo,
        contrasena_hash="",
        esta_activo=peticion.esta_activo,
        es_superadministrador=peticion.es_superadministrador,
    )

    try:
        return caso_uso.ejecutar_con_contrasena(comando, peticion.contrasena)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@enrutador_usuarios.get("/{usuario_id}", response_model=RespuestaUsuario)
def obtener_usuario(
    usuario_id: UUID,
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    consulta = ConsultaObtenerUsuario(servicio)

    try:
        usuario = consulta.ejecutar(usuario_id)
        if str(usuario.tenant_id) != str(usuario_actual.tenant_id):
            raise HTTPException(status_code=403, detail="Tenant inválido")
        return usuario
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@enrutador_usuarios.get("", response_model=list[RespuestaUsuario])
def listar_usuarios(
    tenant_id: UUID = Query(...),
    usuario_actual=Depends(obtener_usuario_actual),
    servicio: ServicioAplicacionIdentidad = Depends(obtener_servicio_identidad),
):
    if str(tenant_id) != str(usuario_actual.tenant_id):
        raise HTTPException(status_code=403, detail="Tenant inválido")

    consulta = ConsultaListarUsuarios(servicio)
    return consulta.ejecutar(tenant_id)

