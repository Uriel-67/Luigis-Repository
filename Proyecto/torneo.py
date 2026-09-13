import datos
import operaciones
import interfaz


def ejecutarPartido(nombreEquipoLocal, nombreRival, listaJugadores):
    """Simula una partida ronda por ronda hasta que un equipo gane 3 rondas."""
    print("")
    print("==============================================================")
    print("INICIANDO PARTIDO:", nombreEquipoLocal, "vs", nombreRival)
    print("Formato: Mejor de 5 rondas (gana el primero en llegar a 3)")
    print("==============================================================")

    matrizPartido = datos.crearMatrizLimpia(len(listaJugadores))
    rondasGanadas = 0
    rondasPerdidas = 0
    numeroRonda = 1
    partidaEnCurso = True

    while partidaEnCurso:
        print("")
        print(">>> DISPUTANDO RONDA", numeroRonda, "<<<")

        victoria, bajasRonda, armados = operaciones.simularRonda(matrizPartido)

        if victoria:
            rondasGanadas = rondasGanadas + 1
            print("Resultado: Ronda GANADA por", nombreEquipoLocal, "| Armados:", armados, "| Bajas:", bajasRonda)
        else:
            rondasPerdidas = rondasPerdidas + 1
            print("Resultado: Ronda PERDIDA contra", nombreRival, "| Armados:", armados, "| Bajas:", bajasRonda)

        print("Marcador:", nombreEquipoLocal, rondasGanadas, "-", rondasPerdidas, nombreRival)
        interfaz.imprimirMatrizFormateada(matrizPartido, listaJugadores, f"ESTADISTICAS DE LA RONDA {numeroRonda}")

        numeroRonda = numeroRonda + 1

        if rondasGanadas == 3 or rondasPerdidas == 3:
            partidaEnCurso = False
        else:
            input("Presione ENTER para continuar a la siguiente ronda...")

    print("")
    if rondasGanadas == 3:
        ganador = nombreEquipoLocal
    else:
        ganador = nombreRival

    print("Fin del cruce: Ganador", ganador)
    return matrizPartido, ganador


def ejecutarTorneoCompleto(listaEquipos, matrizPlanteles, matrizGeneralTorneo, historialPartidas):
    """Ejecuta las dos semifinales y la final, guardando las matrices en memoria."""
    print("")
    print("Iniciando llave de eliminacion directa (4 equipos)...")

    # Partida 1: Semifinal 1 (Luminosity vs Fnatic)
    print("")
    print("--- FASE: SEMIFINAL 1 ---")
    matrizSemi1, ganadorSemi1 = ejecutarPartido(listaEquipos[0], listaEquipos[1], matrizPlanteles[0])
    historialPartidas.append(operaciones.copiarMatriz(matrizSemi1))
    operaciones.acumularEnMatrizGeneral(matrizGeneralTorneo, matrizSemi1)

    # Partida 2: Semifinal 2 (Navi vs Astralis)
    print("")
    print("--- FASE: SEMIFINAL 2 ---")
    matrizSemi2, ganadorSemi2 = ejecutarPartido(listaEquipos[2], listaEquipos[3], matrizPlanteles[2])
    historialPartidas.append(operaciones.copiarMatriz(matrizSemi2))

    # Partida 3: Gran Final (Ganador Semi 1 vs Ganador Semi 2)
    print("")
    print("--- FASE: GRAN FINAL ---")
    matrizFinal, campeon = ejecutarPartido(ganadorSemi1, ganadorSemi2, matrizPlanteles[0])
    historialPartidas.append(operaciones.copiarMatriz(matrizFinal))
    operaciones.acumularEnMatrizGeneral(matrizGeneralTorneo, matrizFinal)

    print("")
    print("¡EL TORNEO HA FINALIZADO!")
    print("CAMPEON DEL TORNEO:", campeon)
    print("Las 3 partidas fueron simuladas y registradas en memoria.")