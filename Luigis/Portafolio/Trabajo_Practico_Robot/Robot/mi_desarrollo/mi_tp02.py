# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones con Menu
#
#  Nombre y apellido: Uriel Aguilera Martinez - Valentino Segatori - Juan Cruz Ali
#  Comision:          Miercoles -TM
# =====================================================================

from robot import ErrorDeSeguridad, Robot
from misiones import MISIONES

VELOCIDAD_LINEAL_MAXIMA = 0.20   # m/s
VELOCIDAD_ANGULAR_MAXIMA = 0.50  # rad/s
TIEMPO_MAXIMO_ORDEN = 10.0       # segundos


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Evalua si la tupla cumple con tipo, estructura y limites."""
    esValido = True

    if type(comando) != tuple and type(comando) != list:
        esValido = False
    elif len(comando) == 0:
        esValido = False
    else:
        tipo = comando[0]

        if tipo == "detenerse" or tipo == "saludar":
            if len(comando) != 1:
                esValido = False

        elif tipo == "avanzar":
            if len(comando) != 3:
                esValido = False
            else:
                velocidad = comando[1]
                tiempo = comando[2]
                esNumeroVel = (type(velocidad) == int or type(velocidad) == float)
                esNumeroTiempo = (type(tiempo) == int or type(tiempo) == float)

                if not esNumeroVel or not esNumeroTiempo:
                    esValido = False
                elif velocidad <= 0 or velocidad > VELOCIDAD_LINEAL_MAXIMA:
                    esValido = False
                elif tiempo <= 0 or tiempo > TIEMPO_MAXIMO_ORDEN:
                    esValido = False

        elif tipo == "girar":
            if len(comando) != 3:
                esValido = False
            else:
                velocidad = comando[1]
                tiempo = comando[2]
                esNumeroVel = (type(velocidad) == int or type(velocidad) == float)
                esNumeroTiempo = (type(tiempo) == int or type(tiempo) == float)

                if not esNumeroVel or not esNumeroTiempo:
                    esValido = False
                elif velocidad == 0 or abs(velocidad) > VELOCIDAD_ANGULAR_MAXIMA:
                    esValido = False
                elif tiempo <= 0 or tiempo > TIEMPO_MAXIMO_ORDEN:
                    esValido = False
        else:
            esValido = False

    return esValido


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta una orden individual y atrapa excepciones del simulador."""
    tipo = comando[0]
    resultadoTexto = ""

    try:
        if tipo == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            resultadoTexto = f"Avanzo {comando[1]} m/s por {comando[2]} s"

        elif tipo == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
            resultadoTexto = f"Giro {comando[1]} rad/s por {comando[2]} s"

        elif tipo == "detenerse":
            robot.detenerse()
            resultadoTexto = "Robot detenido"

        elif tipo == "saludar":
            robot.saludar()
            resultadoTexto = "Saludo completado"

    except ErrorDeSeguridad as errSeguridad:
        resultadoTexto = f"Rechazado por seguridad: {errSeguridad}"

    return resultadoTexto


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la mision registrando estados en una lista homogenea."""
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║ INICIANDO MISION: {len(mision)} COMANDO(S) RECIBIDO(S)                      ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    for i in range(len(mision)):
        comandoActual = mision[i]

        if comando_es_valido(comandoActual):
            mensaje = ejecutar_comando(robot, comandoActual)
            if "Rechazado por seguridad" in mensaje:
                print(f"[RECHAZADO] {comandoActual} -> {mensaje}")
                historial.append(f"RECHAZADO: {comandoActual[0]} (Seguridad)")
            else:
                print(f"[OK] {comandoActual} -> {mensaje}")
                historial.append(f"OK: {comandoActual[0]}")
        else:
            print(f"[RECHAZADO] {comandoActual} -> Parametros invalidos")
            historial.append(f"RECHAZADO: {comandoActual[0]} (Validacion)")

    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║ MISION FINALIZADA                                                 ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra el resumen final utilizando caracteres de linea doble."""
    totalEjecutados = 0
    totalRechazados = 0

    for i in range(len(historial)):
        registro = historial[i]
        if registro.startswith("OK"):
            totalEjecutados += 1
        else:
            totalRechazados += 1

    totalComandos = len(historial)

    print("╔════════════════════════════════════╦══════════════════════════════╗")
    print("║ METRICA                            ║ VALOR                        ║")
    print("╠════════════════════════════════════╬══════════════════════════════╣")
    print(f"║ Total de comandos procesados       ║ {totalComandos:<28} ║")
    print("╠════════════════════════════════════╬══════════════════════════════╣")
    print(f"║ Comandos ejecutados con exito      ║ {totalEjecutados:<28} ║")
    print("╠════════════════════════════════════╬══════════════════════════════╣")
    print(f"║ Comandos rechazados / omitidos     ║ {totalRechazados:<28} ║")
    print("╚════════════════════════════════════╩══════════════════════════════╝")

    if totalRechazados > 0:
        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║ DETALLE DE COMANDOS RECHAZADOS                                    ║")
        print("╠═══════════════════════════════════════════════════════════════════╣")
        for i in range(len(historial)):
            if not historial[i].startswith("OK"):
                detalle = historial[i]
                print(f"║ * {detalle:<63} ║")
        print("╚═══════════════════════════════════════════════════════════════════╝\n")


# =====================================================================
#  INTERFAZ DE USUARIO: MENU PRINCIPAL
# =====================================================================
def mostrarMenu():
    """Imprime el menu utilizando el marco con caracteres especiales."""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                  CONTROLADOR DE MISIONES - GO2                    ║")
    print("╠═══════════════════════════════════════════════════════════════════╣")
    print("║ 1. Mision Basica                                                  ║")
    print("║ 2. Mision Cuadrado                                                ║")
    print("║ 3. Mision con Errores                                             ║")
    print("║ 4. Mision Larga                                                   ║")
    print("║ 5. Salir                                                          ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")


def main():
    robot = Robot()
    robot.conectar()

    continuarPrograma = True

    try:
        while continuarPrograma:
            mostrarMenu()
            entrada = input("Seleccione una mision (1-5): ").strip()

            if entrada.isdigit():
                opcion = int(entrada)
            else:
                opcion = 0

            misionElegida = None

            if opcion == 1:
                misionElegida = MISIONES["basica"]
            elif opcion == 2:
                misionElegida = MISIONES["cuadrado"]
            elif opcion == 3:
                misionElegida = MISIONES["errores"]
            elif opcion == 4:
                misionElegida = MISIONES["larga"]
            elif opcion == 5:
                print("\nCerrando conexion con el simulador...")
                continuarPrograma = False
            else:
                print("\nOpcion invalida. Ingrese un numero del 1 al 5.\n")

            if misionElegida != None:
                historial = []
                ejecutar_mision(robot, misionElegida, historial)
                generar_reporte(historial)

    finally:
        robot.detenerse()
        robot.desconectar()


main()