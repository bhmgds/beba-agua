from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

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
    data: date

    usuario: Optional[Usuario] = Relationship(back_populates="consumos")
