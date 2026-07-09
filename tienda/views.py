from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q, Max
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.db import IntegrityError
from urllib.parse import urlencode
import json
import re


def _productos_venta_ordenados():
    """Productos para el selector de Nueva Venta, ordenados por categoría y luego por peso numérico."""
    def sort_key(p):
        cat = p.id_categoria.nombre if p.id_categoria else 'zzz'
        # Extrae el primer número del nombre (ej. "Extintor 10KG" → 10, "Recarga 1KG" → 1)
        m = re.search(r'(\d+)', p.nombre)
        peso = int(m.group(1)) if m else 9999
        return (cat, peso, p.nombre)

    qs = Producto.objects.select_related('id_categoria').all()
    return sorted(qs, key=sort_key)

from .models import Categoria, Producto, Cliente, Proveedor, Venta, DetalleVenta, Boleta, Factura, Vendedor, VentaVendedor, ConversacionWhatsapp, ConversacionEstado
from .forms import CategoriaForm, ProductoForm, ClienteForm, ProveedorForm, VendedorForm, ClientePerfilForm

#####################################
# VISTAS PUBLICAS
#####################################

def inicio(request):
    CATS_EXCLUIDAS = ['Servicios', 'Accesorios']
    productos_destacados = Producto.objects.exclude(
        id_categoria__nombre__in=CATS_EXCLUIDAS
    )[:4]
    cat_q = request.GET.get('cat_q', '').strip()

    categorias_qs = Categoria.objects.all()
    if cat_q:
        categorias_qs = categorias_qs.filter(nombre__icontains=cat_q)

    categorias = categorias_qs[:10]

    contexto = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
        'cat_q': cat_q,
    }
    return render(request, 'inicio.html', contexto)

def listar_servicios(request):
    q = request.GET.get('q', '')
    servicios = Producto.objects.select_related('id_categoria').filter(
        id_categoria__nombre='Servicios'
    ).filter(
        Q(nombre__icontains='Recarga') |
        Q(nombre__icontains='Recambio') |
        Q(nombre__icontains='Colectivero')
    )
    if q:
        servicios = servicios.filter(nombre__icontains=q)

    carrito = request.session.get('carrito', {})
    carrito_total_items = sum(int(v) for v in carrito.values())

    return render(request, 'servicios/listar.html', {
        'servicios': servicios,
        'carrito_total_items': carrito_total_items,
        'q': q,
    })


def listar_productos(request):
    q = request.GET.get('q', '')
    CATS_EXCLUIDAS = ['Servicios', 'Accesorios']
    productos = Producto.objects.select_related('id_categoria').exclude(
        id_categoria__nombre__in=CATS_EXCLUIDAS
    )
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(id_categoria__nombre__icontains=q)
        )

    carrito = request.session.get('carrito', {})
    carrito_total_items = sum(int(cantidad) for cantidad in carrito.values())

    contexto = {
        'productos': productos,
        'carrito_total_items': carrito_total_items,
        'q': q,
    }
    return render(request, 'productos/listar.html', contexto)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    neto = 0

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id_producto=producto_id)
            subtotal = producto.precio * int(cantidad)
            neto += subtotal
            items.append({
                'producto': producto,
                'cantidad': int(cantidad),
                'subtotal': subtotal,
            })
        except Producto.DoesNotExist:
            continue

    iva = round(neto * 0.19)
    total_con_iva = neto + iva
    carrito_total_items = sum(int(cantidad) for cantidad in carrito.values())

    contexto = {
        'items': items,
        'total': neto,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'carrito_total_items': carrito_total_items,
    }
    return render(request, 'carrito/ver.html', contexto)

@require_POST
def agregar_al_carrito(request):
    try:
        data = json.loads(request.body)
        producto_id = str(data.get('producto_id'))
        cantidad = int(data.get('cantidad', 1))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({'ok': False, 'mensaje': 'Datos inválidos.'}, status=400)

    if cantidad < 1:
        return JsonResponse({'ok': False, 'mensaje': 'Cantidad inválida.'}, status=400)

    producto = get_object_or_404(Producto, id_producto=producto_id)

    carrito = request.session.get('carrito', {})
    cantidad_actual = int(carrito.get(producto_id, 0))
    nueva_cantidad = cantidad_actual + cantidad

    carrito[producto_id] = nueva_cantidad
    request.session['carrito'] = carrito
    request.session.modified = True

    total_items_carrito = sum(int(cantidad) for cantidad in carrito.values())

    return JsonResponse({
        'ok': True,
        'mensaje': f'{producto.nombre} agregado al carrito.',
        'cantidad_en_carrito': nueva_cantidad,
        'total_items_carrito': total_items_carrito,
    })

@require_POST
def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    producto_id = str(id)

    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('ver_carrito')

@require_POST
def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')


#####################################
# AUTENTICACION
#####################################

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('inicio')
        
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

#####################################
#  GESTION DE LAS CATEGORIAS
#####################################

@login_required
def listar_categorias(request):
    q = request.GET.get('q', '')
    if q:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )
    else:
        categorias = Categoria.objects.all()
    contexto = {
        'categorias': categorias,
        'q': q
    }
    return render(request, 'categorias/listar.html', contexto)

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada correctamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'categorias/form.html', contexto)

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id_categoria=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada correctamente.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'categorias/form.html', contexto)
    
    
@login_required
@require_POST
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id_categoria=id)
    try:
        categoria.delete()
        messages.success(request, f'Categoría "{categoria.nombre}" eliminada correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene productos asociados.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar la categoría.')
    return redirect('listar_categorias')
  
