
# Módulo de validaciones del sistema de gestión de extintores

import re

# Algoritmo de validación de RUT
def validar_rut(rut):
    
# Validador  del formato del RUT chileno"""
    rut = rut.replace(".", "").replace("-", "").upper()
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        return False, "Formato de RUT inválido"

    rut_numerico = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplicador = 2
    for i in reversed(rut_numerico):
        suma += int(i) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2

    resto = suma % 11
    dv_calculado = str(11 - resto) if resto != 0 else '0'
    if dv == 'K':
        dv_calculado = 'K'

    if str(dv_calculado) != dv:
        return False, "RUT inválido"

    return True, rut

def validar_email(email):
    
# Valida el formato del email
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email):
        return True, email
    return False, "Formato de email inválido"

def validar_telefono(telefono):
    
# Valida el formato del teléfono chileno
    telefono = telefono.replace(" ", "").replace("-", "").replace("+56", "")
    if telefono.startswith("9") and len(telefono) == 9:
        return True, telefono
    elif len(telefono) == 8:
        return True, telefono
    return False, "Formato de teléfono inválido"

def validar_numero_positivo(texto, campo="valor"):
    
# Valida que sea un número positivo
    try:
        numero = int(texto)
        if numero > 0:
            return True, numero
        return False, f"El {campo} debe ser mayor a 0"
    except ValueError:
        return False, f"El {campo} debe ser un número entero"

def validar_opcion_menu(opcion, opciones_validas):
    
# Valida que la opción esté en el rango válido
    if opcion in opciones_validas:
        return True, opcion
    return False, "Opción inválida"
