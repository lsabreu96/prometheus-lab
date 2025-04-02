import os
from flask import Flask, Response
from prometheus_client import Counter, multiprocess, CollectorRegistry, generate_latest

contador = Counter('numero_de_requisicoes', 'Numero de requisicoes', ['endpoint', 'status_code'])


def get_registry():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return registry
