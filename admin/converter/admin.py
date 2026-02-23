from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta

from django.contrib.auth.models import User
from .models import Plan, UserProfile


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

        # Weekly chart data
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

admin_site.register(User)
admin_site.register(Plan)
admin_site.register(UserProfile)