#####################################
#  GESTION DE PRODUCTOS
#####################################

@login_required
def listar_productos_admin(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.select_related('id_categoria')
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(id_categoria__nombre__icontains=q)
        )
    else:
        productos = productos.all()
    contexto = {
        'productos': productos,
        'q': q
    }
    return render(request, 'productos/listar_admin.html', contexto)

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente.')
            return redirect('listar_productos_admin')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form})


@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('listar_productos_admin')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'producto': producto})


@login_required
@require_POST
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    try:
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
    except RestrictedError:
        messages.error(
            request,
            f'No se puede eliminar el producto "{producto.nombre}" porque tiene registros asociados en ventas o compras.'
        )
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el producto "{producto.nombre}" porque tiene dependencias relacionadas.'
        )
    except Exception:
        messages.error(
            request,
            'Ocurrió un error inesperado al intentar eliminar el producto.'
        )
    return redirect('listar_productos_admin')

#####################################
#  GESTION DE CLIENTES
#####################################

@login_required
def listar_clientes(request):
    q = request.GET.get('q', '')
    if q:
        clientes = Cliente.objects.filter(
            Q(razon_social__icontains=q) | Q(rut_cliente__icontains=q)
        )
    else:
        clientes = Cliente.objects.all()

    # Aquí va paginación que se explicará abajo

    contexto = {
        'clientes': clientes,
        'q': q,
        # 'page_obj': page_obj, si usas paginación
    }
    return render(request, 'clientes/listar.html', contexto)

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.fecha_registro:
                cliente.fecha_registro = timezone.now()
            cliente.save()
            messages.success(request, f'Cliente "{cliente.razon_social}" creado correctamente.')
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'clientes/form.html', contexto)

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_cliente=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.fecha_registro:
                cliente.fecha_registro = timezone.now()
            cliente.save()
            messages.success(request, f'Cliente "{cliente.razon_social}" actualizado correctamente.')
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'clientes/form.html', contexto)


@login_required
@require_POST
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_cliente=id)
    try:
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.razon_social}" eliminado correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el cliente "{cliente.razon_social}" porque tiene documentos asociados.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar el cliente.')
    return redirect('listar_clientes')


#####################################
#  GESTION DE PROVEEDORES
#####################################

@login_required
def listar_proveedores(request):
    q = request.GET.get('q', '')
    if q:
        proveedores = Proveedor.objects.filter(
            Q(nombre_proveedor__icontains=q) | Q(rut_proveedor__icontains=q)
        )
    else:
        proveedores = Proveedor.objects.all()
    contexto = {
        'proveedores': proveedores,
        'q': q
    }
    return render(request, 'proveedores/listar.html', contexto)

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" creado correctamente.')
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    
    contexto = {
        'form':form
    }
    
    return render(request, 'proveedores/form.html', contexto)

@login_required
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" actualizado correctamente.')
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    contexto = {
        'form':form
    }
    
    return render(request, 'proveedores/form.html', contexto)


@login_required
@require_POST
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    try:
        proveedor.delete()
        messages.success(request, f'Proveedor "{proveedor.nombre_proveedor}" eliminado correctamente.')
    except IntegrityError:
        messages.error(
            request,
            f'No se puede eliminar el proveedor "{proveedor.nombre_proveedor}" porque tiene compras asociadas.'
        )
    except Exception:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar el proveedor.')
    return redirect('listar_proveedores')


#####################################
#  VENTAS Y COTIZACIONES
#####################################

