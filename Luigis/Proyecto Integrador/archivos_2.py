import json

def cargarConfiguracion():
    """
    Carga los parametros de configuracion desde configuracion.json.
    Si el archivo no existe o es corrupto, no se reemplaza por defecto y se retorna None.
    """
    try:
        with open("configuracion.json", "rt", encoding="utf-8") as archivoConfiguracion:
            return json.load(archivoConfiguracion)
    except FileNotFoundError:
        print("Error critico: No se encontro el archivo obligatorio 'configuracion.json'.")
        return None
    except (ValueError, OSError) as errorCarga:
        print("Error critico: El archivo 'configuracion.json' esta corrupto o es invalido:", errorCarga)
        return None

def cargarUsuarios():
    """Carga las credenciales de usuarios desde usuarios.csv de forma secuencial."""
    directorioUsuarios = {}
    try:
        with open("usuarios.csv", "rt", encoding="utf-8") as archivoUsuarios:
            archivoUsuarios.readline()
            for lineaTexto in archivoUsuarios:
                lineaLimpia = lineaTexto.rstrip("\n")
                camposRegistro = lineaLimpia.split(";")
                if len(camposRegistro) == 2:
                    nombreUsuario = camposRegistro[0].strip()
                    claveUsuario = camposRegistro[1].strip()
                    directorioUsuarios[nombreUsuario] = claveUsuario
    except (FileNotFoundError, OSError):
        pass
    return directorioUsuarios

def cargarAtletas():
    """Carga el padron de atletas en un diccionario en memoria."""
    padronAtletas = {}
    try:
        with open("atletas.csv", "rt", encoding="utf-8") as archivoAtletas:
            archivoAtletas.readline()
            for lineaTexto in archivoAtletas:
                lineaLimpia = lineaTexto.rstrip("\n")
                camposRegistro = lineaLimpia.split(";")
                if len(camposRegistro) == 3:
                    codigoAtleta = camposRegistro[0].strip()
                    nombreAtleta = camposRegistro[1].strip()
                    categoriaAtleta = camposRegistro[2].strip()
                    padronAtletas[codigoAtleta] = {
                        "nombre": nombreAtleta,
                        "categoria": categoriaAtleta
                    }
    except (FileNotFoundError, OSError):
        pass
    return padronAtletas

def guardarAtleta(codigoAtleta, nombreAtleta, categoriaAtleta):
    """Guarda un nuevo atleta en atletas.csv asegurando persistencia."""
    archivoExiste = False
    try:
        with open("atletas.csv", "rt", encoding="utf-8") as archivoComprobacion:
            archivoExiste = True
    except FileNotFoundError:
        archivoExiste = False

    try:
        with open("atletas.csv", "at", encoding="utf-8") as archivoEscritura:
            if not archivoExiste:
                archivoEscritura.write("codigo_atleta;nombre;categoria\n")
            lineaRegistro = codigoAtleta + ";" + nombreAtleta + ";" + categoriaAtleta + "\n"
            archivoEscritura.write(lineaRegistro)
    except OSError:
        print("Error de disco al intentar guardar el atleta.")

def cargarRegistros():
    """Carga el historial de entrenamientos con fecha completa desde registros.csv."""
    historialRegistros = []
    try:
        with open("registros.csv", "rt", encoding="utf-8") as archivoRegistros:
            archivoRegistros.readline()
            for lineaTexto in archivoRegistros:
                lineaLimpia = lineaTexto.rstrip("\n")
                camposRegistro = lineaLimpia.split(";")
                if len(camposRegistro) == 3:
                    try:
                        minutosEntrenados = float(camposRegistro[2])
                        historialRegistros.append({
                            "codigo_atleta": camposRegistro[0].strip(),
                            "fecha": camposRegistro[1].strip(),
                            "minutos": minutosEntrenados
                        })
                    except ValueError:
                        pass
    except (FileNotFoundError, OSError):
        pass
    return historialRegistros

def guardarRegistro(codigoAtleta, fechaEntrenamiento, minutosEntrenados):
    """Persiste una sesion de entrenamiento en registros.csv."""
    archivoExiste = False
    try:
        with open("registros.csv", "rt", encoding="utf-8") as archivoComprobacion:
            archivoExiste = True
    except FileNotFoundError:
        archivoExiste = False

    try:
        with open("registros.csv", "at", encoding="utf-8") as archivoEscritura:
            if not archivoExiste:
                archivoEscritura.write("codigo_atleta;fecha;minutos\n")
            lineaRegistro = codigoAtleta + ";" + fechaEntrenamiento + ";" + str(minutosEntrenados) + "\n"
            archivoEscritura.write(lineaRegistro)
    except OSError:
        print("Error de disco al intentar guardar el registro.")

def exportarReporte(textoReporte):
    """Exporta el reporte de texto plano a reporte.txt."""
    try:
        with open("reporte.txt", "wt", encoding="utf-8") as archivoReporte:
            archivoReporte.write(textoReporte)
    except OSError:
        print("Error de disco al intentar escribir reporte.txt.")