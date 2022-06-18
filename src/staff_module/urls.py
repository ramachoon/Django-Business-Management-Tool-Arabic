from django.urls import path
from . import views as staff_views

app_name = 'staff_module'
urlpatterns = [
    path('', staff_views.staff_home_page, name='home'),

    # departments
    path('departments/', staff_views.StaffDepartmentList.as_view(), name='department_list'),
    path('departments/detail/<int:pk>', staff_views.StaffDepartmentDetail.as_view(), name='department_detail'),

    # projects
    path('projects/', staff_views.StaffProjectList.as_view(), name='project_list'),
    path('projects/create/<int:department_pk>', staff_views.StaffProjectCreate.as_view(), name='project_create'),
    path('projects/detail/<int:pk>', staff_views.StaffProjectDetail.as_view(), name='project_detail'),
    path('projects/update/<int:pk>', staff_views.StaffProjectUpdate.as_view(), name='project_update'),
    path('projects/delete/<int:pk>', staff_views.StaffProjectDelete.as_view(), name='project_delete'),

    # workdays
    path('workdays/detail/<int:pk>', staff_views.StaffWorkDayDetail.as_view(), name='workday_detail'),
]
