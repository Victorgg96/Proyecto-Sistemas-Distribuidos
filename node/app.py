"""
NodeMesh - nodo de chat.

Un nodo es un proceso independiente que guarda mensajes en memoria y los
expone por HTTP. En esta etapa (Sesion 2) es UN solo nodo, sin replicacion.
La replicacion entre nodos llega en la Sesion 3.
"""

import argparse
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

# Estado del nodo: los mensajes viven en memoria, no en disco ni en una BD.
# Cuando el nodo se apaga, se pierden. Es a proposito para la demo.
mensajes = []

# El puerto en el que corre este nodo. Se llena al arrancar (ver main).
puerto_actual = None


@app.route("/mensajes", methods=["POST"])
def crear_mensaje():
    # Leemos el JSON del body. silent=True evita que Flask lance excepcion
    # si el body no es JSON valido; en ese caso datos queda en None.
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario")
    texto = datos.get("texto")

    # Los dos campos son obligatorios. Si falta alguno, 400.
    if not usuario or not texto:
        return jsonify({"error": "Faltan campos: se requieren 'usuario' y 'texto'"}), 400

    mensaje = {
        "usuario": usuario,
        "texto": texto,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    mensajes.append(mensaje)

    # 201 = creado. Devolvemos el mensaje ya guardado.
    return jsonify(mensaje), 201


@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    # Devolvemos la lista completa tal cual esta en memoria.
    return jsonify(mensajes), 200


@app.route("/salud", methods=["GET"])
def salud():
    # Sirve para saber si el nodo esta vivo y en que puerto responde.
    return jsonify({
        "estado": "ok",
        "puerto": puerto_actual,
        "mensajes_guardados": len(mensajes),
    }), 200


def main():
    global puerto_actual

    parser = argparse.ArgumentParser(description="Nodo de chat NodeMesh")
    parser.add_argument(
        "--puerto",
        type=int,
        default=5001,
        help="Puerto en el que corre el nodo (default 5001)",
    )
    args = parser.parse_args()
    puerto_actual = args.puerto

    # host 0.0.0.0 para que sea alcanzable desde otras maquinas/ngrok.
    app.run(host="0.0.0.0", port=args.puerto)


if __name__ == "__main__":
    main()
