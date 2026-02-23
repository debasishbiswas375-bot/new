from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

def home(request):
    return redirect("/admin/")

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]
