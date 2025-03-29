import os
from flask import Flask, Response, request
import logging
from db import DbManager
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def startup():

    global db_manager
    db_manager = DbManager()
    db_manager.start_connection_pool()    
    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cadastro (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            idade INT
        )
    """)
    conn.commit()
    # Close the cursor and return the connection to the pool
    cursor.close()
    db_manager.release_connection(conn)

startup()

@app.route('/')
def hello():
    return "Olá"


@app.route('/cadastrar', methods=['POST'])
def submit():
    data = request.get_json()
    if not data or not all(key in data for key in ['nome', 'idade']):
        return Response("Payload inválido. Certifique-se de incluir os campos 'nome', 'idade'.", status=400, mimetype='text/plain')
    
    nome = data['nome']
    idade = data['idade']
    
    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cadastro (nome, idade) VALUES (%s, %s)", (nome, idade))
    conn.commit()
    cursor.close()
    db_manager.release_connection(conn)
    return Response("Cadastro realizado", status=200, mimetype='text/plain')


@app.route('/consultar', methods=['GET'])
def consultar():
    nome = request.args.get('nome')
    idade = request.args.get('idade')

    conn = db_manager.get_connection_from_pool()
    cursor = conn.cursor()
    query = "SELECT * FROM cadastro WHERE nome = {} AND idade = {}".format(nome, idade)
    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        return Response("Nenhum registro encontrado", status=404, mimetype='text/plain')
    else:
        response = ""
        for row in rows:
            response += f"ID: {row[0]}, Nome: {row[1]}, Idade: {row[2]}, Endereço: {row[3]}\n"
        return Response(response, status=200, mimetype='text/plain')
    # Close the cursor and return the connection to the pool
    cursor.close()
    db_manager.release_connection(conn)
