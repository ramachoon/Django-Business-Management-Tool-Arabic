from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from core.decorators import staffuser_access_decorator
from core.mixins import StaffAccessMixin
from departments.models import Department
from projects.forms import ProjectsForm
from projects.models import Project, WorkDay


# Create your views here.


@staffuser_access_decorator()
def staff_home_page(request):
    return render(request, 'staff/staff_home_page.html')


class StaffDepartmentList(StaffAccessMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        qs = Department.objects.filter(is_active=True, staff_users__in=[self.request.user])
        return qs

    template_name = 'staff/department_list.html'
    paginate_by = 12
    context_object_name = 'departments'
    permission_required = 'departments.view_department'


class StaffDepartmentDetail(StaffAccessMixin, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        qs = get_object_or_404(
            Department, pk=pk, is_active=True, staff_users__in=[self.request.user]
        )
        return qs

    template_name = 'staff/department_detail.html'
    context_object_name = 'department'
    permission_required = 'departments.view_department'


class StaffProjectList(StaffAccessMixin, PermissionRequiredMixin, ListView):
    def get_queryset(self):
        qs = Project.objects.filter(
            department__staff_users__in=[self.request.user], department__is_active=True
        )
        return qs

    template_name = 'staff/project_list.html'
    paginate_by = 6
    context_object_name = 'projects'
    permission_required = 'projects.view_project'


class StaffProjectDetail(StaffAccessMixin, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Project.objects.get_project_for_staff(pk, self.request.user)

    template_name = 'staff/project_detail.html'
    context_object_name = 'project'
    permission_required = 'projects.view_project'


class StaffProjectCreate(StaffAccessMixin, PermissionRequiredMixin, CreateView):
    def form_valid(self, form):
        project_form = form.save(commit=False)
        department = get_object_or_404(
            Department, pk=self.kwargs.get('department_pk'), is_active=True
        )
        project_form.department = department
        project_form.save()
        return super(StaffProjectCreate, self).form_valid(form)

    model = Project
    template_name = 'staff/project_create_update.html'
    permission_required = 'projects.add_project'
    form_class = ProjectsForm
    success_url = reverse_lazy('staff_module:project_list')


class StaffProjectUpdate(StaffAccessMixin, PermissionRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Project.objects.get_project_for_staff(pk, self.request.user)

    template_name = 'staff/project_create_update.html'
    form_class = ProjectsForm
    success_url = reverse_lazy('staff_module:project_list')
    permission_required = 'projects.change_project'


class StaffProjectDelete(StaffAccessMixin, PermissionRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Project.objects.get_project_for_staff(pk, self.request.user)

    template_name = 'staff/project_delete.html'
    success_url = reverse_lazy('staff_module:project_list')
    permission_required = 'projects.delete_project'


class StaffWorkDayDetail(StaffAccessMixin, PermissionRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return WorkDay.objects.get_work_day_for_staff(pk, self.request.user)

    template_name = 'staff/workday_detail.html'
    context_object_name = 'workday'
    permission_required = 'projects.view_workday'
