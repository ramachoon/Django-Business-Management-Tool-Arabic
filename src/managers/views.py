from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from accounts.models import User

from accounts.forms import UsersForm
from core.decorators import superuser_access_decorator
from core.mixins import (
    SuperuserAccessMixin
)
from departments.forms import DepartmentForm
from departments.models import Department
from projects.forms import ProjectsForm, WorkDaysForm, InvoicesForm, InvoiceDetailsForm, FilterWorkDayForm
from projects.models import Project, WorkDay, Invoice, InvoiceDetail


# Create your views here.


class UsersList(SuperuserAccessMixin, ListView):
    def get_queryset(self):
        users = User.objects.all().order_by('-id')
        filter_params = self.request.GET.get('filter')
        if filter_params == 'customer':
            return users.filter(is_customer=True)
        elif filter_params == 'employee':
            return users.filter(is_employee=True)
        elif filter_params == 'manager':
            return users.filter(is_superuser=True)
        elif filter_params == 'supporter':
            return users.filter(is_supporter=True)
        elif filter_params == 'admin':
            return users.filter(is_admin=True)
        return users

    template_name = 'managers/user_list.html'
    context_object_name = 'users'
    paginate_by = 12


class UserCreate(CreateView):
    model = User
    template_name = 'managers/user_create_update.html'
    success_url = reverse_lazy('managers:user_list')
    form_class = UsersForm


class UserUpdate(SuperuserAccessMixin, UpdateView):
    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        return user

    template_name = 'managers/user_create_update.html'
    success_url = reverse_lazy('managers:user_list')
    form_class = UsersForm


class UserDelete(SuperuserAccessMixin, DeleteView):
    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        return user

    template_name = 'managers/user_delete.html'
    success_url = reverse_lazy('managers:user_list')


@superuser_access_decorator()
def user_activate_deactivate(request, *args, **kwargs):
    user_id = request.POST['user_id']

    try:
        message = 'deactivate'
        user = User.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        elif not user.is_active:
            user.is_active = True
            message = 'activate'
        user.save()
        return HttpResponse(message, status=200)
    except User.DoesNotExist:
        return HttpResponse(status=502)


class DepartmentsList(SuperuserAccessMixin, ListView):
    model = Department
    template_name = 'managers/department_list.html'
    ordering = '-id'
    context_object_name = 'departments'
    paginate_by = 9


class DepartmentDetail(SuperuserAccessMixin, DetailView):
    def get_object(self, queryset=None):
        department = get_object_or_404(Department, id=self.kwargs.get('pk'))
        return department

    template_name = 'managers/department_detail.html'
    context_object_name = 'department'


class DepartmentCreate(SuperuserAccessMixin, CreateView):
    def form_valid(self, form):
        department_form = form.save(commit=False)
        department_form.maker = self.request.user
        department_form.save()
        return super(DepartmentCreate, self).form_valid(form)

    model = Department
    template_name = 'managers/department_create_update.html'
    form_class = DepartmentForm


class DepartmentUpdate(SuperuserAccessMixin, UpdateView):
    def get_object(self, queryset=None):
        department = get_object_or_404(Department, id=self.kwargs.get('pk'))
        return department

    def form_valid(self, form):
        department_form = form.save(commit=False)
        department_form.maker = self.request.user
        department_form.save()
        return super(DepartmentUpdate, self).form_valid(form)

    template_name = 'managers/department_create_update.html'
    form_class = DepartmentForm


class DepartmentDelete(SuperuserAccessMixin, DeleteView):
    def get_object(self, queryset=None):
        department = get_object_or_404(Department, id=self.kwargs.get('pk'))
        return department

    template_name = 'managers/department_delete.html'
    success_url = reverse_lazy('managers:department_list')


class ProjectsList(SuperuserAccessMixin, ListView):
    model = Project
    template_name = 'managers/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6
    ordering = '-id'


class ProjectDetail(SuperuserAccessMixin, DetailView):
    model = Project
    template_name = 'managers/project_detail.html'


class ProjectCreate(SuperuserAccessMixin, CreateView):
    model = Project
    template_name = 'managers/project_create_update.html'
    form_class = ProjectsForm


