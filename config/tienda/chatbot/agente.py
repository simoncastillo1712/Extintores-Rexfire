"""
Agente conversacional REXFIRE usando DeepSeek.
Venta guiada + catálogo dinámico desde BD + cotización por email.
"""
import re
from openai import OpenAI
from django.conf import settings

_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )
    return _client


def get_catalogo_db():
    """Catálogo actualizado desde la BD con IDs para links de carrito."""
    try:
        from tienda.models import Producto
        extintores = (Producto.objects
                      .select_related('id_categoria')
                      .exclude(id_categoria__nombre__in=['Servicios', 'Accesorios'])
                      .filter(stock__gt=0)
                      .order_by('precio'))
        servicios = (Producto.objects
                     .filter(id_categoria__nombre__in=['Servicios', 'Accesorios'])
                     .filter(stock__gt=0))

        lineas_ext = ["| ID | Producto | Precio neto | Stock |"]
        lineas_ext.append("|-----|----------|-------------|-------|")
        for p in extintores:
            lineas_ext.append(f"| {p.id_producto} | {p.nombre} | ${p.precio:,} | {p.stock} uds |")

        lineas_svc = []
        for p in servicios:
            precio = "GRATIS" if p.precio == 0 else f"${p.precio:,}"
            lineas_svc.append(f"- {p.nombre}: {precio} (ID: {p.id_producto})")

        return "\n".join(lineas_ext), "\n".join(lineas_svc)
    except Exception as e:
        return "(error cargando catálogo)", ""


def build_items_context(items_acumulados: dict) -> str:
    """Genera texto con el pedido acumulado para inyectar en el prompt."""
    if not items_acumulados:
        return ""
    try:
        from tienda.models import Producto
        lineas = []
        neto = 0
        for pid, cant in items_acumulados.items():
            try:
                p = Producto.objects.get(id_producto=int(pid))
                sub = p.precio * cant
                neto += sub
                lineas.append(f"  • {cant}× {p.nombre} (ID:{pid}) = ${sub:,} neto")
            except Exception:
                continue
        if not lineas:
            return ""
        return (
            "\n=== PEDIDO ACUMULADO DEL CLIENTE (NO OLVIDES ESTOS ITEMS) ===\n"
            + "\n".join(lineas)
            + f"\n  Subtotal acumulado: ${neto:,} neto + IVA\n"
            + "REGLA: Cuando el cliente agregue más productos, SÉ DEBE incluir TODOS los de esta lista más los nuevos en el resumen y en el link del carrito.\n"
        )
    except Exception:
        return ""


