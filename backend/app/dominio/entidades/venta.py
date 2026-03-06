# ==========================================================
# ENTIDAD VENTA
# SISTEMA CENTRAL DE TRANSACCIONES DEL NEGOCIO
# ==========================================================
#
# ESTA CLASE REPRESENTA UNA VENTA DENTRO DEL SISTEMA.
#
# UNA VENTA ES LA TRANSACCIÓN COMERCIAL DONDE UN CLIENTE
# ADQUIERE UNO O VARIOS PRODUCTOS O SERVICIOS.
#
# EN EL DOMINIO DEL NEGOCIO, LA VENTA ES CRÍTICA PORQUE:
#
# • GENERA INGRESOS
# • REGISTRA HISTORIAL DE CLIENTES
# • PERMITE CONTROLAR EL ESTADO DE LA TRANSACCIÓN
# • ACTUALIZA FECHAS DE CREACIÓN Y MODIFICACIÓN
#
# ESTE OBJETO CONTIENE:
#
# - VALIDACIONES DE DATOS
# - REGLAS DE NEGOCIO
# - ESTADO DE LA VENTA
# - COMPORTAMIENTO DE LA VENTA
# - SERIALIZACIÓN PARA APIs O JSON
#
# ==========================================================

from datetime import datetime, timezone
from typing import Optional, Dict, Any


