from django.contrib import admin
from django.urls import path
from converter.views import register_user, login_user, get_plans, verify_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('verify-email/', verify_email),
    path('login/', login_user),
    path('plans/', get_plans),
]
