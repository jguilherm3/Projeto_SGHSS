# app/database.py (Versão SQLite)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MUDANÇA AQUI: Usamos SQLite em vez de PostgreSQL
# Isso criará um arquivo chamado 'sghss.db' na pasta do seu projeto.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sghss.db"

# Configuração específica para SQLite (check_same_thread=False é necessário apenas no SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para obter o banco de dados (Dependência)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()