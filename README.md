# Beba Agua 💧

Beba Agua é um aplicativo web simples para você e sua esposa acompanharem o consumo diário de água de forma prática e motivadora.

## Funcionalidades

- Cadastro e login de usuários  
- Registro da quantidade de água ingerida em ml  
- Visualização do total diário consumido  
- Ranking diário entre os usuários  
- Interface responsiva para celulares, tablets e desktops  

## Tecnologias

- Python 3.10+  
- FastAPI  
- SQLModel com SQLite ou PostgreSQL  
- Jinja2 para templates HTML  
- CSS personalizado  
- Hospedagem no Railway  

## Como rodar localmente

1. Clone o repositório:  
   ```bash
   git clone https://github.com/seu-usuario/beba-agua.git
   cd beba-agua
   ```

2. Crie e ative o ambiente virtual:  
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows Git Bash
   ```

3. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```

4. Rode a aplicação:  
   ```bash
   uvicorn main:app --reload
   ```

5. Acesse em http://localhost:8000 no seu navegador.

## Deploy

A aplicação está preparada para deploy no Railway com as configurações em `requirements.txt` e `Procfile`.

## Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

---

## Contato

Bruno Miguel — brhrmiguel@gmail.com

Projeto criado para facilitar o consumo saudável de água.
```
