import re

"""FUNCION VALIDAR CODIGO"""
def validar_formato_codigo(codigo):
    patron = r"^[A-Z][0-9]{2}$"
    if re.search(patron, codigo):
        return True
    return False

"""FUNCION VALIDAR USUARIO"""
def validar_formato_usuario(usuario):
    patron = r"^[a-zA-Z0-9]{4,10}$"
    if re.search(patron, usuario):
        return True
    return False

"""FUNCION BUSQUEDA RECURSIVA ATLETA"""
def existe_atleta_recursivo(codigo, lista_codigos, indice=0):
    if indice >= len(lista_codigos):
        return False
    if lista_codigos[indice] == codigo:
        return True
    return existe_atleta_recursivo(codigo, lista_codigos, indice + 1)