import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

URL_BASE_DATOS = os.getenv("DATABASE_URL")

if not URL_BASE_DATOS:
    raise RuntimeError("No se encontro DATABASE_URL en el archivo .env")

motor = create_engine(
    URL_BASE_DATOS,
    pool_pre_ping=True,
)

SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor,
)


def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
        