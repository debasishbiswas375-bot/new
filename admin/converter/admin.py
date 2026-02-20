from django.contrib import admin
from .models import Plan, UserProfile


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "default_credits")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "credits",
        "files_converted"
    )
