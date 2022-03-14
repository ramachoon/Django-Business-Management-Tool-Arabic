from django.urls import path
from .views import main_view

app_name = 'core'
urlpatterns = [
    path('', main_view, name='main_view')
]
