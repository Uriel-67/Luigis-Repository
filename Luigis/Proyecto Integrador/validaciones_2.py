import re

def validarFormatoCodigo(codigoIngresado):
    """Valida patron de 1 letra mayuscula y 2 numeros mediante expresiones regulares."""
    try:
        patronCodigo = r"^[A-Z][0-9]{2}$"
        if re.search(patronCodigo, codigoIngresado):
            return True
        return False
    except (TypeError, AttributeError):
        raise TypeError("El codigo debe ser una cadena de texto.")

def validarFormatoUsuario(usuarioIngresado):
    """Valida formato alfanumerico de 4 a 10 caracteres."""
    try:
        patronUsuario = r"^[a-zA-Z0-9]{4,10}$"
        if re.search(patronUsuario, usuarioIngresado):
            return True
        return False
    except (TypeError, AttributeError):
        return False

def validarFormatoFecha(fechaIngresada):
    """Valida el formato DD/MM/AAAA mediante expresion regular y
    comprueba la coherencia numerica de dias (1-31) y meses (1-12)."""
    try:
        patronFecha = r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$"
        if not re.search(patronFecha, fechaIngresada):
            return False

        partesFecha = fechaIngresada.split("/")
        diaValor = int(partesFecha[0])
        mesValor = int(partesFecha[1])
        anioValor = int(partesFecha[2])

        if mesValor < 1 or mesValor > 12:
            return False
        if diaValor < 1 or diaValor > 31:
            return False
        if anioValor < 1900 or anioValor > 2100:
            return False

        return True
    except (TypeError, AttributeError, ValueError):
        return False

def convertirFechaANumero(fechaTexto):
    """Convierte una fecha DD/MM/AAAA a un entero AAAAEMMDD para comparacion lineal."""
    partesFecha = fechaTexto.split("/")
    diaValor = int(partesFecha[0])
    mesValor = int(partesFecha[1])
    anioValor = int(partesFecha[2])
    return anioValor * 10000 + mesValor * 100 + diaValor

def existeAtletaRecursivo(codigoBuscado, listaCodigos, indicePosicion=0):
    """Busqueda lineal recursiva con caso base identificable sobre coleccion de codigos."""
    if indicePosicion >= len(listaCodigos):
        return False
    if listaCodigos[indicePosicion] == codigoBuscado:
        return True
    return existeAtletaRecursivo(codigoBuscado, listaCodigos, indicePosicion + 1)