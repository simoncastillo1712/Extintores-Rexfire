import os
from pathlib import Path
from dotenv import load_dotenv

# .env está en la raíz del proyecto (mismo nivel que manage.py)
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Seguridad ───────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-96m@+e%4r+kqa^c1x2a$97-zfd5t0!-z574gu10ec@sxo%lt1%'
)

DEBUG = os.getenv('DEBUG', 'True') == 'True'

_extra_hosts = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.trycloudflare.com',
    '.railway.app',
    'extintoresrexfire.cl',
    'www.extintoresrexfire.cl',
] + _extra_hosts

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://extintoresrexfire.cl',
    'https://www.extintoresrexfire.cl',
    'https://*.trycloudflare.com',
]

# ─── Aplicaciones ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rexfire.urls'
WSGI_APPLICATION = 'rexfire.wsgi.application'

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tienda.context_processors.carrito_count',
            ],
        },
    },
]

# ─── Base de datos ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.getenv('DB_NAME',     'extintores'),
        'USER':     os.getenv('DB_USER',     'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', '1234'),
        'HOST':     os.getenv('DB_HOST',     'localhost'),
        'PORT':     os.getenv('DB_PORT',     '3306'),
        'OPTIONS':  {'charset': 'utf8mb4'},
    }
}

# ─── Validación de contraseñas ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login_view'

# ─── Internacionalización ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-cl'
TIME_ZONE     = 'America/Santiago'
USE_I18N      = True
USE_TZ        = True

# ─── Archivos estáticos y media ───────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Servicios externos (desde .env) ──────────────────────────────────────────
DEEPSEEK_API_KEY  = os.getenv('DEEPSEEK_API_KEY',  '')
DEEPSEEK_MODEL    = os.getenv('DEEPSEEK_MODEL',    'deepseek-chat')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

TWILIO_ACCOUNT_SID   = os.getenv('TWILIO_ACCOUNT_SID',   '')
TWILIO_AUTH_TOKEN    = os.getenv('TWILIO_AUTH_TOKEN',     '')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM',  '')

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER',     '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = f"Extintores REXFIRE <{os.getenv('EMAIL_HOST_USER', 'extintoresrexfire@gmail.com')}>"
