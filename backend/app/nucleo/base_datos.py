# ==========================================================
# IMPORTACIONES NECESARIAS PARA LA CONEXIÓN A BASE DE DATOS
# ==========================================================

# CREATE_ENGINE ES LA FUNCIÓN DE SQLALCHEMY QUE CREA
# EL MOTOR DE CONEXIÓN HACIA LA BASE DE DATOS.
# ESTE MOTOR ADMINISTRA:
# - CONEXIONES
# - POOL DE CONEXIONES
# - COMUNICACIÓN CON POSTGRESQL
from sqlalchemy import create_engine

# DECLARATIVE_BASE PERMITE CREAR UNA CLASE BASE
# DE LA CUAL HEREDARÁN TODOS LOS MODELOS ORM.
# ESTO ES PARTE DEL SISTEMA DE MAPEO OBJETO-RELACIONAL.
from sqlalchemy.ext.declarative import declarative_base

# SESSIONMAKER CREA UNA FÁBRICA DE SESIONES
# QUE PERMITE INTERACTUAR CON LA BASE DE DATOS.
from sqlalchemy.orm import sessionmaker

# IMPORTAMOS LA CONFIGURACIÓN CENTRAL DEL PROYECTO
# DESDE EL MÓDULO DE CONFIGURACIÓN.
# AQUÍ SE ENCUENTRAN VARIABLES COMO:
# - DATABASE_URL
# - DEBUG
from app.nucleo.config import configuracion


# ==========================================================
# MOTOR DE BASE DE DATOS
# ==========================================================
# EL MOTOR ES EL COMPONENTE CENTRAL DE SQLALCHEMY
# QUE MANEJA LA CONEXIÓN CON LA BASE DE DATOS.
#
# CREATE_ENGINE RECIBE LA URL DE CONEXIÓN DEFINIDA
# EN LAS VARIABLES DE ENTORNO.
#
# OPCIONES IMPORTANTES:
#
# pool_pre_ping=True
#    VERIFICA QUE LA CONEXIÓN SIGA ACTIVA ANTES
#    DE UTILIZARLA DESDE EL POOL.
#    EVITA ERRORES DE CONEXIÓN CAÍDA.
#
# echo=configuracion.DEBUG
#    SI DEBUG ESTÁ ACTIVADO SE IMPRIMEN
#    TODAS LAS CONSULTAS SQL EN CONSOLA.
#    ESTO ES MUY ÚTIL DURANTE DESARROLLO.
motor = create_engine(
    configuracion.DATABASE_URL,
    pool_pre_ping=True,
    echo=configuracion.DEBUG
)


# ==========================================================
# FÁBRICA DE SESIONES
# ==========================================================
# SESSIONMAKER CREA UNA FÁBRICA QUE GENERA
# SESIONES DE BASE DE DATOS.
#
# UNA SESIÓN ES EL OBJETO QUE PERMITE:
# - CONSULTAR DATOS
# - INSERTAR REGISTROS
# - ACTUALIZAR
# - ELIMINAR
#
# CONFIGURACIONES IMPORTANTES:
#
# autocommit=False
#    LAS TRANSACCIONES NO SE CONFIRMAN
#    AUTOMÁTICAMENTE. SE DEBE HACER
#    db.commit() MANUALMENTE.
#
# autoflush=False
#    EVITA QUE LOS CAMBIOS SE SINCRONICEN
#    AUTOMÁTICAMENTE CON LA BASE DE DATOS.
#
# bind=motor
#    ASOCIA ESTA SESIÓN CON EL MOTOR
#    DE BASE DE DATOS DEFINIDO ARRIBA.
SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor
)


# ==========================================================
# BASE PARA MODELOS ORM
# ==========================================================
# DECLARATIVE_BASE CREA UNA CLASE BASE
# DE LA CUAL HEREDARÁN TODOS LOS MODELOS.
#
# EJEMPLO:
#
# class Usuario(Base):
#     __tablename__ = "usuarios"
#
# ESTO PERMITE QUE SQLALCHEMY MAPEE
# CLASES PYTHON A TABLAS SQL.
Base = declarative_base()


# ==========================================================
# DEPENDENCIA PARA ENDPOINTS FASTAPI
# ==========================================================
# ESTA FUNCIÓN SE UTILIZA COMO DEPENDENCIA
# EN LOS ENDPOINTS DE FASTAPI PARA OBTENER
# UNA SESIÓN DE BASE DE DATOS.
#
# EJEMPLO DE USO:
#
# @router.get("/usuarios")
# def listar_usuarios(db: Session = Depends(obtener_bd)):
#     return db.query(Usuario).all()
#
# FUNCIONAMIENTO:
#
# 1. SE CREA UNA SESIÓN NUEVA
# 2. SE ENTREGA AL ENDPOINT
# 3. CUANDO TERMINA LA PETICIÓN
#    LA SESIÓN SE CIERRA AUTOMÁTICAMENTE
#
# ESTO EVITA:
# - FUGAS DE CONEXIÓN
# - SESIONES ABIERTAS
# - PROBLEMAS DE CONCURRENCIA
def obtener_bd():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
