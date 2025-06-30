from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from datetime import datetime, time
from zoneinfo import ZoneInfo  # ✅ Para timezone

from database import engine, criar_db_e_tabelas
from models import Usuario, Consumo

from typing import Optional
from passlib.context import CryptContext
from auth import hash_senha, verificar_senha, get_usuario_logado, logout
from dotenv import load_dotenv
import os

load_dotenv()  # carrega variáveis do .env

SECRET_KEY = os.getenv("SECRET_KEY")

templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_db_e_tabelas()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_session():
    with Session(engine) as session:
        yield session


def get_usuario_logado(request: Request, session: Session) -> Optional[Usuario]:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return session.get(Usuario, user_id)


@app.get("/")
def pagina_inicial(request: Request, session: Session = Depends(get_session)):
    usuario = get_usuario_logado(request, session)
    if not usuario:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    fuso = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(fuso)
    inicio_dia = datetime.combine(agora.date(), time.min, tzinfo=fuso)
    fim_dia = datetime.combine(agora.date(), time.max, tzinfo=fuso)

    consumos = session.exec(
        select(Consumo).where(
            Consumo.usuario_id == usuario.id,
            Consumo.data >= inicio_dia,
            Consumo.data <= fim_dia,
        )
    ).all()

    for consumo in consumos:
        consumo.data_formatada = consumo.data.astimezone(fuso).strftime("%H:%M")

    total = sum(c.quantidade for c in consumos)

    ranking_data = session.exec(
        select(Usuario.nome, Consumo.quantidade)
        .join(Consumo, Consumo.usuario_id == Usuario.id)
        .where(Consumo.data >= inicio_dia, Consumo.data <= fim_dia)
    ).all()

    ranking_dict = {}
    for nome, qtd in ranking_data:
        ranking_dict[nome] = ranking_dict.get(nome, 0) + qtd
    ranking = sorted(ranking_dict.items(), key=lambda x: x[1], reverse=True)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "usuario": usuario,
            "consumos": consumos,
            "total": total,
            "ranking": ranking,
        },
    )



@app.post("/registrar")
def registrar_consumo(
    request: Request,
    quantidade: int = Form(...),
    session: Session = Depends(get_session),
):
    usuario = get_usuario_logado(request, session)
    if not usuario:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # ✅ Agora com fuso horário
    fuso = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(fuso)

    consumo = Consumo(usuario_id=usuario.id, quantidade=quantidade, data=agora)
    session.add(consumo)
    session.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request, "erro": None},
    )


@app.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    session: Session = Depends(get_session),
):
    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            request,
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"},
        )

    request.session["user_id"] = usuario.id
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@app.get("/registrar-usuario")
def registrar_usuario_get(request: Request):
    return templates.TemplateResponse(
        request,
        "registrar.html",
        {"request": request, "erro": None},
    )


@app.post("/registrar-usuario")
def registrar_usuario_post(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    session: Session = Depends(get_session),
):
    existe = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if existe:
        return templates.TemplateResponse(
            request,
            "registrar.html",
            {"request": request, "erro": "Email já cadastrado"},
        )

    senha_hash = hash_senha(senha)
    usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    session.add(usuario)
    session.commit()

    request.session["user_id"] = usuario.id
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
