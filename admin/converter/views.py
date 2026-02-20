from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .models import Plan, UserProfile
import json


# ==============================
# REGISTER USER
# ==============================
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        # Create Free Plan if not exists
        free_plan, _ = Plan.objects.get_or_create(
            name="Free",
            defaults={"default_credits": 100}
        )

        UserProfile.objects.create(
            user=user,
            plan=free_plan,
            credits=free_plan.default_credits
        )

        return JsonResponse({"message": "User registered successfully"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ==============================
# LOGIN USER
# ==============================
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ==============================
# USER INFO (Plan + Credits)
# ==============================
def user_info(request):
    username = request.GET.get("username")

    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)

        return JsonResponse({
            "plan": profile.plan.name if profile.plan else "None",
            "credits": profile.credits,
            "files_converted": profile.files_converted
        })
    except:
        return JsonResponse({"error": "User not found"}, status=404)


# ==============================
# FILE CONVERSION (TRACK USAGE)
# ==============================
def convert_file(request):
    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)

            if profile.credits <= 0:
                return JsonResponse({"error": "No credits left"}, status=400)

            # Simulate conversion
            profile.credits -= 1
            profile.files_converted += 1
            profile.save()

            return JsonResponse({"message": "File converted successfully"})
        except:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
