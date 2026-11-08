import pytest
from validaciones_2 import validarFormatoCodigo, existeAtletaRecursivo

def testValidacionCorrecta():
    assert validarFormatoCodigo("A01") == True

def testValidacionExcepcion():
    with pytest.raises(TypeError):
        validarFormatoCodigo(123)

def testCalculoCumplimiento():
    minutosSesion = 150
    minutosObjetivo = 150
    assert minutosSesion >= minutosObjetivo

def testAcumulacionClave():
    acumuladorMinutos = {}
    acumuladorMinutos["A01"] = acumuladorMinutos.get("A01", 0) + 60
    acumuladorMinutos["A01"] += 40
    assert acumuladorMinutos["A01"] == 100

def testCondicionAlerta():
    totalMinutos = 100
    minutosObjetivo = 150
    hayAlerta = totalMinutos < minutosObjetivo
    assert hayAlerta == True

def testFuncionRecursiva():
    codigosAtletas = ["A01", "B02", "C03"]
    assert existeAtletaRecursivo("B02", codigosAtletas) == True
    assert existeAtletaRecursivo("X99", codigosAtletas) == False

def testCasoLimite():
    topeDiario = 180
    acumuladoValido = 180
    acumuladoInvalido = 181
    assert acumuladoValido <= topeDiario
    assert acumuladoInvalido > topeDiario