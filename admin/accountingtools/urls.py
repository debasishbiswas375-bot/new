from django.contrib import admin
from django.urls import path
from converter import views

# --- EMERGENCY DATABASE REBUILD ---
try:
    from django.core.management import call_command
    print("🔨 Building fresh database tables...")
    # This creates the tables without checking for old history
    call_command('migrate', '--run-syncdb', interactive=False)
    
    # Restore the Admin User
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Database and Admin ready!")
except Exception as e:
    print(f"⚠️ Startup Status: {e}")
# ----------------------------------

admin.site.site_header = "Accounting Expert"
admin.site.site_title = "Accounting Expert Portal"
admin.site.index_title = "Welcome to Accounting Expert"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
