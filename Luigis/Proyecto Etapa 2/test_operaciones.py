import pytest
from validaciones_2 import validar_formato_codigo, existe_atleta_recursivo

"""FUNCION TEST VALIDACION CORRECTA"""
def test_validacion_correcta():
    assert validar_formato_codigo("A01") == True

"""FUNCION TEST VALIDACION EXCEPCION"""
def test_validacion_excepcion():
    with pytest.raises(TypeError):
        validar_formato_codigo(123)

"""FUNCION TEST CUMPLIMIENTO"""
def test_calculo_cumplimiento():
    minutos = 150
    objetivo = 150
    assert minutos >= objetivo

"""FUNCION TEST ACUMULACION"""
def test_acumulacion_clave():
    acumulador = {}
    acumulador["A01"] = acumulador.get("A01", 0) + 60
    acumulador["A01"] += 40
    assert acumulador["A01"] == 100

"""FUNCION TEST CONDICION ALERTA"""
def test_condicion_alerta():
    total = 100
    objetivo = 150
    alerta = total < objetivo
    assert alerta == True

"""FUNCION TEST RECURSIVIDAD"""
def test_funcion_recursiva():
    codigos = ["A01", "B02", "C03"]
    assert existe_atleta_recursivo("B02", codigos) == True
    assert existe_atleta_recursivo("X99", codigos) == False

"""FUNCION TEST CASO LIMITE"""
def test_caso_limite():
    tope = 180
    acumulado_valido = 180
    acumulado_invalido = 181
    assert acumulado_valido <= tope
    assert acumulado_invalido > tope