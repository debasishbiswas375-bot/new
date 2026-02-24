from django.contrib import admin
from .models import Plan, UserProfile

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months', 'credit_limit')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Use list_select_related to reduce database hits to Supabase
    list_select_related = ('user', 'plan')
    list_display = ('get_username', 'get_plan_name', 'user_credits', 'expiry_date')
    search_fields = ('user__username', 'full_name', 'phone')

    def get_username(self, obj):
        return obj.user.username if obj.user else "No User"
    get_username.short_description = 'Username'

    def get_plan_name(self, obj):
        return obj.plan.name if obj.plan else "No Plan"
    get_plan_name.short_description = 'Plan'
