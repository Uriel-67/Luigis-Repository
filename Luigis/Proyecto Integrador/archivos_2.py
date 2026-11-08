import json

"""FUNCION CARGAR CONFIGURACION"""
def cargar_configuracion():
    try:
        with open("configuracion.json", "rt", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, ValueError, OSError):
        print("Archivo configuracion.json faltante o invalido. Usando defecto.")
        return {
            "MAXIMO_DIARIO": 180,
            "OBJETIVO_SEMANAL": 150,
            "CATEGORIAS_ADMITIDAS": ["Infantiles", "Cadetes", "Juveniles", "Mayores"]
        }

"""FUNCION CARGAR USUARIOS"""
def cargar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.csv", "rt", encoding="utf-8") as archivo:
            archivo.readline()
            for linea in archivo:
                campos = linea.rstrip("\n").split(";")
                if len(campos) == 2:
                    usuarios[campos[0]] = campos[1]
    except (FileNotFoundError, OSError):
        pass
    return usuarios

"""FUNCION CARGAR ATLETAS"""
def cargar_atletas():
    atletas = {}
    try:
        with open("atletas.csv", "rt", encoding="utf-8") as archivo:
            archivo.readline()
            for linea in archivo:
                campos = linea.rstrip("\n").split(";")
                if len(campos) == 3:
                    atletas[campos[0]] = {
                        "nombre": campos[1],
                        "categoria": campos[2]
                    }
    except (FileNotFoundError, OSError):
        pass
    return atletas

"""FUNCION GUARDAR ATLETA"""
def guardar_atleta(codigo, nombre, categoria):
    existe = False
    try:
        with open("atletas.csv", "rt", encoding="utf-8") as archivo:
            existe = True
    except FileNotFoundError:
        pass
        
    try:
        with open("atletas.csv", "at", encoding="utf-8") as archivo:
            if not existe:
                archivo.write("codigo_atleta;nombre;categoria\n")
            archivo.write(codigo + ";" + nombre + ";" + categoria + "\n")
    except OSError:
        print("Error al guardar atleta.")

"""FUNCION CARGAR REGISTROS"""
def cargar_registros():
    registros = []
    try:
        with open("registros.csv", "rt", encoding="utf-8") as archivo:
            archivo.readline()
            for linea in archivo:
                campos = linea.rstrip("\n").split(";")
                if len(campos) == 3:
                    try:
                        minutos = float(campos[2])
                        registros.append({
                            "codigo_atleta": campos[0],
                            "dia": campos[1],
                            "minutos": minutos
                        })
                    except ValueError:
                        pass
    except (FileNotFoundError, OSError):
        pass
    return registros

"""FUNCION GUARDAR REGISTRO"""
def guardar_registro(codigo, dia, minutos):
    existe = False
    try:
        with open("registros.csv", "rt", encoding="utf-8") as archivo:
            existe = True
    except FileNotFoundError:
        pass
        
    try:
        with open("registros.csv", "at", encoding="utf-8") as archivo:
            if not existe:
                archivo.write("codigo_atleta;dia;minutos\n")
            archivo.write(codigo + ";" + dia + ";" + str(minutos) + "\n")
    except OSError:
        print("Error al guardar registro.")

"""FUNCION EXPORTAR REPORTES"""
def exportar_reporte(texto):
    try:
        with open("reporte.txt", "wt", encoding="utf-8") as archivo:
            archivo.write(texto)
    except OSError:
        print("Error al escribir el reporte.")