from rest_framework.decorators import api_view
from rest_framework.response import Response
from jose import jwt
from django.conf import settings
from decimal import Decimal
from .models import UserProfile, Plan, ConversionLog


def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except Exception:
        return None


@api_view(['POST'])
def process_conversion(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return Response({"error": "No token provided"})

    token = auth_header.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        return Response({"error": "Invalid token"})

    email = payload.get("email")

    profile, created = UserProfile.objects.get_or_create(email=email)

    if created:
        startup = Plan.objects.filter(name="Startup").first()
        if startup:
            profile.plan = startup
            profile.credits = startup.credits
            profile.save()

    if profile.credits < Decimal("0.10"):
        return Response({"error": "Not enough credits"})

    profile.credits -= Decimal("0.10")
    profile.save()

    ConversionLog.objects.create(
        email=email,
        file_name="converted_file.pdf",
        credits_used=Decimal("0.10")
    )

    return Response({
        "message": "Conversion successful",
        "remaining_credits": profile.credits
    })
