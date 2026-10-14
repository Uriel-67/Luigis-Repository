# Validaciones, calculos, busquedas e informes.
# Sistema de Seguimiento de Entrenamientos - LUIGI'S

from datos import DIAS_SEMANA, CATEGORIAS_ADMITIDAS, OBJETIVO_SEMANAL, MAXIMO_DIARIO


# --- validaciones y registro de atletas ---

def validar_formato_codigo(codigo):
    """El codigo debe ser una letra y dos numeros, ej A01."""
    if len(codigo) != 3:
        return False
    letra = codigo[0]
    numeros = codigo[1:]
    return letra.isalpha() and numeros.isdigit()


def buscar_indice_por_codigo(atletas, codigo):
    """Busca un atleta por codigo (sin importar mayus/minus) y
    devuelve su indice, o -1 si no existe."""
    codigo = codigo.upper()
    for i in range(len(atletas)):
        if atletas[i][0].upper() == codigo:
            return i
    return -1


def registrar_atleta(atletas, matriz, codigo, nombre, categoria):
    """Valida y registra un atleta nuevo. Si esta todo bien, agrega
    su tupla a atletas y una fila de ceros a matriz. Devuelve
    (True, mensaje) o (False, mensaje) segun corresponda."""
    codigo = codigo.strip().upper()
    nombre = nombre.strip()
    categoria = categoria.strip()

    if not validar_formato_codigo(codigo):
        return False, "Codigo invalido. Formato esperado: una letra y dos numeros (ej: A01)."

    if buscar_indice_por_codigo(atletas, codigo) != -1:
        return False, f"Ya existe un atleta registrado con el codigo {codigo}."

    if nombre == "":
        return False, "El nombre no puede estar vacio."

    if categoria not in CATEGORIAS_ADMITIDAS:
        return False, f"Categoria invalida. Debe ser una de: {', '.join(CATEGORIAS_ADMITIDAS)}."

    atletas.append((codigo, nombre, categoria))
    matriz.append([0] * len(DIAS_SEMANA))
    return True, f"Atleta {nombre} ({codigo}) registrado correctamente."


# carga de minutos 

def validar_dia(dia):
    """Devuelve el indice del dia (0 a 6) si es valido, o -1 si no."""
    dia = dia.strip().capitalize()
    if dia in DIAS_SEMANA:
        return DIAS_SEMANA.index(dia)
    return -1


def registrar_minutos(atletas, matriz, codigo, dia, minutos_texto):
    """Suma una sesion de entrenamiento al dia indicado (no reemplaza
    lo que ya habia). Valida que el atleta exista, que el dia sea
    valido, que los minutos sean un numero positivo, y que el
    acumulado del dia no supere el maximo diario. Devuelve
    (True, mensaje) o (False, mensaje) con el motivo del rechazo."""
    indice_atleta = buscar_indice_por_codigo(atletas, codigo)
    if indice_atleta == -1:
        return False, f"No existe ningun atleta con el codigo {codigo}."

    indice_dia = validar_dia(dia)
    if indice_dia == -1:
        return False, f"'{dia}' no es un dia valido. Debe ser uno de: {', '.join(DIAS_SEMANA)}."

    try:
        minutos_nuevos = float(minutos_texto)
    except (TypeError, ValueError):
        return False, "El valor de minutos debe ser numerico."

    if minutos_nuevos < 0:
        return False, "El valor de minutos no puede ser negativo."

    acumulado_actual = matriz[indice_atleta][indice_dia]
    acumulado_final = acumulado_actual + minutos_nuevos

    if acumulado_final > MAXIMO_DIARIO:
        return False, (
            f"No se puede registrar: el acumulado de {dia} pasaria a "
            f"{acumulado_final} minutos, superando el maximo diario de "
            f"{MAXIMO_DIARIO}."
        )

    matriz[indice_atleta][indice_dia] = acumulado_final
    return True, f"Se registraron {minutos_nuevos} minutos el {dia}. Total del dia: {acumulado_final}."


#  calculos por atleta 

def total_semanal(fila_minutos):
    """Total de minutos de la semana para un atleta."""
    return sum(fila_minutos)


def promedio_diario(fila_minutos):
    """Promedio diario, calculado sobre los 7 dias siempre
    (entrene o no entrene todos los dias)."""
    return total_semanal(fila_minutos) / len(DIAS_SEMANA)


def porcentaje_cumplimiento(fila_minutos):
    """Porcentaje sobre el objetivo semanal. Puede pasar el 100%
    si el atleta entreno de mas."""
    return (total_semanal(fila_minutos) / OBJETIVO_SEMANAL) * 100


def alcanzo_objetivo(fila_minutos):
    """True si el atleta ya llego a los 150 minutos."""
    return total_semanal(fila_minutos) >= OBJETIVO_SEMANAL


# comprension de listas, conteos y alertas 

def atletas_no_alcanzaron_objetivo(atletas, matriz):
    """Atletas que todavia no llegaron al objetivo semanal, con lo
    acumulado hasta el momento. Usa comprension de listas."""
    return [
        atletas[i] for i in range(len(atletas))
        if total_semanal(matriz[i]) < OBJETIVO_SEMANAL
    ]


