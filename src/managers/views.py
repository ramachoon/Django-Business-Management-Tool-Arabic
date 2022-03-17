from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
from projects.forms import ProjectsForm
from projects.models import Project, WorkDay


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

class WorkDayDetail(SuperuserAccessMixin, DetailView):
    model = WorkDay
    template_name = 'managers/workday_detail.html'
