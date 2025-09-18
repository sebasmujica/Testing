from __future__ import annotations
from Server import server as server_module
from unittest.mock import Mock
import pytest

def test_sacar_cliente(monkeypatch: pytest.MonkeyPatch) -> None:
    server_module.clientes.clear()
    
    cliente1 = Mock(name="Cliente1")
    cliente2 = Mock(name="Cliente2")
    server_module.clientes[cliente1] = "Dummy"
    server_module.clientes[cliente2] = "Dummy2"

    broadcast_mock = Mock("broadcast")

    monkeypatch.setattr(server_module,"broadcast",broadcast_mock)

    server_module.sacar_cliente(cliente1)

    assert cliente2 in server_module.clientes