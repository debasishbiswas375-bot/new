from django.contrib import admin
from .models import Plan, Profile

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'monthly_limit')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'plan')
    list_filter = ('plan',)
    search_fields = ('email', 'username')
