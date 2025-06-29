from passlib.context import CryptContext
from fastapi import Request
from sqlmodel import Session
from models import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(password: str) -> str:
    return pwd_context.hash(password)

def verificar_senha(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_usuario_logado(request: Request, session: Session) -> Usuario | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    usuario = session.get(Usuario, user_id)
    return usuario

def logout(request: Request):
    request.session.clear()
