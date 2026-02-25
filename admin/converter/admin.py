from django.contrib import admin
from .models import UserProfile, Plan
from django.contrib.auth.models import User


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "safe_user", "plan", "user_credits", "expiry_date")
    search_fields = ("full_name",)

    def get_queryset(self, request):
        """
        Only show profiles that still have a valid user.
        This prevents 500 error.
        """
        qs = super().get_queryset(request)
        return qs.filter(user__isnull=False)

    def safe_user(self, obj):
        return obj.user.username if obj.user_id else "Deleted User"

    safe_user.short_description = "User"


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "credit_limit", "duration_months")