@login_required
def nueva_venta(request):
    if request.method == 'POST':
        tipo_documento = request.POST.get('tipo_documento', 'boleta')
        cliente_mode = request.POST.get('cliente_mode', 'new')

        # Obtener o crear cliente
        cliente = None
        if cliente_mode == 'existing':
            cliente_id = request.POST.get('cliente_id', '').strip()
            if cliente_id:
                cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
        else:
            rut = request.POST.get('nuevo_rut', '').strip()
            nombre = request.POST.get('nuevo_nombre', '').strip()
            if rut and nombre:
                cliente, _ = Cliente.objects.get_or_create(
                    rut_cliente=rut,
                    defaults={
                        'razon_social': nombre,
                        'direccion': request.POST.get('nuevo_direccion', '').strip() or None,
                        'telefono': request.POST.get('nuevo_telefono', '').strip() or None,
                        'email': request.POST.get('nuevo_email', '').strip() or None,
                        'fecha_registro': timezone.now(),
                    }
                )

        # Procesar líneas de productos y servicios
        producto_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        precios_form = request.POST.getlist('precio_unitario[]')

        if not any(producto_ids):
            messages.error(request, 'Debe agregar al menos un producto o servicio.')
            return render(request, 'ventas/nueva.html', {
                'clientes': Cliente.objects.all().order_by('razon_social'),
                'productos': _productos_venta_ordenados(),
            })

        neto = 0
        lineas = []
        for i, pid in enumerate(producto_ids):
            if not pid:
                continue
            try:
                producto = Producto.objects.get(id_producto=int(pid))
                cantidad = max(1, int(cantidades[i]) if i < len(cantidades) else 1)
                # Usar precio del formulario (permite override del precio de BD)
                precio_raw = precios_form[i] if i < len(precios_form) else '0'
                precio_unit = max(0, int(float(precio_raw or 0)))
                subtotal = precio_unit * cantidad
                neto += subtotal
                lineas.append((producto, cantidad, precio_unit, subtotal))
            except (Producto.DoesNotExist, ValueError, TypeError):
                continue

        if not lineas:
            messages.error(request, 'No se encontraron productos válidos.')
            return render(request, 'ventas/nueva.html', {
                'clientes': Cliente.objects.all().order_by('razon_social'),
                'productos': _productos_venta_ordenados(),
            })

        iva = round(neto * 0.19)
        total = neto + iva

        # Crear Venta
        venta = Venta(fecha=timezone.now(), total=total, tipo_documento=tipo_documento)
        venta.save()

        # Crear DetalleVenta
        for producto, cantidad, precio_unit, subtotal in lineas:
            DetalleVenta(
                id_venta=venta,
                id_producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unit,
                subtotal=subtotal,
            ).save()

        # Crear Boleta o Factura
        if tipo_documento == 'boleta':
            ultimo = Boleta.objects.aggregate(m=Max('numero_boleta'))['m'] or 0
            Boleta(id_venta=venta, numero_boleta=ultimo + 1, fecha_emision=timezone.now()).save()
        else:
            ultimo = Factura.objects.aggregate(m=Max('numero_factura'))['m'] or 0
            Factura(
                id_venta=venta,
                numero_factura=ultimo + 1,
                fecha_emision=timezone.now(),
                id_cliente=cliente,
            ).save()

        # Registrar vendedor y comisión
        vendedor_id = request.POST.get('vendedor_id', '').strip()
        vendedor_obj = None
        if vendedor_id:
            try:
                vendedor_obj = Vendedor.objects.get(id_vendedor=int(vendedor_id))
            except (Vendedor.DoesNotExist, ValueError):
                pass

        comision = round(neto * 0.20)
        VentaVendedor(
            id_venta=venta,
            id_vendedor=vendedor_obj,
            id_cliente=cliente.id_cliente if cliente else None,
            nombre_cliente=cliente.razon_social if cliente else None,
            neto=neto,
            comision=comision,
        ).save()

        messages.success(request, 'Venta registrada exitosamente.')
        url = reverse('ver_cotizacion', args=[venta.id_venta])
        if cliente and tipo_documento == 'boleta':
            url += f'?cliente_id={cliente.id_cliente}'
        return redirect(url)

    # GET
    return render(request, 'ventas/nueva.html', {
        'clientes': Cliente.objects.all().order_by('razon_social'),
        'productos': _productos_venta_ordenados(),
        'vendedores': Vendedor.objects.filter(activo=True).order_by('nombre'),
    })


