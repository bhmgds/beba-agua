from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime  # ✅ corrigido aqui

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha_hash: str

    consumos: List["Consumo"] = Relationship(back_populates="usuario")

class Consumo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    quantidade: int  # em mililitros
    data: datetime  # ✅ agora armazena data e hora

    usuario: Optional[Usuario] = Relationship(back_populates="consumos")
