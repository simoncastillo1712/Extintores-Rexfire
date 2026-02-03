
# Módulo del sistema de menú interactivo


from modules import gestion_datos, funciones_utiles
import os

def limpiar_pantalla():
# Limpia la pantalla luego de cada gestión
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado(titulo):
# Muestra un encabezado decorado
    print("\n" + "="*40)
    print(f" {titulo}")
    print("="*40)

def menu_principal():
# Menú principal del sistema
    while True:
        limpiar_pantalla()
        mostrar_encabezado("SISTEMA DE GESTIÓN EXTINTORES REXFIRE")
        print("\nMENÚ PRINCIPAL:")
        print("1. Registrar nuevo cliente")
        print("2. Registrar nuevo pedido")
        print("3. Listar todos los clientes")
        print("4. Listar todos los pedidos")
        print("5. Buscar cliente por RUT")
        print("6. Ver estadísticas")
        print("7. Calcular cotización rápida")
        print("8. Guardar datos en archivo")
        print("9. Cargar datos desde archivo")
        print("0. Salir del sistema")
        
        opcion = input("\nSeleccione una opción (0-9): ").strip()
        
        if opcion == '1':
            gestion_datos.registrar_cliente()
        elif opcion == '2':
            gestion_datos.registrar_pedido()
        elif opcion == '3':
            gestion_datos.listar_clientes()
        elif opcion == '4':
            gestion_datos.listar_pedidos()
        elif opcion == '5':
            funciones_utiles.buscar_cliente_por_rut()
        elif opcion == '6':
            funciones_utiles.mostrar_estadisticas()
        elif opcion == '7':
            funciones_utiles.cotizacion_rapida()
        elif opcion == '8':
            funciones_utiles.guardar_datos_archivo()
        elif opcion == '9':
            funciones_utiles.cargar_datos_archivo()
        elif opcion == '0':
            print("\n Gracias por usar el sistema ")
            print("Sesión Cerrada")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

def submenu_extintores():
    
# Submenú para selección de tipos de extintores
    precios = funciones_utiles.obtener_precios_extintores()
    
    print("\n" + "-"*40)
    print("TIPOS DE EXTINTORES DISPONIBLES:")
    print("-"*40)
    
    for i, (peso, datos) in enumerate(precios.items(), 1):
        print(f"{i}. {peso} - ${datos['nuevo']:,} (nuevo)")
    
    opcion = input("\nSeleccione el tipo de extintor (1-7): ").strip()
    
    mapeo_opciones = {
        '1': '1kg',
        '2': '2kg',
        '3': '4kg',
        '4': '6kg',
        '5': '10kg',
        '6': '25kg',
        '7': '50kg'
    }
    
    return mapeo_opciones.get(opcion)