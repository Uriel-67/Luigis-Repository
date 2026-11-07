from validaciones_2 import validar_formato_codigo, existe_atleta_recursivo
from archivos_2 import guardar_atleta, guardar_registro, exportar_reporte

"""FUNCION REGISTRAR ATLETA"""
def registrar_atleta(atletas, config, codigo, nombre, categoria):
    if not validar_formato_codigo(codigo):
        return False, "Formato de codigo invalido. Use una letra mayuscula y dos numeros."
        
    lista_codigos = list(atletas.keys())
    if existe_atleta_recursivo(codigo, lista_codigos):
        return False, "El atleta ya se encuentra registrado."
        
    if not nombre:
        return False, "El nombre no puede estar vacio."
        
    if categoria not in config["CATEGORIAS_ADMITIDAS"]:
        return False, "Categoria invalida."
        
    atletas[codigo] = {"nombre": nombre, "categoria": categoria}
    guardar_atleta(codigo, nombre, categoria)
    return True, "Atleta registrado correctamente."

"""FUNCION REGISTRAR MINUTOS"""
def registrar_minutos(atletas, registros, config, codigo, dia, minutos_texto):
    lista_codigos = list(atletas.keys())
    if not existe_atleta_recursivo(codigo, lista_codigos):
        return False, "No existe el atleta."
        
    try:
        minutos = float(minutos_texto)
    except ValueError:
        return False, "Los minutos deben ser numericos."
        
    if minutos < 0:
        return False, "Los minutos no pueden ser negativos."
        
    acumulado_diario = 0
    for r in registros:
        if r["codigo_atleta"] == codigo and r["dia"] == dia:
            acumulado_diario += r["minutos"]
            
    if acumulado_diario + minutos > config["MAXIMO_DIARIO"]:
        return False, "Supera el maximo diario permitido."
        
    nuevo_registro = {"codigo_atleta": codigo, "dia": dia, "minutos": minutos}
    registros.append(nuevo_registro)
    guardar_registro(codigo, dia, minutos)
    return True, "Entrenamiento registrado correctamente."

"""FUNCION REPORTE FILTRADO"""
def reporte_filtrado(atletas, registros, codigo):
    lista_codigos = list(atletas.keys())
    if not existe_atleta_recursivo(codigo, lista_codigos):
        print("Atleta no encontrado.")
        return
        
    atleta = atletas[codigo]
    print(f"Ficha de {atleta['nombre']} - {atleta['categoria']}")
    total = 0
    for r in registros:
        if r["codigo_atleta"] == codigo:
            print(f"Dia: {r['dia']} - Minutos: {r['minutos']}")
            total += r["minutos"]
    print(f"Total historico: {total} minutos.")

"""FUNCION REPORTE GENERAL"""
def reporte_general(atletas, registros):
    if not registros:
        print("No hay registros historicos.")
        return
        
    totales_categoria = {}
    total_global = 0
    
    for r in registros:
        codigo = r["codigo_atleta"]
        if codigo in atletas:
            cat = atletas[codigo]["categoria"]
            mins = r["minutos"]
            totales_categoria[cat] = totales_categoria.get(cat, 0) + mins
            total_global += mins
            
    print(f"Total de minutos historicos globales: {total_global}")
    for cat, mins in totales_categoria.items():
        print(f"Categoria {cat}: {mins} minutos.")

"""FUNCION REPORTE ALERTAS"""
def reporte_alertas(atletas, registros, config, semana_evaluar):
    if not atletas:
        print("No hay atletas registrados.")
        return
        
    acumuladores = {}
    for codigo in atletas:
        acumuladores[codigo] = 0
        
    for r in registros:
        if r["dia"].startswith(semana_evaluar):
            codigo = r["codigo_atleta"]
            if codigo in acumuladores:
                acumuladores[codigo] += r["minutos"]
                
    salida = f"Atletas que no alcanzaron el objetivo en {semana_evaluar}:\n"
    hay_alertas = False
    
    for codigo, total in acumuladores.items():
        if total < config["OBJETIVO_SEMANAL"]:
            nombre = atletas[codigo]["nombre"]
            salida += f"{codigo} - {nombre} ({total} min)\n"
            hay_alertas = True
            
    if hay_alertas:
        print(salida)
        exportar_reporte(salida)
        print("Reporte exportado a reporte.txt")
    else:
        print("Todos alcanzaron el objetivo en ese periodo.")

"""FUNCION RESUMEN UNICOS"""
def resumen_unicos(registros):
    unicos = set()
    for r in registros:
        unicos.add(r["codigo_atleta"])
        
    print(f"Cantidad de atletas unicos con actividad: {len(unicos)}")
    for codigo in unicos:
        print(codigo)