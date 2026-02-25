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
        return self.name or "Unnamed Plan"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True, null=True)

    user_credits = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)

    def generate_otp(self):
        self.email_otp = str(random.randint(100000, 999999))
        self.save(update_fields=["email_otp"])

    def activate_plan(self, plan):
        self.plan = plan
        self.user_credits = plan.credit_limit
        self.expiry_date = timezone.now().date() + timedelta(days=30 * plan.duration_months)
        self.save(update_fields=["plan", "user_credits", "expiry_date"])

    def __str__(self):
        # ULTRA SAFE — prevents 500 if user deleted
        if self.user_id:
            return self.user.username
        return f"Orphaned Profile {self.id}"
