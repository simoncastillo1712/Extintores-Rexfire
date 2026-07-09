from django import template

register = template.Library()


@register.filter
def clp(value):
    """Formatea un número como peso chileno: 1.234.567"""
    try:
        n = int(value)
        return f'{n:,}'.replace(',', '.')
    except (ValueError, TypeError):
        return value


@register.filter
def despacho_neto(neto):
    """Retorna el costo neto de despacho según el monto neto de la venta."""
    try:
        n = int(neto)
        if n >= 300000:
            return 0
        elif n >= 50000:
            return 6800
        else:
            return None  # Sin despacho
    except (ValueError, TypeError):
        return None
