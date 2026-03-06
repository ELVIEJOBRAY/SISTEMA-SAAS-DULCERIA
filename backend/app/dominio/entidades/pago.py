# ==========================================================
# ENTIDAD PAGO
# SISTEMA DE TRANSACCIONES FINANCIERAS DEL NEGOCIO
# ==========================================================
#
# ESTA CLASE REPRESENTA UN PAGO ASOCIADO A UNA VENTA.
# LOS PAGOS SON CRUCIALES EN EL SISTEMA FINANCIERO,
# YA QUE CONFIRMAN EL INGRESO Y PERMITEN EL CONTROL
# DE ESTADOS FINANCIEROS DEL NEGOCIO.
#
# UN PAGO PUEDE TENER DIFERENTES MÉTODOS Y ESTADOS,
# Y PUEDE SER RECHAZADO, REEMBOLSADO O ANULADO.
#
# ==========================================================

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from enum import Enum


# ==========================================================
# ENUM MÉTODOS DE PAGO
# ==========================================================
# DEFINE LOS MÉTODOS QUE EL SISTEMA PERMITE PARA PAGOS
# ==========================================================
class MetodoPago(Enum):
    EFECTIVO = "efectivo"
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA = "transferencia"
    OTRO = "otro"


# ==========================================================
# ENUM ESTADOS DEL PAGO
# ==========================================================
# DEFINE LOS ESTADOS QUE UN PAGO PUEDE TENER DURANTE SU CICLO
# ==========================================================
class EstadoPago(Enum):
    PENDIENTE = "pendiente"       # Pago creado pero no procesado
    COMPLETADO = "completado"     # Pago recibido correctamente
    RECHAZADO = "rechazado"       # Pago denegado o fallido
    REEMBOLSADO = "reembolsado"   # Pago devuelto al cliente
    ANULADO = "anulado"           # Pago cancelado antes de completarse