def ver_cotizacion(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    detalles = DetalleVenta.objects.filter(id_venta=venta).select_related('id_producto')

    neto = sum(d.subtotal for d in detalles)
    iva = round(neto * 0.19)
    total = neto + iva

    try:
        boleta = venta.boleta
    except Boleta.DoesNotExist:
        boleta = None

    try:
        factura = venta.factura
    except Factura.DoesNotExist:
        factura = None

    numero_documento = None
    if boleta:
        numero_documento = boleta.numero_boleta
    elif factura:
        numero_documento = factura.numero_factura
    else:
        numero_documento = venta.id_venta

    cliente = None
    if factura and factura.id_cliente:
        cliente = factura.id_cliente
    elif request.GET.get('cliente_id'):
        try:
            cliente = Cliente.objects.get(id_cliente=int(request.GET['cliente_id']))
        except (Cliente.DoesNotExist, ValueError):
            pass

    # Calcular despacho según monto neto
    if neto >= 300000:
        despacho_neto = 0
        despacho_tipo = 'gratis'
    elif neto >= 50000:
        despacho_neto = 6800
        despacho_tipo = 'cobro'
    else:
        despacho_neto = None
        despacho_tipo = 'sin_despacho'

    despacho_iva = round(despacho_neto * 0.19) if despacho_neto else 0
    despacho_total = (despacho_neto or 0) + despacho_iva

    total_con_despacho_neto = neto + (despacho_neto or 0)
    total_con_despacho_iva = round(total_con_despacho_neto * 0.19)
    total_con_despacho = total_con_despacho_neto + total_con_despacho_iva

    return render(request, 'ventas/cotizacion.html', {
        'venta': venta,
        'detalles': detalles,
        'neto': neto,
        'iva': iva,
        'total': total,
        'numero_documento': numero_documento,
        'cliente': cliente,
        'boleta': boleta,
        'factura': factura,
        'despacho_neto': despacho_neto,
        'despacho_iva': despacho_iva,
        'despacho_total': despacho_total,
        'despacho_tipo': despacho_tipo,
        'total_con_despacho_neto': total_con_despacho_neto,
        'total_con_despacho_iva': total_con_despacho_iva,
        'total_con_despacho': total_con_despacho,
    })


#####################################
#  AUTENTICACIÓN Y COMPRA DE CLIENTES
#####################################

def cliente_login(request):
    next_url = request.GET.get('next', reverse('checkout'))
    error = None
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        if not rut:
            error = 'Ingresa tu RUT para continuar.'
        else:
            try:
                cliente = Cliente.objects.get(rut_cliente=rut)
                request.session['cliente_id'] = cliente.id_cliente
                request.session['cliente_nombre'] = cliente.razon_social
                return redirect(next_url)
            except Cliente.DoesNotExist:
                qs = urlencode({'rut': rut, 'next': next_url})
                return redirect(f"{reverse('cliente_registro')}?{qs}")
    return render(request, 'clientes/cliente_login.html', {
        'next': next_url,
        'error': error,
    })


def cliente_registro(request):
    next_url = request.GET.get('next', reverse('checkout'))
    rut_inicial = request.GET.get('rut', '')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            if not cliente.fecha_registro:
                cliente.fecha_registro = timezone.now()
            cliente.save()
            request.session['cliente_id'] = cliente.id_cliente
            request.session['cliente_nombre'] = cliente.razon_social
            messages.success(request, f'¡Bienvenido/a {cliente.razon_social}! Cuenta creada exitosamente.')
            return redirect(next_url)
        next_url = request.POST.get('next', next_url)
    else:
        form = ClienteForm(initial={'rut_cliente': rut_inicial})
    return render(request, 'clientes/cliente_registro.html', {
        'form': form,
        'next': next_url,
    })


@require_POST
def cliente_logout_view(request):
    request.session.pop('cliente_id', None)
    request.session.pop('cliente_nombre', None)
    return redirect('inicio')


def checkout(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect(f"{reverse('cliente_login')}?next={reverse('checkout')}")

    cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
    carrito = request.session.get('carrito', {})

    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')

    CATS_EXTINTORES = ['PQS (Polvo Químico Seco)', 'CO2 (Dióxido de Carbono)']

    items, neto = [], 0
    for pid, cantidad in carrito.items():
        try:
            producto = Producto.objects.select_related('id_categoria').get(id_producto=int(pid))
            sub = producto.precio * int(cantidad)
            neto += sub
            items.append({
                'producto': producto,
                'cantidad': int(cantidad),
                'subtotal': sub,
            })
        except (Producto.DoesNotExist, ValueError):
            continue

    # Contar unidades de extintores NUEVOS (no recargas/recambios)
    extintores_nuevos = sum(
        item['cantidad'] for item in items
        if item['producto'].id_categoria and
        item['producto'].id_categoria.nombre in CATS_EXTINTORES
    )

    # IDs de accesorios y servicios regalo para los modales
    gancho_id = senialetica_id = instalacion_id = capacitacion_id = None
    if extintores_nuevos > 0:
        try:
            gancho_id = Producto.objects.get(nombre='Gancho extintor').id_producto
            senialetica_id = Producto.objects.get(nombre='Señalética extintor').id_producto
        except Producto.DoesNotExist:
            pass
        try:
            instalacion_id = Producto.objects.get(nombre='Instalación de extintores').id_producto
        except Producto.DoesNotExist:
            pass
        try:
            capacitacion_id = Producto.objects.get(nombre='Capacitación uso de extintores').id_producto
        except Producto.DoesNotExist:
            pass

    iva = round(neto * 0.19)
    total = neto + iva

    if request.method == 'POST':
        if not items:
            messages.error(request, 'No hay productos válidos en el carrito.')
            return redirect('ver_carrito')

        origen = request.session.pop('carrito_origen', 'web')
        venta = Venta(fecha=timezone.now(), total=total, tipo_documento='boleta', origen=origen)
        venta.save()

        for item in items:
            DetalleVenta(
                id_venta=venta,
                id_producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['producto'].precio,
                subtotal=item['subtotal'],
            ).save()

        ultimo = Boleta.objects.aggregate(m=Max('numero_boleta'))['m'] or 0
        Boleta(id_venta=venta, numero_boleta=ultimo + 1, fecha_emision=timezone.now()).save()

        VentaVendedor(
            id_venta=venta,
            id_vendedor=None,
            id_cliente=cliente.id_cliente,
            nombre_cliente=cliente.razon_social,
            neto=neto,
            comision=0,
        ).save()

        request.session['carrito'] = {}
        request.session.modified = True

        messages.success(request, '¡Compra confirmada! Aquí está tu boleta.')
        return redirect(f"{reverse('ver_cotizacion', args=[venta.id_venta])}?cliente_id={cliente.id_cliente}")

    return render(request, 'carrito/checkout.html', {
        'cliente': cliente,
        'items': items,
        'neto': neto,
        'iva': iva,
        'total': total,
        'extintores_nuevos': extintores_nuevos,
        'gancho_id': gancho_id,
        'senialetica_id': senialetica_id,
        'instalacion_id': instalacion_id,
        'capacitacion_id': capacitacion_id,
    })


#####################################
#  VENTAS — LISTADO Y DETALLE
#####################################

def _build_venta_row(v):
    """Construye un dict con todos los datos de una venta."""
    try:
        boleta = v.boleta
    except Boleta.DoesNotExist:
        boleta = None

    try:
        factura = v.factura
    except Factura.DoesNotExist:
        factura = None

    try:
        info = v.info_vendedor
    except VentaVendedor.DoesNotExist:
        info = None

    tipo = 'Boleta' if boleta else ('Factura' if factura else '—')
    numero = boleta.numero_boleta if boleta else (factura.numero_factura if factura else '—')

    cliente_obj = None
    if factura and factura.id_cliente:
        cliente_obj = factura.id_cliente
    elif info and info.id_cliente:
        try:
            cliente_obj = Cliente.objects.get(id_cliente=info.id_cliente)
        except Cliente.DoesNotExist:
            pass

    # Neto: desde VentaVendedor si está disponible, sino derivado del total
    if info and info.neto:
        neto = info.neto
    else:
        neto = round(v.total / 1.19)

    return {
        'venta': v,
        'tipo': tipo,
        'numero': numero,
        'boleta': boleta,
        'factura': factura,
        'info': info,
        'cliente': cliente_obj,
        'nombre_cliente': info.nombre_cliente if info else None,
        'neto': neto,
    }


#####################################
#  PERFIL E HISTORIAL DEL CLIENTE
#####################################

def _cliente_requerido(request, next_url=None):
    """Redirige al login de cliente si no hay sesión activa."""
    if not next_url:
        next_url = request.path
    if not request.session.get('cliente_id'):
        return redirect(f"{reverse('cliente_login')}?next={next_url}")
    return None


def editar_perfil_cliente(request):
    redir = _cliente_requerido(request)
    if redir:
        return redir

    cliente = get_object_or_404(Cliente, id_cliente=request.session['cliente_id'])

    if request.method == 'POST':
        form = ClientePerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            request.session['cliente_nombre'] = cliente.razon_social
            messages.success(request, 'Tus datos fueron actualizados correctamente.')
            return redirect('editar_perfil_cliente')
    else:
        form = ClientePerfilForm(instance=cliente)

    return render(request, 'clientes/perfil.html', {'form': form, 'cliente': cliente})


def historial_compras(request):
    redir = _cliente_requerido(request)
    if redir:
        return redir

    cliente = get_object_or_404(Cliente, id_cliente=request.session['cliente_id'])

    ventas_info = (VentaVendedor.objects
                   .filter(id_cliente=cliente.id_cliente)
                   .select_related('id_venta')
                   .order_by('-id_venta__fecha'))

    compras = []
    for vv in ventas_info:
        v = vv.id_venta
        try:
            boleta = v.boleta
        except Boleta.DoesNotExist:
            boleta = None
        try:
            factura = v.factura
        except Factura.DoesNotExist:
            factura = None

        tipo = 'Boleta' if boleta else ('Factura' if factura else '—')
        numero = (boleta.numero_boleta if boleta else
                  factura.numero_factura if factura else '—')

        detalles = DetalleVenta.objects.filter(id_venta=v).select_related('id_producto')
        compras.append({
            'venta': v,
            'tipo': tipo,
            'numero': numero,
            'neto': vv.neto,
            'total': v.total,
            'detalles': detalles,
        })

    return render(request, 'clientes/historial.html', {
        'cliente': cliente,
        'compras': compras,
    })


@login_required
def listar_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    rows = [_build_venta_row(v) for v in ventas]
    return render(request, 'ventas/listar_ventas.html', {'rows': rows})


@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    detalles = DetalleVenta.objects.filter(id_venta=venta).select_related('id_producto')
    row = _build_venta_row(venta)

    neto = sum(d.subtotal for d in detalles)
    iva = round(neto * 0.19)

    if neto >= 300000:
        despacho_neto, despacho_tipo = 0, 'gratis'
    elif neto >= 50000:
        despacho_neto, despacho_tipo = 6800, 'cobro'
    else:
        despacho_neto, despacho_tipo = None, 'sin_despacho'

    despacho_iva = round((despacho_neto or 0) * 0.19)
    total_neto = neto + (despacho_neto or 0)
    total_final = total_neto + round(total_neto * 0.19)

    return render(request, 'ventas/detalle_venta.html', {
        **row,
        'detalles': detalles,
        'neto': neto,
        'iva': iva,
        'despacho_neto': despacho_neto,
        'despacho_tipo': despacho_tipo,
        'despacho_iva': despacho_iva,
        'total_neto': total_neto,
        'total_final': total_final,
        'vendedores_disponibles': Vendedor.objects.filter(activo=True).order_by('nombre'),
    })


@login_required
@require_POST
def asignar_vendedor(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    vendedor_id = request.POST.get('vendedor_id', '').strip()
    vendedor = get_object_or_404(Vendedor, id_vendedor=int(vendedor_id))

    try:
        vv = venta.info_vendedor
    except VentaVendedor.DoesNotExist:
        vv = None

    if vv:
        vv.id_vendedor = vendedor
        vv.comision = round(vv.neto * 0.20)
        vv.save()
    else:
        detalles = DetalleVenta.objects.filter(id_venta=venta)
        neto = sum(d.subtotal for d in detalles)
        VentaVendedor(
            id_venta=venta,
            id_vendedor=vendedor,
            neto=neto,
            comision=round(neto * 0.20),
        ).save()

    messages.success(request, f'Vendedor "{vendedor.nombre}" asignado correctamente.')
    return redirect('detalle_venta', venta_id=venta_id)


#####################################
#  VENDEDORES — CRUD + COMISIONES
#####################################

@login_required
def listar_vendedores(request):
    vendedores = Vendedor.objects.all().order_by('nombre')
    data = []
    for v in vendedores:
        vv = VentaVendedor.objects.filter(id_vendedor=v)
        data.append({
            'vendedor': v,
            'num_ventas': vv.count(),
            'total_neto': sum(x.neto for x in vv),
            'total_comision': sum(x.comision for x in vv),
        })
    return render(request, 'vendedores/listar.html', {'data': data})


@login_required
def crear_vendedor(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            v = form.save()
            messages.success(request, f'Vendedor "{v.nombre}" creado correctamente.')
            return redirect('listar_vendedores')
    else:
        form = VendedorForm()
    return render(request, 'vendedores/form.html', {'form': form})


@login_required
def editar_vendedor(request, id):
    vendedor = get_object_or_404(Vendedor, id_vendedor=id)
    if request.method == 'POST':
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            v = form.save()
            messages.success(request, f'Vendedor "{v.nombre}" actualizado.')
            return redirect('listar_vendedores')
    else:
        form = VendedorForm(instance=vendedor)
    return render(request, 'vendedores/form.html', {'form': form, 'vendedor': vendedor})


@login_required
@require_POST
def eliminar_vendedor(request, id):
    vendedor = get_object_or_404(Vendedor, id_vendedor=id)
    nombre = vendedor.nombre
    vendedor.delete()
    messages.success(request, f'Vendedor "{nombre}" eliminado.')
    return redirect('listar_vendedores')


@login_required
def comisiones_vendedor(request, id):
    vendedor = get_object_or_404(Vendedor, id_vendedor=id)
    ventas = (VentaVendedor.objects
              .filter(id_vendedor=vendedor)
              .select_related('id_venta')
              .order_by('-id_venta__fecha'))
    total_neto = sum(v.neto for v in ventas)
    total_comision = sum(v.comision for v in ventas)
    return render(request, 'vendedores/comisiones.html', {
        'vendedor': vendedor,
        'ventas': ventas,
        'total_neto': total_neto,
        'total_comision': total_comision,
    })


#####################################
#  HISTORIAL CHATBOT (admin)
#####################################

def _autodetectar_estado(mensajes):
    """Infiere el estado de compra analizando el contenido de los mensajes."""
    texto = ' '.join(m.contenido for m in mensajes).lower()
    # Compra concretada: bot confirmó pago/pedido
    if 'compra confirmada' in texto or 'pedido confirmado' in texto or 'venta registrada' in texto:
        return 'concretada'
    # Cotización enviada
    if '✅' in texto and ('cotización' in texto or 'cotizacion' in texto):
        return 'cotizacion_enviada'
    # Cart links = mostró oferta concreta
    if 'agregar_rapido' in texto or 'agregar_multiples' in texto:
        return 'interesado'
    # Solo habló de precios/productos sin llegar a link
    if any(w in texto for w in ['precio', 'extintor', 'pqs', 'co2', 'kg', 'cuánto', 'cuanto']):
        return 'en_consulta'
    return 'en_consulta'


@login_required
def listar_ventas_chatbot(request):
    """Ventas originadas desde el chatbot (origen='chatbot'). Comisión = 0."""
    ventas = (Venta.objects
              .filter(origen='chatbot')
              .prefetch_related('detalleventa_set__id_producto')
              .order_by('-fecha'))

    # Totales globales
    total_neto       = sum(int(v.total / 1.19) for v in ventas)
    total_iva        = sum(v.total - int(v.total / 1.19) for v in ventas)
    total_general    = sum(v.total for v in ventas)
    ahorro_comisiones = round(total_neto * 0.20)   # lo que costaría con vendedor humano al 20%

    return render(request, 'chatbot/ventas_chatbot.html', {
        'ventas':             ventas,
        'total_neto':         total_neto,
        'total_iva':          total_iva,
        'total_general':      total_general,
        'ahorro_comisiones':  ahorro_comisiones,
    })


@login_required
def listar_conversaciones(request):
    """Lista de contactos únicos con estado de compra."""
    from django.db.models import Max, Count
    from django.utils import timezone as tz
    import datetime

    ultimos = (ConversacionWhatsapp.objects
               .values('telefono')
               .annotate(ultima_fecha=Max('fecha'), total=Count('id'))
               .order_by('-ultima_fecha'))

    ahora = tz.now()
    contactos = []
    for row in ultimos:
        tel = row['telefono']
        mensajes    = list(ConversacionWhatsapp.objects.filter(telefono=tel).order_by('fecha'))
        ultimo_msg  = mensajes[-1] if mensajes else None

        # Estado manual guardado (o None si no existe)
        estado_obj  = ConversacionEstado.objects.filter(telefono=tel).first()

        # Si no hay estado manual, autodetectar
        if estado_obj:
            estado_compra = estado_obj.estado
        else:
            estado_compra = _autodetectar_estado(mensajes)

        # Auto-abandono: interesado sin actividad por 3 días → abandonada
        if estado_compra == 'interesado' and (ahora - row['ultima_fecha']) > datetime.timedelta(days=3):
            estado_obj, _ = ConversacionEstado.objects.get_or_create(telefono=tel)
            if estado_obj.estado in ('en_consulta', 'interesado'):
                estado_obj.estado = 'abandonada'
                estado_obj.save()
                estado_compra = 'abandonada'

        # Estado de actividad (para badge secundario)
        hace = ahora - row['ultima_fecha']
        if hace < datetime.timedelta(hours=1):
            actividad = 'reciente'
        elif ultimo_msg and ultimo_msg.rol == 'user':
            actividad = 'espera'
        else:
            actividad = 'respondido'

        contactos.append({
            'telefono':     tel,
            'ultimo_msg':   ultimo_msg,
            'total':        row['total'],
            'ultima_fecha': row['ultima_fecha'],
            'actividad':    actividad,
            'estado_compra': estado_compra,
            'tiene_estado_manual': bool(estado_obj),
        })

    return render(request, 'chatbot/lista.html', {
        'contactos': contactos,
        'opciones_estado': ConversacionEstado.ESTADOS,
    })


@login_required
@require_POST
def enviar_recordatorio_whatsapp(request):
    """Envía un mensaje de recordatorio de carrito abandonado al cliente por WhatsApp."""
    telefono = request.POST.get('telefono', '').strip()
    if not telefono:
        messages.error(request, 'Teléfono no válido.')
        return redirect('listar_conversaciones')

    # Obtener los productos que el bot le ofreció (del historial)
    historial_msgs = ConversacionWhatsapp.objects.filter(telefono=telefono).order_by('fecha')
    texto_conv = ' '.join(m.contenido for m in historial_msgs)

    # Extraer nombre del cliente si aparece en la conversación
    nombre_match = re.search(
        r'(?:hola[,\s]+|buenas[,\s]+)([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
        texto_conv
    )
    nombre = nombre_match.group(1) if nombre_match else 'Cliente'

    site_url = request.build_absolute_uri('/').rstrip('/')
    mensaje = (
        f"¡Hola {nombre}! 👋 Te escribimos desde *Extintores REXFIRE*.\n\n"
        f"Notamos que hace unos días estuviste revisando nuestros extintores "
        f"pero no pudiste completar tu compra. 🛒\n\n"
        f"¿Podemos ayudarte a concretar? Nuestros precios siguen vigentes y "
        f"contamos con stock disponible 🔥\n\n"
        f"Recuerda que en compras de extintores nuevos incluimos:\n"
        f"✅ Instalación GRATIS\n"
        f"✅ Capacitación GRATIS\n\n"
        f"Escríbeme aquí mismo o visita nuestra tienda:\n"
        f"🌐 {site_url}\n"
        f"📞 +569 7555 5423"
    )

    try:
        from twilio.rest import Client as TwilioClient
        from django.conf import settings
        client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=telefono,
            body=mensaje,
        )
        # Guardar en historial
        ConversacionWhatsapp.objects.create(
            telefono=telefono, rol='assistant', contenido=mensaje
        )
        # Actualizar estado a "interesado" (relanzamos el proceso de venta)
        ConversacionEstado.objects.update_or_create(
            telefono=telefono,
            defaults={'estado': 'interesado'},
        )
        messages.success(request, f'✅ Recordatorio enviado a {telefono}.')
    except Exception as e:
        messages.error(request, f'Error al enviar: {e}')

    from urllib.parse import urlencode as _ue
    return redirect(f"{reverse('detalle_conversacion')}?{_ue({'tel': telefono})}")


@login_required
@require_POST
def actualizar_estado_conversacion(request):
    """Actualiza manualmente el estado de compra de una conversación."""
    telefono = request.POST.get('telefono', '')
    estado   = request.POST.get('estado', '')
    notas    = request.POST.get('notas', '')
    if telefono and estado:
        ConversacionEstado.objects.update_or_create(
            telefono=telefono,
            defaults={'estado': estado, 'notas': notas},
        )
        messages.success(request, 'Estado actualizado.')
    from urllib.parse import urlencode as _ue
    return redirect(f"{reverse('detalle_conversacion')}?{_ue({'tel': telefono})}")


@login_required
def detalle_conversacion(request):
    """Hilo completo de mensajes con un contacto (telefono viene como ?tel=...)."""
    telefono = request.GET.get('tel', '')
    if not telefono:
        return redirect('listar_conversaciones')
    mensajes   = ConversacionWhatsapp.objects.filter(telefono=telefono).order_by('fecha')
    estado_obj = ConversacionEstado.objects.filter(telefono=telefono).first()
    estado_compra = estado_obj.estado if estado_obj else _autodetectar_estado(list(mensajes))
    return render(request, 'chatbot/detalle.html', {
        'telefono':      telefono,
        'mensajes':      mensajes,
        'estado_compra': estado_compra,
        'notas':         estado_obj.notas if estado_obj else '',
        'opciones_estado': ConversacionEstado.ESTADOS,
    })


#####################################
#  CHATBOT WEB (AJAX en el sitio)
#####################################


def chatbot_web(request):
    """Endpoint AJAX para el chat embebido en el sitio."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        mensaje = data.get('mensaje', '').strip()
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'error': 'Datos inválidos'}, status=400)

    if not mensaje:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)

    from tienda.chatbot.agente import responder, _parse_cart_link
    from tienda.chatbot.cotizacion import enviar_cotizacion

    historial        = request.session.get('chat_web_historial', [])
    items_acumulados = request.session.get('chat_items_acumulados', {})
    site_url         = request.build_absolute_uri('/').rstrip('/')

    respuesta_visible, cotizacion_params = responder('web', mensaje, historial, site_url, items_acumulados)

    # Actualizar items acumulados con lo que el bot incluyó en su link
    nuevos = _parse_cart_link(respuesta_visible)
    if nuevos:
        for pid, cant in nuevos.items():
            items_acumulados[pid] = cant          # el bot ya calculó el total correcto
        request.session['chat_items_acumulados'] = items_acumulados

    if cotizacion_params:
        nombre = cotizacion_params.get('nombre', '')
        email  = cotizacion_params.get('email', '')
        items  = cotizacion_params.get('items', '')
        ya_enviado = request.session.get('cotizacion_email_enviado') == email
        if nombre and email and items and not ya_enviado:
            print(f"[COTIZACION] Enviando a {email} | items={items}")
            ok = enviar_cotizacion(nombre, email, items)
            if ok:
                request.session['cotizacion_email_enviado'] = email
                respuesta_visible += f'\n\n✅ ¡Cotización enviada a {email}! Revisa también spam.'
            else:
                respuesta_visible += '\n\n⚠️ No pude enviar el correo. Escríbenos a extintoresrexfire@gmail.com'

    historial.append({'role': 'user',      'content': mensaje})
    historial.append({'role': 'assistant', 'content': respuesta_visible})
    request.session['chat_web_historial'] = historial[-20:]
    request.session.modified = True

    return JsonResponse({'respuesta': respuesta_visible})


#####################################
#  CARRITO RÁPIDO (desde link de WhatsApp)
#####################################

def agregar_rapido(request, producto_id):
    """Agrega 1 unidad al carrito desde un link."""
    producto = get_object_or_404(Producto, id_producto=producto_id)
    pid = str(producto_id)
    carrito = request.session.get('carrito', {})
    carrito[pid] = int(carrito.get(pid, 0)) + 1
    request.session['carrito'] = carrito
    request.session['carrito_origen'] = 'chatbot'
    request.session.modified = True
    messages.success(request, f'✅ {producto.nombre} agregado al carrito.')
    return redirect('ver_carrito')


def agregar_multiples(request):
    """Agrega múltiples productos desde un link con ?items=ID:CANT,ID:CANT"""
    items_str = request.GET.get('items', '')
    carrito = request.session.get('carrito', {})
    agregados = []
    for item in items_str.split(','):
        item = item.strip()
        if ':' not in item:
            continue
        pid, cant_str = item.split(':', 1)
        pid = pid.strip()
        try:
            cant = max(1, int(cant_str.strip()))
            p = Producto.objects.get(id_producto=int(pid))
            carrito[pid] = int(carrito.get(pid, 0)) + cant
            agregados.append(f'{cant}× {p.nombre}')
        except (Producto.DoesNotExist, ValueError):
            continue
    request.session['carrito'] = carrito
    request.session.modified = True
    if agregados:
        request.session['carrito_origen'] = 'chatbot'
        messages.success(request, '✅ Agregado al carrito: ' + ', '.join(agregados))
    return redirect('ver_carrito')


#####################################
#  CHATBOT WHATSAPP
#####################################

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
@require_POST
def webhook_whatsapp(request):
    """Recibe mensajes de WhatsApp vía Twilio y responde con IA."""
    from tienda.chatbot.agente import responder
    from tienda.chatbot.cotizacion import enviar_cotizacion

    telefono = request.POST.get('From', '').strip()
    mensaje  = request.POST.get('Body', '').strip()

    if not telefono or not mensaje:
        return HttpResponse('', content_type='text/xml')

    # URL pública del sitio (para links de carrito en el chat)
    site_url = request.build_absolute_uri('/').rstrip('/')

    # Historial reciente (últimos 10 mensajes = 5 turnos)
    historial_qs = (ConversacionWhatsapp.objects
                    .filter(telefono=telefono)
                    .order_by('-fecha')[:10])
    historial = [
        {'role': m.rol, 'content': m.contenido}
        for m in reversed(list(historial_qs))
    ]

    # Guardar mensaje del usuario
    ConversacionWhatsapp.objects.create(telefono=telefono, rol='user', contenido=mensaje)

    # Obtener respuesta de la IA (ahora devuelve tupla)
    respuesta_visible, cotizacion_params = responder(telefono, mensaje, historial, site_url)

    # Enviar cotización por email si el bot recopiló los datos
    if cotizacion_params:
        nombre = cotizacion_params.get('nombre', '')
        email  = cotizacion_params.get('email', '')
        items  = cotizacion_params.get('items', '')
        if nombre and email and items:
            ok = enviar_cotizacion(nombre, email, items)
            if ok:
                respuesta_visible += f"\n\n✅ ¡Listo! Te envié la cotización a {email}. Revisa también tu carpeta de spam."
            else:
                respuesta_visible += "\n\n⚠️ Tuve un problema enviando el correo. Escríbenos a extintoresrexfire@gmail.com"

    # Guardar respuesta del bot
    ConversacionWhatsapp.objects.create(telefono=telefono, rol='assistant', contenido=respuesta_visible)

    # Responder a Twilio en formato TwiML
    from twilio.twiml.messaging_response import MessagingResponse
    twiml = MessagingResponse()
    twiml.message(respuesta_visible[:1600])
    return HttpResponse(str(twiml).encode('utf-8'), content_type='text/xml; charset=utf-8')
