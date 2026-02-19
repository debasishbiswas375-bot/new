from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.shortcuts import redirect # Added for redirect

# Automatically creates your admin user on startup
def auto_create_admin():
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "Deba9002043666")
    except Exception:
        pass

auto_create_admin()

# Function to handle the redirect to Streamlit
def redirect_to_streamlit(request):
    return redirect("https://tally-tools.streamlit.app/")

admin.site.site_header = "Accounting Expert Admin Portal"
admin.site.site_title = "Accounting Expert Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line fixes the "Not Found" error by redirecting the home page
    path('', redirect_to_streamlit), 
]
