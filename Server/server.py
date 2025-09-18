from __future__ import annotations

import socket
import threading
from typing import Optional


HOST = '127.0.0.1'
PORT = 12345

lock: threading.Lock = threading.Lock()

server: Optional[socket.socket] = None

clientes: dict[socket.socket, str] = {}


def configure_server(host: str = HOST, port: int = PORT) -> socket.socket:

    global server

    if server is not None:
        raise RuntimeError("El servidor ya fue configurado")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((host, port))
    srv.listen()
    server = srv
    return srv


def get_server() -> socket.socket:
    if server is None:
        raise RuntimeError("El servidor no está configurado")
    return server


def sacar_cliente(cliente: socket.socket) -> None:
    try:
        nickname = clientes[cliente]
        del clientes[cliente]
        cliente.close()
        print(f"{nickname} salio")
        broadcast(f'{nickname} dejo el chat...'.encode(), cliente)
        print(f"\nClientes conectados : {len(clientes)}")
    except Exception:
        print('No se pudo sacar cliente')


def broadcast(mensaje: bytes, client: socket.socket) -> None:
    with lock:
        for cliente in list(clientes.keys()):
            if cliente != client:
                try:
                    cliente.send(mensaje)
                except Exception:
                    sacar_cliente(cliente)


def handle(client: socket.socket) -> None:
    while True:
        try:
            mensaje = client.recv(1024)
            if mensaje:
                
                broadcast(mensaje, client)
            else:
                break
        except Exception:
            print("error al manejar cliente")
            break
    sacar_cliente(client)


def recibir() -> None:
    while True:
        srv = get_server()
        client, address = srv.accept()
        client.settimeout(10)
        try:
            client.send('Nickname'.encode())
            nickname = client.recv(1024).decode()
            client.settimeout(None)
        except socket.timeout:
            print("Cliente no envio su nickname")
            client.close()
            continue

        with lock:
            clientes[client] = nickname

        print(f"Nickname of the client is: {nickname} ")
        broadcast(f"{nickname} se unio al chat...".encode(), client)
        client.send(f"Conectado al servidor como {nickname}".encode())
        print(f"\nClientes conectados : {len(clientes)}")

        thread: threading.Thread = threading.Thread(target=handle, args=(client,), daemon=True)
        thread.start()


def main() -> None:
    srv = configure_server()
    print('Servidor abierto...')
    try:
        recibir()
    except KeyboardInterrupt:
        print("\nServidor interrumpido")
    finally:
        clientes.clear()
        print("\nServidor Cerrado")
        srv.close()


if __name__ == "__main__":
    main()
