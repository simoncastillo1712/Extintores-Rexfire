from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp/webhook/', views.webhook_whatsapp, name='webhook_whatsapp'),
    path('agregar_rapido/<int:producto_id>/', views.agregar_rapido, name='agregar_rapido'),
    path('agregar_multiples/', views.agregar_multiples, name='agregar_multiples'),
    path('chat/', views.chatbot_web, name='chatbot_web'),
    path('chatbot/ventas/', views.listar_ventas_chatbot, name='listar_ventas_chatbot'),
    path('chatbot/conversaciones/', views.listar_conversaciones, name='listar_conversaciones'),
    path('chatbot/conversaciones/detalle/', views.detalle_conversacion, name='detalle_conversacion'),
    path('chatbot/conversaciones/estado/', views.actualizar_estado_conversacion, name='actualizar_estado_conversacion'),
    path('chatbot/conversaciones/recordatorio/', views.enviar_recordatorio_whatsapp, name='enviar_recordatorio_whatsapp'),
    path('', views.inicio, name='inicio'),
    path('listar_productos', views.listar_productos, name='listar_productos'),
    path('servicios/', views.listar_servicios, name='listar_servicios'),
    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    
    # VISTAS ADMIN #
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),
    path('listar_productos_admin/', views.listar_productos_admin, name='listar_productos_admin'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # VENTAS Y COTIZACIONES
    path('nueva_venta/', views.nueva_venta, name='nueva_venta'),
    path('cotizacion/<int:venta_id>/', views.ver_cotizacion, name='ver_cotizacion'),

    # AUTENTICACIÓN Y COMPRA DE CLIENTES
    path('cliente/login/',    views.cliente_login,          name='cliente_login'),
    path('cliente/registro/', views.cliente_registro,       name='cliente_registro'),
    path('cliente/logout/',   views.cliente_logout_view,    name='cliente_logout'),
    path('cliente/perfil/',   views.editar_perfil_cliente,  name='editar_perfil_cliente'),
    path('cliente/historial/', views.historial_compras,     name='historial_compras'),
    path('carrito/checkout/', views.checkout,               name='checkout'),

    # VENTAS
    path('ventas/',                views.listar_ventas,   name='listar_ventas'),
    path('ventas/<int:venta_id>/', views.detalle_venta,          name='detalle_venta'),
    path('ventas/<int:venta_id>/asignar-vendedor/', views.asignar_vendedor, name='asignar_vendedor'),

    # VENDEDORES
    path('vendedores/',                        views.listar_vendedores,    name='listar_vendedores'),
    path('vendedores/crear/',                  views.crear_vendedor,       name='crear_vendedor'),
    path('vendedores/editar/<int:id>/',        views.editar_vendedor,      name='editar_vendedor'),
    path('vendedores/eliminar/<int:id>/',      views.eliminar_vendedor,    name='eliminar_vendedor'),
    path('vendedores/comisiones/<int:id>/',    views.comisiones_vendedor,  name='comisiones_vendedor'),

    # IMPRESORA DE ETIQUETAS
    path('etiquetas/',                         views.impresora_etiquetas,  name='impresora_etiquetas'),
    path('etiquetas/<int:pk>/imprimir/',       views.imprimir_etiqueta,    name='imprimir_etiqueta'),
    path('etiquetas/ajuste/',                  views.ajuste_impresion,     name='ajuste_impresion'),
]