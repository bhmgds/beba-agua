from sqlmodel import SQLModel, create_engine
import os

# 🚧 Troque pelo seu banco em produção caso deseje (ex: Railway)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///banco.db")

# Se for SQLite, precisamos ativar a flag check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

# Função para criar as tabelas (usada no lifespan do FastAPI)
def criar_db_e_tabelas():
    SQLModel.metadata.create_all(engine)
