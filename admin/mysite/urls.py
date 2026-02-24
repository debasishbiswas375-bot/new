from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

def home_redirect(request):
    return redirect("https://newtool.streamlit.app")

urlpatterns = [
    path("", home_redirect),  # root redirect
    path("admin/", admin.site.urls),
]