def contar_cumplimiento(atletas, matriz):
    """Cuenta cuantos atletas alcanzaron el objetivo y cuantos no.
    Devuelve (cantidad_alcanzo, cantidad_no_alcanzo)."""
    no_alcanzaron = atletas_no_alcanzaron_objetivo(atletas, matriz)
    cantidad_no_alcanzo = len(no_alcanzaron)
    cantidad_alcanzo = len(atletas) - cantidad_no_alcanzo
    return cantidad_alcanzo, cantidad_no_alcanzo


#  totales por categoria (con empate) 

def totales_por_categoria(atletas, matriz):
    """Minutos totales acumulados por cada categoria en la semana.
    Devuelve (CATEGORIAS_ADMITIDAS, lista_de_totales)."""
    totales = [0] * len(CATEGORIAS_ADMITIDAS)
    for i in range(len(atletas)):
        categoria = atletas[i][2]
        indice_categoria = CATEGORIAS_ADMITIDAS.index(categoria)
        totales[indice_categoria] += total_semanal(matriz[i])
    return CATEGORIAS_ADMITIDAS, totales


def categorias_con_mas_minutos(atletas, matriz):
    """Categoria (o categorias, si empatan) con mas minutos en la
    semana. Devuelve (lista_de_categorias, valor_maximo). Si no hay
    atletas, devuelve ([], 0)."""
    if len(atletas) == 0:
        return [], 0
    nombres, totales = totales_por_categoria(atletas, matriz)
    maximo = max(totales)
    categorias_maximas = [nombres[i] for i in range(len(nombres)) if totales[i] == maximo]
    return categorias_maximas, maximo


#  atleta/s con mas minutos (con empate) 

def atletas_con_mas_minutos(atletas, matriz):
    """Atleta (atletas si empatan) con mas minutos en la semana.
    Devuelve (lista_de_atletas, valor_maximo). Si no hay atletas,
    devuelve ([], 0)."""
    if len(atletas) == 0:
        return [], 0
    totales = [total_semanal(fila) for fila in matriz]
    maximo = max(totales)
    ganadores = [atletas[i] for i in range(len(atletas)) if totales[i] == maximo]
    return ganadores, maximo


# ranking general (lambda y slicing) 

def ranking_general(atletas, matriz):
    """Atletas ordenados de mayor a menor por minutos de la semana,
    usando lambda como criterio de sorted(). Cada elemento del
    resultado es (atleta, total_minutos)."""
    pares = [(atletas[i], total_semanal(matriz[i])) for i in range(len(atletas))]
    ranking = sorted(pares, key=lambda par: par[1], reverse=True)
    return ranking


def top_tres(ranking):
    """Primeros 3 puestos del ranking, con slicing."""
    return ranking[:3]


#  resumen diario del club y dia de mayor volumen (con empate) 

def resumen_diario_club(matriz):
    """Recorre la matriz por columnas: suma los minutos de todos
    los atletas para cada dia. Devuelve una lista de 7 valores,
    en el mismo orden que DIAS_SEMANA."""
    totales_por_dia = [0] * len(DIAS_SEMANA)
    for fila in matriz:
        for indice_dia in range(len(DIAS_SEMANA)):
            totales_por_dia[indice_dia] += fila[indice_dia]
    return totales_por_dia


def dia_mayor_volumen(matriz):
    """Dia (dias si empatan) con mas minutos entrenados entre
    todos los atletas. Reutiliza resumen_diario_club(). Devuelve
    (lista_de_dias, valor_maximo), o ([], 0) si no hay minutos cargados."""
    totales_por_dia = resumen_diario_club(matriz)
    if len(totales_por_dia) == 0 or max(totales_por_dia, default=0) == 0:
        return [], 0
    maximo = max(totales_por_dia)
    dias_maximos = [DIAS_SEMANA[i] for i in range(len(DIAS_SEMANA)) if totales_por_dia[i] == maximo]
    return dias_maximos, maximo


# promedio general del club 

def promedio_general_club(atletas, matriz):
    """Promedio semanal de minutos por atleta en todo el club.
    Controla que haya al menos un atleta para no dividir por cero.
    Devuelve (True, promedio) o (False, mensaje_de_error)."""
    if len(atletas) == 0:
        return False, "No hay atletas registrados: no se puede calcular el promedio general."

    suma_totales = sum(total_semanal(fila) for fila in matriz)
    promedio = suma_totales / len(atletas)
    return True, promedio


#  busqueda por codigo 

def obtener_ficha_atleta(atletas, matriz, codigo):
    """Busca un atleta por codigo y arma su ficha completa como
    tupla: (codigo, nombre, categoria, minutos_por_dia, total_semanal,
    promedio_diario, porcentaje_cumplimiento, alcanzo_objetivo).
    Devuelve (True, ficha) o (False, mensaje) si no existe."""
    indice = buscar_indice_por_codigo(atletas, codigo)
    if indice == -1:
        return False, f"No existe ningun atleta con el codigo {codigo}."

    codigo_atleta, nombre, categoria = atletas[indice]
    fila = matriz[indice]

    ficha = (
        codigo_atleta,
        nombre,
        categoria,
        fila,
        total_semanal(fila),
        promedio_diario(fila),
        porcentaje_cumplimiento(fila),
        alcanzo_objetivo(fila),
    )
    return True, ficha
