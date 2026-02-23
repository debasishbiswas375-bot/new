import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()

# --- PERMANENT DATABASE BUILDER ---
# This runs every time Render starts to ensure the database exists.
try:
    print("🚀 WAKING UP & BUILDING DATABASE...")
    
    # 1. Update the blueprints (just in case)
    call_command('makemigrations', 'converter', interactive=False)
    
    # 2. Build the tables
    call_command('migrate', interactive=False)
    
    # 3. Ensure the Admin user always exists
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        print("👤 RESTORING ADMIN USER...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        
    print("✅ SYSTEM READY!")

except Exception as e:
    print(f"⚠️ STARTUP INFO: {e}")
