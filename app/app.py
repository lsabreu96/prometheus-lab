import os
import logging
import time
from flask import Flask, Response, request
from db import DbManager
from metrics import contador, get_registry, tempo_de_requisicao
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from start import startup

logger = logging.getLogger(__name__)

app = Flask(__name__)
db_manager = startup()


@app.before_request
def start_time():
    request.start_time = time.time()


@app.after_request
def log_request(response):
    request_duration = time.time() - request.start_time
    tempo_de_requisicao.labels(request.path).observe(request_duration)
    return response


@app.route('/')
def hello():
    return "Olá"


@tempo_de_requisicao.time()
@app.route('/cadastrar', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or not all(key in data for key in ['nome', 'idade']):
        contador.labels('/cadastrar', '400').inc()
        return \
            Response(
                "Payload inválido. Certifique-se de incluir os campos 'nome', 'idade'.", 
                status=400, mimetype='text/plain'
            )
    
    nome = data['nome']
    idade = data['idade']
    
    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cadastro (nome, idade) VALUES (%s, %s)", (nome, idade))
    conn.commit()
    cursor.close()
    db_manager.release_connection(conn)
    contador.labels('/cadastrar', '200').inc()
    return Response("Cadastro realizado", status=200, mimetype='text/plain')


@tempo_de_requisicao.time()
@app.route('/consultar', methods=['GET'])
def consultar():
    nome = request.args.get('nome')
    idade = request.args.get('idade')

    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    query = "SELECT * FROM cadastro WHERE nome = '{}' AND idade = '{}'".format(nome, idade)
    cursor.execute(query)

    rows = cursor.fetchall()

    if not rows:
        contador.labels('/consultar', '404').inc()
        return Response("Nenhum registro encontrado", status=404, mimetype='text/plain')
    else:
        contador.labels('/consultar', '200').inc()
        response = ""
        for row in rows:
            response += f"ID: {row[0]}, Nome: {row[1]}, Idade: {row[2]}\n"
        return Response(response, status=200, mimetype='text/plain')

    cursor.close()
    db_manager.release_connection(conn)


@app.route('/metrics')
def metrics():
    registry = get_registry()
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
