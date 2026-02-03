# Sistema de Gestión de Extintores

## Descripción
Sistema de gestión de clientes y pedidos para empresa de venta y recarga de extintores, desarrollado en Python como parte del módulo 3 del Bootcamp

## Objetivo
Automatizar el proceso de gestión de clientes, ventas y recargas de extintores, aplicando conceptos de Python nivel intermedio.

# Funcionalidades Principales

## Gestión de Clientes
- Registro de clientes (personas y empresas)
- Almacenamiento de datos básicos y de contacto
- Búsqueda por RUT
- Listado completo de clientes

## Gestión de Pedidos
- Registro de ventas de extintores nuevos
- Registro de recargas de extintores
- Sistema de precios diferenciados
- Cálculo automático de IVA (19%)

## Sistema de Precios
- Extintores nuevos: 1kg($9.500) a 50kg($290.000)
- Recargas: $4.000 a $10.000 según tamaño
- Extintores reacondicionados: 50% descuento frente a los extintores nuevos

## Reportes y Estadísticas
- Listado de clientes y pedidos
- Estadísticas de ventas
- Cotizaciones rápidas
- Cálculo de ingresos totales

# Estructura del Proyecto

/extintores_system/
├── main.py      # Punto de entrada
├── README.md    # Documentación
├── modules/     # Módulos del sistema
│ ├── init.py
│ ├── datos_basicos.py
│ ├── validaciones.py
│ ├── menu.py
│ ├── gestion_datos.py
│ └── funciones_utiles.py
└── data/        # Datos guardados
├── clientes.json
└── pedidos.json


