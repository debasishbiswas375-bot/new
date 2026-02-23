from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta

from .models import Plan, UserProfile


# ==========================================
# PLAN ADMIN
# ==========================================
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "credit_limit",
        "duration_display",
    )

    search_fields = ("name",)
    list_filter = ("duration_months",)

    def duration_display(self, obj):
        return f"{obj.duration_months} Month(s)"
    duration_display.short_description = "Duration"


# ==========================================
# USER PROFILE INLINE
# ==========================================
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


# ==========================================
# OPTIMIZED USER ADMIN
# ==========================================
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "get_plan",
        "get_credits",
        "get_expiry",
        "is_staff",
    )

    search_fields = ("username", "email", "first_name", "last_name")

    list_select_related = ("userprofile",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("userprofile")

    def get_plan(self, obj):
        if hasattr(obj, "userprofile") and obj.userprofile.plan:
            return obj.userprofile.plan.name
        return "-"
    get_plan.short_description = "Plan"

    def get_credits(self, obj):
        if hasattr(obj, "userprofile"):
            return obj.userprofile.user_credits
        return "-"
    get_credits.short_description = "Credits"

    def get_expiry(self, obj):
        if hasattr(obj, "userprofile") and obj.userprofile.expiry_date:
            return obj.userprofile.expiry_date
        return "-"
    get_expiry.short_description = "Expiry Date"


# Unregister default User admin
admin.site.unregister(User)

# Register new one
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
