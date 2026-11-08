from archivos_2 import cargarConfiguracion, cargarUsuarios, cargarAtletas, cargarRegistros
from validaciones_2 import validarFormatoUsuario
from operaciones_2 import (
    registrarAtleta, registrarMinutos, reporteFiltrado, 
    reporteGeneral, reporteAlertas, resumenUnicos
)

def login(usuariosRegistrados):
    """Administra el acceso con control interactivo de maximo 3 intentos."""
    intentosRestantes = 3
    sesionIniciada = False

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               ACCESO AL SISTEMA - CLUB LUIGI'S               ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ Ingrese sus credenciales de operador para continuar.         ║")
    print("║ Formato usuario: 4 a 10 caracteres alfanumericos.            ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    while intentosRestantes > 0 and not sesionIniciada:
        print()
        print("Intentos restantes:", intentosRestantes)
        nombreUsuario = input("-> Ingrese Usuario (ej: admin123): ").strip()

        if not validarFormatoUsuario(nombreUsuario):
            print("Formato incorrecto. El usuario debe tener entre 4 y 10 caracteres alfanumericos.")
            intentosRestantes -= 1
        else:
            claveUsuario = input("-> Ingrese Contraseña: ").strip()
            if nombreUsuario in usuariosRegistrados and usuariosRegistrados[nombreUsuario] == claveUsuario:
                sesionIniciada = True
                print()
                print("Acceso concedido. Bienvenido al sistema.")
            else:
                print("Credenciales invalidas. Verifique usuario o contraseña.")
                intentosRestantes -= 1

    return sesionIniciada

def mostrarMenu():
    """Despliega el menu principal en consola."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            SISTEMA DE SEGUIMIENTO DE ENTRENAMIENTO           ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║ 1. Registrar nuevo atleta                                    ║")
    print("║ 2. Registrar sesion de minutos                               ║")
    print("║ 3. Consultar reporte filtrado por atleta                     ║")
    print("║ 4. Ver reporte general por categorias                        ║")
    print("║ 5. Generar reporte de alertas semanales                      ║")
    print("║ 6. Ver resumen de atletas unicos con actividad               ║")
    print("║ 7. Salir del sistema                                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def main():
    datosConfiguracion = cargarConfiguracion()
    if datosConfiguracion is None:
        print("Ejecucion cancelada: Imposible iniciar el sistema sin configuracion valida.")
        return

    directorioUsuarios = cargarUsuarios()
    if len(directorioUsuarios) == 0:
        print("Error: No se encontro usuarios.csv o el archivo esta vacio. Revise el archivo base.")
        return

    if not login(directorioUsuarios):
        print()
        print("Acceso denegado: Se agotaron los intentos disponibles.")
        return

    padronAtletas = cargarAtletas()
    historialRegistros = cargarRegistros()
    sistemaActivo = True

    while sistemaActivo:
        mostrarMenu()
        opcionElegida = input("Seleccione una opcion (1-7): ").strip()

        if opcionElegida == "1":
            print()
            print("--- REGISTRO DE ATLETA ---")
            print("Datos requeridos:")
            print(" - Codigo: 1 letra mayuscula y 2 numeros (ej: A01, B05).")
            print(" - Nombre: Texto no vacio (ej: Lionel Messi).")
            
            textoCategorias = ""
            esPrimerElemento = True
            for categoriaActual in datosConfiguracion["CATEGORIAS_ADMITIDAS"]:
                if esPrimerElemento:
                    textoCategorias = categoriaActual
                    esPrimerElemento = False
                else:
                    textoCategorias = textoCategorias + ", " + categoriaActual
            
            print(" - Categoria: Debe ser una de las admitidas [" + textoCategorias + "].")
            print()
            codigoIngresado = input("Ingrese Codigo: ").strip()
            nombreIngresado = input("Ingrese Nombre completo: ").strip()
            categoriaIngresada = input("Ingrese Categoria: ").strip()

            operacionExitosa, mensajeResultado = registrarAtleta(
                padronAtletas, datosConfiguracion, codigoIngresado, nombreIngresado, categoriaIngresada
            )
            print()
            print("Resultado:", mensajeResultado)

        elif opcionElegida == "2":
            print()
            print("--- REGISTRO DE MINUTOS DE ENTRENAMIENTO ---")
            print("Datos requeridos:")
            print(" - Codigo de atleta: Debe existir en el padron registrado.")
            print(" - Fecha: Formato completo DD/MM/AAAA (ej: 05/10/2024).")
            print(" - Minutos: Mayor o igual a 0 (Maximo diario permitido:", datosConfiguracion["MAXIMO_DIARIO"], "min).")
            print()
            codigoAtleta = input("Ingrese Codigo de atleta existente: ").strip()
            fechaEntrenamiento = input("Ingrese Fecha de entrenamiento (DD/MM/AAAA): ").strip()
            minutosSesion = input("Ingrese Cantidad de minutos: ").strip()

            operacionExitosa, mensajeResultado = registrarMinutos(
                padronAtletas, historialRegistros, datosConfiguracion, codigoAtleta, fechaEntrenamiento, minutosSesion
            )
            print()
            print("Resultado:", mensajeResultado)

        elif opcionElegida == "3":
            print()
            print("--- CONSULTA DE FICHA INDIVIDUAL ---")
            print("Dato requerido: Codigo de atleta registrado previamente (ej: A01).")
            codigoConsulta = input("Ingrese Codigo del atleta: ").strip()
            reporteFiltrado(padronAtletas, historialRegistros, codigoConsulta)

        elif opcionElegida == "4":
            print()
            print("--- REPORTE HISTORICO GENERAL ---")
            reporteGeneral(padronAtletas, historialRegistros)

        elif opcionElegida == "5":
            print()
            print("--- GENERAR REPORTE DE ALERTAS SEMANALES ---")
            print("Defina el rango semanal a evaluar ingresando fecha de inicio y de fin.")
            fechaInicio = input("Ingrese Fecha de inicio (DD/MM/AAAA, ej: 01/10/2024): ").strip()
            fechaFin = input("Ingrese Fecha de cierre (DD/MM/AAAA, ej: 07/10/2024): ").strip()
            reporteAlertas(padronAtletas, historialRegistros, datosConfiguracion, fechaInicio, fechaFin)

        elif opcionElegida == "6":
            print()
            print("--- RESUMEN DE IDENTIFICADORES UNICOS ---")
            resumenUnicos(historialRegistros)

        elif opcionElegida == "7":
            print()
            print("Cerrando el sistema. Hasta luego.")
            sistemaActivo = False

        else:
            print("Opcion invalida. Debe ingresar un numero del 1 al 7.")

main()