import os
from flask import Flask, Response
from log import uWSGILogParser

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/var/log/uwsgi.log")
log_parser = uWSGILogParser(LOG_FILE_PATH)

app = Flask(__name__)

@app.route('/')
def hello():
    return "Olá"

@app.route('/metrics')
def metrics():
    try:
        metrics_data = log_parser.parse_uwsgi_logs()
        return Response(metrics_data, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error parsing logs: {e}", status=500, mimetype='text/plain')
