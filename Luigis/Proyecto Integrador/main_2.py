from archivos_2 import cargar_configuracion, cargar_usuarios, cargar_atletas, cargar_registros
from validaciones_2 import validar_formato_usuario
from operaciones_2 import (
    registrar_atleta, registrar_minutos, reporte_filtrado, 
    reporte_general, reporte_alertas, resumen_unicos
)

"""FUNCION LOGIN"""
def login(usuarios):
    intentos = 3
    while intentos > 0:
        usuario = input("Usuario: ")
        if not validar_formato_usuario(usuario):
            print("Formato invalido. Use 4 a 10 caracteres alfanumericos.")
            intentos -= 1
            continue
            
        contrasena = input("Contraseña: ")
        if usuario in usuarios and usuarios[usuario] == contrasena:
            return True
        print("Credenciales incorrectas.")
        intentos -= 1
    return False

"""FUNCION MOSTRAR MENU"""
def mostrar_menu():
    print("\n===== MENU PRINCIPAL =====")
    print("1. Registrar atleta")
    print("2. Registrar minutos")
    print("3. Reporte filtrado")
    print("4. Reporte general")
    print("5. Reporte de alertas")
    print("6. Resumen de unicos")
    print("7. Salir")

"""FUNCION PRINCIPAL"""
def main():
    config = cargar_configuracion()
    usuarios = cargar_usuarios()
    
    if not usuarios:
        print("No hay usuarios registrados. Agregue usuarios.csv.")
        return
        
    if not login(usuarios):
        print("Acceso denegado.")
        return
        
    atletas = cargar_atletas()
    registros = cargar_registros()
    continuar = True
    
    while continuar:
        mostrar_menu()
        opcion = input("Elegi una opcion: ")
        
        if opcion == "1":
            codigo = input("Codigo (ej A01): ")
            nombre = input("Nombre: ")
            categoria = input("Categoria: ")
            ok, msj = registrar_atleta(atletas, config, codigo, nombre, categoria)
            print(msj)
        elif opcion == "2":
            codigo = input("Codigo del atleta: ")
            dia = input("Dia (ej S1-Lunes): ")
            minutos = input("Minutos: ")
            ok, msj = registrar_minutos(atletas, registros, config, codigo, dia, minutos)
            print(msj)
        elif opcion == "3":
            codigo = input("Codigo a consultar: ")
            reporte_filtrado(atletas, registros, codigo)
        elif opcion == "4":
            reporte_general(atletas, registros)
        elif opcion == "5":
            semana = input("Ingrese el periodo a evaluar (ej S1): ")
            reporte_alertas(atletas, registros, config, semana)
        elif opcion == "6":
            resumen_unicos(registros)
        elif opcion == "7":
            print("Hasta luego.")
            continuar = False
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()