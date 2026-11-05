# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones con Menu
#
#  Integrantes: Uriel Aguilera Martinez - Valentino Segatori - Juan Cruz Ali
#  Comision:    Miercoles - TM
# =====================================================================

from robot import ErrorDeSeguridad, Robot
from misiones import MISIONES

velocidadLinealMaxima = 0.20   # m/s
velocidadAngularMaxima = 0.50  # rad/s
tiempoMaximoOrden = 10.0       # segundos


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comandoEsValido(comando):
    """Evalua si la tupla cumple con tipo, estructura y limites permitidos."""
    esValido = True

    if not comando:
        esValido = False
    else:
        tipoOrden = comando[0]

        if tipoOrden == "detenerse" or tipoOrden == "saludar":
            if len(comando) != 1:
                esValido = False

        elif tipoOrden == "avanzar":
            if len(comando) != 3:
                esValido = False
            else:
                velocidadDato = comando[1]
                tiempoDato = comando[2]
                esNumero = True

                try:
                    velocidadValor = float(velocidadDato)
                    tiempoValor = float(tiempoDato)
                except (ValueError, TypeError):
                    esNumero = False

                if not esNumero:
                    esValido = False
                elif velocidadValor <= 0 or velocidadValor > velocidadLinealMaxima:
                    esValido = False
                elif tiempoValor <= 0 or tiempoValor > tiempoMaximoOrden:
                    esValido = False

        elif tipoOrden == "girar":
            if len(comando) != 3:
                esValido = False
            else:
                velocidadDato = comando[1]
                tiempoDato = comando[2]
                esNumero = True

                try:
                    velocidadValor = float(velocidadDato)
                    tiempoValor = float(tiempoDato)
                except (ValueError, TypeError):
                    esNumero = False

                if not esNumero:
                    esValido = False
                else:
                    magnitudGiro = velocidadValor if velocidadValor >= 0 else -velocidadValor

                    if velocidadValor == 0 or magnitudGiro > velocidadAngularMaxima:
                        esValido = False
                    elif tiempoValor <= 0 or tiempoValor > tiempoMaximoOrden:
                        esValido = False
        else:
            esValido = False

    return esValido


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutarComando(robot, comando):
    """Ejecuta una orden individual y atrapa excepciones del simulador."""
    tipoOrden = comando[0]
    resultadoTexto = ""

    try:
        if tipoOrden == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            resultadoTexto = f"Avanzo {comando[1]} m/s por {comando[2]} s"

        elif tipoOrden == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
            resultadoTexto = f"Giro {comando[1]} rad/s por {comando[2]} s"

        elif tipoOrden == "detenerse":
            robot.detenerse()
            resultadoTexto = "Robot detenido"

        elif tipoOrden == "saludar":
            robot.saludar()
            resultadoTexto = "Saludo completado"

    except ErrorDeSeguridad as errorSeguridad:
        resultadoTexto = f"Rechazado por seguridad: {errorSeguridad}"

    return resultadoTexto


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutarMision(robot, mision, historial):
    """Recorre la mision registrando estados en una lista homogenea de strings."""
    print("\n╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║ INICIANDO MISION: {len(mision)} COMANDO(S) RECIBIDO(S)                      ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    for posicion in range(len(mision)):
        comandoActual = mision[posicion]

        if comandoEsValido(comandoActual):
            mensajeEjecucion = ejecutarComando(robot, comandoActual)

            if len(mensajeEjecucion) >= 23 and mensajeEjecucion[:23] == "Rechazado por seguridad":
                print(f"[RECHAZADO] {comandoActual} -> {mensajeEjecucion}")
                historial.append(f"RECHAZADO: {comandoActual[0]} (Seguridad)")
            else:
                print(f"[OK] {comandoActual} -> {mensajeEjecucion}")
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
def generarReporte(historial):
    """Muestra el resumen final analizando el historial con rebanadas."""
    totalEjecutados = 0
    totalRechazados = 0

    for indice in range(len(historial)):
        registro = historial[indice]
        
        if len(registro) >= 2 and registro[:2] == "OK":
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
        for indice in range(len(historial)):
            lineaDetalle = historial[indice]
            if not (len(lineaDetalle) >= 2 and lineaDetalle[:2] == "OK"):
                print(f"║ * {lineaDetalle:<63} ║")
        print("╚═══════════════════════════════════════════════════════════════════╝\n")


# =====================================================================
#  INTERFAZ DE USUARIO: MENU PRINCIPAL
# =====================================================================
def mostrarMenu():
    """Imprime el menu utilizando el marco con caracteres especiales."""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                   CONTROLADOR DE MISIONES - GO2                   ║")
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
            entradaUsuario = input("Seleccione una mision (1-5): ").strip()

            if entradaUsuario.isdigit():
                opcionElegida = int(entradaUsuario)
            else:
                opcionElegida = 0

            misionElegida = None

            if opcionElegida == 1:
                misionElegida = MISIONES["basica"]
            elif opcionElegida == 2:
                misionElegida = MISIONES["cuadrado"]
            elif opcionElegida == 3:
                misionElegida = MISIONES["errores"]
            elif opcionElegida == 4:
                misionElegida = MISIONES["larga"]
            elif opcionElegida == 5:
                print("\nCerrando conexion con el simulador...")
                continuarPrograma = False
            else:
                print("\nOpcion invalida. Ingrese un numero del 1 al 5.\n")

            if misionElegida is not None:
                historialOperaciones = []
                ejecutarMision(robot, misionElegida, historialOperaciones)
                generarReporte(historialOperaciones)

    finally:
        robot.detenerse()
        robot.desconectar()


main()