from pydantic_settings import BaseSettings
from typing import Optional

class Configuracion(BaseSettings):
    # ==========================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ==========================================
    # Cadena de conexión a PostgreSQL
    # Lee del archivo .env
    DATABASE_URL: str
    
    # ==========================================
    # CONFIGURACIÓN DE REDIS
    # ==========================================
    # URL de conexión a Redis para caché
    REDIS_URL: str
    
    # ==========================================
    # CONFIGURACIÓN DE SEGURIDAD JWT
    # ==========================================
    # Secreto para firmar tokens JWT
    JWT_SECRET: str
    # Algoritmo de firma (por defecto HS256)
    JWT_ALGORITHM: str = "HS256"
    # Tiempo de expiración del token en minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==========================================
    # CONFIGURACIÓN DE ENTORNO
    # ==========================================
    # Entorno actual (development, production)
    ENVIRONMENT: str = "development"
    # Modo debug (True en desarrollo, False en producción)
    DEBUG: bool = True
    
    # ==========================================
    # CONFIGURACIÓN GENERAL DE LA API
    # ==========================================
    # Prefijo global para endpoints v1
    API_V1_PREFIX: str = "/api/v1"
    # Nombre del proyecto para documentación
    PROJECT_NAME: str = "SGDD API"
    # Versión actual de la API
    VERSION: str = "0.1.0"
    
    class Config:
        # Archivo de donde leer las variables
        env_file = ".env"
        # Sensible a mayúsculas
        case_sensitive = True

# Instancia global de configuración
configuracion = Configuracion()
