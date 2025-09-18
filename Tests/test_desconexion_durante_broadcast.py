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
def test_broadcast_desconexion_inesperada_remueve_cliente(clientes_mock,monkeypatch: pytest.MonkeyPatch):
    c_emisor, c_ok, c_desconexion = clientes_mock

    server_module.clientes[c_emisor] = "Dummy1"
    server_module.clientes[c_ok] = "Dummy2"
    server_module.clientes[c_desconexion] = "Dummy3"

    c_desconexion.send.side_effect = BrokenPipeError("Desconexion")

    sacar_cliente_mock = Mock(name="sacar_cliente")
    monkeypatch.setattr(server_module,"sacar_cliente",sacar_cliente_mock)

    mensaje = b"msj"
    server_module.broadcast(mensaje, c_emisor)

    c_emisor.send.assert_not_called()
    c_ok.send.assert_called_once_with(mensaje)
    sacar_cliente_mock.assert_called_once()



