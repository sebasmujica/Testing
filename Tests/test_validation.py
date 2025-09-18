import pytest
from validation import *
class TestValidation:
    @pytest.mark.parametrize("txt",["hola", " hola ", "hola\n", "😃", "a"*100])
    def test_valid(self,txt):
        assert is_valid(txt) is True

    @pytest.mark.parametrize("txt",["", "  ", "\n", "\r\n", None])
    def test_invalid_empty(self,txt):
        assert is_valid(txt) is False

    def test_too_long(self):
        assert is_valid("a"*150) is False


#Prueba TDD
#RED
'''@pytest.mark.parametrize(("entrada", "esperado"), [
    ("  hola  ", "hola"),
    ("a\r\nb\r\n", "a\nb\n"),
    ("\t x \t", "x")
])
def test_sanitize_red(entrada, esperado):
    assert sanitize_input_Red(entrada) == esperado'''


#GREEN
@pytest.mark.parametrize(("entrada", "esperado"), [
    ("  hola  ", "hola"),
    ("a\r\nb\r\n", "a\nb\n"),
    ("\ra\rb", "\na\nb"),
    ("\t x \t", "x")
])
def test_sanitize_green(entrada, esperado):
    assert sanitize_input_Green(entrada) == esperado


#Refactor
@pytest.mark.parametrize(("entrada", "esperado"), [
    ("  hola  ", "hola"),
    ("a\r\nb\r\n", "a\nb\n"),
    ("\t x \t", "x")
])
def test_sanitize_refactor(entrada, esperado):
    assert sanitize_input_Refactor(entrada) == esperado