class ProjectUpdate(SuperuserAccessMixin, UpdateView):
    model = Project
    template_name = 'managers/project_create_update.html'
    form_class = ProjectsForm


class ProjectDelete(SuperuserAccessMixin, DeleteView):
    model = Project
    template_name = 'managers/project_delete.html'
    success_url = reverse_lazy('managers:project_list')


class WorkDayList(SuperuserAccessMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(WorkDayList, self).get_context_data(**kwargs)
        context['filter_form'] = FilterWorkDayForm()
        return context

    model = WorkDay
    template_name = 'managers/workday_list.html'
    context_object_name = 'workdays'
    paginate_by = 30


class WorkDayPrintList(SuperuserAccessMixin, ListView):
    def get_queryset(self):
        get_method = self.request.GET
        accessibility = get_method.get('accessibility')
        from_date = get_method.get('from_date')
        to_date = get_method.get('to_date')
        if accessibility and from_date and to_date:
            queryset = WorkDay.objects.filter_workday(
                from_date=from_date,
                to_date=to_date,
                accessibility=accessibility,
            )
            return queryset
        raise Http404

    template_name = 'managers/workday_print_list.html'
    context_object_name = 'workdays'


class WorkDayDetail(SuperuserAccessMixin, DetailView):
    model = WorkDay
    template_name = 'managers/workday_detail.html'


class WorkDayCreate(SuperuserAccessMixin, CreateView):
    model = WorkDay
    template_name = 'managers/workday_create_update.html'
    form_class = WorkDaysForm


class WorkDayUpdate(SuperuserAccessMixin, UpdateView):
    model = WorkDay
    template_name = 'managers/workday_create_update.html'
    form_class = WorkDaysForm


class WorkDayDelete(SuperuserAccessMixin, DeleteView):
    model = WorkDay
    template_name = 'managers/workday_delete.html'
    success_url = reverse_lazy('managers:project_list')


class InvoiceDetailView(SuperuserAccessMixin, DetailView):
    model = Invoice
    template_name = 'managers/invoice_detail.html'


class InvoicePrintDetail(SuperuserAccessMixin, DetailView):
    model = Invoice
    template_name = 'managers/invoice_print_detail.html'


def invoice_create(request, *args, **kwargs):
    invoice_form = InvoicesForm(request.POST or None)
    invoice_detail_formset = formset_factory(InvoiceDetailsForm, extra=0)
    formset = invoice_detail_formset(request.POST or None)

    if all([invoice_form.is_valid(), formset.is_valid()]):
        invoice = invoice_form.save()
        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.invoice = invoice
            factor_detail.save()

        return redirect(
            reverse_lazy(
                'managers:invoice_detail',
                kwargs={'pk': invoice.pk}
            )
        )

    context = {
        'factor_form': invoice_form,
        'factor_detail_formset': formset,
        'form_length': 0
    }
    return render(request, 'managers/invoice_create_update.html', context=context)


def invoice_update(request, *args, **kwargs):
    # get factor
    invoice = get_object_or_404(Invoice, pk=kwargs.get('pk'))

    invoice_form = InvoicesForm(request.POST or None, instance=invoice)
    invoice_detail_formset = modelformset_factory(
        InvoiceDetail, form=InvoiceDetailsForm, extra=0, can_delete=True
    )
    qs = invoice.invoice_details.all()
    formset = invoice_detail_formset(request.POST or None, queryset=qs)

    if all([invoice_form.is_valid(), formset.is_valid()]):
        invoice = invoice_form.save()

        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.invoice = invoice
            if form.cleaned_data['DELETE']:
                factor_detail.delete()
            else:
                factor_detail.save()

        return redirect(
            reverse_lazy(
                'managers:invoice_detail',
                kwargs={'pk': invoice.pk}
            )
        )

    context = {
        'factor_form': invoice_form,
        'factor_detail_formset': formset,
        'factor': invoice,
        'form_length': qs.count()
    }
    return render(request, 'managers/invoice_create_update.html', context=context)


class InvoiceDelete(SuperuserAccessMixin, DeleteView):
    model = Invoice
    template_name = 'managers/invoice_delete.html'
    success_url = reverse_lazy('managers:project_list')
