import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import UserProfile, Plan


# ======================================================
# GET PLANS
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
# REGISTER USER WITH OTP
# ======================================================
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            full_name = data.get("full_name")
            company = data.get("company")
            phone = data.get("phone")
            address = data.get("address")
            pin_code = data.get("pin_code")
            district = data.get("district")
            state = data.get("state")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            profile = UserProfile.objects.create(
                user=user,
                full_name=full_name,
                company=company,
                phone=phone,
                address=address,
                pin_code=pin_code,
                district=district,
                state=state,
            )

            profile.generate_otp()

            send_mail(
                "Verify Your Email - Accounting Expert",
                f"Your OTP is {profile.email_otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"message": "User created. Check email for OTP."}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# ======================================================
# VERIFY EMAIL OTP
# ======================================================
@csrf_exempt
def verify_email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        otp = data.get("otp")

        try:
            profile = UserProfile.objects.get(user__username=username)

            if profile.email_otp == otp:
                profile.email_verified = True
                profile.email_otp = None
                profile.save()
                return JsonResponse({"message": "Email verified successfully"})

            return JsonResponse({"error": "Invalid OTP"}, status=400)

        except:
            return JsonResponse({"error": "User not found"}, status=404)


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

            if not profile.email_verified:
                return JsonResponse({"error": "Email not verified"}, status=403)

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
