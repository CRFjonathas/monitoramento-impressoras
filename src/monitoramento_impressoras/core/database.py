from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# O banco de dados será criado na raiz do projeto
DATABASE_URL = "sqlite:///./centro_comando.db"

# Argumento obrigatório para o SQLite trabalhar bem com o fluxo do FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()