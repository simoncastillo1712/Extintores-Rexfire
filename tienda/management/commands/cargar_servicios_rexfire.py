from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Carga categorías y productos de servicios y accesorios REXFIRE'

    def handle(self, *args, **options):
        # Categorías
        cat_servicios, created = Categoria.objects.get_or_create(
            nombre='Servicios',
            defaults={'descripcion': 'Servicios de recarga, recambio, capacitación e instalación de extintores'}
        )
        self.stdout.write(self.style.SUCCESS(f'Categoría: {cat_servicios.nombre}') if created
                          else f'Categoría ya existe: {cat_servicios.nombre}')

        cat_accesorios, created = Categoria.objects.get_or_create(
            nombre='Accesorios',
            defaults={'descripcion': 'Accesorios para extintores: señalética y ganchos de instalación'}
        )
        self.stdout.write(self.style.SUCCESS(f'Categoría: {cat_accesorios.nombre}') if created
                          else f'Categoría ya existe: {cat_accesorios.nombre}')

        cat_recargas, _ = Categoria.objects.get_or_create(
            nombre='Recargas',
            defaults={'descripcion': 'Recarga de extintores (revisión técnica y certificación)'}
        )
        cat_recambios, _ = Categoria.objects.get_or_create(
            nombre='Recambios',
            defaults={'descripcion': 'Recambio de extintores'}
        )
        cat_spray, _ = Categoria.objects.get_or_create(
            nombre='Extintor Spray',
            defaults={'descripcion': 'Extintores en formato spray'}
        )

        # Servicios y accesorios
        items = [
            {
                'nombre': 'Recarga Extintor 1KG',
                'precio': 4000,
                'stock': 999,
                'id_categoria': cat_recargas,
                'descripcion': 'Recarga de extintor PQS 1KG. Incluye revisión técnica y certificación.',
            },
            {
                'nombre': 'Recarga Extintor 2KG',
                'precio': 6000,
                'stock': 999,
                'id_categoria': cat_recargas,
                'descripcion': 'Recarga de extintor PQS 2KG. Incluye revisión técnica y certificación.',
            },
            {
                'nombre': 'Recarga Extintor 4KG',
                'precio': 8000,
                'stock': 999,
                'id_categoria': cat_recargas,
                'descripcion': 'Recarga de extintor PQS 4KG. Incluye revisión técnica y certificación.',
            },
            {
                'nombre': 'Recarga Extintor 6KG y 10KG',
                'precio': 10000,
                'stock': 999,
                'id_categoria': cat_recargas,
                'descripcion': 'Recarga de extintor PQS 6KG o 10KG. Incluye revisión técnica y certificación.',
            },
            {
                'nombre': 'Recambio Extintor Taxis y Colectivos 1KG',
                'precio': 3000,
                'stock': 999,
                'id_categoria': cat_recambios,
                'descripcion': 'Recambio de extintor 1KG para taxis y colectivos.',
            },
            {
                'nombre': 'Recambio Extintor 1KG',
                'precio': 4000,
                'stock': 999,
                'id_categoria': cat_recambios,
                'descripcion': 'Recambio de extintor 1KG.',
            },
            {
                'nombre': 'Recambio Extintor 2KG',
                'precio': 6000,
                'stock': 999,
                'id_categoria': cat_recambios,
                'descripcion': 'Recambio de extintor 2KG.',
            },
            {
                'nombre': 'Recambio Extintor 4KG',
                'precio': 8000,
                'stock': 999,
                'id_categoria': cat_recambios,
                'descripcion': 'Recambio de extintor 4KG.',
            },
            {
                'nombre': 'Recambio Extintor 6KG y 10KG',
                'precio': 10000,
                'stock': 999,
                'id_categoria': cat_recambios,
                'descripcion': 'Recambio de extintor 6KG o 10KG.',
            },
            {
                'nombre': 'Capacitación uso de extintores',
                'precio': 0,
                'stock': 999,
                'id_categoria': cat_servicios,
                'descripcion': 'Capacitación al equipo de trabajo sobre uso correcto de extintores. '
                               'Sin costo adicional, incluido como valor agregado.',
            },
            {
                'nombre': 'Instalación de extintores',
                'precio': 5000,
                'stock': 999,
                'id_categoria': cat_servicios,
                'descripcion': 'Instalación profesional de extintores en su local o empresa. '
                               'Valor por extintor.',
            },
            {
                'nombre': 'Señalética extintor',
                'precio': 1500,
                'stock': 999,
                'id_categoria': cat_accesorios,
                'descripcion': 'Señalética oficial para extintores según normativa. '
                               'Valor por unidad.',
            },
            {
                'nombre': 'Gancho extintor',
                'precio': 2000,
                'stock': 999,
                'id_categoria': cat_accesorios,
                'descripcion': 'Gancho de pared para la instalación del extintor. '
                               'Valor por unidad.',
            },
            {
                'nombre': 'Extintor Spray',
                'precio': 3500,
                'stock': 999,
                'id_categoria': cat_spray,
                'descripcion': 'Extintor en formato spray.',
            },
        ]

        # Producto genérico antiguo: reemplazado por los recambios por tamaño
        from tienda.models import DetalleVenta
        antiguo = Producto.objects.filter(nombre='Recambio de Extintor').first()
        if antiguo and not DetalleVenta.objects.filter(id_producto=antiguo).exists():
            antiguo.delete()

        for item in items:
            obj, created = Producto.objects.update_or_create(
                nombre=item['nombre'],
                defaults={
                    'precio': item['precio'],
                    'stock': item['stock'],
                    'id_categoria': item['id_categoria'],
                    'descripcion': item['descripcion'],
                }
            )
            if created:
                precio_label = f"${item['precio']:,}" if item['precio'] > 0 else 'GRATIS'
                self.stdout.write(self.style.SUCCESS(f'  Creado: {obj.nombre} ({precio_label})'))
            else:
                self.stdout.write(f'  Actualizado: {obj.nombre}')

        self.stdout.write(self.style.SUCCESS('\nServicios y accesorios cargados exitosamente.'))
