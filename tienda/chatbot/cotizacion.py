"""
Genera y envía cotizaciones por correo electrónico.
"""
from django.core.mail import EmailMessage
from django.conf import settings


def enviar_cotizacion(nombre: str, email: str, items_str: str) -> bool:
    """
    Envía cotización HTML al cliente.
    items_str: "ID_PROD:CANTIDAD,ID_PROD:CANTIDAD"  (IDs numéricos)
    """
    try:
        from tienda.models import Producto

        items = []
        neto = 0
        for item in items_str.split(','):
            item = item.strip()
            if ':' not in item:
                continue
            prod_ref, cant_str = item.rsplit(':', 1)
            prod_ref = prod_ref.strip()
            try:
                cant = max(1, int(cant_str.strip()))
            except ValueError:
                cant = 1

            # Buscar por ID numérico o por nombre parcial
            try:
                prod_id = int(prod_ref)
                p = Producto.objects.get(id_producto=prod_id)
            except (ValueError, Producto.DoesNotExist):
                try:
                    p = Producto.objects.filter(nombre__icontains=prod_ref).first()
                    if not p:
                        continue
                except Exception:
                    continue

            sub = p.precio * cant
            neto += sub
            items.append({'nombre': p.nombre, 'precio': p.precio, 'cant': cant, 'sub': sub})

        if not items:
            return False

        iva = round(neto * 0.19)
        total = neto + iva

        # Despacho
        if neto >= 300_000:
            despacho_txt = "Despacho GRATIS (compra sobre $300.000 neto)"
            despacho_val = 0
        elif neto >= 50_000:
            despacho_txt = "Despacho $6.800 + IVA = $8.092"
            despacho_val = 8092
        else:
            despacho_txt = "Retiro en sucursal (Santa Gemita 909 L.202B, Maipú)"
            despacho_val = 0

        total_final = total + despacho_val

        # Filas de productos en HTML
        filas = ""
        for it in items:
            filas += f"""
            <tr>
                <td style="padding:8px;border-bottom:1px solid #eee;">{it['nombre']}</td>
                <td style="padding:8px;border-bottom:1px solid #eee;text-align:center;">{it['cant']}</td>
                <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">${it['precio']:,}</td>
                <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">${it['sub']:,}</td>
            </tr>"""

        html = f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:20px;">
  <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">

    <!-- Header -->
    <div style="background:#CC0000;padding:24px 32px;">
      <h1 style="color:#fff;margin:0;font-size:22px;">🔥 Extintores REXFIRE</h1>
      <p style="color:#ffcccc;margin:4px 0 0;">Cotización Oficial</p>
    </div>

    <!-- Saludo -->
    <div style="padding:24px 32px 8px;">
      <p style="font-size:15px;">Estimado/a <strong>{nombre}</strong>,</p>
      <p style="color:#555;font-size:14px;">
        Adjuntamos su cotización según lo solicitado. Todos nuestros extintores
        están <strong>certificados CESMEC</strong> y cumplen con la normativa chilena vigente.
      </p>
    </div>

    <!-- Tabla de productos -->
    <div style="padding:8px 32px 16px;">
      <table style="width:100%;border-collapse:collapse;font-size:14px;">
        <thead>
          <tr style="background:#f0f0f0;">
            <th style="padding:10px 8px;text-align:left;">Producto</th>
            <th style="padding:10px 8px;text-align:center;">Cant.</th>
            <th style="padding:10px 8px;text-align:right;">Precio unit.</th>
            <th style="padding:10px 8px;text-align:right;">Subtotal</th>
          </tr>
        </thead>
        <tbody>{filas}</tbody>
      </table>
    </div>

    <!-- Totales -->
    <div style="padding:8px 32px 24px;">
      <table style="width:100%;font-size:14px;margin-left:auto;max-width:300px;">
        <tr>
          <td style="padding:4px 8px;color:#555;">Subtotal neto:</td>
          <td style="padding:4px 8px;text-align:right;">${neto:,}</td>
        </tr>
        <tr>
          <td style="padding:4px 8px;color:#555;">IVA (19%):</td>
          <td style="padding:4px 8px;text-align:right;">${iva:,}</td>
        </tr>
        <tr style="background:#fff0f0;">
          <td style="padding:8px;font-weight:bold;color:#CC0000;">TOTAL:</td>
          <td style="padding:8px;text-align:right;font-weight:bold;color:#CC0000;">${total:,}</td>
        </tr>
        <tr>
          <td colspan="2" style="padding:6px 8px;font-size:12px;color:#777;">{despacho_txt}</td>
        </tr>
        {"" if despacho_val == 0 else f'<tr style="background:#fff8f0;"><td style="padding:8px;font-weight:bold;">TOTAL CON DESPACHO:</td><td style="padding:8px;text-align:right;font-weight:bold;">${total_final:,}</td></tr>'}
      </table>
    </div>

    <!-- Regalos -->
    <div style="padding:12px 32px;background:#fff8f0;border-left:4px solid #FF6600;margin:0 32px 20px;">
      <p style="margin:0;font-size:13px;color:#CC4400;">
        <strong>🎁 Incluido en compras de extintores nuevos:</strong><br>
        ✅ Instalación GRATIS &nbsp;|&nbsp; ✅ Capacitación al equipo GRATIS
      </p>
    </div>

    <!-- Pago -->
    <div style="padding:8px 32px 20px;">
      <p style="font-size:13px;color:#555;margin:0 0 6px;"><strong>Formas de pago:</strong></p>
      <p style="font-size:13px;color:#555;margin:0;">
        Efectivo o transferencia sin recargo.<br>
        Tarjeta / Redcompra: +1,5%.<br>
        RUT: 77.995.139-1 | Cta. Vista Mercado Pago N° 1046537846
      </p>
    </div>

    <!-- Footer -->
    <div style="background:#222;padding:16px 32px;text-align:center;">
      <p style="color:#aaa;font-size:12px;margin:0;">
        Cotización válida por <strong style="color:#fff;">3 días hábiles</strong><br>
        Santa Gemita 909 L.202B, Maipú &nbsp;|&nbsp; +569 7555 5423 / +569 4344 7066<br>
        extintoresrexfire@gmail.com
      </p>
    </div>

  </div>
</body>
</html>"""

        msg = EmailMessage(
            subject="Cotización Extintores REXFIRE",
            body=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        msg.content_subtype = "html"
        msg.send()
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False
