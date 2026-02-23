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
    }
}


# =========================================================
# 📦 INSTALLED APPS
# =========================================================
INSTALLED_APPS = [

    # Jazzmin MUST be before admin
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
# 🧩 MIDDLEWARE
# =========================================================
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
# 📂 STATIC FILES (RENDER PRODUCTION READY)
# =========================================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# 🔐 RENDER HTTPS FIX (VERY IMPORTANT)
# =========================================================
CSRF_TRUSTED_ORIGINS = [
    "https://accountingexpert.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# =========================================================
# 🎨 JAZZMIN PROFESSIONAL SETTINGS (NO COLOR SWITCHER)
# =========================================================
JAZZMIN_SETTINGS = {
    "site_title": "Accounting Expert Admin",
    "site_header": "Accounting Expert",
    "site_brand": "Accounting Expert",
    "welcome_sign": "Welcome to Accounting Expert Dashboard",
    "copyright": "Accounting Expert Pvt Ltd",

    "show_sidebar": True,
    "navigation_expanded": True,

    # 🚫 Disable theme/color builder
    "show_ui_builder": False,

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "converter.Plan": "fas fa-box",
        "converter.UserProfile": "fas fa-id-card",
    },

    "topmenu_links": [
        {"name": "View Website", "url": "/", "new_window": True},
    ],
}


JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-primary",

    # Fixed theme (no dark mode toggle)
    "theme": "cosmo",
    "dark_mode_theme": None,
}
