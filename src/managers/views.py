from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from accounts.models import User

from .forms import UsersForm
from core.mixins import (
    SuperuserAccessMixin
)


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
    paginate_by = 9


class UserCreate(SuperuserAccessMixin, CreateView):
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
