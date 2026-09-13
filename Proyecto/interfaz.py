import datos
import operaciones


def mostrarMenuCuadro():
    """Muestra el menu principal de opciones en la terminal."""
    print("+--------------------------------------------------------------+")
    print("|                SISTEMA DE TORNEOS DE ESPORTS                 |")
    print("+--------------------------------------------------------------+")
    print("| 1. Simular Torneo Completo (4 Equipos: Semis y Final)        |")
    print("| 2. Consultar Metricas de un Jugador por ID                   |")
    print("| 3. Ver Historial de Matrices por Partida                     |")
    print("| 4. Informes Generales y Ranking Global                       |")
    print("| 5. Salir del Programa                                        |")
    print("+--------------------------------------------------------------+")


def imprimirMatrizFormateada(matriz, listaJugadores, titulo):
    """Muestra una matriz en pantalla con formato de tabla prolijo."""
    print("")
    print("---", titulo, "---")
    print("+--------------+-------+--------+---------+---------+--------+------+")
    print("| Jugador      | Kills | Deaths | Assists | Dinero  | Rondas | MVPs |")
    print("+--------------+-------+--------+---------+---------+--------+------+")
    for i in range(len(listaJugadores)):
        s = matriz[i]
        nombre = f"{listaJugadores[i]:<12}"
        print(f"| {nombre} | {s[0]:<5} | {s[1]:<6} | {s[2]:<7} | ${s[3]:<6} | {s[4]:<6} | {s[5]:<4} |")
    print("+--------------+-------+--------+---------+---------+--------+------+")


def mostrarFichaIndividual(idJugador, listaJugadores, matrizGeneral):
    """Imprime los datos estadisticos detallados de un solo jugador."""
    rondas = matrizGeneral[idJugador][datos.colRondas]
    kills = matrizGeneral[idJugador][datos.colKills]
    if rondas > 0:
        promedio = round(kills / rondas, 2)
    else:
        promedio = 0.0

    print("")
    print("+----------------------------------------------------+")
    print("| FICHA DEL JUGADOR:", listaJugadores[idJugador])
    print("+----------------------------------------------------+")
    print("| ID Posicional       :", idJugador)
    print("| Bajas Totales       :", kills)
    print("| Muertes Totales     :", matrizGeneral[idJugador][datos.colDeaths])
    print("| Asistencias Totales :", matrizGeneral[idJugador][datos.colAssists])
    print("| Dinero Acumulado    : $", matrizGeneral[idJugador][datos.colDinero])
    print("| Rondas Jugadas      :", rondas)
    print("| MVPs Obtenidos      :", matrizGeneral[idJugador][datos.colMvps])
    print("| Promedio Kills/Ronda:", promedio)
    print("+----------------------------------------------------+")


def consultarJugador(matrizGeneral, listaJugadores):
    """Pide un ID al usuario, valida el numero y muestra la ficha del jugador."""
    idValido = False
    idJugador = 0
    while not idValido:
        entrada = input("Ingrese el ID del jugador (0 a 4): ")
        if entrada.isdigit():
            idNumero = int(entrada)
            if idNumero >= 0 and idNumero < len(listaJugadores):
                idJugador = idNumero
                idValido = True
            else:
                print("Error: El ID debe estar entre 0 y 4.")
        else:
            print("Error: Debe ingresar un numero entero.")

    mostrarFichaIndividual(idJugador, listaJugadores, matrizGeneral)


def mostrarReportesGlobales(matrizGeneral, listaJugadores):
    """Calcula e imprime los cinco informes y rankings generales del torneo."""
    print("")
    print("==============================================================")
    print("                INFORMES GLOBALES DEL TORNEO                  ")
    print("==============================================================")

    imprimirMatrizFormateada(matrizGeneral, listaJugadores, "MATRIZ CONSOLIDADA DEL EQUIPO")

    totalKills, totalDinero = operaciones.calcularAcumulados(matrizGeneral)
    print("")
    print("1. ACUMULADOS:")
    print("   Total de bajas en el torneo:", totalKills)
    print("   Dinero total administrado: $", totalDinero)

    quiebra, promedio = operaciones.verificarAlertaQuiebra(matrizGeneral)
    print("")
    print("2. REPORTE FINANCIERO:")
    print("   Saldo promedio por jugador: $", round(promedio, 2))
    if quiebra:
        print("   ALERTA: Situacion critica / Quiebra (Promedio menor a $2000)")
    else:
        print("   ESTADO: Economia solvente")

    jugadoresMvp = [listaJugadores[i] for i in range(len(matrizGeneral)) if matrizGeneral[i][datos.colMvps] > 0]
    print("")
    print("3. JUGADORES CLAVE (AL MENOS 1 MVP):")
    print("   Cantidad con MVP:", len(jugadoresMvp))
    for nombre in jugadoresMvp:
        print("   *", nombre)

    ranking = operaciones.generarRanking(matrizGeneral, listaJugadores)
    topTres = ranking[:3]
    print("")
    print("4. RANKING POR BAJAS (TOP 3):")
    for pos in range(len(topTres)):
        print(f"   {pos + 1}. {topTres[pos][0]} con {topTres[pos][1]} kills en {topTres[pos][2]} rondas")

    mejoresPorRonda, mejorPromedio = operaciones.buscarMejorJugadorPorRondas(matrizGeneral, listaJugadores)
    print("")
    print("5. MEJOR JUGADOR RELATIVO (KILLS / RONDA):")
    for j in mejoresPorRonda:
        print("   *", j, "con promedio de", round(mejorPromedio, 2), "bajas por ronda")


def consultarHistorialPartidas(historialPartidas, nombresPartidas, matrizPlanteles):
    """Muestra la lista de partidas jugadas y permite abrir las estadisticas de una."""
    print("")
    print("--- HISTORIAL DE PARTIDAS ALMACENADAS ---")
    for i in range(len(historialPartidas)):
        print(f"{i + 1}. {nombresPartidas[i]}")

    seleccionValida = False
    while not seleccionValida:
        entradaP = input("Seleccione el numero de partida a ver (1-3): ")
        if entradaP.isdigit():
            idx = int(entradaP)
            if idx >= 1 and idx <= len(historialPartidas):
                plantelAMostrar = matrizPlanteles[0] if idx != 2 else matrizPlanteles[2]
                imprimirMatrizFormateada(
                    historialPartidas[idx - 1],
                    plantelAMostrar,
                    f"ESTADISTICAS FINALES DE {nombresPartidas[idx - 1]}"
                )
                seleccionValida = True
            else:
                print("Numero fuera de rango.")
        else:
            print("Ingrese un numero entero.")