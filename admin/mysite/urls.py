from django.contrib import admin
from django.urls import path
from converter.views import register_user, login_user

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('register/', register_user),
    path('login/', login_user),
]
