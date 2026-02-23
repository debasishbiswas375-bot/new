from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
# USER PROFILE ADMIN
# ==========================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_plan",
        "user_credits",
        "expiry_date",
    )

    search_fields = ("user__username",)
    list_select_related = ("user", "plan")

    def get_plan(self, obj):
        if obj.plan:
            return obj.plan.name
        return "-"
    get_plan.short_description = "Plan"


# ==========================================
# CUSTOM USER ADMIN (Shows Plan + Credits)
# ==========================================
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "get_plan",
        "get_credits",
        "get_expiry",
        "is_staff",
    )

    list_select_related = ("userprofile",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("userprofile__plan")

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
    get_expiry.short_description = "Expiry"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
