from django.urls import path
from . import views as staff_views

app_name = 'staff_module'
urlpatterns = [
    path('', staff_views.staff_home_page, name='home')
]
