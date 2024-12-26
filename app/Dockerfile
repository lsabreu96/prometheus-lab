# Usando a imagem base do Python
FROM python:3.9-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o arquivo de requisitos e instalando dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiando o código do aplicativo
COPY app.py app.py

# Comando para rodar o aplicativo
CMD ["python", "app.py"]
