from django.urls import path
from . import views as managers_views

app_name = 'managers'
urlpatterns = [
    path('users/', managers_views.UsersList.as_view(), name='user_list'),
]
