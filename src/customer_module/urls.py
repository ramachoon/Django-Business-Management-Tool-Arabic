from django.urls import path
from . import views as customer_views

app_name = 'customer_module'

urlpatterns = [
    path('', customer_views.customer_home_page, name='home')
]
