import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# 🔐 SECURITY
# =========================================================
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["accountingexpert.onrender.com"]


# =========================================================
# 🗄 DATABASE (SUPABASE / POSTGRES)
# =========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "CONN_MAX_AGE": 0,
    }
}


# =========================================================
# 📦 INSTALLED APPS
# =========================================================
INSTALLED_APPS = [

    # Jazzmin MUST stay first
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "converter",
]


# =========================================================
# 🧩 MIDDLEWARE (ORDER VERY IMPORTANT)
# =========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # MUST be right after SecurityMiddleware
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


# =========================================================
# 🔐 PASSWORD VALIDATION
# =========================================================
AUTH_PASSWORD_VALIDATORS = []


# =========================================================
# 🌍 INTERNATIONALIZATION
# =========================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# =========================================================
# 📂 STATIC FILES (FIX FOR JAZZMIN DROPDOWN)
# =========================================================
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = []

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# 🔐 RENDER HTTPS FIX
# =========================================================
CSRF_TRUSTED_ORIGINS = [
    "https://accountingexpert.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# =========================================================
# 🎨 JAZZMIN CLEAN SETTINGS
# =========================================================
JAZZMIN_SETTINGS = {
    "site_title": "Accounting Expert Admin",
    "site_header": "Accounting Expert",
    "site_brand": "Accounting Expert",
    "welcome_sign": "Welcome to Accounting Expert Dashboard",
    "copyright": "Accounting Expert Pvt Ltd",

    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,
    "usermenu_links": [
    {"name": "Logout", "url": "admin:logout"},
],

    # Show text beside user icon
    "navbar_small_text": False,

    # DO NOT ADD topmenu_links (it breaks logout dropdown)

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "converter.Plan": "fas fa-box",
        "converter.UserProfile": "fas fa-id-card",
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-primary",
    "theme": "cosmo",
    "dark_mode_theme": None,
}
