from django.urls import path
from . import views as managers_views

app_name = 'managers'
urlpatterns = [
    path('users/', managers_views.UsersList.as_view(), name='user_list'),
    path('users/create/', managers_views.UserCreate.as_view(), name='user_create'),
    path('users/update/<int:pk>', managers_views.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>', managers_views.UserDelete.as_view(), name='user_delete'),
    path('users/is-active', managers_views.user_activate_deactivate, name='user_is_active'),
]
