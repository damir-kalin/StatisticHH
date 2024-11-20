import os 
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logger import logger

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# from sqlalchemy import create_engine

# engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False) # строка для настройки сериализации json объектов
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    logger.info("Creating a session with the database.")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("The database session is closed.")
        db.close()