# ==========================================================
# ENTIDAD PAGO
# ==========================================================
class Pago:

    # ======================================================
    # CONSTRUCTOR DEL PAGO
    # ======================================================
    # SE EJECUTA CUANDO SE CREA UN PAGO PARA UNA VENTA.
    # SU RESPONSABILIDAD INCLUYE:
    #
    # 1 VALIDAR LOS DATOS DE ENTRADA
    # 2 ASIGNAR ATRIBUTOS DEL OBJETO
    # 3 ASEGURAR QUE EL PAGO SEA VÁLIDO
    # ======================================================

    def __init__(
        self,
        id: Optional[int],
        venta_id: int,
        monto: float,
        metodo: MetodoPago,
        estado: EstadoPago = EstadoPago.PENDIENTE,
        referencia: Optional[str] = None,
        fecha_pago: Optional[datetime] = None,
        notas: Optional[str] = None
    ) -> None:

        # ==================================================
        # VALIDACIONES
        # ==================================================
        # VALIDAMOS QUE LA VENTA EXISTA Y EL MONTO SEA CORRECTO

        if venta_id <= 0:
            raise ValueError("ID DE VENTA INVÁLIDO")
        self.venta_id = venta_id

        if monto <= 0:
            raise ValueError("EL MONTO DEL PAGO DEBE SER MAYOR A CERO")
        self.monto = monto

        # EL MÉTODO DE PAGO YA ESTÁ TIPADO COMO MetodoPago
        self.metodo = metodo

        # EL ESTADO DE PAGO YA ESTÁ TIPADO COMO EstadoPago
        self.estado = estado

        # ==================================================
        # ASIGNACIÓN DE ATRIBUTOS ADICIONALES
        # ==================================================
        self.id = id
        self.referencia = referencia
        self.fecha_pago = fecha_pago or datetime.now(timezone.utc)  # Si no se pasa fecha, se asigna la actual
        self.notas = notas  # Comentarios adicionales o motivo de rechazo/reembolso

    # ======================================================
    # MÉTODO COMPLETAR PAGO
    # ======================================================
    # CAMBIA EL ESTADO DEL PAGO A COMPLETADO
    # SOLO SI ESTÁ PENDIENTE
    # ======================================================
    def completar(self, referencia: Optional[str] = None) -> None:

        if self.estado != EstadoPago.PENDIENTE:
            raise ValueError(
                f"NO SE PUEDE COMPLETAR UN PAGO EN ESTADO {self.estado.value}"
            )

        self.estado = EstadoPago.COMPLETADO

        if referencia:
            self.referencia = referencia

    # ======================================================
    # MÉTODO RECHAZAR PAGO
    # ======================================================
    # CAMBIA EL ESTADO DEL PAGO A RECHAZADO
    # SOLO SI ESTÁ PENDIENTE
    # ======================================================
    def rechazar(self, motivo: Optional[str] = None) -> None:

        if self.estado != EstadoPago.PENDIENTE:
            raise ValueError(
                f"NO SE PUEDE RECHAZAR UN PAGO EN ESTADO {self.estado.value}"
            )

        self.estado = EstadoPago.RECHAZADO

        if motivo:
            self.notas = motivo

    # ======================================================
    # MÉTODO REEMBOLSAR PAGO
    # ======================================================
    # CAMBIA EL ESTADO DEL PAGO A REEMBOLSADO
    # SOLO SI ESTÁ COMPLETADO
    # ======================================================
    def reembolsar(self, motivo: Optional[str] = None) -> None:

        if self.estado != EstadoPago.COMPLETADO:
            raise ValueError(
                f"NO SE PUEDE REEMBOLSAR UN PAGO EN ESTADO {self.estado.value}"
            )

        self.estado = EstadoPago.REEMBOLSADO

        if motivo:
            self.notas = motivo

    # ======================================================
    # MÉTODO ANULAR PAGO
    # ======================================================
    # CAMBIA EL ESTADO DEL PAGO A ANULADO
    # SOLO SI ESTÁ PENDIENTE
    # ======================================================
    def anular(self) -> None:

        if self.estado != EstadoPago.PENDIENTE:
            raise ValueError(
                f"NO SE PUEDE ANULAR UN PAGO EN ESTADO {self.estado.value}"
            )

        self.estado = EstadoPago.ANULADO

    # ======================================================
    # MÉTODOS DE CONSULTA DE ESTADO
    # ======================================================
    # PERMITEN VERIFICAR RÁPIDAMENTE EL ESTADO ACTUAL DEL PAGO
    # ======================================================
    def esta_completado(self) -> bool:
        return self.estado == EstadoPago.COMPLETADO

    def esta_pendiente(self) -> bool:
        return self.estado == EstadoPago.PENDIENTE

    def esta_rechazado(self) -> bool:
        return self.estado == EstadoPago.RECHAZADO

    def esta_reembolsado(self) -> bool:
        return self.estado == EstadoPago.REEMBOLSADO

    # ======================================================
    # SERIALIZACIÓN
    # ======================================================
    # CONVIERTE EL PAGO A DICCIONARIO
    # PARA RESPUESTAS API O JSON
    # ======================================================
    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "venta_id": self.venta_id,
            "monto": self.monto,
            "metodo": self.metodo.value,
            "estado": self.estado.value,
            "referencia": self.referencia,
            "fecha_pago": self.fecha_pago.isoformat(),
            "notas": self.notas
        }

    # ======================================================
    # REPRESENTACIÓN DEL OBJETO
    # ======================================================
    # DEFINE CÓMO SE IMPRIME EL OBJETO EN CONSOLA
    # MUY ÚTIL PARA DEPURACIÓN
    # ======================================================
    def __repr__(self) -> str:

        return (
            f"<Pago "
            f"id={self.id} "
            f"venta_id={self.venta_id} "
            f"monto={self.monto} "
            f"metodo={self.metodo.value} "
            f"estado={self.estado.value}>"
        )