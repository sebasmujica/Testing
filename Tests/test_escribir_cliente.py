from __future__ import annotations

from unittest.mock import Mock

import pytest

from Client import client as cliente


def test_escribir_envia_mensajes(monkeypatch: pytest.MonkeyPatch) -> None:
    socket_mock = Mock(spec=["send", "close"])

    monkeypatch.setattr(cliente, "builtins.input", Mock(side_effect=["Hola", "/salir"]))
    monkeypatch.setattr(cliente, "nickname", "Sebas")
    monkeypatch.setattr(cliente, "cliente", socket_mock)

    cliente.escribir()

    socket_mock.send.assert_called_once_with("Sebas: Hola".encode())
    socket_mock.close.assert_called_once_with()
