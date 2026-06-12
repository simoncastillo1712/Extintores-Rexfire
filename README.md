# 🔥 Extintores REXFIRE — Sistema de Gestión de Ventas + Chatbot IA

Sistema web completo para la gestión comercial de **Extintores REXFIRE**, empresa chilena certificada CESMEC dedicada a la venta, recarga, recambio e instalación de extintores de incendio.

Incluye tienda pública con carrito de compras, panel de administración, y **REXI**: un asistente de ventas con inteligencia artificial que opera vía chat en el sitio web y WhatsApp, con catálogo en tiempo real, generación de cotizaciones por email y seguimiento de conversaciones.

---

## ✨ Funcionalidades principales

### 🤖 REXI — Asistente de Ventas con IA (chatbot)

- **Chat flotante** en todas las páginas del sitio (esquina inferior derecha)
- Venta guiada: recomienda el extintor exacto según uso, ambiente y normativa
- **Catálogo en vivo** integrado con la base de datos — precios y stock siempre actualizados
- Botón **"Agregar al carrito"** directamente en la respuesta del chatbot (1 o N productos a la vez)
- **Acumulación de pedido**: recuerda todos los productos discutidos en la conversación
- **Cotizaciones por email**: genera y envía una cotización detallada (HTML) al correo del cliente cuando lo solicita
- Respuestas con tablas comparativas de productos renderizadas correctamente en el chat
- Canal **WhatsApp** (Twilio Sandbox) para clientes que prefieren ese canal
- Apertura automática a los 15 segundos con mensaje de bienvenida
- Historial de sesión por usuario (no mezcla conversaciones entre clientes)

### 🛒 Tienda pública (sin login)

- Catálogo de extintores con modal de detalle: especificaciones técnicas y recomendaciones
- Página de **Recargas y Servicios** (`/servicios/`) con información de normativa chilena anual
- Búsqueda de productos por nombre o categoría
- Carrito persistente en sesión, visible en todas las páginas
- Precios en peso chileno (`$1.234.567`)

### 👤 Autenticación de clientes

- Identificación por **RUT** (sin contraseña)
- Registro de nuevos clientes con datos completos
- Menú desplegable con: **Mis datos**, **Mis compras**, **Cerrar sesión**
- Edición de perfil (nombre, dirección, teléfono, email — RUT bloqueado)
- Historial de compras con link a boleta imprimible

### 💳 Flujo de compra

- Checkout con detalle del pedido, datos del cliente y formas de pago
- **Modal automático** al llegar al checkout cuando hay extintores nuevos:
  - Sugiere gancho y señalética (1 por extintor nuevo)
  - Modal regalo: instalación y capacitación sin costo incluidas en boleta
- Badge **GRATIS** en ítems sin costo
- Despacho calculado automáticamente según monto neto
- Boleta descargable en PDF (impresión del navegador)
- Campo **origen** en ventas: distingue si la compra provino del chatbot o la web directa

### 🖥️ Panel de administración

#### Inventario
- CRUD completo de **Productos** con subida de imagen
- CRUD de **Categorías** y **Proveedores**
- Control de stock (oculto al público)

#### Gestión Comercial
- CRUD de **Clientes** con validación de RUT
- CRUD de **Vendedores** con comisión automática del 20% sobre neto
- **Nueva Venta** con precio editable por línea, selector de vendedor y alerta de despacho
- Listado de ventas con detalle, boleta y asignación de vendedor post-venta
- Reporte de comisiones por vendedor

#### Chatbot — Panel de control
- **Conversaciones**: historial completo de chats por cliente (web y WhatsApp)
  - Estado manual: En consulta / Interesado / Cotización enviada / Concretada / **Abandonada**
  - **Auto-abandono**: si el cliente estuvo interesado y no regresó en 3 días, cambia automáticamente
  - **Botón "Recordar"**: envía mensaje de WhatsApp al cliente con carrito abandonado
  - Notas internas por conversación
- **Ventas por REXI**: reporte de ventas originadas desde el chatbot
  - Total facturado, subtotal neto, IVA
  - **Ahorro en comisiones**: muestra el 20% del neto que se habría pagado a un vendedor humano

---

## 🛠 Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Django 6.0.3 (Python 3.14) |
| Base de datos | MySQL 8.0 + mysqlclient 2.2.8 |
| IA / Chatbot | DeepSeek API (deepseek-chat, compatible OpenAI) |
| WhatsApp | Twilio WhatsApp Sandbox |
| Email | Gmail SMTP (App Password) |
| Exposición local | Cloudflare Tunnel (`cloudflared`) |
| Frontend | Bootstrap 5.3.2 + Bootstrap Icons 1.10.5 |
| Imágenes | Pillow 12.2.0 |
| Variables de entorno | python-dotenv |
| Autenticación admin | Django Auth |
| Autenticación cliente | Sesión Django (RUT) |
| Filtros personalizados | `\|clp` (peso chileno), `\|despacho_neto` |

---

## ⚙️ Requisitos previos

