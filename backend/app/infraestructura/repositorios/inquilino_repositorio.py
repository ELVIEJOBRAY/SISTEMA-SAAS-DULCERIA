from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone

from app.dominio.entidades.inquilino import Inquilino, PlanSuscripcion, EstadoTenant
from app.infraestructura.repositorios.base_repositorio import RepositorioBase
from app.infraestructura.repositorios.modelos import InquilinoModelo


class RepositorioInquilino(RepositorioBase[Inquilino]):
    """
    REPOSITORIO PARA LA ENTIDAD INQUILINO (TENANT).
    
    PROPORCIONA OPERACIONES CRUD Y MÉTODOS ESPECÍFICOS
    PARA LA GESTIÓN DE INQUILINOS EN EL SISTEMA SAAS.
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    # ======================================================
    # OPERACIONES CRUD BÁSICAS
    # ======================================================
    
    def obtener_por_id(self, id: int) -> Optional[Inquilino]:
        """
        OBTIENE UN INQUILINO POR SU ID.
        """
        modelo = self.db.get(InquilinoModelo, id)
        if modelo:
            return self._modelo_a_entidad(modelo)
        return None
    
    def obtener_todos(self) -> List[Inquilino]:
        """
        OBTIENE TODOS LOS INQUILINOS.
        """
        resultados = self.db.execute(select(InquilinoModelo))
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def guardar(self, entidad: Inquilino) -> Inquilino:
        """
        GUARDA UN INQUILINO (CREA O ACTUALIZA).
        """
        if entidad.id is None:
            # ==================================================
            # CREAR NUEVO INQUILINO
            # ==================================================
            modelo = InquilinoModelo(
                nombre=entidad.nombre,
                subdominio=entidad.subdominio,
                plan=entidad.plan.value,           # Convertimos Enum a string
                estado=entidad.estado.value,        # Convertimos Enum a string
                max_usuarios=entidad.max_usuarios,
                max_productos=entidad.max_productos,
                fecha_creacion=datetime.now(timezone.utc)
            )
            self.db.add(modelo)
            self.db.flush()  # Para obtener el ID generado
            entidad.id = modelo.id
        else:
            # ==================================================
            # ACTUALIZAR INQUILINO EXISTENTE
            # ==================================================
            modelo = self.db.get(InquilinoModelo, entidad.id)
            if modelo:
                modelo.nombre = entidad.nombre
                modelo.subdominio = entidad.subdominio
                modelo.plan = entidad.plan.value
                modelo.estado = entidad.estado.value
                modelo.max_usuarios = entidad.max_usuarios
                modelo.max_productos = entidad.max_productos
        
        return entidad
    
    def eliminar(self, id: int) -> bool:
        """
        ELIMINA UN INQUILINO POR SU ID.
        """
        modelo = self.db.get(InquilinoModelo, id)
        if modelo:
            self.db.delete(modelo)
            return True
        return False
    
    def contar(self) -> int:
        """
        CUENTA EL NÚMERO TOTAL DE INQUILINOS.
        """
        return self.db.query(InquilinoModelo).count()
    
    # ======================================================
    # MÉTODOS ESPECÍFICOS DE INQUILINO
    # ======================================================
    
    def buscar_por_subdominio(self, subdominio: str) -> Optional[Inquilino]:
        """
        BUSCA UN INQUILINO POR SU SUBDOMINIO.
        """
        resultado = self.db.execute(
            select(InquilinoModelo).where(InquilinoModelo.subdominio == subdominio)
        )
        modelo = resultado.scalar_one_or_none()
        if modelo:
            return self._modelo_a_entidad(modelo)
        return None
    
    def buscar_por_plan(self, plan: PlanSuscripcion) -> List[Inquilino]:
        """
        BUSCA INQUILINOS POR SU PLAN DE SUSCRIPCIÓN.
        """
        resultados = self.db.execute(
            select(InquilinoModelo).where(InquilinoModelo.plan == plan.value)
        )
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def buscar_activos(self) -> List[Inquilino]:
        """
        OBTIENE TODOS LOS INQUILINOS ACTIVOS.
        """
        resultados = self.db.execute(
            select(InquilinoModelo).where(InquilinoModelo.estado == EstadoTenant.ACTIVO.value)
        )
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    
    def buscar_en_prueba(self) -> List[Inquilino]:
        """
        OBTIENE TODOS LOS INQUILINOS EN PERÍODO DE PRUEBA.
        """
        resultados = self.db.execute(
            select(InquilinoModelo).where(InquilinoModelo.estado == EstadoTenant.EN_PRUEBA.value)
        )
        modelos = resultados.scalars().all()
        return [self._modelo_a_entidad(m) for m in modelos]
    
    # ======================================================
    # CONVERSIÓN MODELO ↔ ENTIDAD
    # ======================================================
    
    def _modelo_a_entidad(self, modelo: InquilinoModelo) -> Inquilino:
        """
        CONVIERTE UN MODELO ORM A ENTIDAD DE DOMINIO.
        """
        return Inquilino(
            id=modelo.id,
            nombre=modelo.nombre,
            subdominio=modelo.subdominio,
            plan=PlanSuscripcion(modelo.plan),      # Convertimos string a Enum
            estado=EstadoTenant(modelo.estado),     # Convertimos string a Enum
            max_usuarios=modelo.max_usuarios,
            max_productos=modelo.max_productos,
            fecha_creacion=modelo.fecha_creacion
        )
