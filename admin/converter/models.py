from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# ===============================
# PLAN (Template)
# ===============================
class Plan(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=0)
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name


# ===============================
# USER SUBSCRIPTION
# ===============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    credits_remaining = models.IntegerField(default=0)

    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

    def activate_plan(self, plan):
        self.plan = plan
        self.credits_remaining = plan.credits
        self.subscription_start = timezone.now()
        self.subscription_end = timezone.now() + timedelta(days=plan.duration_days)
        self.save()

    def is_active(self):
        if self.subscription_end:
            return timezone.now() <= self.subscription_end
        return False

    def __str__(self):
        return self.user.username
