"""
NodeMesh - nodo de chat distribuido.

Cada nodo es un proceso independiente que guarda mensajes en memoria y los
expone por HTTP. Los nodos se conocen entre si (via --peers) y replican los
mensajes: cuando a un nodo le llega un mensaje de un CLIENTE, lo reenvia a
los demas nodos para que todos tengan la misma conversacion.

Dos formas de que entre un mensaje:
  - POST /mensajes  -> lo usa un CLIENTE. El nodo guarda y REPLICA a sus peers.
  - POST /replicar  -> lo usa OTRO NODO. El nodo solo guarda, NO reenvia.
Esa separacion es lo que evita un bucle infinito de reenvios.
"""

import argparse
import uuid
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Estado del nodo: los mensajes viven en memoria. Al apagar el nodo se pierden.
mensajes = []

# Lista de URLs de los otros nodos (ej. "http://10.20.11.71:5001"). Se llena
# al arrancar con --peers. Si esta vacia, el nodo trabaja solo, sin replicar.
peers = []

# El puerto en el que corre este nodo. Se llena en main().
puerto_actual = None


def ya_existe(id_mensaje):
    # Evita guardar dos veces el mismo mensaje (por si llega repetido).
    return any(m["id"] == id_mensaje for m in mensajes)


@app.route("/mensajes", methods=["POST"])
def crear_mensaje():
    # Entrada de un CLIENTE: guardamos y replicamos a los demas nodos.
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario")
    texto = datos.get("texto")

    if not usuario or not texto:
        return jsonify({"error": "Faltan campos: se requieren 'usuario' y 'texto'"}), 400

    # El nodo de origen arma el mensaje completo: id y timestamp se fijan aqui
    # una sola vez, para que todas las copias en los demas nodos sean iguales.
    mensaje = {
        "id": uuid.uuid4().hex,
        "usuario": usuario,
        "texto": texto,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    mensajes.append(mensaje)

    replicar_a_peers(mensaje)

    return jsonify(mensaje), 201


@app.route("/replicar", methods=["POST"])
def recibir_replica():
    # Entrada de OTRO NODO: solo guardamos, NO reenviamos (asi no hay bucle).
    mensaje = request.get_json(silent=True) or {}

    # Un mensaje replicado debe venir armado desde el nodo de origen.
    if not mensaje.get("id") or not mensaje.get("usuario") or not mensaje.get("texto"):
        return jsonify({"error": "Mensaje replicado invalido"}), 400

    if ya_existe(mensaje["id"]):
        return jsonify({"estado": "ya existia, ignorado"}), 200

    mensajes.append(mensaje)
    return jsonify({"estado": "replicado"}), 201


@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    return jsonify(mensajes), 200


@app.route("/salud", methods=["GET"])
def salud():
    return jsonify({
        "estado": "ok",
        "puerto": puerto_actual,
        "mensajes_guardados": len(mensajes),
        "peers": peers,
    }), 200


def replicar_a_peers(mensaje):
    # Mandamos el mensaje a cada peer por su endpoint /replicar.
    # Cada llamada va protegida: si un peer esta caido, NO tumbamos este nodo;
    # solo ese peer se pierde el mensaje. Esto es la tolerancia a fallos.
    for peer in peers:
        try:
            # El header ngrok-skip-browser-warning evita que ngrok gratis meta
            # su pagina de advertencia cuando los nodos se hablan por una URL
            # publica de ngrok. En red local no estorba.
            requests.post(
                f"{peer}/replicar",
                json=mensaje,
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=3,
            )
        except requests.exceptions.RequestException as e:
            # No frenamos: avisamos en consola y seguimos con el siguiente.
            print(f"[replicacion] no se pudo replicar a {peer}: {e}")


def main():
    global puerto_actual, peers

    parser = argparse.ArgumentParser(description="Nodo de chat NodeMesh")
    parser.add_argument(
        "--puerto",
        type=int,
        default=5001,
        help="Puerto en el que corre el nodo (default 5001)",
    )
    parser.add_argument(
        "--peers",
        nargs="*",
        default=[],
        help="URLs de los otros nodos, separadas por espacio "
             "(ej. --peers http://10.20.11.71:5001 http://10.20.11.72:5001)",
    )
    args = parser.parse_args()
    puerto_actual = args.puerto
    # Quitamos una posible diagonal al final para no armar URLs con // dobles.
    peers = [p.rstrip("/") for p in args.peers]

    print(f"Nodo escuchando en el puerto {puerto_actual}")
    print(f"Peers configurados: {peers if peers else 'ninguno (modo solo)'}")

    # host 0.0.0.0 para que sea alcanzable desde otras maquinas / ngrok.
    app.run(host="0.0.0.0", port=args.puerto)


if __name__ == "__main__":
    main()
