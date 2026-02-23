import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import UserProfile, Plan


# ================= GET PLANS =================
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


# ================= REGISTER =================
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Missing fields"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        profile = UserProfile.objects.create(user=user)

        free_plan = Plan.objects.first()
        if free_plan:
            profile.activate_plan(free_plan)

        return JsonResponse({"success": True}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ================= LOGIN =================
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        profile = UserProfile.objects.get(user=user)

        if not profile.is_active():
            return JsonResponse({"error": "Subscription expired"}, status=403)

        return JsonResponse({
            "success": True,
            "username": username,
            "plan": profile.plan.name if profile.plan else None,
            "credits_remaining": profile.user_credits,
            "expiry_date": profile.expiry_date
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


# ================= CHECK CREDITS =================
@csrf_exempt
def check_credits(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)

            return JsonResponse({
                "credits_remaining": profile.user_credits,
                "expiry_date": profile.expiry_date
            })
        except:
            return JsonResponse({"error": "User not found"}, status=404)


# ================= USE CREDIT =================
@csrf_exempt
def use_credit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)

            if not profile.is_active():
                return JsonResponse({"error": "Subscription expired"}, status=403)

            if not profile.use_credit():
                return JsonResponse({"error": "No credits left"}, status=403)

            return JsonResponse({
                "success": True,
                "credits_remaining": profile.user_credits
            })

        except:
            return JsonResponse({"error": "User not found"}, status=404)
