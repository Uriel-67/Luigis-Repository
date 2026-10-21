# Constantes y estructuras iniciales del sistema.
# Sistema de Seguimiento de Entrenamientos - LUIGI'S

# Dias de la semana. Es tupla porque no cambia en toda la ejecucion.
DIAS_SEMANA = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")

# Categorias del club por franja etaria. Tambien es tupla fija. Cada atleta va a pertenecer a una sola de estas cuatro.
CATEGORIAS_ADMITIDAS = ("Infantiles", "Cadetes", "Juveniles", "Mayores")

# Objetivo semanal de minutos (igual para todas las categorias).
OBJETIVO_SEMANAL = 150

# Maximo de minutos acumulados por atleta en un mismo dia.
MAXIMO_DIARIO = 180


def crear_estructuras():
    """
    Crea la lista de atletas y la matriz de minutos vacias.
    atletas guarda tuplas (codigo, nombre, categoria) y matriz[i]
    son los 7 minutos (uno por dia) del atleta que esta en atletas[i]. Quedan
    alineadas por indice. Cada atleta nuevo suma una fila de ceros.
    """
    atletas = []
    matriz = []
    return atletas, matriz
