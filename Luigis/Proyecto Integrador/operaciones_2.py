from validaciones_2 import (
    validarFormatoCodigo, validarFormatoFecha,
    convertirFechaANumero, existeAtletaRecursivo
)
from archivos_2 import guardarAtleta, guardarRegistro, exportarReporte

def registrarAtleta(padronAtletas, datosConfiguracion, codigoAtleta, nombreAtleta, categoriaAtleta):
    """Valida los campos e incorpora un nuevo atleta al padron."""
    if not validarFormatoCodigo(codigoAtleta):
        return False, "Formato de codigo invalido. Requiere 1 letra mayuscula y 2 digitos (ej: A01)."

    if codigoAtleta in padronAtletas:
        return False, "El atleta ya se encuentra registrado con ese codigo."

    if len(nombreAtleta) == 0:
        return False, "El nombre no puede estar vacio."

    categoriaValida = ""
    categoriaIngresadaLimpia = categoriaAtleta.strip().lower()

    for categoriaItem in datosConfiguracion["CATEGORIAS_ADMITIDAS"]:
        if categoriaItem.lower() == categoriaIngresadaLimpia:
            categoriaValida = categoriaItem

    if len(categoriaValida) == 0:
        textoCategorias = ""
        esPrimerElemento = True
        for cat in datosConfiguracion["CATEGORIAS_ADMITIDAS"]:
            if esPrimerElemento:
                textoCategorias = cat
                esPrimerElemento = False
            else:
                textoCategorias = textoCategorias + ", " + cat
        return False, "Categoria invalida. Opciones admitidas: " + textoCategorias + "."

    padronAtletas[codigoAtleta] = {"nombre": nombreAtleta, "categoria": categoriaValida}
    guardarAtleta(codigoAtleta, nombreAtleta, categoriaValida)
    return True, "Atleta registrado exitosamente."

def registrarMinutos(padronAtletas, historialRegistros, datosConfiguracion, codigoAtleta, fechaEntrenamiento, textoMinutos):
    """Valida y agrega un registro de entrenamiento con fecha completa y tope diario."""
    if codigoAtleta not in padronAtletas:
        return False, "El atleta indicado no existe en el padron registrado."

    if not validarFormatoFecha(fechaEntrenamiento):
        return False, "Formato de fecha invalido. Debe utilizar DD/MM/AAAA (ej: 05/10/2024)."

    try:
        minutosEntrenados = float(textoMinutos)
    except ValueError:
        return False, "Los minutos deben ser un valor numerico."

    if minutosEntrenados < 0:
        return False, "Los minutos no pueden ser un valor negativo."

    minutosAcumuladosDiarios = 0
    for sesion in historialRegistros:
        if sesion["codigo_atleta"] == codigoAtleta and sesion["fecha"] == fechaEntrenamiento:
            minutosAcumuladosDiarios += sesion["minutos"]

    if minutosAcumuladosDiarios + minutosEntrenados > datosConfiguracion["MAXIMO_DIARIO"]:
        minutosDisponibles = datosConfiguracion["MAXIMO_DIARIO"] - minutosAcumuladosDiarios
        return False, "Supera el maximo diario permitido (" + str(datosConfiguracion["MAXIMO_DIARIO"]) + " min). Minutos disponibles para ese dia: " + str(minutosDisponibles) + "."

    nuevoRegistroSesion = {"codigo_atleta": codigoAtleta, "fecha": fechaEntrenamiento, "minutos": minutosEntrenados}
    historialRegistros.append(nuevoRegistroSesion)
    guardarRegistro(codigoAtleta, fechaEntrenamiento, minutosEntrenados)
    return True, "Entrenamiento registrado exitosamente."

def reporteFiltrado(padronAtletas, historialRegistros, codigoAtleta):
    """Muestra el historial y la ficha de un atleta especifico localizandolo por clave."""
    if codigoAtleta not in padronAtletas:
        print("Atleta no encontrado en el sistema.")
        return

    datosAtleta = padronAtletas[codigoAtleta]
    print()
    print("Ficha del Atleta:", datosAtleta["nombre"], "| Categoria:", datosAtleta["categoria"])
    print("══════════════════════════════════════════════════════════════")
    minutosTotales = 0
    tieneActividadRegistrada = False
    for sesion in historialRegistros:
        if sesion["codigo_atleta"] == codigoAtleta:
            print("Fecha:", sesion["fecha"], "| Minutos:", sesion["minutos"])
            minutosTotales += sesion["minutos"]
            tieneActividadRegistrada = True

    if not tieneActividadRegistrada:
        print("Sin sesiones de entrenamiento registradas.")
    print("Total acumulado historico:", minutosTotales, "minutos.")

