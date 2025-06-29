from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pagina_inicial_redirect():
    # Como o usuário não está logado, espera redirecionar para /login
    response = client.get("/", follow_redirects=False)  # <-- aqui
    assert response.status_code == 307 or response.status_code == 302
    assert response.headers["location"] == "/login"

def test_login_get():
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<form" in response.text  # verifica que o form existe
