from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    return HttpResponse("Django Backend Running ✅")


# ===============================
# REGISTER USER API
# ===============================
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not password:
                return JsonResponse(
                    {"error": "Username and password required"},
                    status=400
                )

            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {"error": "Username already exists"},
                    status=400
                )

            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                is_active=True
            )

            return JsonResponse(
                {"message": "User created successfully"},
                status=201
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ===============================
# LOGIN USER API
# ===============================
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            password = data.get("password")

            user = User.objects.filter(username=username).first()

            if user and check_password(password, user.password):
                return JsonResponse(
                    {"message": "Login successful"},
                    status=200
                )

            return JsonResponse(
                {"error": "Invalid credentials"},
                status=400
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
