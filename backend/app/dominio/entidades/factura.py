# ============================================================
# IMPORTACIONES NECESARIAS PARA TIPADO FUERTE EN PRODUCCIÓN
# ============================================================

from __future__ import annotations

from typing import List, Optional
from dataclasses import dataclass
from decimal import Decimal


# ============================================================
# ENTIDAD: IMPUESTO
# REPRESENTA UN IMPUESTO APLICADO A UNA FACTURA
# ============================================================

@dataclass
class Impuesto:
    # --------------------------------------------------------
    # NOMBRE DEL IMPUESTO (EJEMPLO: "IVA", "ISR")
    # --------------------------------------------------------
    nombre: str

    # --------------------------------------------------------
    # TASA DEL IMPUESTO EN PORCENTAJE
    # EJEMPLO: Decimal("0.16") PARA UN 16%
    # --------------------------------------------------------
    tasa: Decimal

    # --------------------------------------------------------
    # VALOR MONETARIO CALCULADO DEL IMPUESTO
    # SE OBTIENE MULTIPLICANDO SUBTOTAL * TASA
    # --------------------------------------------------------
    valor: Decimal


# ============================================================
# ENTIDAD: DESCUENTO
# REPRESENTA UN DESCUENTO APLICADO A UNA FACTURA
# ============================================================

@dataclass
class Descuento:
    # --------------------------------------------------------
    # NOMBRE DEL DESCUENTO (EJEMPLO: "PROMOCION_VERANO")
    # --------------------------------------------------------
    nombre: str

    # --------------------------------------------------------
    # VALOR MONETARIO DEL DESCUENTO
    # SE RESTA DEL TOTAL FINAL DE LA FACTURA
    # --------------------------------------------------------
    valor: Decimal


# ============================================================
# CLASE PRINCIPAL: FACTURA
# IMPLEMENTACIÓN EMPRESARIAL CON TIPADO EXPLÍCITO
# SIGUE EL PATRÓN DDD (DOMAIN DRIVEN DESIGN)
# ============================================================

