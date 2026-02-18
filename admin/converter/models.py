from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100) # e.g., Free, Pro, Gold
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monthly_limit = models.IntegerField(default=5) # Conversions allowed

    class Meta:
        db_table = 'plans'
        managed = False 

    def __str__(self):
        return self.name

class Profile(models.Model):
    id = models.UUIDField(primary_key=True) # Matches Supabase Auth UUID
    email = models.EmailField()
    username = models.CharField(max_length=255, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'profiles'
        managed = False

    def __str__(self):
        return self.email