def reporteGeneral(padronAtletas, historialRegistros):
    """Calcula totales acumulados por categoria y global."""
    if len(historialRegistros) == 0:
        print("No hay registros historicos cargados.")
        return

    totalesPorCategoria = {}
    minutosTotalesGlobales = 0

    for sesion in historialRegistros:
        codigoAtleta = sesion["codigo_atleta"]
        if codigoAtleta in padronAtletas:
            nombreCategoria = padronAtletas[codigoAtleta]["categoria"]
            minutosSesion = sesion["minutos"]
            totalesPorCategoria[nombreCategoria] = totalesPorCategoria.get(nombreCategoria, 0) + minutosSesion
            minutosTotalesGlobales += minutosSesion

    print()
    print("Total historico global acumulado:", minutosTotalesGlobales, "minutos.")
    print("Desglose por categoria admitida:")
    for categoriaItem, minutosSubtotal in totalesPorCategoria.items():
        print(" * Categoria", categoriaItem + ":", minutosSubtotal, "minutos.")

def reporteAlertas(padronAtletas, historialRegistros, datosConfiguracion, fechaInicioTexto, fechaFinTexto):
    """
    Detecta atletas que no alcanzaron el objetivo semanal en un lapso de 7 dias,
    incluyendo explicitamente a los atletas registrados sin actividad (0 minutos).
    """
    if len(padronAtletas) == 0:
        print("No hay atletas registrados en el padron.")
        return

    if not validarFormatoFecha(fechaInicioTexto) or not validarFormatoFecha(fechaFinTexto):
        print("Fechas invalidas. Deben tener formato DD/MM/AAAA (ej: 01/10/2024 al 07/10/2024).")
        return

    numeroInicio = convertirFechaANumero(fechaInicioTexto)
    numeroFin = convertirFechaANumero(fechaFinTexto)

    if numeroInicio > numeroFin:
        print("Error de rango: La fecha de inicio debe ser anterior o igual a la fecha de fin.")
        return

    acumuladoresPeriodo = {}
    for codigoAtleta in padronAtletas:
        acumuladoresPeriodo[codigoAtleta] = 0

    for sesion in historialRegistros:
        if validarFormatoFecha(sesion["fecha"]):
            fechaSesionNumero = convertirFechaANumero(sesion["fecha"])
            if numeroInicio <= fechaSesionNumero <= numeroFin:
                codigoAtleta = sesion["codigo_atleta"]
                if codigoAtleta in acumuladoresPeriodo:
                    acumuladoresPeriodo[codigoAtleta] += sesion["minutos"]

    periodoIdentificador = fechaInicioTexto + " al " + fechaFinTexto
    textoSalida = "Atletas que no alcanzaron el objetivo semanal (" + str(datosConfiguracion["OBJETIVO_SEMANAL"]) + " min) entre " + periodoIdentificador + ":\n"
    existenAlertas = False

    for codigoAtleta, totalAcumulado in acumuladoresPeriodo.items():
        if totalAcumulado < datosConfiguracion["OBJETIVO_SEMANAL"]:
            nombreAtleta = padronAtletas[codigoAtleta]["nombre"]
            if totalAcumulado == 0:
                textoSalida += " - " + codigoAtleta + ": " + nombreAtleta + " (Sin actividad registrada: 0 min alcanzados)\n"
            else:
                textoSalida += " - " + codigoAtleta + ": " + nombreAtleta + " (" + str(totalAcumulado) + " min alcanzados)\n"
            existenAlertas = True

    if existenAlertas:
        print()
        print(textoSalida.rstrip("\n"))
        exportarReporte(textoSalida)
        print("Informe generado y exportado exitosamente a 'reporte.txt'.")
    else:
        print()
        print("Felicitaciones: Todos los atletas alcanzaron o superaron el objetivo semanal en el periodo.")

def resumenUnicos(historialRegistros):
    """Muestra cantidad e identificadores unicos mediante conjuntos."""
    codigosUnicos = set()
    for sesion in historialRegistros:
        codigosUnicos.add(sesion["codigo_atleta"])

    print()
    print("Cantidad total de atletas con actividad registrada:", len(codigosUnicos))
    print("Identificadores encontrados:")
    for codigoIdentificador in sorted(list(codigosUnicos)):
        print(" ->", codigoIdentificador)