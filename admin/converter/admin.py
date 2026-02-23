from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib import admin
from .models import Plan, UserProfile


class MyAdminSite(AdminSite):
    site_header = "Accounting Expert"
    site_title = "Accounting Expert Admin"
    index_title = "Dashboard"
    index_template = "admin/dashboard.html"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["total_users"] = User.objects.count()
        extra_context["total_plans"] = Plan.objects.count()
        extra_context["total_profiles"] = UserProfile.objects.count()
        return super().index(request, extra_context=extra_context)


admin_site = MyAdminSite(name="myadmin")

# Register models
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Plan)
admin_site.register(UserProfile)
