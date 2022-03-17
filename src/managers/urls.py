from django.urls import path
from . import views as managers_views

app_name = 'managers'
urlpatterns = [
    # users
    path('users/', managers_views.UsersList.as_view(), name='user_list'),
    path('users/create/', managers_views.UserCreate.as_view(), name='user_create'),
    path('users/update/<int:pk>', managers_views.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>', managers_views.UserDelete.as_view(), name='user_delete'),
    path('users/is-active', managers_views.user_activate_deactivate, name='user_is_active'),

    # departments
    path('departments/', managers_views.DepartmentsList.as_view(), name='department_list'),
    path('departments/create/', managers_views.DepartmentCreate.as_view(), name='department_create'),
    path('departments/detail/<int:pk>', managers_views.DepartmentDetail.as_view(), name='department_detail'),
    path('departments/update/<int:pk>', managers_views.DepartmentUpdate.as_view(), name='department_update'),
    path('departments/delete/<int:pk>', managers_views.DepartmentDelete.as_view(), name='department_delete'),

    # projects
    path('projects/', managers_views.ProjectsList.as_view(), name='project_list'),
    path('projects/create/', managers_views.ProjectCreate.as_view(), name='project_create'),
    path('projects/detail/<int:pk>', managers_views.ProjectDetail.as_view(), name='project_detail'),
    path('projects/update/<int:pk>', managers_views.ProjectUpdate.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', managers_views.ProjectDelete.as_view(), name='project_delete'),

    # work days
    path('workdays/create/', managers_views.WorkDayCreate.as_view(), name='workday_create'),
    path('workdays/detail/<int:pk>', managers_views.WorkDayDetail.as_view(), name='workday_detail'),
    path('workdays/update/<int:pk>', managers_views.WorkDayUpdate.as_view(), name='workday_update'),
]