- Python 3.10+
- MySQL 8.0+
- pip
- Cuenta [DeepSeek](https://platform.deepseek.com) (chatbot IA)
- Cuenta [Twilio](https://console.twilio.com) (WhatsApp, opcional)
- Cuenta Gmail con Contraseña de Aplicación (cotizaciones, opcional)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/simoncastillo1712/Extintores-Rexfire.git
cd Extintores-Rexfire
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

### 5. Configurar la base de datos

Crear la base de datos en MySQL:

```sql
CREATE DATABASE extintores CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Editar `config/config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'extintores',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 6. Aplicar migraciones

```bash
python config/manage.py migrate
```

### 7. Crear superusuario administrador

```bash
python config/manage.py createsuperuser
```

### 8. Cargar catálogo de productos y servicios

```bash
python config/manage.py cargar_productos_rexfire
python config/manage.py cargar_servicios_rexfire
```

### 9. Iniciar el servidor

```bash
python config/manage.py runserver
```

Acceder en: **http://127.0.0.1:8000**  
Login admin: **http://127.0.0.1:8000/login_view**

---

## 🌐 Webhook WhatsApp (Twilio + Cloudflare Tunnel)

Para habilitar el chatbot por WhatsApp en desarrollo local:

```bash
# Terminal 1: servidor Django
python config/manage.py runserver

# Terminal 2: túnel público
cloudflared tunnel --url http://localhost:8000
```

Copiar la URL generada (ej: `https://xxxx.trycloudflare.com`) y configurarla en la consola de Twilio:
- **Webhook URL**: `https://xxxx.trycloudflare.com/whatsapp/webhook/`
- **Método**: POST

Para unirse al sandbox de WhatsApp: enviar `join iron-balance` a **+1 415 523 8886**

---

## 📁 Estructura del proyecto

```
tienda/
├── .env.example               # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
├── README.md
└── config/
    ├── manage.py
    ├── config/                        # Configuración Django
    │   ├── settings.py               # DB, email, API keys desde .env
    │   ├── urls.py
    │   └── wsgi.py
    ├── media/                         # Imágenes de productos (subidas)
    └── tienda/                        # App principal
        ├── models.py                  # Producto, Venta, Vendedor, Cliente,
        │                              #   ConversacionWhatsapp, ConversacionEstado
        ├── views.py                   # Todas las vistas (tienda, admin, chatbot)
        ├── urls.py                    # Rutas URL
        ├── forms.py
        ├── context_processors.py      # Contador de carrito global
        ├── chatbot/
        │   ├── agente.py             # Lógica IA: catálogo en vivo, prompt, acumulación
        │   └── cotizacion.py         # Generación y envío de cotizaciones por email
        ├── management/
        │   └── commands/
        │       ├── cargar_productos_rexfire.py
        │       └── cargar_servicios_rexfire.py
        ├── migrations/
        ├── templatetags/
        │   └── rexfire_filters.py    # |clp (peso chileno), |despacho_neto
        ├── static/
        │   ├── css/style.css         # Estilos + chat widget flotante
        │   └── js/script.js          # Chat REXI: formatMessage, tablas, botones carrito
        └── templates/
            ├── base.html             # Navbar, widget REXI flotante, footer
            ├── inicio.html
            ├── auth/
            ├── carrito/              # ver.html, checkout.html
            ├── chatbot/
            │   ├── lista.html        # Lista de conversaciones con estado
            │   ├── detalle.html      # Hilo de chat + panel de estado/notas
            │   └── ventas_chatbot.html  # Reporte ventas + ahorro comisiones
            ├── clientes/
            ├── productos/
            ├── proveedores/
            ├── servicios/
            ├── ventas/               # nueva, cotizacion, listado, detalle
            └── vendedores/           # listado, form, comisiones
```

---

## 💰 Reglas de negocio

| Concepto | Valor |
|---|---|
| IVA | 19% |
| Despacho Santiago — sobre $300.000 neto | **Gratis** |
| Despacho Santiago — $50.000 a $300.000 neto | $6.800 + IVA |
| Mínimo para despacho | $50.000 neto |
| Comisión vendedor humano | 20% del neto |
| Comisión REXI (chatbot) | **$0** |
| Ahorro estimado con REXI | 20% del neto (lo que habría cobrado un vendedor) |
| Regalo por compra de extintores nuevos | Instalación + Capacitación sin costo |
| Accesorios sugeridos por extintor nuevo | 1 Gancho ($2.000) + 1 Señalética ($1.200) |
| Auto-abandono de conversación | 3 días sin actividad en estado "Interesado" |

---

## 🧪 Comandos útiles

```bash
# Iniciar servidor
python config/manage.py runserver

# Verificar configuración
python config/manage.py check

# Ver migraciones aplicadas
python config/manage.py showmigrations tienda

# Cargar catálogo
python config/manage.py cargar_productos_rexfire
python config/manage.py cargar_servicios_rexfire

# Crear superusuario
python config/manage.py createsuperuser
```

---

## 🔐 Seguridad para producción

```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['tu-dominio.cl']
```

Nunca subas el archivo `.env` al repositorio. Usa el archivo `.env.example` como referencia.

---

## 📞 Información de la empresa

**Extintores REXFIRE**  
Santa Gemita 909 L.202B, Maipú  
+569 7555 5423  
extintoresrexfire@gmail.com  
RUT: 77.995.139-1  
Certificado CESMEC

---

## 📄 Licencia

Proyecto de uso privado — © Extintores REXFIRE. Todos los derechos reservados.
