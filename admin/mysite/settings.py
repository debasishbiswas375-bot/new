import os
from pathlib import Path
import dj_database_url

# =========================
# 1. CORE PATHS & SECURITY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-accounting-expert-final-2026'
)
DATABASE_URL = os.environ.get('DATABASE_URL')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://accountingexpert.onrender.com',
    'https://newtool.streamlit.app'
]

# =========================
# 2. APPLICATION DEFINITION
# =========================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Ensure this points to the Config class to load signals
    'converter.apps.ConverterConfig', 
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

ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# =========================
# 4. DATABASE CONFIG (SUPABASE)
# =========================
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            # CRITICAL: Prevents 502 Bad Gateway timeouts on Render/Supabase
            conn_health_checks=True, 
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =========================
# 5. STATIC FILES (RENDER)
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# 6. RENDER SECURITY SETTINGS
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "yourgmail@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"

# Jazzmin settings to stabilize Admin interface
JAZZMIN_SETTINGS = {
    "site_title": "Accounting Expert",
    "site_header": "Accounting Expert",
    "welcome_sign": "Welcome to Accounting Expert",
    "user_avatar": None,
}

# =========================
# 7. SELF-HEALING: AUTO-FIX MISSING PROFILES
# =========================
# This block runs on server startup to ensure existing users have profiles
import django
django.setup()
from django.contrib.auth.models import User
try:
    from converter.models import UserProfile
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)
except Exception:
    pass # Prevent build failure if migrations aren't finished
