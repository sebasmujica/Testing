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
def test_broadcasting(clientes_mock, monkeypatch: pytest.MonkeyPatch):
    
    #Se crean clientes falsos
    c1, c2, c3 = clientes_mock

    server_module.clientes[c1] = "Dummy1"
    server_module.clientes[c2] = "Dummy2"
    server_module.clientes[c3] = "Dummy3"

    server_module.broadcast(b"msj" , c1)

    c1.send.assert_not_called()
    c2.send.assert_called_once()
    c3.send.assert_called_once()




