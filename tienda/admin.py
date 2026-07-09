from django.contrib import admin
from .models import *


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'precio', 'stock', 'id_categoria', 'imagen')


admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Proveedor)