class Factura:

    # --------------------------------------------------------
    # CONSTRUCTOR PRINCIPAL
    # INICIALIZA TODOS LOS ATRIBUTOS DE LA FACTURA
    # --------------------------------------------------------
    def __init__(
        self,
        numero: str,
        impuestos: Optional[List[Impuesto]] = None,
        descuentos: Optional[List[Descuento]] = None
    ) -> None:

        # ----------------------------------------------------
        # IDENTIFICADOR ÚNICO DE LA FACTURA
        # EJEMPLO: "FAC-2026-0001"
        # ----------------------------------------------------
        self.numero: str = numero

        # ----------------------------------------------------
        # LISTA DE IMPUESTOS APLICADOS A LA FACTURA
        # TIPADO FUERTE PARA EVITAR list[Unknown]
        # SI NO SE PASAN, SE INICIA COMO LISTA VACÍA
        # ----------------------------------------------------
        self.impuestos: List[Impuesto] = impuestos if impuestos is not None else []

        # ----------------------------------------------------
        # LISTA DE DESCUENTOS APLICADOS A LA FACTURA
        # TIPADO FUERTE PARA EVITAR list[Unknown]
        # SI NO SE PASAN, SE INICIA COMO LISTA VACÍA
        # ----------------------------------------------------
        self.descuentos: List[Descuento] = descuentos if descuentos is not None else []

        # ----------------------------------------------------
        # SUBTOTAL: SUMA DE TODOS LOS ITEMS SIN IMPUESTOS
        # SE ACTUALIZA AL AGREGAR LÍNEAS DE PRODUCTOS
        # ----------------------------------------------------
        self.subtotal: Decimal = Decimal("0.00")

        # ----------------------------------------------------
        # TOTAL FINAL: SUBTOTAL + IMPUESTOS - DESCUENTOS
        # SE CALCULA CON calcular_total()
        # ----------------------------------------------------
        self.total: Decimal = Decimal("0.00")

        # ----------------------------------------------------
        # LISTA DE LÍNEAS DE PRODUCTO EN LA FACTURA
        # CADA LÍNEA REPRESENTA UN PRODUCTO Y SU CANTIDAD
        # ----------------------------------------------------
        self.lineas: List[LineaFactura] = []

        # ----------------------------------------------------
        # ESTADO ACTUAL DE LA FACTURA
        # VALORES POSIBLES: BORRADOR, EMITIDA, PAGADA, ANULADA
        # ----------------------------------------------------
        self.estado: str = "BORRADOR"

        # ----------------------------------------------------
        # EVENTOS DE DOMINIO (DDD)
        # REGISTRA TODO LO QUE HA OCURRIDO EN ESTA FACTURA
        # ----------------------------------------------------
        self._eventos: List[str] = []


    # --------------------------------------------------------
    # MÉTODO PRIVADO: REGISTRAR EVENTOS DE DOMINIO
    # SE LLAMA INTERNAMENTE CADA VEZ QUE ALGO CAMBIA
    # LOS EVENTOS PUEDEN USARSE PARA AUDITORÍA O MENSAJERÍA
    # --------------------------------------------------------
    def _registrar_evento(self, evento: str) -> None:

        # AGREGAR EL EVENTO A LA LISTA INTERNA
        self._eventos.append(evento)


    # --------------------------------------------------------
    # MÉTODO PRIVADO: VALIDAR QUE LA FACTURA NO ESTÁ ANULADA
    # SE LLAMA ANTES DE CUALQUIER OPERACIÓN DE MODIFICACIÓN
    # LANZA ValueError SI LA FACTURA YA FUE ANULADA
    # --------------------------------------------------------
    def _validar_no_anulada(self) -> None:

        # VERIFICAR ESTADO ANTES DE PERMITIR CAMBIOS
        if self.estado == "ANULADA":
            raise ValueError("NO SE PUEDE MODIFICAR UNA FACTURA ANULADA")


    # --------------------------------------------------------
    # AGREGAR LÍNEA DE PRODUCTO
    # REGISTRA UN PRODUCTO Y SU CANTIDAD EN LA FACTURA
    # RECALCULA EL SUBTOTAL AUTOMÁTICAMENTE
    # --------------------------------------------------------
    def agregar_linea(self, linea: LineaFactura) -> None:

        # VALIDAR QUE LA FACTURA PUEDE MODIFICARSE
        self._validar_no_anulada()

        # VALIDAR QUE LA CANTIDAD SEA POSITIVA
        if linea.cantidad <= 0:
            raise ValueError("LA CANTIDAD DEBE SER MAYOR A CERO")

        # VALIDAR QUE EL PRECIO UNITARIO SEA POSITIVO
        if linea.precio_unitario <= Decimal("0.00"):
            raise ValueError("EL PRECIO UNITARIO DEBE SER MAYOR A CERO")

        # AGREGAR LA LÍNEA A LA LISTA
        self.lineas.append(linea)

        # RECALCULAR EL SUBTOTAL CON LA NUEVA LÍNEA
        self.subtotal += linea.precio_unitario * Decimal(str(linea.cantidad))

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("LINEA_AGREGADA")


    # --------------------------------------------------------
    # AGREGAR IMPUESTO A LA FACTURA
    # SOLO SE PUEDE AGREGAR SI LA FACTURA NO ESTÁ ANULADA
    # --------------------------------------------------------
    def agregar_impuesto(self, impuesto: Impuesto) -> None:

        # VALIDAR QUE LA FACTURA PUEDE MODIFICARSE
        self._validar_no_anulada()

        # VALIDAR QUE EL VALOR DEL IMPUESTO NO SEA NEGATIVO
        if impuesto.valor < Decimal("0.00"):
            raise ValueError("EL VALOR DEL IMPUESTO NO PUEDE SER NEGATIVO")

        # AGREGAR EL IMPUESTO A LA LISTA
        self.impuestos.append(impuesto)

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("IMPUESTO_AGREGADO")


    # --------------------------------------------------------
    # AGREGAR DESCUENTO A LA FACTURA
    # EL DESCUENTO NO PUEDE SUPERAR EL SUBTOTAL
    # --------------------------------------------------------
    def agregar_descuento(self, descuento: Descuento) -> None:

        # VALIDAR QUE LA FACTURA PUEDE MODIFICARSE
        self._validar_no_anulada()

        # VALIDAR QUE EL DESCUENTO NO SEA NEGATIVO
        if descuento.valor < Decimal("0.00"):
            raise ValueError("EL VALOR DEL DESCUENTO NO PUEDE SER NEGATIVO")

        # VALIDAR QUE EL DESCUENTO NO SUPERE EL SUBTOTAL
        total_descuentos = self.calcular_total_descuentos() + descuento.valor
        if total_descuentos > self.subtotal:
            raise ValueError("LOS DESCUENTOS NO PUEDEN SUPERAR EL SUBTOTAL")

        # AGREGAR EL DESCUENTO A LA LISTA
        self.descuentos.append(descuento)

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("DESCUENTO_AGREGADO")


    # --------------------------------------------------------
    # EMITIR FACTURA
    # CAMBIA EL ESTADO DE BORRADOR A EMITIDA
    # SOLO SE PUEDE EMITIR SI TIENE AL MENOS UNA LÍNEA
    # --------------------------------------------------------
    def emitir(self) -> None:

        # VALIDAR QUE LA FACTURA PUEDE MODIFICARSE
        self._validar_no_anulada()

        # VALIDAR QUE TENGA AL MENOS UNA LÍNEA DE PRODUCTO
        if not self.lineas:
            raise ValueError("LA FACTURA DEBE TENER AL MENOS UNA LÍNEA")

        # CALCULAR EL TOTAL ANTES DE EMITIR
        self.calcular_total()

        # CAMBIAR ESTADO A EMITIDA
        self.estado = "EMITIDA"

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("FACTURA_EMITIDA")


    # --------------------------------------------------------
    # MARCAR FACTURA COMO PAGADA
    # SOLO SE PUEDE PAGAR SI ESTÁ EN ESTADO EMITIDA
    # --------------------------------------------------------
    def marcar_pagada(self) -> None:

        # VALIDAR QUE ESTÉ EMITIDA ANTES DE PAGAR
        if self.estado != "EMITIDA":
            raise ValueError("SOLO SE PUEDE PAGAR UNA FACTURA EMITIDA")

        # CAMBIAR ESTADO A PAGADA
        self.estado = "PAGADA"

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("FACTURA_PAGADA")


    # --------------------------------------------------------
    # ANULAR FACTURA
    # UNA FACTURA ANULADA NO PUEDE MODIFICARSE NI PAGARSE
    # --------------------------------------------------------
    def anular(self) -> None:

        # VALIDAR QUE NO ESTÉ YA ANULADA
        if self.estado == "ANULADA":
            raise ValueError("LA FACTURA YA ESTÁ ANULADA")

        # CAMBIAR ESTADO A ANULADA
        self.estado = "ANULADA"

        # REGISTRAR EVENTO DE DOMINIO
        self._registrar_evento("FACTURA_ANULADA")


    # --------------------------------------------------------
    # CALCULAR TOTAL DE IMPUESTOS
    # SUMA EL VALOR DE TODOS LOS IMPUESTOS EN LA LISTA
    # RETORNA Decimal("0.00") SI NO HAY IMPUESTOS
    # --------------------------------------------------------
    def calcular_total_impuestos(self) -> Decimal:

        # INICIAR ACUMULADOR EN CERO
        total = Decimal("0.00")

        # SUMAR EL VALOR DE CADA IMPUESTO
        for impuesto in self.impuestos:
            total += impuesto.valor

        return total


    # --------------------------------------------------------
    # CALCULAR TOTAL DE DESCUENTOS
    # SUMA EL VALOR DE TODOS LOS DESCUENTOS EN LA LISTA
    # RETORNA Decimal("0.00") SI NO HAY DESCUENTOS
    # --------------------------------------------------------
    def calcular_total_descuentos(self) -> Decimal:

        # INICIAR ACUMULADOR EN CERO
        total = Decimal("0.00")

        # SUMAR EL VALOR DE CADA DESCUENTO
        for descuento in self.descuentos:
            total += descuento.valor

        return total


    # --------------------------------------------------------
    # CALCULAR TOTAL FINAL DE LA FACTURA
    # FÓRMULA: SUBTOTAL + IMPUESTOS - DESCUENTOS
    # ACTUALIZA self.total Y LO RETORNA
    # --------------------------------------------------------
    def calcular_total(self) -> Decimal:

        # OBTENER SUMA DE TODOS LOS IMPUESTOS
        total_impuestos = self.calcular_total_impuestos()

        # OBTENER SUMA DE TODOS LOS DESCUENTOS
        total_descuentos = self.calcular_total_descuentos()

        # CALCULAR Y GUARDAR EL TOTAL FINAL
        self.total = self.subtotal + total_impuestos - total_descuentos

        return self.total


    # --------------------------------------------------------
    # OBTENER TODOS LOS EVENTOS DE DOMINIO REGISTRADOS
    # ÚTIL PARA AUDITORÍA, MENSAJERÍA O TESTING
    # RETORNA UNA COPIA PARA PROTEGER LA LISTA INTERNA
    # --------------------------------------------------------
    def obtener_eventos(self) -> List[str]:

        # RETORNAR COPIA PARA NO EXPONER LA LISTA INTERNA
        return list(self._eventos)


    # --------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO DE LA FACTURA
    # SE MUESTRA AL HACER print() O str() DEL OBJETO
    # --------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"<Factura numero={self.numero} "
            f"estado={self.estado} "
            f"subtotal={self.subtotal} "
            f"total={self.total}>"
        )


# ============================================================
# ENTIDAD: LÍNEA DE FACTURA
# REPRESENTA UN PRODUCTO Y SU CANTIDAD DENTRO DE LA FACTURA
# ============================================================

@dataclass
class LineaFactura:

    # --------------------------------------------------------
    # NOMBRE DEL PRODUCTO EN ESTA LÍNEA
    # --------------------------------------------------------
    nombre_producto: str

    # --------------------------------------------------------
    # CANTIDAD DE UNIDADES DEL PRODUCTO
    # DEBE SER UN ENTERO POSITIVO MAYOR A CERO
    # --------------------------------------------------------
    cantidad: int

    # --------------------------------------------------------
    # PRECIO UNITARIO DEL PRODUCTO
    # SE MULTIPLICA POR cantidad PARA OBTENER EL SUBTOTAL
    # --------------------------------------------------------
    precio_unitario: Decimal