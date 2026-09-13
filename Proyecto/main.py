import datos
import torneo
import interfaz


def main():
    listaEquipos = ["Luminosity", "Fnatic", "Navi", "Astralis"]
    matrizPlanteles = [
        ["Coldzera", "FalleN", "Fer", "Taco", "Fnx"],
        ["Olofmeister", "Flusha", "JW", "Krimz", "Dennis"],
        ["Simple", "Flamie", "Edward", "Zeus", "Guardian"],
        ["Device", "Dupreeh", "Xyp9x", "Kjaerbye", "Gla1ve"]
    ]

    miEquipo = matrizPlanteles[0]
    matrizGeneralTorneo = datos.crearMatrizGeneral(len(miEquipo))
    historialPartidas = []
    nombresPartidas = [
        f"Semifinal 1 ({listaEquipos[0]} vs {listaEquipos[1]})",
        f"Semifinal 2 ({listaEquipos[2]} vs {listaEquipos[3]})",
        f"Gran Final"
    ]
    torneoJugado = False

    continuarMenu = True
    while continuarMenu:
        print("")
        interfaz.mostrarMenuCuadro()
        entrada = input("Seleccione una opcion (1-5): ")

        if entrada.isdigit():
            opcion = int(entrada)
        else:
            opcion = 0

        if opcion == 1:
            if torneoJugado:
                print("El torneo ya fue disputado. Consulte los resultados en el menu.")
            else:
                torneo.ejecutarTorneoCompleto(listaEquipos, matrizPlanteles, matrizGeneralTorneo, historialPartidas)
                torneoJugado = True

        elif opcion == 2:
            if not torneoJugado:
                print("Aun no se jugaron partidos. Ejecute la opcion 1 primero.")
            else:
                interfaz.consultarJugador(matrizGeneralTorneo, miEquipo)

        elif opcion == 3:
            if not torneoJugado:
                print("Aun no hay historial registrado. Ejecute la opcion 1 primero.")
            else:
                interfaz.consultarHistorialPartidas(historialPartidas, nombresPartidas, matrizPlanteles)

        elif opcion == 4:
            if not torneoJugado:
                print("Aun no hay estadisticas del torneo. Juegue primero la opcion 1.")
            else:
                interfaz.mostrarReportesGlobales(matrizGeneralTorneo, miEquipo)

        elif opcion == 5:
            print("Cerrando el simulador de torneos.")
            continuarMenu = False

        else:
            print("Opcion incorrecta. Ingrese un valor del 1 al 5.")


if __name__ == "__main__":
    main()