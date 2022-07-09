from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.decorators import customer_access_decorator
from core.mixins import CustomerAccessMixin
from projects.models import Project, WorkDay, Invoice


# Create your views here.


@customer_access_decorator()
def customer_home_page(request):
    context = {
        'text': 'داشبورد کارفرما'
    }
    return render(request, 'core/panel/pages/panel_home_page.html', context)


class CustomerProjectList(CustomerAccessMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        qs = Project.objects.filter(
            customers__in=[self.request.user], department__is_active=True, accessibility='only_customer'
        )
        return qs

    template_name = 'core/panel/pages/project_list.html'
    paginate_by = 6
    context_object_name = 'projects'
    permission_required = 'projects.view_project'


class CustomerProjectDetail(CustomerAccessMixin, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Project.objects.get_project_for_customer(pk, self.request.user)

    template_name = 'core/panel/pages/project_detail.html'
    context_object_name = 'project'
    permission_required = 'projects.view_project'


class CustomerWorkDayDetail(CustomerProjectDetail, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return WorkDay.objects.get_work_day_for_customer(pk, self.request.user)

    template_name = 'core/panel/pages/workday_detail.html'
    context_object_name = 'workday'
    permission_required = 'projects.view_workday'


class CustomerInvoiceDetail(CustomerAccessMixin, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Invoice.objects.get_invoice_for_customer(pk, self.request.user)

    template_name = 'core/panel/pages/invoice_detail.html'
    context_object_name = 'invoice'
    permission_required = 'projects.view_invoice'
