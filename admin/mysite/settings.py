import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SECURITY
# ==============================
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["*"]

# ==============================
# APPLICATIONS
# ==============================
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "converter",
]

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# ==============================
# DATABASE (SUPABASE)
# ==============================
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=0,
        ssl_require=True
    )
}

# ==============================
# PASSWORD VALIDATION
# ==============================
AUTH_PASSWORD_VALIDATORS = []

# ==============================
# INTERNATIONALIZATION
# ==============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==============================
# STATIC FILES
# ==============================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================
# HTTPS FIX FOR RENDER
# ==============================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = ["https://accountingexpert.onrender.com"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ==============================
# JAZZMIN SETTINGS
# ==============================
JAZZMIN_SETTINGS = {
    "site_title": "Accounting Expert Admin",
    "site_header": "Accounting Expert",
    "site_brand": "Accounting Expert",
    "welcome_sign": "Welcome to Admin",
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-primary",
}
