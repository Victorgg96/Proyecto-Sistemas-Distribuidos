"""
NodeMesh - nodo de chat.

Un nodo es un proceso independiente que guarda mensajes en memoria y los
expone por HTTP. El mismo archivo se puede levantar varias veces en puertos
distintos para formar una red simple de nodos.
"""

import argparse
import json
from datetime import datetime, timezone
from threading import Lock
from urllib.error import URLError
from urllib.request import Request, urlopen
from uuid import uuid4

from flask import Flask, jsonify, request

app = Flask(__name__)

# Estado local del nodo. No hay memoria compartida entre procesos:
# cada nodo guarda su propia copia y se sincroniza por HTTP.
mensajes = []
ids_mensajes = set()
lock_mensajes = Lock()

# Configuracion del proceso actual. Se llena al arrancar desde la consola.
nodo_actual = None
puerto_actual = None
vecinos = []


def crear_payload_mensaje(usuario, texto):
    # Cada mensaje necesita un id para no duplicarlo al replicar entre nodos.
    return {
        "id": str(uuid4()),
        "usuario": usuario,
        "texto": texto,
        "origen": nodo_actual,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def guardar_mensaje(mensaje):
    # El lock evita inconsistencias si Flask atiende dos peticiones a la vez.
    with lock_mensajes:
        if mensaje["id"] in ids_mensajes:
            return False

        mensajes.append(mensaje)
        ids_mensajes.add(mensaje["id"])
        return True


def replicar_mensaje(mensaje):
    # La replicacion es mejor esfuerzo: si un vecino esta caido, este nodo sigue.
    fallos = []
    cuerpo = json.dumps(mensaje).encode("utf-8")

    for vecino in vecinos:
        url = f"{vecino}/replicar"
        request_http = Request(
            url,
            data=cuerpo,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request_http, timeout=2):
                pass
        except URLError:
            fallos.append(vecino)

    return fallos


def normalizar_url(url):
    # Evita errores comunes como dejar una diagonal final en el vecino.
    return url.rstrip("/")


@app.route("/mensajes", methods=["POST"])
def crear_mensaje():
    # Endpoint publico: un cliente manda usuario/texto a cualquier nodo.
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario")
    texto = datos.get("texto")

    if not usuario or not texto:
        return jsonify({"error": "Faltan campos: se requieren 'usuario' y 'texto'"}), 400

    mensaje = crear_payload_mensaje(usuario, texto)
    guardar_mensaje(mensaje)
    fallos = replicar_mensaje(mensaje)

    return jsonify({
        "mensaje": mensaje,
        "replicado_a": [vecino for vecino in vecinos if vecino not in fallos],
        "replicas_fallidas": fallos,
    }), 201


@app.route("/replicar", methods=["POST"])
def recibir_replica():
    # Endpoint interno: lo usan otros nodos para enviar una copia del mensaje.
    mensaje = request.get_json(silent=True) or {}
    campos_requeridos = {"id", "usuario", "texto", "origen", "timestamp"}

    if not campos_requeridos.issubset(mensaje):
        return jsonify({"error": "Replica invalida: faltan campos obligatorios"}), 400

    guardado = guardar_mensaje(mensaje)
    estado = "guardado" if guardado else "duplicado"

    return jsonify({"estado": estado, "id": mensaje["id"]}), 200


@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    # Se devuelve una copia para no exponer la lista mientras podria cambiar.
    with lock_mensajes:
        return jsonify(list(mensajes)), 200


@app.route("/salud", methods=["GET"])
def salud():
    # Permite diagnosticar rapido que nodo responde y cuantos mensajes conoce.
    with lock_mensajes:
        total_mensajes = len(mensajes)

    return jsonify({
        "estado": "ok",
        "nodo": nodo_actual,
        "puerto": puerto_actual,
        "vecinos": vecinos,
        "mensajes_guardados": total_mensajes,
    }), 200


def main():
    global nodo_actual, puerto_actual, vecinos

    parser = argparse.ArgumentParser(description="Nodo de chat NodeMesh")
    parser.add_argument(
        "--puerto",
        type=int,
        default=5001,
        help="Puerto en el que corre el nodo (default 5001)",
    )
    parser.add_argument(
        "--nodo",
        default=None,
        help="Nombre legible del nodo (default nodo-<puerto>)",
    )
    parser.add_argument(
        "--vecinos",
        nargs="*",
        default=[],
        help="URLs de otros nodos, por ejemplo: http://localhost:5002",
    )
    args = parser.parse_args()

    puerto_actual = args.puerto
    nodo_actual = args.nodo or f"nodo-{args.puerto}"
    vecinos = [normalizar_url(vecino) for vecino in args.vecinos]

    # host 0.0.0.0 para que sea alcanzable desde otras maquinas/ngrok.
    app.run(host="0.0.0.0", port=args.puerto)


if __name__ == "__main__":
    main()
