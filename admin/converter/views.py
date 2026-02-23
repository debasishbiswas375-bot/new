import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, Plan


# ======================================================
# GET ALL PLANS (NEW API)
# ======================================================
def get_plans(request):
    plans = Plan.objects.all()

    data = []
    for plan in plans:
        data.append({
            "id": plan.id,
            "name": plan.name,
            "price": float(plan.price),
            "duration_months": plan.duration_months,
            "credit_limit": plan.credit_limit,
        })

    return JsonResponse({"plans": data})


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

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # assign first plan automatically (or signup free if exists)
            plan = Plan.objects.first()

            profile = UserProfile.objects.create(user=user)
            if plan:
                profile.activate_plan(plan)

            return JsonResponse({
                "success": True,
                "plan": plan.name if plan else None
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

            if profile.expiry_date and profile.expiry_date < timezone.now().date():
                return JsonResponse({"error": "Subscription expired"}, status=403)

            return JsonResponse({
                "success": True,
                "username": username,
                "plan": profile.plan.name if profile.plan else None,
                "credits_remaining": profile.user_credits,
                "expiry_date": profile.expiry_date
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
