from django.urls import path
from converter.admin import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
]
