import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")

def obtener_conexion():
    if not DATABASE_URL or not str(DATABASE_URL).strip():
        raise RuntimeError("No se encontro la variable de entorno DATABASE_URL.")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def crear_cursor():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    return conexion, cursor

def obtener_cursor():
    conexion = obtener_conexion()
    return conexion.cursor()

def cerrar_cursor(cursor):
    try:
        if cursor is not None:
            cursor.close()
    except Exception:
        pass

def cerrar_conexion(conexion):
    try:
        if conexion is not None:
            conexion.close()
    except Exception:
        pass
