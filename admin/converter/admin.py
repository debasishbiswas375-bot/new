# converter/admin.py

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    # Remove 'credit_limit' and 'duration_months' if they don't exist in models.py
    list_display = ('name', 'price') # Adjust based on what ACTUALLY exists

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Remove 'user_credits' and 'expiry_date' if they don't exist in models.py
    list_display = ('user', 'plan') # Adjust based on what ACTUALLY exists
