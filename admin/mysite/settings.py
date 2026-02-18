import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ... (Keep your SECRET_KEY, DEBUG, and INSTALLED_APPS as they are) ...

# FIX NAMESPACES (Change from 'mysite' to your folder name)
ROOT_URLCONF = 'accountingtools.urls'
WSGI_APPLICATION = 'accountingtools.wsgi.application'

# DATABASE CONFIGURATION
# This ensures Django uses Supabase on Render but SQLite locally
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
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

# RENDER SECURITY SETTINGS (Add these to the end of the file)
# This fixes the Login Refresh loop by recognizing Render's HTTPS proxy
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True # Optional: Forces all traffic to HTTPS
