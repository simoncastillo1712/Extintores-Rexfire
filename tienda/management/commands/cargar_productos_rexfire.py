from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Carga las categorías y productos de Extintores REXFIRE'

    def handle(self, *args, **options):
        # Categorías
        cat_pqs, created = Categoria.objects.get_or_create(
            nombre='PQS (Polvo Químico Seco)',
            defaults={
                'descripcion': 'Extintores de polvo químico seco multiuso para fuegos Clase A-B-C'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Categoría creada: {cat_pqs.nombre}'))
        else:
            self.stdout.write(f'Categoría ya existe: {cat_pqs.nombre}')

        cat_co2, created = Categoria.objects.get_or_create(
            nombre='CO2 (Dióxido de Carbono)',
            defaults={
                'descripcion': 'Extintores de gas CO2 para equipos eléctricos y electrónicos'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Categoría creada: {cat_co2.nombre}'))
        else:
            self.stdout.write(f'Categoría ya existe: {cat_co2.nombre}')

        # Productos
        productos = [
            {
                'nombre': 'Extintor 1KG PQS',
                'precio': 9500,
                'stock': 100,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 1A:2B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 10 a 15 seg. | '
                    'Recomendado para Vehículos Particulares'
                ),
            },
            {
                'nombre': 'Extintor 2KG PQS',
                'precio': 14500,
                'stock': 80,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 2A:5B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 10 a 15 seg. | '
                    'Recomendado para Camionetas, utilitarios, habitaciones pequeñas y embarcaciones'
                ),
            },
            {
                'nombre': 'Extintor 4KG PQS',
                'precio': 23500,
                'stock': 60,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 4A:10B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 15 a 25 seg. | '
                    'Recomendado para Locomoción Escolar, Camiones de carga, Bodegas y Negocios pequeños'
                ),
            },
            {
                'nombre': 'Extintor 6KG PQS',
                'precio': 28500,
                'stock': 50,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 6A:20B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 15 a 25 seg. | '
                    'Recomendado para Camiones de Transporte de Gas, Buses y Domicilios Particulares'
                ),
            },
            {
                'nombre': 'Extintor 10KG PQS',
                'precio': 39500,
                'stock': 30,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 10A:40B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 15 a 25 seg. | '
                    'Recomendado para Camiones grandes, empresas, bodegas, industrias, '
                    'comercios, edificios, colegios, casas amplias, minería'
                ),
            },
            {
                'nombre': 'Extintor 5KG CO2',
                'precio': 58500,
                'stock': 20,
                'id_categoria': cat_co2,
                'descripcion': (
                    'Aislante Eléctrico hasta 100.000 Volts | Potencial de Extinción 5B:C | '
                    'Fuegos Clase B-C | Tiempo de Descarga 21 seg. | '
                    'Recomendado para empresas, domicilios, salas eléctricas, salas de servidores, '
                    'cocinas, equipos electrógenos, oficinas, talleres mecánicos'
                ),
            },
            {
                'nombre': 'Extintor 25KG PQS',
                'precio': 250000,
                'stock': 10,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 40A:60B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 15 a 25 seg. | '
                    'Recomendado para Bodegas, Industrias, Colegios, Clínicas, Empresas grandes'
                ),
            },
            {
                'nombre': 'Extintor 50KG PQS',
                'precio': 290000,
                'stock': 5,
                'id_categoria': cat_pqs,
                'descripcion': (
                    'Fosfato Monoamónico 75% | Potencial de Extinción 40A:80B-C | '
                    'Fuegos Clase A-B-C | Gas Propulsor: Nitrógeno | '
                    'Tiempo de Descarga 15 a 25 seg. | '
                    'Recomendado para Camiones grandes, Empresas, bodegas, industrias, '
                    'comercios, edificios, colegios, Universidades, minería'
                ),
            },
        ]

        for p in productos:
            obj, created = Producto.objects.update_or_create(
                nombre=p['nombre'],
                defaults={
                    'precio': p['precio'],
                    'stock': p['stock'],
                    'id_categoria': p['id_categoria'],
                    'descripcion': p['descripcion'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Producto creado: {obj.nombre}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'  Producto actualizado: {obj.nombre}'))

        self.stdout.write(self.style.SUCCESS('\nCarga completada exitosamente.'))
