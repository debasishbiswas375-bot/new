import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import UserProfile, Plan


# ======================================================
# REGISTER USER
# ======================================================
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Missing fields"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Create Django user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Get signup free plan
            try:
                plan = Plan.objects.get(name="signup free")
            except Plan.DoesNotExist:
                return JsonResponse({"error": "Signup plan not found"}, status=500)

            # Create profile + activate plan
            profile = UserProfile.objects.create(user=user)
            profile.activate_plan(plan)

            return JsonResponse({
                "success": True,
                "plan": plan.name,
                "credits": plan.credits,
                "expires_on": profile.subscription_end
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ======================================================
# LOGIN USER
# ======================================================
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if not user:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

            profile = UserProfile.objects.get(user=user)

            # Check expiry
            if not profile.is_active():
                return JsonResponse({"error": "Subscription expired"}, status=403)

            return JsonResponse({
                "success": True,
                "username": username,
                "plan": profile.plan.name if profile.plan else None,
                "credits_remaining": profile.credits_remaining,
                "expires_on": profile.subscription_end
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
