# Menu general.
# Sistema de Seguimiento de Entrenamientos - LUIGI'S

from datos import DIAS_SEMANA, CATEGORIAS_ADMITIDAS, OBJETIVO_SEMANAL, MAXIMO_DIARIO, crear_estructuras
from operaciones import (
    registrar_atleta,
    registrar_minutos,
    obtener_ficha_atleta,
    atletas_no_alcanzaron_objetivo,
    contar_cumplimiento,
    totales_por_categoria,
    categorias_con_mas_minutos,
    atletas_con_mas_minutos,
    ranking_general,
    top_tres,
    resumen_diario_club,
    dia_mayor_volumen,
    promedio_general_club,
    total_semanal,
    promedio_diario,
    porcentaje_cumplimiento,
    alcanzo_objetivo,
)


def mostrar_menu():
    print("\n===== SISTEMA DE SEGUIMIENTO DE ENTRENAMIENTOS - LUIGI'S =====")
    print("1. Mostrar informacion general del sistema")
    print("2. Registrar atleta")
    print("3. Registrar minutos de entrenamiento")
    print("4. Listar atletas")
    print("5. Consultar el entrenamiento de un atleta puntual")
    print("6. Buscar atleta por codigo")
    print("7. Mostrar indicadores")
    print("8. Mostrar alertas")
    print("9. Generar informes")
    print("10. Salir")


def opcion_info_general(atletas):
    print("\n-- Informacion general del sistema --")
    print("Club: LUIGI'S - Sistema de Seguimiento de Entrenamientos")
    print(f"Categorias admitidas: {', '.join(CATEGORIAS_ADMITIDAS)}")
    print(f"Dias de la semana administrados: {', '.join(DIAS_SEMANA)}")
    print(f"Objetivo semanal de entrenamiento: {OBJETIVO_SEMANAL} minutos")
    print(f"Maximo de minutos acumulados por dia: {MAXIMO_DIARIO} minutos")
    print(f"Atletas registrados actualmente: {len(atletas)}")


def opcion_registrar_atleta(atletas, matriz):
    print("\n-- Registrar atleta --")
    codigo = input("Codigo (una letra y dos numeros, ej A01): ")
    nombre = input("Nombre: ")
    print(f"Categorias admitidas: {', '.join(CATEGORIAS_ADMITIDAS)}")
    categoria = input("Categoria: ")

    ok, mensaje = registrar_atleta(atletas, matriz, codigo, nombre, categoria)
    print(mensaje)


def opcion_registrar_minutos(atletas, matriz):
    print("\n-- Registrar minutos de entrenamiento --")
    codigo = input("Codigo del atleta: ")
    print(f"Dias validos: {', '.join(DIAS_SEMANA)}")
    dia = input("Dia: ")
    minutos = input("Minutos de la sesion: ")

    ok, mensaje = registrar_minutos(atletas, matriz, codigo, dia, minutos)
    print(mensaje)


def opcion_listar_atletas(atletas):
    print("\n-- Listado de atletas --")
    if len(atletas) == 0:
        print("Todavia no hay atletas registrados.")
        return
    for codigo, nombre, categoria in atletas:
        print(f"{codigo} | {nombre} | {categoria}")


def _mostrar_ficha(ficha):
    codigo, nombre, categoria, minutos_por_dia, total, promedio, porcentaje, alcanzo = ficha
    print(f"Codigo: {codigo}")
    print(f"Nombre: {nombre}")
    print(f"Categoria: {categoria}")
    for i in range(len(DIAS_SEMANA)):
        print(f"  {DIAS_SEMANA[i]}: {minutos_por_dia[i]} min")
    print(f"Total semanal: {total} min")
    print(f"Promedio diario: {promedio:.2f} min")
    print(f"Porcentaje de cumplimiento: {porcentaje:.1f}%")
    if alcanzo:
        print("Estado: alcanzo el objetivo semanal.")
    else:
        print("Estado: todavia no alcanzo el objetivo semanal.")


def opcion_consultar_atleta(atletas, matriz):
    print("\n-- Consultar entrenamiento de un atleta --")
    codigo = input("Codigo del atleta: ")
    ok, resultado = obtener_ficha_atleta(atletas, matriz, codigo)
    if not ok:
        print(resultado)
        return
    _mostrar_ficha(resultado)


def opcion_buscar_por_codigo(atletas, matriz):
    print("\n-- Buscar atleta por codigo --")
    codigo = input("Codigo a buscar: ")
    ok, resultado = obtener_ficha_atleta(atletas, matriz, codigo)
    if not ok:
        print(resultado)
        return
    _mostrar_ficha(resultado)


def opcion_mostrar_indicadores(atletas, matriz):
    print("\n-- Indicadores generales del club --")
    if len(atletas) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return

    ok, promedio = promedio_general_club(atletas, matriz)
    if ok:
        print(f"Promedio general del club: {promedio:.2f} min por atleta.")
    else:
        print(promedio)

    dias_maximos, minutos_dia_max = dia_mayor_volumen(matriz)
    if dias_maximos:
        print(f"Dia/s con mayor volumen de entrenamiento: {', '.join(dias_maximos)} ({minutos_dia_max} min).")
    else:
        print("Todavia no hay minutos cargados para calcular el dia de mayor volumen.")

    categorias_maximas, minutos_cat_max = categorias_con_mas_minutos(atletas, matriz)
    if categorias_maximas and minutos_cat_max > 0:
        print(f"Categoria/s con mayor cantidad de minutos: {', '.join(categorias_maximas)} ({minutos_cat_max} min).")
    else:
        print("Todavia no hay minutos cargados para calcular la categoria con mas minutos.")

    cantidad_alcanzo, cantidad_no_alcanzo = contar_cumplimiento(atletas, matriz)
    print(f"Atletas que alcanzaron el objetivo semanal: {cantidad_alcanzo}")
    print(f"Atletas que todavia no alcanzaron el objetivo semanal: {cantidad_no_alcanzo}")


