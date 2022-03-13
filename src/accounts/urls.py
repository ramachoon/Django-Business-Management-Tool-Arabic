from django.urls import path
from .views import (
    otp_login,
    verify_phone_otp
)

app_name = 'account'
urlpatterns = [
    path('login/', otp_login, name='login'),
    path('login/verify/', verify_phone_otp, name='verify_otp'),
]
