# Módulo de funciones útiles del sistema de extintores


from modules import datos_basicos, validaciones, menu
import os
import json

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def buscar_cliente_por_rut():
    
# Busca un cliente por su RUT
    limpiar_pantalla()
    menu.mostrar_encabezado("BÚSQUEDA DE CLIENTE POR RUT")

    rut = input("Ingrese el RUT a buscar (sin puntos ni guión): ").strip()
    valido, resultado = validaciones.validar_rut(rut)
    if not valido:
        print(f" {resultado}")
        return

    rut = resultado

# Buscar cliente
    cliente_encontrado = None
    for cliente in datos_basicos.lista_clientes:
        if cliente['rut'] == rut:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        print("\n CLIENTE ENCONTRADO:")
        print("-" * 40)
        print(f"RUT: {cliente_encontrado['rut']}")
        print(f"Nombre: {cliente_encontrado['nombre']}")
        print(f"Email: {cliente_encontrado['email']}")
        print(f"Teléfono: {cliente_encontrado['telefono']}")
        print(f"Dirección: {cliente_encontrado['direccion']}")

# Mostrar pedidos del cliente
        pedidos_cliente = [p for p in datos_basicos.lista_pedidos if p['cliente_rut'] == rut]
        if pedidos_cliente:
            print(f"\nPedidos realizados: {len(pedidos_cliente)}")
            total_gastado = sum(p['total'] for p in pedidos_cliente)
            print(f"Total gastado (con IVA): ${total_gastado:,}")
    else:
        print(" Cliente no encontrado.")

def mostrar_estadisticas():
    
# Muestra estadísticas del sistema, con su total de pedidos
    menu.mostrar_encabezado("ESTADÍSTICAS DEL SISTEMA")

    total_clientes = len(datos_basicos.lista_clientes)
    total_pedidos = len(datos_basicos.lista_pedidos)

    print(f"Total de clientes registrados: {total_clientes}")
    print(f"Total de pedidos realizados: {total_pedidos}")

    if total_pedidos > 0:
        total_ingresos = sum(p['total'] for p in datos_basicos.lista_pedidos)
        print(f"Total de ingresos: ${total_ingresos:,}")

# Estadísticas por tipo de extintor
        tipos_extintor = {}
        for pedido in datos_basicos.lista_pedidos:
            tipo = pedido['tipo_extintor']
            if tipo not in tipos_extintor:
                tipos_extintor[tipo] = 0
            tipos_extintor[tipo] += pedido['cantidad']

        print("\nExtintores vendidos por tipo:")
        for tipo, cantidad in sorted(tipos_extintor.items()):
            print(f"   {tipo}: {cantidad} unidades")

def cotizacion_rapida():
    
# Calcular una cotización rápida
    limpiar_pantalla()
    menu.mostrar_encabezado("COTIZACIÓN RÁPIDA")

# Seleccionar tipo de extintor
    tipo_extintor = menu.submenu_extintores()
    if not tipo_extintor:
        print("Tipo de extintor inválido.")
        input("\nPresione Enter para continuar...")
        return

# Seleccionar cantidad
    while True:
        cantidad = input("Cantidad: ").strip()
        valido, resultado = validaciones.validar_numero_positivo(cantidad, "cantidad")
        if valido:
            cantidad = resultado
            break
        print(f"{resultado}")

# Seleccionar tipo (nuevo o recarga)
    while True:
        print("\nTipo de servicio:")
        print("1. Nuevo")
        print("2. Recarga")
        opcion = input("Seleccione (1-2): ").strip()
        if opcion == '1':
            tipo_servicio = 'nuevo'
            precio_unitario = datos_basicos.precios_extintores[tipo_extintor]['nuevo']
            break
        elif opcion == '2':
            tipo_servicio = 'recarga'
            precio_unitario = datos_basicos.precios_extintores[tipo_extintor]['recarga']
            break
        else:
            print("Opción inválida.")

# Calcular total
    total = precio_unitario * cantidad
    total_con_iva = int(total * 1.19)  # IVA 19%

    print("\nCOTIZACIÓN:")
    print("-" * 40)
    print(f"Tipo de extintor: {tipo_extintor}")
    print(f"Cantidad: {cantidad}")
    print(f"Tipo de servicio: {tipo_servicio}")
    print(f"Precio unitario: ${precio_unitario:,}")
    print(f"TOTAL + IVA: ${total_con_iva:,}")

def guardar_datos_archivo():
# Guardar los datos en archivos JSON
    limpiar_pantalla()
    menu.mostrar_encabezado("GUARDAR DATOS")

    try:
# Crear directorio data si no existe
        os.makedirs('data', exist_ok=True)

 # Guardar clientes
        with open('data/clientes.json', 'w', encoding='utf-8') as f:
            json.dump(datos_basicos.lista_clientes, f, indent=4, ensure_ascii=False)

# Guardar pedidos
        with open('data/pedidos.json', 'w', encoding='utf-8') as f:
            json.dump(datos_basicos.lista_pedidos, f, indent=4, ensure_ascii=False)

        print(" Datos guardados exitosamente en la carpeta 'data'!")
    except Exception as e:
        print(f" Error al guardar los datos: {e}")

def cargar_datos_archivo():
# Cargar los datos desde archivos JSON
    limpiar_pantalla()
    menu.mostrar_encabezado("CARGAR DATOS")

    try:
# Cargar clientes
        if os.path.exists('data/clientes.json'):
            with open('data/clientes.json', 'r', encoding='utf-8') as f:
                datos_basicos.lista_clientes = json.load(f)
            print("Clientes cargados exitosamente!")
        else:
            print("Archivo de clientes no encontrado.")

# Cargar pedidos
        if os.path.exists('data/pedidos.json'):
            with open('data/pedidos.json', 'r', encoding='utf-8') as f:
                datos_basicos.lista_pedidos = json.load(f)
                
# Actualizar contador de pedidos
                if datos_basicos.lista_pedidos:
                    datos_basicos.contador_pedidos = max(p['id'] for p in datos_basicos.lista_pedidos) + 1
            print(" Pedidos cargados exitosamente!")
        else:
            print("Archivo de pedidos no encontrado.")

    except Exception as e:
        print(f"Error al cargar los datos: {e}")

def obtener_precios_extintores():
    
# Retorna los precios de los extintores 
    return datos_basicos.precios_extintores
