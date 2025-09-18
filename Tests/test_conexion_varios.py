from __future__ import annotations
import pytest
from unittest.mock import Mock
from Server import server as server_module


@pytest.fixture()
def clientes_mock(request):
    server_module.clientes.clear()
    mock = [Mock() for _ in range(request.param)]
    yield mock
    server_module.clientes.clear()

@pytest.mark.parametrize("clientes_mock", [3], indirect=True)
def test_conexion_varios(clientes_mock, monkeypatch: pytest.MonkeyPatch):

    #Se crean clientes falsos
    c1, c2, c3 = clientes_mock
    
    srv = Mock(name="listening_socket")
    

    c1.recv.side_effect = [b"Dummy1"]
    c2.recv.side_effect = [b"Dummy2"]
    c3.recv.side_effect = [b"Dummy3"]
    srv.accept.side_effect = [(c1, ("127.0.0.1", 50000)),(c2, ("127.0.0.1", 50000)),(c3, ("127.0.0.1", 50000)), KeyboardInterrupt()]

    server_module.server = srv

    broadcast_mock = Mock(name="broadcast")
    monkeypatch.setattr(server_module, "broadcast", broadcast_mock)


    created_threads: list[tuple] = []

    def fake_thread(*, target=None, args=(), daemon=False):
        thread = Mock(name="thread")
        thread.start = Mock(name="start")
        created_threads.append((target, args, daemon, thread))
        return thread

    monkeypatch.setattr(server_module.threading,"Thread", fake_thread)

    with pytest.raises(KeyboardInterrupt):
        server_module.recibir()

    assert len(created_threads) == 3
    assert len(server_module.clientes) == 3
    for target, args, daemon, thread in created_threads:
        assert args in [(c1,),(c2,),(c3,)]
    
    server_module.server = None