class Venta:

    # ======================================================
    # CONSTANTES DE ESTADO
    # ======================================================
    # SE DEFINEN LOS ESTADOS PERMITIDOS DE LA VENTA COMO
    # CONSTANTES PARA EVITAR ERRORES DE ESCRITURA ("STRINGS MÁGICOS")
    # Y GARANTIZAR CONSISTENCIA EN EL SISTEMA.
    # ======================================================

    ESTADO_PENDIENTE = "pendiente"      # Venta iniciada pero no finalizada
    ESTADO_COMPLETADA = "completada"    # Venta finalizada correctamente
    ESTADO_CANCELADA = "cancelada"      # Venta anulada o cancelada

    # ======================================================
    # LISTA DE ESTADOS VÁLIDOS
    # ======================================================
    # DEFINIMOS UNA LISTA OFICIAL DE ESTADOS PERMITIDOS
    # PARA USO EN VALIDACIONES INTERNAS.
    # ======================================================

    ESTADOS_VALIDOS = [
        ESTADO_PENDIENTE,
        ESTADO_COMPLETADA,
        ESTADO_CANCELADA
    ]

    # ======================================================
    # CONSTRUCTOR DE LA VENTA
    # ======================================================
    # ESTE MÉTODO SE EJECUTA CUANDO SE CREA UNA VENTA.
    #
    # SU RESPONSABILIDAD ES:
    #
    # 1 VALIDAR LOS DATOS RECIBIDOS
    # 2 ASIGNAR ATRIBUTOS INICIALES
    # 3 GARANTIZAR QUE EL OBJETO VENTA SEA VÁLIDO
    # ======================================================

    def __init__(
        self,
        id: Optional[int],
        cliente_id: int,
        total: float,
        estado: str = ESTADO_PENDIENTE
    ) -> None:

        # ==================================================
        # VALIDACIONES
        # ==================================================

        # VALIDAR QUE EL CLIENTE EXISTE Y ES VÁLIDO
        self.cliente_id = self._validar_cliente(cliente_id)

        # VALIDAR QUE EL TOTAL ES CORRECTO
        self.total = self._validar_total(total)

        # VALIDAR QUE EL ESTADO SEA UNO DE LOS PERMITIDOS
        self.estado = self._validar_estado(estado)

        # ==================================================
        # ASIGNACIÓN DE ATRIBUTOS
        # ==================================================

        self.id = id  # ID de la venta, normalmente asignado por BD
        self.fecha_creacion = datetime.now(timezone.utc)  # Fecha de creación
        self.fecha_actualizacion = datetime.now(timezone.utc)  # Fecha de última modificación

    # ======================================================
    # VALIDACIÓN DEL CLIENTE
    # ======================================================
    # ESTE MÉTODO GARANTIZA QUE LA VENTA ESTÉ ASOCIADA
    # A UN CLIENTE VÁLIDO.
    #
    # SI EL ID DEL CLIENTE ES MENOR O IGUAL A CERO,
    # SE LANZA UNA EXCEPCIÓN.
    # ======================================================

    def _validar_cliente(self, cliente_id: int) -> int:
        """
        VALIDA QUE LA VENTA TENGA UN CLIENTE ASOCIADO.
        """

        if cliente_id <= 0:
            raise ValueError("ID DE CLIENTE INVÁLIDO")

        return cliente_id

    # ======================================================
    # VALIDACIÓN DEL TOTAL
    # ======================================================
    # ESTE MÉTODO GARANTIZA QUE EL TOTAL DE LA VENTA
    # NO SEA NEGATIVO.
    # ======================================================

    def _validar_total(self, total: float) -> float:

        if total < 0:
            raise ValueError("EL TOTAL DE LA VENTA NO PUEDE SER NEGATIVO")

        return total

    # ======================================================
    # VALIDACIÓN DEL ESTADO
    # ======================================================
    # ESTE MÉTODO VERIFICA QUE EL ESTADO DE LA VENTA
    # ESTÉ DENTRO DE LOS ESTADOS PERMITIDOS.
    # ======================================================

    def _validar_estado(self, estado: str) -> str:

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"ESTADO INVÁLIDO. ESTADOS PERMITIDOS: {self.ESTADOS_VALIDOS}"
            )

        return estado

    # ======================================================
    # COMPLETAR VENTA
    # ======================================================
    # ESTE MÉTODO CAMBIA EL ESTADO DE LA VENTA
    # A COMPLETADA.
    #
    # TAMBIÉN ACTUALIZA LA FECHA DE MODIFICACIÓN.
    # ======================================================

    def completar(self) -> None:

        self.estado = self.ESTADO_COMPLETADA
        self._registrar_actualizacion()

    # ======================================================
    # CANCELAR VENTA
    # ======================================================
    # ESTE MÉTODO CAMBIA EL ESTADO DE LA VENTA
    # A CANCELADA.
    #
    # TAMBIÉN ACTUALIZA LA FECHA DE MODIFICACIÓN.
    # ======================================================

    def cancelar(self) -> None:

        self.estado = self.ESTADO_CANCELADA
        self._registrar_actualizacion()

    # ======================================================
    # CONSULTAS DE ESTADO
    # ======================================================
    # MÉTODOS PARA VERIFICAR EL ESTADO ACTUAL DE LA VENTA.
    # ESTO FACILITA VALIDACIONES Y LOGICA DE NEGOCIO.
    # ======================================================

    def esta_completada(self) -> bool:
        return self.estado == self.ESTADO_COMPLETADA

    def esta_cancelada(self) -> bool:
        return self.estado == self.ESTADO_CANCELADA

    # ======================================================
    # REGISTRO DE ACTUALIZACIONES
    # ======================================================
    # ACTUALIZA LA FECHA DE MODIFICACIÓN CADA VEZ QUE
    # SE CAMBIA EL ESTADO DE LA VENTA.
    # ======================================================

    def _registrar_actualizacion(self) -> None:
        self.fecha_actualizacion = datetime.now(timezone.utc)

    # ======================================================
    # SERIALIZACIÓN
    # ======================================================
    # CONVIERTE LA VENTA A UN DICCIONARIO
    # PARA RESPUESTAS API O JSON.
    # ======================================================

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "total": self.total,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat()
        }

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    # DEFINE CÓMO SE IMPRIME EL OBJETO EN CONSOLA,
    # MUY ÚTIL PARA DEPURACIÓN.
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"<Venta "
            f"id={self.id} "
            f"cliente_id={self.cliente_id} "
            f"total={self.total} "
            f"estado='{self.estado}'>"
        )