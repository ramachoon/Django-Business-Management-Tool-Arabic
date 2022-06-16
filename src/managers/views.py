from django.contrib.auth.models import Group
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.models import User, IPAddress
from accounts.forms import UsersForm
from core.decorators import superuser_access_decorator
from core.mixins import SuperuserAccessMixin
from departments.forms import DepartmentForm
from departments.models import Department
from projects.forms import ProjectsForm, WorkDaysForm, InvoicesForm, InvoiceDetailsForm, FilterWorkDayForm
from projects.models import Project, WorkDay, Invoice, InvoiceDetail
from storeroom.models import Kala, KalaDetail, KalaHistory


# Create your views here.


@superuser_access_decorator()
def managers_home_page(request):
    return render(request, 'managers/managers_home_page.html', {})


class AccountUpdate(SuperuserAccessMixin, UpdateView):
    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.request.user.username)
        return user

    template_name = 'managers/account_update.html'
    success_url = reverse_lazy('managers:account_update')
    fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'bio')


class UsersList(SuperuserAccessMixin, ListView):
    def get_queryset(self):
        users = User.objects.all().order_by('-last_login')
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
        elif filter_params == 'staff':
            return users.filter(is_staff=True)
        return users

    template_name = 'managers/user_list.html'
    context_object_name = 'users'
    paginate_by = 8


class UserCreate(SuperuserAccessMixin, CreateView):
    model = User
    template_name = 'managers/user_create_update.html'
    success_url = reverse_lazy('managers:user_list')
    form_class = UsersForm


class UserUpdate(SuperuserAccessMixin, UpdateView):
    model = User
    template_name = 'managers/user_create_update.html'
    success_url = reverse_lazy('managers:user_list')
    form_class = UsersForm


class UserDelete(SuperuserAccessMixin, DeleteView):
    model = User
    template_name = 'managers/user_delete.html'
    success_url = reverse_lazy('managers:user_list')


class GroupList(SuperuserAccessMixin, ListView):
    model = Group
    template_name = 'managers/group_list.html'
    context_object_name = 'groups'
    paginate_by = 12
    ordering = '-id'


class GroupCreate(SuperuserAccessMixin, CreateView):
    model = Group
    template_name = 'managers/group_create_update.html'
    success_url = reverse_lazy('managers:group_list')
    fields = ('name', 'permissions')


class GroupDelete(SuperuserAccessMixin, DeleteView):
    model = Group
    template_name = 'managers/group_delete.html'
    success_url = reverse_lazy('managers:group_list')


class GroupUpdate(SuperuserAccessMixin, UpdateView):
    model = Group
    template_name = 'managers/group_create_update.html'
    success_url = reverse_lazy('managers:group_list')
    fields = ('name', 'permissions')


@superuser_access_decorator()
def user_activate_deactivate(request, *args, **kwargs):
    if request.method == "POST":
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

    raise Http404


class DepartmentsList(SuperuserAccessMixin, ListView):
    model = Department
    template_name = 'managers/department_list.html'
    context_object_name = 'departments'
    paginate_by = 9


class DepartmentDetail(SuperuserAccessMixin, DetailView):
    model = Department
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
    def form_valid(self, form):
        department_form = form.save(commit=False)
        department_form.maker = self.request.user
        department_form.save()
        return super(DepartmentUpdate, self).form_valid(form)

    model = Department
    template_name = 'managers/department_create_update.html'
    form_class = DepartmentForm


class DepartmentDelete(SuperuserAccessMixin, DeleteView):
    model = Department
    template_name = 'managers/department_delete.html'
    success_url = reverse_lazy('managers:department_list')


class ProjectsList(SuperuserAccessMixin, ListView):
    model = Project
    template_name = 'managers/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6


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


class InvoiceList(SuperuserAccessMixin, ListView):
    model = Invoice
    template_name = 'managers/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 30


class InvoiceDetailView(SuperuserAccessMixin, DetailView):
    model = Invoice
    template_name = 'managers/invoice_detail.html'


class InvoicePrintDetail(SuperuserAccessMixin, DetailView):
    model = Invoice
    template_name = 'managers/invoice_print_detail.html'


@superuser_access_decorator()
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


@superuser_access_decorator()
def invoice_update(request, *args, **kwargs):
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


