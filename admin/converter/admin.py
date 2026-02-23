from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Plan, UserProfile


# =========================
# 🔥 CUSTOM ADMIN SITE
# =========================
class CustomAdminSite(AdminSite):
    site_header = "Accounting Expert"
    site_title = "Accounting Expert Admin"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("", self.admin_view(self.dashboard), name="index"),
        ]
        return custom_urls + urls

    def dashboard(self, request):
        today = now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        total_users = User.objects.count()
        total_plans = Plan.objects.count()
        total_profiles = UserProfile.objects.count()

        users_today = User.objects.filter(date_joined__date=today).count()
        users_week = User.objects.filter(date_joined__date__gte=week_ago).count()
        users_month = User.objects.filter(date_joined__date__gte=month_ago).count()

        weekly_data = (
            User.objects.filter(date_joined__date__gte=week_ago)
            .extra(select={"day": "date(date_joined)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        labels = [str(entry["day"]) for entry in weekly_data]
        data = [entry["count"] for entry in weekly_data]

        context = dict(
            self.each_context(request),
            total_users=total_users,
            total_plans=total_plans,
            total_profiles=total_profiles,
            users_today=users_today,
            users_week=users_week,
            users_month=users_month,
            chart_labels=labels,
            chart_data=data,
        )

        return TemplateResponse(request, "admin/dashboard.html", context)


admin_site = CustomAdminSite(name="custom_admin")


# =========================
# 🔥 INLINE USER PROFILE
# =========================
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


# =========================
# 🔥 EXTENDED USER ADMIN
# =========================
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "get_plan",
        "get_expiry",
        "is_staff",
    )

    def get_plan(self, obj):
        if hasattr(obj, "userprofile") and obj.userprofile.plan:
            return obj.userprofile.plan.name
        return "-"
    get_plan.short_description = "Plan"

    def get_expiry(self, obj):
        if hasattr(obj, "userprofile") and obj.userprofile.expiry_date:
            return obj.userprofile.expiry_date
        return "-"
    get_expiry.short_description = "Renewal Date"


# =========================
# REGISTER MODELS
# =========================
admin_site.register(User, CustomUserAdmin)
admin_site.register(Plan)
admin_site.register(UserProfile)
