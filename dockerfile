FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema (ex: para psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copia o requirements.txt e instala os pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta correta (o Northflank respeita EXPOSE)
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