def opcion_mostrar_alertas(atletas, matriz):
    print("\n-- Atletas que todavia no alcanzaron el objetivo semanal --")
    if len(atletas) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return

    pendientes = atletas_no_alcanzaron_objetivo(atletas, matriz)
    if len(pendientes) == 0:
        print("Todos los atletas ya alcanzaron el objetivo semanal.")
        return

    for codigo, nombre, categoria in pendientes:
        indice = [a[0] for a in atletas].index(codigo)
        total = total_semanal(matriz[indice])
        print(f"{codigo} | {nombre} | {categoria} | {total} min (le faltan {OBJETIVO_SEMANAL - total} min)")


def informe_ranking_general(atletas, matriz):
    print("\n-- Ranking general (por minutos acumulados) --")
    ranking = ranking_general(atletas, matriz)
    if len(ranking) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return
    for puesto, (atleta, total) in enumerate(ranking, start=1):
        print(f"{puesto}. {atleta[1]} ({atleta[0]}) - {total} min")

    print("\nTop 3:")
    for puesto, (atleta, total) in enumerate(top_tres(ranking), start=1):
        print(f"{puesto}. {atleta[1]} ({atleta[0]}) - {total} min")


def informe_resumen_por_categoria(atletas, matriz):
    print("\n-- Resumen de minutos por categoria --")
    if len(atletas) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return
    nombres, totales = totales_por_categoria(atletas, matriz)
    for i in range(len(nombres)):
        print(f"{nombres[i]}: {totales[i]} min")


def informe_pendientes_objetivo(atletas, matriz):
    print("\n-- Atletas que todavia no alcanzaron el objetivo semanal --")
    opcion_mostrar_alertas(atletas, matriz)


def informe_promedio_por_atleta(atletas, matriz):
    print("\n-- Promedio semanal de minutos por atleta --")
    if len(atletas) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return
    for i in range(len(atletas)):
        codigo, nombre, categoria = atletas[i]
        promedio = promedio_diario(matriz[i])
        print(f"{codigo} | {nombre}: {promedio:.2f} min/dia")


def informe_maximos_minutos(atletas, matriz):
    print("\n-- Atleta/s con mayor cantidad de minutos --")
    ganadores, maximo = atletas_con_mas_minutos(atletas, matriz)
    if len(ganadores) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return
    for codigo, nombre, categoria in ganadores:
        print(f"{codigo} | {nombre} | {categoria} - {maximo} min")


def informe_resumen_diario_club(atletas, matriz):
    print("\n-- Resumen diario del club (volumen total por dia) --")
    if len(atletas) == 0:
        print("No hay datos suficientes: todavia no hay atletas registrados.")
        return
    totales_por_dia = resumen_diario_club(matriz)
    for i in range(len(DIAS_SEMANA)):
        print(f"{DIAS_SEMANA[i]}: {totales_por_dia[i]} min")

    dias_maximos, minutos_max = dia_mayor_volumen(matriz)
    if dias_maximos:
        print(f"Dia/s con mayor volumen: {', '.join(dias_maximos)} ({minutos_max} min).")


def opcion_generar_informes(atletas, matriz):
    print("\n===== INFORMES =====")
    print("1. Ranking general")
    print("2. Resumen de minutos por categoria")
    print("3. Atletas que todavia no alcanzaron el objetivo semanal")
    print("4. Promedio semanal de minutos por atleta")
    print("5. Atleta/s con mayor cantidad de minutos")
    print("6. Resumen diario del club")
    opcion = input("Elegi un informe: ")

    if opcion == "1":
        informe_ranking_general(atletas, matriz)
    elif opcion == "2":
        informe_resumen_por_categoria(atletas, matriz)
    elif opcion == "3":
        informe_pendientes_objetivo(atletas, matriz)
    elif opcion == "4":
        informe_promedio_por_atleta(atletas, matriz)
    elif opcion == "5":
        informe_maximos_minutos(atletas, matriz)
    elif opcion == "6":
        informe_resumen_diario_club(atletas, matriz)
    else:
        print("Opcion invalida.")


def main():
    atletas, matriz = crear_estructuras()
    continuar = True

    while continuar:
        mostrar_menu()
        opcion = input("Elegi una opcion: ")

        if opcion == "1":
            opcion_info_general(atletas)
        elif opcion == "2":
            opcion_registrar_atleta(atletas, matriz)
        elif opcion == "3":
            opcion_registrar_minutos(atletas, matriz)
        elif opcion == "4":
            opcion_listar_atletas(atletas)
        elif opcion == "5":
            opcion_consultar_atleta(atletas, matriz)
        elif opcion == "6":
            opcion_buscar_por_codigo(atletas, matriz)
        elif opcion == "7":
            opcion_mostrar_indicadores(atletas, matriz)
        elif opcion == "8":
            opcion_mostrar_alertas(atletas, matriz)
        elif opcion == "9":
            opcion_generar_informes(atletas, matriz)
        elif opcion == "10":
            print("Hasta luego.")
            continuar = False
        else:
            print("Opcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    main()
