from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Admin auto-creation logic
def auto_create_admin():
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "Deba9002043666")
    except Exception:
        pass

auto_create_admin()

# Redirect function
def redirect_to_streamlit(request):
    # Change this URL if your Streamlit link has changed!
    return redirect("https://tally-tools.streamlit.app/")

admin.site.site_header = "Accounting Expert Admin Portal"
admin.site.site_title = "Accounting Expert Admin Portal"
admin.site.index_title = "Welcome to the Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),  # Your working admin portal
    path('', redirect_to_streamlit),  # Redirects the 'Not Found' root to Streamlit
]
