from django.urls import path
from . import views as managers_views

app_name = 'managers'
urlpatterns = [
    path('', managers_views.managers_home_page, name='home'),
    path('update/', managers_views.AccountUpdate.as_view(), name='account_update'),

    # users
    path('users/', managers_views.UsersList.as_view(), name='user_list'),
    path('users/create/', managers_views.UserCreate.as_view(), name='user_create'),
    path('users/update/<int:pk>', managers_views.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>', managers_views.UserDelete.as_view(), name='user_delete'),
    path('users/is-active', managers_views.user_activate_deactivate, name='user_is_active'),

    # groups
    path('groups/', managers_views.GroupList.as_view(), name='group_list'),
    path('groups/create/', managers_views.GroupCreate.as_view(), name='group_create'),
    path('groups/update/<int:pk>', managers_views.GroupUpdate.as_view(), name='group_update'),
    path('groups/delete/<int:pk>', managers_views.GroupDelete.as_view(), name='group_delete'),

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
    path('workdays/', managers_views.WorkDayList.as_view(), name='workday_list'),
    path('workdays/print/', managers_views.WorkDayPrintList.as_view(), name='workday_print_list'),
    path('workdays/create/', managers_views.WorkDayCreate.as_view(), name='workday_create'),
    path('workdays/detail/<int:pk>', managers_views.WorkDayDetail.as_view(), name='workday_detail'),
    path('workdays/update/<int:pk>', managers_views.WorkDayUpdate.as_view(), name='workday_update'),
    path('workdays/delete/<int:pk>', managers_views.WorkDayDelete.as_view(), name='workday_delete'),

    # invoices
    path('invoices/', managers_views.InvoiceList.as_view(), name='invoice_list'),
    path('invoices/create/', managers_views.invoice_create, name='invoice_create'),
    path('invoices/<str:pk>', managers_views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/print/<str:pk>', managers_views.InvoicePrintDetail.as_view(), name='invoice_print_detail'),
    path('invoices/update/<str:pk>', managers_views.invoice_update, name='invoice_update'),
    path('invoices/delete/<str:pk>', managers_views.InvoiceDelete.as_view(), name='invoice_delete'),

    # Storeroom
    path('storeroom/kala-list/', managers_views.KalaList.as_view(), name='kala_list'),
    path('storeroom/kala-detail/<str:pk>', managers_views.KalaDetail.as_view(), name='kala_detail'),

    # ip address
    path('activities/', managers_views.IPAddressList.as_view(), name='ip_address_list'),
]
