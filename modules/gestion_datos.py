# Módulo de gestión de datos del sistema de extintores

from modules import datos_basicos, validaciones, menu
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def registrar_cliente():

#Registra un nuevo cliente
    limpiar_pantalla()
    menu.mostrar_encabezado("REGISTRO DE NUEVO CLIENTE")

    cliente = {}

# Ingresar RUT
    while True:
        rut = input("RUT (sin puntos ni guión): ").strip()
        valido, resultado = validaciones.validar_rut(rut)
        if valido:
            cliente['rut'] = resultado
            break
        print(f" {resultado}")

# Verificar si el cliente ya existe
    for c in datos_basicos.lista_clientes:
        if c['rut'] == cliente['rut']:
            print(" Ya existe un cliente con ese RUT.")
            return

# Ingresar nombre
    while True:
        nombre = input("Nombre completo: ").strip()
        if len(nombre) >= 3:
            cliente['nombre'] = nombre.title()
            break
        print(" El nombre debe tener al menos 3 caracteres.")

# Ingresar email
    while True:
        email = input("Email: ").strip()
        valido, resultado = validaciones.validar_email(email)
        if valido:
            cliente['email'] = resultado
            break
        print(f"{resultado}")

# Ingresar teléfono
    while True:
        telefono = input("Teléfono (9 dígitos): ").strip()
        valido, resultado = validaciones.validar_telefono(telefono)
        if valido:
            cliente['telefono'] = resultado
            break
        print(f"{resultado}")

# Ingresar dirección
    while True:
        direccion = input("Dirección: ").strip()
        if len(direccion) >= 10:
            cliente['direccion'] = direccion
            break
        print("La dirección debe tener al menos 10 caracteres.")

# Agregar cliente a la lista
    datos_basicos.lista_clientes.append(cliente)
    print("Cliente registrado exitosamente!")

def registrar_pedido():
    
#Registra un nuevo pedido
    limpiar_pantalla()
    menu.mostrar_encabezado("REGISTRO DE NUEVO PEDIDO")

# Verificar que existan clientes
    if not datos_basicos.lista_clientes:
        print(" No hay clientes registrados. Registre un cliente primero.")
        return

    pedido = {}

# Seleccionar cliente
    print("CLIENTES REGISTRADOS:")
    for i, cliente in enumerate(datos_basicos.lista_clientes, 1):
        print(f"{i}. {cliente['nombre']} - {cliente['rut']}")

    while True:
        opcion = input(f"\nSeleccione cliente (1-{len(datos_basicos.lista_clientes)}): ").strip()
        valido, resultado = validaciones.validar_opcion_menu(opcion, [str(i) for i in range(1, len(datos_basicos.lista_clientes)+1)])
        if valido:
            cliente_seleccionado = datos_basicos.lista_clientes[int(resultado)-1]
            pedido['cliente_rut'] = cliente_seleccionado['rut']
            pedido['cliente_nombre'] = cliente_seleccionado['nombre']
            break
        print(f" {resultado}")

# Seleccionar tipo de extintor
    tipo_extintor = menu.submenu_extintores()
    if not tipo_extintor:
        print(" Tipo de extintor inválido.")
        return
    pedido['tipo_extintor'] = tipo_extintor

# Seleccionar cantidad
    while True:
        cantidad = input("Cantidad: ").strip()
        valido, resultado = validaciones.validar_numero_positivo(cantidad, "cantidad")
        if valido:
            pedido['cantidad'] = resultado
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
            print(" Opción inválida.")
    pedido['tipo_servicio'] = tipo_servicio
    pedido['precio_unitario'] = precio_unitario

# Calcular total
    total = precio_unitario * pedido['cantidad']
    total_con_iva = int(total * 1.19)  # IVA 19%
    pedido['total'] = total_con_iva

# Asignar ID y fecha
    pedido['id'] = datos_basicos.contador_pedidos
    datos_basicos.contador_pedidos += 1

# Agregar pedido a la lista
    datos_basicos.lista_pedidos.append(pedido)

    print("\n PEDIDO REGISTRADO EXITOSAMENTE!")
    print("-" * 40)
    print(f"ID Pedido: {pedido['id']}")
    print(f"Cliente: {pedido['cliente_nombre']}")
    print(f"Tipo: {pedido['tipo_extintor']} - {pedido['tipo_servicio']}")
    print(f"Cantidad: {pedido['cantidad']}")
    print(f"TOTAL + IVA: ${pedido['total']:,}")

def listar_clientes():
    """Lista todos los clientes registrados"""
    limpiar_pantalla()
    menu.mostrar_encabezado("LISTADO DE CLIENTES")

    if not datos_basicos.lista_clientes:
        print(" No hay clientes registrados.")
    else:
        print(f"Total de clientes: {len(datos_basicos.lista_clientes)}\n")
        print("-" * 80)
        print(f"{'RUT':<12} {'Nombre':<25} {'Email':<25} {'Teléfono':<12}")
        print("-" * 80)

        for cliente in datos_basicos.lista_clientes:
            print(f"{cliente['rut']:<12} {cliente['nombre']:<25} {cliente['email']:<25} {cliente['telefono']:<12}")

def listar_pedidos():
    """Lista todos los pedidos registrados"""
    limpiar_pantalla()
    menu.mostrar_encabezado("LISTADO DE PEDIDOS")

    if not datos_basicos.lista_pedidos:
        print(" No hay pedidos registrados.")
    else:
        print(f"Total de pedidos: {len(datos_basicos.lista_pedidos)}\n")
        print("-" * 100)
        print(f"{'ID':<5} {'Cliente':<20} {'Tipo':<8} {'Cant.':<6} {'Servicio':<8} {'Total+IVA':<10}")
        print("-" * 100)

        for pedido in datos_basicos.lista_pedidos:
            print(f"{pedido['id']:<5} {pedido['cliente_nombre']:<20} {pedido['tipo_extintor']:<8} {pedido['cantidad']:<6} {pedido['tipo_servicio']:<8} ${pedido['total']:<10,}")
