from django.contrib import admin
from django.urls import path
from .views import register_user, login_user, user_info, convert_file

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/user-info/', user_info),
    path('api/convert/', convert_file),
]
