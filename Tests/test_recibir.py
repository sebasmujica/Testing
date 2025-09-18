from __future__ import annotations

from unittest.mock import Mock

import pytest

from Server import server as server_module


def test_recibir_registra_cliente(monkeypatch: pytest.MonkeyPatch) -> None:
    server_module.clientes.clear()

    srv = Mock(name="listening_socket")
    client = Mock(name="client_socket")

    client.recv.side_effect = [b"Dummy"]

    srv.accept.side_effect = [(client, ("127.0.0.1", 50000)), KeyboardInterrupt()]

    server_module.server = srv

    broadcast_mock = Mock(name="broadcast")
    monkeypatch.setattr(server_module, "broadcast", broadcast_mock)

    created_threads: list[tuple] = []

    def fake_thread(*, target=None, args=(), daemon=False):
        thread = Mock(name="thread")
        thread.start = Mock(name="start")
        created_threads.append((target, args, daemon, thread))
        return thread

    monkeypatch.setattr(server_module.threading, "Thread", fake_thread)

    with pytest.raises(KeyboardInterrupt):
        server_module.recibir()

    assert server_module.clientes[client] == "Dummy"

    assert client.settimeout.call_args_list == [((10,), {}), ((None,), {})]

    assert client.send.call_args_list[0].args[0] == b"Nickname"
    assert client.send.call_args_list[1].args[0] == b"Conectado al servidor como Dummy"

    broadcast_mock.assert_called_once_with(b"Dummy se unio al chat...", client)

    assert len(created_threads) == 1
    target, args, daemon, thread = created_threads[0]
    assert target is server_module.handle
    assert args == (client,)
    assert daemon is True
    thread.start.assert_called_once_with()

    server_module.server = None
    server_module.clientes.clear()
