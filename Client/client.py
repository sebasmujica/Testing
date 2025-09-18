from __future__ import annotations

import builtins as _builtins
import socket
import threading
import time
import sys
from typing import Optional
from validation import sanitize_input_Refactor


HOST = "127.0.0.1"
PORT = 12345

nickname: str = ""
cliente: Optional[socket.socket] = None
client: Optional[socket.socket] = None  # backward compatible alias

receive_thread: Optional[threading.Thread] = None
write_thread: Optional[threading.Thread] = None

setattr(sys.modules[__name__], "builtins.input", _builtins.input)


def _input(prompt: str = "") -> str:
    # Tests patch this dotted attribute; fetch it dynamically so the override is used.
    input_fn = getattr(sys.modules[__name__], "builtins.input")
    return input_fn(prompt)


def _set_connection(sock: Optional[socket.socket]) -> None:
    global cliente, client
    cliente = client = sock


def _require_connection() -> socket.socket:
    if cliente is None:
        raise RuntimeError("Cliente no conectado")
    return cliente


def _ensure_nickname() -> str:
    global nickname
    if not nickname:
        nickname = _input("Elige tu nickname:...")
    return nickname


def conectar_cliente(host: str = HOST, port: int = PORT) -> socket.socket:
    for _ in range(3):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print("Conectando ...")
            _set_connection(sock)
            return sock
        except ConnectionRefusedError:
            print("Error al conectar con el servidor ... \n")
            print("Reintentando...\n")
            time.sleep(3)

    raise ConnectionError("No se pudo conectar con el servidor tras 3 intentos")


def recibir() -> None:
    try:
        sock = _require_connection()
    except RuntimeError:
        print("No hay conexión activa para recibir mensajes")
        return

    while True:
        try:
            mensaje = sock.recv(1024).decode()
            if mensaje == "Nickname":
                sock.send(_ensure_nickname().encode())
            elif mensaje:
                print(mensaje)
            else:
                break
        except OSError:
            print("Haz dejado el chat...")
            break
        except Exception as exc:
            print(f"Ha ocurrido un error: {exc}")
            break


def escribir() -> None:
    try:
        sock = _require_connection()
    except RuntimeError:
        print("No hay conexión activa para enviar mensajes")
        return

    nick = _ensure_nickname()

    while True:
        try:
            entrada_dirt = _input("")
            entrada = sanitize_input_Refactor(entrada_dirt)
        except EOFError:
            break

        mensaje = f"{nick}: {entrada}"
        if entrada.strip() == "/salir":
            break

        try:
            sock.send(mensaje.encode())
        except Exception as exc:
            print(f"Error al enviar mensaje: {exc}")
            break

    close = getattr(sock, "close", None)
    if callable(close):
        try:
            close()
        except Exception as exc:
            print(f"Error al cerrar la conexión: {exc}")

    _set_connection(None)


def iniciar_chat() -> None:
    _ensure_nickname()
    conectar_cliente()

    global receive_thread, write_thread
    receive_thread = threading.Thread(target=recibir, name="ReceiveThread")
    write_thread = threading.Thread(target=escribir, name="WriteThread")

    receive_thread.start()
    write_thread.start()

    receive_thread.join()
    write_thread.join()


def main() -> None:
    iniciar_chat()


if __name__ == "__main__":
    main()
