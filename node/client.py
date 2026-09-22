"""
Cliente de consola para NodeMesh.

Sirve para mandar mensajes a un nodo escribiendolos a mano, sin Postman.
Le dices a que nodo conectarte con --nodo y luego escribes lo que quieras.

Comandos dentro del cliente:
  ver    -> muestra todos los mensajes que tiene ese nodo
  salir  -> termina el cliente
"""

import argparse

import requests

# Este header evita la pagina de advertencia de ngrok cuando el nodo esta
# expuesto por una URL publica. En red local no estorba.
HEADERS = {"ngrok-skip-browser-warning": "true"}


def mostrar_mensajes(base):
    try:
        r = requests.get(f"{base}/mensajes", headers=HEADERS, timeout=5)
        mensajes = r.json()
    except requests.exceptions.RequestException as e:
        print(f"[error] no pude leer del nodo: {e}")
        return

    if not mensajes:
        print("(todavia no hay mensajes)")
        return
    for m in mensajes:
        print(f"  {m['timestamp']}  {m['usuario']}: {m['texto']}")


def main():
    parser = argparse.ArgumentParser(description="Cliente de consola NodeMesh")
    parser.add_argument(
        "--nodo",
        default="http://localhost:5001",
        help="URL del nodo al que te conectas (default http://localhost:5001)",
    )
    args = parser.parse_args()
    base = args.nodo.rstrip("/")

    print(f"Conectado a {base}")
    usuario = input("Tu nombre de usuario: ").strip() or "anonimo"
    print("Escribe un mensaje y Enter para enviarlo.")
    print("Comandos: 'ver' muestra todos los mensajes, 'salir' termina.")

    while True:
        texto = input(f"{usuario}> ").strip()

        if texto == "salir":
            break
        if texto == "ver":
            mostrar_mensajes(base)
            continue
        if not texto:
            continue

        try:
            r = requests.post(
                f"{base}/mensajes",
                json={"usuario": usuario, "texto": texto},
                headers=HEADERS,
                timeout=5,
            )
            if r.status_code == 201:
                print("  [enviado]")
            else:
                print(f"  [el nodo respondio {r.status_code}: {r.text}]")
        except requests.exceptions.RequestException as e:
            print(f"  [error] no pude enviar al nodo: {e}")


if __name__ == "__main__":
    main()
