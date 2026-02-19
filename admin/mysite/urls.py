from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect #
from django.contrib.auth.models import User

# Keep your auto-admin trick
def auto_create_admin():
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "Deba9002043666")
    except Exception:
        pass

auto_create_admin()

# Function to handle the jump to Streamlit
def jump_to_streamlit(request):
    return redirect("https://newtool.streamlit.app/")

urlpatterns = [
    path('admin/', admin.site.urls), # Keep this so you can still use your admin panel
    path('', jump_to_streamlit),     # This sends the home page to Streamlit
]
