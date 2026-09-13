import random
import datos


def copiarMatriz(matriz):
    """Hace una copia independiente de la matriz elemento por elemento."""
    copia = []
    for f in range(len(matriz)):
        filaNueva = []
        for c in range(len(matriz[0])):
            filaNueva.append(matriz[f][c])
        copia.append(filaNueva)
    return copia


def acumularEnMatrizGeneral(matrizGeneral, matrizPartido):
    """Suma las estadisticas de un partido jugado a la matriz global del torneo."""
    for f in range(len(matrizPartido)):
        matrizGeneral[f][datos.colKills] = matrizGeneral[f][datos.colKills] + matrizPartido[f][datos.colKills]
        matrizGeneral[f][datos.colDeaths] = matrizGeneral[f][datos.colDeaths] + matrizPartido[f][datos.colDeaths]
        matrizGeneral[f][datos.colAssists] = matrizGeneral[f][datos.colAssists] + matrizPartido[f][datos.colAssists]
        matrizGeneral[f][datos.colDinero] = matrizGeneral[f][datos.colDinero] + matrizPartido[f][datos.colDinero]
        matrizGeneral[f][datos.colRondas] = matrizGeneral[f][datos.colRondas] + matrizPartido[f][datos.colRondas]
        matrizGeneral[f][datos.colMvps] = matrizGeneral[f][datos.colMvps] + matrizPartido[f][datos.colMvps]


def procesarCompraAutomatica(matrizStats):
    """Descuenta la plata segun lo que alcanza y cuenta cuantos se armaron."""
    armados = 0
    for i in range(len(matrizStats)):
        saldo = matrizStats[i][datos.colDinero]
        if saldo >= datos.configEconomia[0]:
            matrizStats[i][datos.colDinero] = matrizStats[i][datos.colDinero] - datos.configEconomia[0]
            armados = armados + 1
        elif saldo >= datos.configEconomia[1]:
            matrizStats[i][datos.colDinero] = matrizStats[i][datos.colDinero] - datos.configEconomia[1]
            armados = armados + 1
    return armados


def calcularProbabilidad(armados):
    """Calcula el porcentaje de probabilidad de victoria segun los armados."""
    if armados == 5:
        return 80
    elif armados >= 3:
        return 50
    elif armados >= 1:
        return 35
    else:
        return 20


def simularRonda(matrizStats):
    """Simula una ronda de juego, reparte las bajas y actualiza la plata."""
    armados = procesarCompraAutomatica(matrizStats)
    probabilidad = calcularProbabilidad(armados)
    tirada = random.randint(1, 100)
    victoria = (tirada <= probabilidad)

    killsRonda = [0, 0, 0, 0, 0]
    if victoria:
        totalKills = 5
    else:
        totalKills = random.randint(0, 4)

    for k in range(totalKills):
        tirador = random.randint(0, 4)
        killsRonda[tirador] = killsRonda[tirador] + 1
        matrizStats[tirador][datos.colKills] = matrizStats[tirador][datos.colKills] + 1

        asistidor = random.randint(0, 4)
        if asistidor != tirador:
            matrizStats[asistidor][datos.colAssists] = matrizStats[asistidor][datos.colAssists] + 1

    if totalKills > 0:
        maxKills = killsRonda[0]
        idMvp = 0
        for i in range(1, len(killsRonda)):
            if killsRonda[i] > maxKills:
                maxKills = killsRonda[i]
                idMvp = i
        matrizStats[idMvp][datos.colMvps] = matrizStats[idMvp][datos.colMvps] + 1

    if victoria:
        premioRonda = datos.configEconomia[3]
    else:
        premioRonda = datos.configEconomia[4]

    for i in range(len(matrizStats)):
        matrizStats[i][datos.colRondas] = matrizStats[i][datos.colRondas] + 1
        if not victoria:
            matrizStats[i][datos.colDeaths] = matrizStats[i][datos.colDeaths] + 1

        ganancia = premioRonda + (killsRonda[i] * datos.configEconomia[2])
        nuevoSaldo = matrizStats[i][datos.colDinero] + ganancia
        if nuevoSaldo > datos.configEconomia[5]:
            matrizStats[i][datos.colDinero] = datos.configEconomia[5]
        else:
            matrizStats[i][datos.colDinero] = nuevoSaldo

    totalBajas = 0
    for b in killsRonda:
        totalBajas = totalBajas + b

    return victoria, totalBajas, armados


def calcularAcumulados(matrizStats):
    """Calcula el total de bajas y el dinero total de todo el equipo."""
    totalKills = 0
    totalDinero = 0
    for i in range(len(matrizStats)):
        totalKills = totalKills + matrizStats[i][datos.colKills]
        totalDinero = totalDinero + matrizStats[i][datos.colDinero]
    return totalKills, totalDinero


def verificarAlertaQuiebra(matrizStats):
    """Revisa si el saldo promedio del equipo baja de 2000 pesos."""
    totalKills, totalDinero = calcularAcumulados(matrizStats)
    promedio = totalDinero / len(matrizStats)
    estaEnQuiebra = (promedio < 2000)
    return estaEnQuiebra, promedio


def buscarMejorJugadorPorRondas(matrizStats, listaJugadores):
    """Busca al jugador con mayor promedio de bajas por ronda jugada."""
    mejores = []
    mejorPromedio = -1.0
    for i in range(len(matrizStats)):
        rondas = matrizStats[i][datos.colRondas]
        kills = matrizStats[i][datos.colKills]
        if rondas > 0:
            promedio = kills / rondas
        else:
            promedio = 0.0

        if promedio > mejorPromedio:
            mejorPromedio = promedio
            mejores = [listaJugadores[i]]
        elif promedio == mejorPromedio and mejorPromedio > 0:
            mejores.append(listaJugadores[i])
    return mejores, mejorPromedio


def generarRanking(matrizStats, listaJugadores):
    """Arma el ranking de jugadores ordenado de mayor a menor por bajas."""
    ranking = []
    for i in range(len(listaJugadores)):
        ranking.append((listaJugadores[i], matrizStats[i][datos.colKills], matrizStats[i][datos.colRondas]))
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking