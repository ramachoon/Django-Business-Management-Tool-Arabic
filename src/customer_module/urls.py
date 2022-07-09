from django.urls import path
from . import views as customer_views

app_name = 'customer_module'

urlpatterns = [
    path('', customer_views.customer_home_page, name='home'),

    # projects
    path('projects/', customer_views.CustomerProjectList.as_view(), name='project_list'),
    path('projects/<int:pk>', customer_views.CustomerProjectDetail.as_view(), name='project_detail'),

    # work days
    path('workdays/<int:pk>', customer_views.CustomerWorkDayDetail.as_view(), name='workday_detail'),

    # invoices
    path('invoices/<str:pk>', customer_views.CustomerInvoiceDetail.as_view(), name='invoice_detail'),
]