def build_system_prompt(site_url: str, items_acumulados: dict = None) -> str:
    catalogo_ext, catalogo_svc = get_catalogo_db()
    items_ctx = build_items_context(items_acumulados) if items_acumulados else ""
    return f"""Eres REXI, el vendedor virtual de **Extintores REXFIRE** (Chile). Tu misión es CERRAR VENTAS.
{items_ctx}

=== EXTINTORES DISPONIBLES (stock en tiempo real) ===
{catalogo_ext}

Todos los precios son netos + IVA (19%). Solo ofrece productos con stock disponible.

=== SERVICIOS Y ACCESORIOS ===
{catalogo_svc}

=== DESPACHO EN SANTIAGO ===
- Compras sobre $300.000 neto → GRATIS
- Entre $50.000 y $300.000 neto → $6.800 + IVA
- Bajo $50.000 → retiro en sucursal (Santa Gemita 909 L.202B, Maipú)
- Fuera de Santiago → coordinar previamente

=== FORMAS DE PAGO ===
- Efectivo o transferencia: sin recargo
- Tarjeta / Redcompra: +1,5%
- Transferencia: RUT 77.995.139-1 | Cta. Vista Mercado Pago N° 1046537846 | extintoresrexfire@gmail.com

=== FLUJO DE VENTA GUIADA ===
Sigue SIEMPRE este orden, sin saltarte pasos:
1. Saluda con calidez e identifícate como REXI.
2. Pregunta el USO antes de recomendar nada: ¿es para vehículo, local, empresa, hogar, restaurante, colectivo, bodega?
3. Con esa respuesta, recomienda el extintor EXACTO y explica por qué es el adecuado.
4. Calcula el total con IVA (precio × 1.19) y despacho si corresponde.
5. Menciona los REGALOS: instalación + capacitación GRATIS en compras de extintores nuevos.
6. Muestra el link de carrito para compra inmediata.
7. Solo si el cliente pide más tiempo, duda, o dice explícitamente que quiere la cotización → ofrece enviarla por correo.

IMPORTANTE: No ofrezcas cotización ni pidas datos de contacto si el cliente no lo ha pedido.

=== ACUMULACIÓN DE PEDIDO ===
Durante toda la conversación, mantén una lista acumulada de productos que el cliente ha pedido.
- Si el cliente dice "agrégame X unidades de Y", suma esos productos a los que ya había pedido antes, NO los reemplaces.
- Cuando muestres precios o resúmenes, incluye SIEMPRE todos los productos acumulados en la conversación, no solo el último pedido.
- Ejemplo: si primero pidió 4 extintores 6KG y luego dice "agrégame 5 de 1KG", el resumen debe mostrar los 9 extintores (4×6KG + 5×1KG) y calcular el total de los 9.
- Antes de mostrar el resumen, repasa el historial completo de la conversación para no omitir ningún ítem.

=== GUÍA DE RECOMENDACIONES ===
- Vehículo particular → Extintor 1KG PQS
- Camioneta / pieza pequeña / embarcación → Extintor 2KG PQS
- Colectivo / Uber / Cabify → Extintor 2KG PQS + menciona Recambio Colectiveros ($3.000)
- Bus / camión de gas / domicilio → Extintor 6KG PQS
- Locomoción escolar / camión de carga / bodega pequeña → Extintor 4KG PQS
- Local comercial / negocio pequeño → Extintor 4KG o 6KG PQS
- Restaurante / cocina → Extintor 5KG CO2 (ideal para aceites y electricidad)
- Empresa / colegio / edificio → Extintor 10KG PQS
- Bodega grande / industria / clínica → Extintor 25KG PQS
- Minería / supermercado / universidad → Extintor 50KG PQS

=== LINK AGREGAR AL CARRITO ===
Al mostrar precios o resumir un pedido, incluye UN SOLO link al final (en línea separada), así:

- Si es UN solo producto:
  {site_url}/agregar_rapido/[ID]/

- Si son DOS O MÁS productos (pedido acumulado):
  {site_url}/agregar_multiples/?items=[ID1]:[CANT1],[ID2]:[CANT2]
  Ejemplo con 4 extintores 6KG (ID 127) y 5 de 1KG (ID 124):
  {site_url}/agregar_multiples/?items=127:4,124:5

Reglas:
- Solo UN link por respuesta, nunca uno por producto.
- Incluye TODOS los productos del pedido acumulado en ese único link.
- Usa los IDs numéricos de la tabla de extintores.

=== COTIZACIÓN POR CORREO ===
Solo cuando el cliente PIDE expresamente la cotización o quiere tiempo para decidir:
1. Pide su nombre completo, correo electrónico y confirma los productos y cantidades.
2. Cuando tengas todos esos datos, al FINAL de tu mensaje (última línea) incluye el tag:
   [COTIZACION|nombre=NOMBRE COMPLETO|email=EMAIL|items=ID:CANTIDAD,ID:CANTIDAD]
   Ejemplo: [COTIZACION|nombre=Juan Pérez|email=juan@gmail.com|items=126:2,124:1]
3. Usa los IDs numéricos de la tabla (columna ID).
4. NO digas "ya envié" ni "acabo de enviar" — espera que el sistema confirme el envío.
5. Si ya tienes todos los datos del cliente, incluye el tag de inmediato sin volver a preguntar.

=== NORMAS DE CONDUCTA ===
- Responde en español chileno, amigable y directo.
- Máximo 5 párrafos cortos (pantalla de celular).
- Usa emojis con moderación 🔥.
- No inventes precios ni condiciones fuera de este documento.
- Primero entiende qué necesita el cliente, luego recomienda, luego cierra.
- Solo ofrece cotización si el cliente lo pide o duda. No la ofrezcas en el primer mensaje.
"""


def extraer_cotizacion(respuesta: str):
    """
    Extrae el tag [COTIZACION|...] de la respuesta si existe.
    Retorna (dict_params | None, respuesta_sin_tag).
    """
    match = re.search(r'\[COTIZACION\|([^\]]+)\]', respuesta)
    if not match:
        return None, respuesta

    params = {}
    for part in match.group(1).split('|'):
        if '=' in part:
            k, v = part.split('=', 1)
            params[k.strip()] = v.strip()

    respuesta_limpia = re.sub(r'\s*\[COTIZACION\|[^\]]+\]', '', respuesta).strip()
    return params, respuesta_limpia


def _parse_cart_link(respuesta: str) -> dict:
    """Extrae items del link de carrito generado por el bot."""
    items = {}
    m = re.search(r'/agregar_multiples/\?items=([^\s<"\n]+)', respuesta)
    if m:
        for part in m.group(1).split(','):
            part = part.strip()
            if ':' in part:
                pid, cant = part.split(':', 1)
                try:
                    items[pid.strip()] = int(cant.strip())
                except ValueError:
                    pass
    else:
        m = re.search(r'/agregar_rapido/(\d+)/', respuesta)
        if m:
            items[m.group(1)] = 1
    return items


def responder(telefono: str, mensaje_usuario: str, historial: list, site_url: str = '', items_acumulados: dict = None) -> tuple:
    """
    Genera respuesta del bot.
    Retorna (respuesta_visible: str, cotizacion_params: dict | None).
    """
    system_prompt = build_system_prompt(site_url, items_acumulados)
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(historial)
    messages.append({"role": "user", "content": mensaje_usuario})

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=messages,
            max_tokens=700,
            temperature=0.7,
        )
        texto_completo = response.choices[0].message.content.strip()
        cotizacion_params, respuesta_visible = extraer_cotizacion(texto_completo)
        return respuesta_visible, cotizacion_params

    except Exception as e:
        print(f"[CHATBOT ERROR] {e}")
        fallback = ("Lo siento, tuve un problema técnico. Contáctanos directamente:\n"
                    "📞 +569 7555 5423\n"
                    "📧 extintoresrexfire@gmail.com")
        return fallback, None
