from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


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

    user_credits = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)

    def activate_plan(self, plan):
        self.plan = plan
        self.user_credits = plan.credit_limit
        self.expiry_date = timezone.now().date() + timedelta(days=30 * plan.duration_months)
        self.save()

    def is_active(self):
        if not self.expiry_date:
            return False
        return self.expiry_date >= timezone.now().date()

    def use_credit(self):
        if self.user_credits <= 0:
            return False
        self.user_credits -= 1
        self.save()
        return True

    def __str__(self):
        return self.user.username
