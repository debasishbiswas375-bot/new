import os
print("FOLDERS:", os.listdir())

from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth.models import User
from core.views import register_user, login_user, home


# Auto-create admin user
def auto_create_admin():
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin",
                "admin@example.com",
                "Deba9002043666"
            )
    except Exception:
        pass


auto_create_admin()


def jump_to_streamlit(request):
    return redirect("https://newtool.streamlit.app/")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user),
    path('api/login/', login_user),
    path('', home),  # backend check
]
