from django.contrib import admin
from .models import UserProfile, Plan


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "user_credits", "expiry_date")
    search_fields = ("user__username", "full_name")


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "credit_limit", "duration_months")