class KalaList(SuperuserAccessMixin, ListView):
    def get_queryset(self):
        kala_filter = self.request.GET.get('filter')
        if kala_filter == '0':
            return Kala.objects.filter(filter=0)
        elif kala_filter == '1':
            return Kala.objects.filter(filter=1)
        else:
            return Kala.objects.all()

    template_name = 'managers/kala_list.html'
    paginate_by = 30


class KalaDetailView(SuperuserAccessMixin, DetailView):
    model = Kala
    template_name = 'managers/kala_detail.html'


class KalaCreate(SuperuserAccessMixin, CreateView):
    model = Kala
    template_name = 'managers/kala_create_update.html'
    fields = ('name', 'description', 'filter')


class KalaUpdate(SuperuserAccessMixin, UpdateView):
    model = Kala
    template_name = 'managers/kala_create_update.html'
    fields = ('name', 'description', 'filter')


class KalaDelete(SuperuserAccessMixin, DeleteView):
    model = Kala
    template_name = 'managers/kala_delete.html'
    success_url = reverse_lazy('managers:kala_list')


def create_kala_detail(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_detail_name = cd.get('kala_detail_name')
        kala_detail_quantity = cd.get('kala_detail_quantity')
        kala_detail_price = cd.get('kala_detail_price')
        kala_detail_total = cd.get('kala_detail_total')

        try:
            # validate data and create KalaDetail
            if kala_detail_name and kala_detail_quantity and \
                    kala_detail_price and kala_detail_total:
                kala_detail = KalaDetail(
                    kala_id=kala_id,
                    name=kala_detail_name,
                    quantity=kala_detail_quantity,
                    price=kala_detail_price,
                    total=kala_detail_total
                )
                kala_detail.save()

            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_details_content.html', context)
            })
        except Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


def update_kala_detail(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_detail_id = cd.get('kala_detail_id')
        kala_detail_name = cd.get('kala_detail_name')
        kala_detail_quantity = cd.get('kala_detail_quantity')
        kala_detail_price = cd.get('kala_detail_price')
        kala_detail_total = cd.get('kala_detail_total')

        try:
            kala_detail = KalaDetail.objects.get(id=kala_detail_id)
            # validate data and create KalaDetail
            if kala_detail_name and kala_detail_quantity and \
                    kala_detail_price and kala_detail_total:
                kala_detail.name = kala_detail_name
                kala_detail.quantity = kala_detail_quantity
                kala_detail.price = kala_detail_price
                kala_detail.total = kala_detail_total
                kala_detail.save()

            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_details_content.html', context)
            })
        except KalaDetail.DoesNotExist or Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


def delete_kala_detail(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_detail_id = cd.get('kala_detail_id')

        try:
            kala_detail = KalaDetail.objects.get(id=kala_detail_id)
            kala_detail.delete()
            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_details_content.html', context)
            })
        except KalaDetail.DoesNotExist or Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


def create_kala_history(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_history_date = cd.get('kala_history_date')
        kala_history_description = cd.get('kala_history_description')

        try:
            # validate data and create KalaHistory
            if kala_history_date and kala_history_description:
                kala_history = KalaHistory(
                    kala_id=kala_id,
                    date=kala_history_date,
                    short_description=kala_history_description
                )
                kala_history.save()

            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_histories_content.html', context)
            })
        except Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


def update_kala_history(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_history_id = cd.get('kala_history_id')
        kala_history_date = cd.get('kala_history_date')
        kala_history_description = cd.get('kala_history_description')

        try:
            kala_history = KalaHistory.objects.get(id=kala_history_id)
            # validate data and create KalaHistory
            if kala_history_date and kala_history_description:
                kala_history.date = kala_history_date
                kala_history.short_description = kala_history_description
                kala_history.save()

            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_histories_content.html', context)
            })
        except KalaHistory.DoesNotExist or Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


def delete_kala_history(request):
    if request.method == 'POST':
        # cleaned data
        cd = request.POST
        kala_id = cd.get('kala_id')
        kala_history_id = cd.get('kala_history_id')

        try:
            kala_history = KalaHistory.objects.get(id=kala_history_id)
            kala_history.delete()
            kala = Kala.objects.get(id=kala_id)

            context = {
                'kala': kala
            }
            return JsonResponse({
                'status': 'success',
                'template': render_to_string('managers/contents/kala_histories_content.html', context)
            })
        except KalaDetail.DoesNotExist or Kala.DoesNotExist:
            return HttpResponse(status=404)
    else:
        raise Http404


class IPAddressList(SuperuserAccessMixin, ListView):
    model = IPAddress
    template_name = 'managers/ip_address_list.html'
    paginate_by = 30
