from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import random


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.IntegerField(default=1)
    credit_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    # NEW FIELDS
    full_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)

    user_credits = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)

    def generate_otp(self):
        self.email_otp = str(random.randint(100000, 999999))
        self.save()

    def activate_plan(self, plan):
        self.plan = plan
        self.user_credits = plan.credit_limit
        self.expiry_date = timezone.now().date() + timedelta(days=30 * plan.duration_months)
        self.save()

    def __str__(self):
        return self.user.username
