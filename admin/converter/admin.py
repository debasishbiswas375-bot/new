from django.contrib import admin
from .models import UserProfile, Plan


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "safe_user", "plan", "user_credits", "expiry_date")
    search_fields = ("user__username", "full_name")

    def safe_user(self, obj):
        if obj.user_id:
            return obj.user.username
        return "Deleted User"

    safe_user.short_description = "User"


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "credit_limit", "duration_months")
