from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ConversionLog, Product, Subscription

# Register the User model
admin.site.register(User, UserAdmin)

# Register the Logs
@admin.register(ConversionLog)
class LogAdmin(admin.ModelAdmin):  # <--- FIXED (Removed .site)
    list_display = ('user', 'file_name', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')

# Register the New Products & Prices
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # <--- FIXED (Removed .site)
    list_display = ('name', 'price', 'is_active')
    list_editable = ('price', 'is_active')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):  # <--- FIXED (Removed .site)
    list_display = ('user', 'product', 'start_date', 'is_active')
