from django.urls import path
from .views import (
    otp_login
)

app_name = 'account'
urlpatterns = [
    path('login/', otp_login, name='login')
]
