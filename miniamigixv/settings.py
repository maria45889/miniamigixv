from pathlib import Path
import os
from dotenv import load_dotenv

# 🔐 Cargar variables .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ==============================
# 🌐 HOSTS (Permitir Local y Ngrok)
# ==============================
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '127.0.0.2',
    '.ngrok-free.dev',
    '.ngrok.io',
]

# ==============================
# 🔐 CSRF (Seguridad para formularios)
# ==============================
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.2:8000',
    'https://*.ngrok-free.dev',
    'https://*.ngrok.io',
]

# ==============================
# 🔒 SEGURIDAD
# ==============================
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==============================
# 📦 APPS
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'chat',
    # 🔐 Allauth (Google OAuth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# ==============================
# 🧠 MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'miniamigixv.urls'

# ==============================
# 🖥️ TEMPLATES
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'miniamigixv.wsgi.application'

# ==============================
# 🗄️ BASE DE DATOS
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================
# 🔐 VALIDADORES
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# 🌎 INTERNACIONALIZACIÓN
# ==============================
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# ==============================
# 📁 ARCHIVOS ESTÁTICOS
# ==============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'chat' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================
# 📂 MEDIA
# ==============================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================
# 👤 USUARIO PERSONALIZADO
# ==============================
AUTH_USER_MODEL = 'chat.Usuario'

# ==============================
# 🔑 LOGIN
# ==============================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================
# 🌐 DJANGO-ALLAUTH (Google OAuth)
# ==============================
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuración de allauth
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
# ACCOUNT_ADAPTER = 'chat.adapter.MyAccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'chat.adapter.MySocialAccountAdapter'
ACCOUNT_LOGIN_URL = '/login/'
ACCOUNT_SIGNUP_URL = '/registro/'
ACCOUNT_LOGOUT_URL = '/logout/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Configuración del proveedor Google
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
        }
    }
}

# Redirigir después de login social
SOCIALACCOUNT_LOGIN_ON_GET = True
