from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=100)
    credits = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ConversionLog(models.Model):
    email = models.EmailField()
    file_name = models.CharField(max_length=255)
    credits_used = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
