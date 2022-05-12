from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from departments.models import Department
from projects.models import Project


# Create your views here.


def staff_home_page(request):
    return render(request, 'staff/staff_home_page.html')


class StaffDepartmentList(ListView):
    def get_queryset(self):
        qs = Department.objects.filter(is_active=True, staff_users__in=[self.request.user])
        return qs

    template_name = 'staff/department_list.html'
    paginate_by = 12
    context_object_name = 'departments'


class StaffDepartmentDetail(DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        qs = get_object_or_404(
            Department, pk=pk, is_active=True, staff_users__in=[self.request.user]
        )
        return qs

    template_name = 'staff/department_detail.html'
    context_object_name = 'department'


class StaffProjectList(ListView):
    def get_queryset(self):
        qs = Project.objects.filter(
            department__staff_users__in=[self.request.user], department__is_active=True
        )
        return qs

    template_name = 'staff/project_list.html'
    paginate_by = 6
    context_object_name = 'projects'


class StaffProjectDetail(DetailView):
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        qs = get_object_or_404(
            Project, pk=pk, department__staff_users__in=[self.request.user], department__is_active=True
        )
        return qs

    template_name = 'staff/project_detail.html'
    context_object_name = 'project'
