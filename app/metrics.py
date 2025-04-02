import os
from flask import Flask, Response
from prometheus_client import (
    Counter, multiprocess, CollectorRegistry,
    Summary
)

contador = Counter('numero_de_requisicoes', 'Numero de requisicoes', ['endpoint', 'status_code'])
tempo_de_requisicao = Summary('tempo_de_requisicao', 'Tempo de requisicao', ['endpoint'])

def get_registry():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return registry
