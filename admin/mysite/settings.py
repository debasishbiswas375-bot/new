import os
from pathlib import Path
import dj_database_url

# =========================
# 1. CORE PATHS & SECURITY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-accounting-expert-final-2026"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "accountingexpert.onrender.com",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://accountingexpert.onrender.com",
    "https://newtool.streamlit.app",
]

# =========================
# 2. APPLICATION DEFINITION
# =========================
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "converter.apps.ConverterConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"

# =========================
# 3. TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # optional root templates
        "APP_DIRS": True,  # IMPORTANT for converter/templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================
# 4. DATABASE CONFIG (Render / Supabase)
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=0,
        ssl_require=True,
    )
}

# =========================
# 5. STATIC FILES (Render)
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# 6. LOGIN / LOGOUT SETTINGS
# =========================
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# =========================
# 7. DEFAULT FIELD
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# 8. PRODUCTION SECURITY
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# =========================
# 9. EMAIL CONFIG
# =========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# =========================
# 10. JAZZMIN ADMIN UI
# =========================
JAZZMIN_SETTINGS = {
    "site_title": "Accounting Expert",
    "site_header": "Accounting Expert",
    "welcome_sign": "Welcome to Accounting Expert",
    "user_avatar": None,
    "topmenu_links": [
    {"name": "Logout", "url": "/admin/logout/", "new_window": False},
],
}
