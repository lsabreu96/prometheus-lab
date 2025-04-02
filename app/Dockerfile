# Usando a imagem base do Python
FROM python:3.11-slim

# Instala compilador C para rodar o uwsgi
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    libpcre3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o código do aplicativo
COPY . /app/
RUN pip install -r requirements.txt --no-cache-dir

# Comando para rodar o aplicativo
CMD ["uwsgi", "--ini", "app.ini"]
