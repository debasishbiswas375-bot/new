import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import UserProfile, Plan


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

            # Assign first available plan
            plan = Plan.objects.first()

            UserProfile.objects.create(
                user=user,
                plan=plan
            )

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            password = data.get("password")

            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
