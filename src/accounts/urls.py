from django.urls import path
from .views import (
    otp_login,
    verify_phone_otp,
    register
)

app_name = 'account'
urlpatterns = [
    path('login/', otp_login, name='login'),
    path('register/', register, name='register'),
    path('login/verify/', verify_phone_otp, name='verify_otp'),
]
