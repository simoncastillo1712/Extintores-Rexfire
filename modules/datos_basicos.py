
# Módulo de datos básicos del sistema de gestión de extintores


# Listas para almacenar datos en memoria
lista_clientes = []
lista_pedidos = []

# Precios de extintores (en pesos chilenos)
precios_extintores = {
    '1kg': {'nuevo': 9500, 'recarga': 4000},
    '2kg': {'nuevo': 14500, 'recarga': 6000},
    '4kg': {'nuevo': 23500, 'recarga': 8000},
    '6kg': {'nuevo': 28500, 'recarga': 10000},
    '10kg': {'nuevo': 39500, 'recarga': 10000},
    '25kg': {'nuevo': 250000, 'recarga': 50000},
    '50kg': {'nuevo': 290000, 'recarga': 100000}
}

# Contador para IDs de pedidos
contador_pedidos = 1
