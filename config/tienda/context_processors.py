def carrito_count(request):
    try:
        carrito = request.session.get('carrito', {})
        total = sum(int(q) for q in carrito.values() if q is not None)
    except Exception:
        total = 0
    return {'carrito_total_items_global': total}
