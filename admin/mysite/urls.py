from django.contrib import admin
from django.urls import path
from converter.views import (
    register_user,
    login_user,
    get_plans,
    check_credits,
    use_credit
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/plans/', get_plans),
    path('api/check-credits/', check_credits),
    path('api/use-credit/', use_credit),
]
